"""
CARESAFE CSV Event Demo
-----------------------
Reads an ESP32/MPU6050 CSV recording and flags *candidate high-motion events*
using adjustable thresholds. This is a prototype demonstration, NOT a validated
fall detector. Thresholds are in m/s^2 for acceleration magnitude and rad/s
for gyroscope magnitude.
"""
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

DEFAULT_ACC_THRESHOLD = 22.0
DEFAULT_GYRO_THRESHOLD = 3.0
DEFAULT_MERGE_GAP_SECONDS = 1.0

def main():
    parser = argparse.ArgumentParser(description="CARESAFE threshold-based CSV event demo")
    parser.add_argument("csv_file", help="Path to recording CSV, e.g. near_fall_01.csv")
    parser.add_argument("--acc-threshold", type=float, default=DEFAULT_ACC_THRESHOLD,
                        help="Acceleration magnitude threshold in m/s^2 (default: 22)")
    parser.add_argument("--gyro-threshold", type=float, default=DEFAULT_GYRO_THRESHOLD,
                        help="Gyroscope magnitude threshold in rad/s (default: 3)")
    parser.add_argument("--merge-gap", type=float, default=DEFAULT_MERGE_GAP_SECONDS,
                        help="Merge nearby flagged samples within this many seconds (default: 1)")
    args = parser.parse_args()

    path = Path(args.csv_file)
    if not path.exists():
        raise SystemExit(f"File not found: {path}\nTip: run this command from the folder containing the CSV, or provide the full path.")

    df = pd.read_csv(path)
    df.columns = [str(c).strip().lower() for c in df.columns]
    required = {"ax", "ay", "az", "gx", "gy", "gz"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Missing required columns: {', '.join(sorted(missing))}\nExpected ax, ay, az, gx, gy, gz.")

    for col in required:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=list(required)).reset_index(drop=True)
    if df.empty:
        raise SystemExit("No usable sensor rows found.")

    if "acc_mag" not in df.columns:
        df["acc_mag"] = np.sqrt(df["ax"]**2 + df["ay"]**2 + df["az"]**2)
    else:
        df["acc_mag"] = pd.to_numeric(df["acc_mag"], errors="coerce")
        df["acc_mag"] = df["acc_mag"].fillna(np.sqrt(df["ax"]**2 + df["ay"]**2 + df["az"]**2))
    if "gyro_mag" not in df.columns:
        df["gyro_mag"] = np.sqrt(df["gx"]**2 + df["gy"]**2 + df["gz"]**2)
    else:
        df["gyro_mag"] = pd.to_numeric(df["gyro_mag"], errors="coerce")
        df["gyro_mag"] = df["gyro_mag"].fillna(np.sqrt(df["gx"]**2 + df["gy"]**2 + df["gz"]**2))

    if "timestamp_us" in df.columns:
        t = pd.to_numeric(df["timestamp_us"], errors="coerce")
        if t.notna().sum() > 1:
            seconds = (t.ffill().fillna(0) - t.ffill().fillna(0).iloc[0]) / 1_000_000.0
        else:
            seconds = pd.Series(np.arange(len(df)) / 100.0)
    elif "timestamp_ms" in df.columns:
        t = pd.to_numeric(df["timestamp_ms"], errors="coerce").ffill().fillna(0)
        seconds = (t - t.iloc[0]) / 1000.0
    elif "time_s" in df.columns:
        seconds = pd.to_numeric(df["time_s"], errors="coerce").ffill().fillna(0)
        seconds = seconds - seconds.iloc[0]
    else:
        seconds = pd.Series(np.arange(len(df)) / 100.0)

    df["time_s"] = seconds
    # Flag a high-motion sample if either channel crosses its threshold.
    # The CSV demo deliberately calls these "candidate events", not confirmed falls.
    df["candidate_sample"] = (
        (df["acc_mag"] >= args.acc_threshold) |
        (df["gyro_mag"] >= args.gyro_threshold)
    )

    flagged = df.index[df["candidate_sample"]].tolist()
    groups = []
    for idx in flagged:
        if not groups or (df.loc[idx, "time_s"] - df.loc[groups[-1][-1], "time_s"]) > args.merge_gap:
            groups.append([idx])
        else:
            groups[-1].append(idx)

    event_rows = []
    for number, group in enumerate(groups, start=1):
        part = df.loc[group]
        acc_idx = part["acc_mag"].idxmax()
        gyro_idx = part["gyro_mag"].idxmax()
        peak_acc = df.loc[acc_idx]
        peak_gyro = df.loc[gyro_idx]
        event_rows.append({
            "event_id": number,
            "start_time_s": round(float(part["time_s"].min()), 3),
            "end_time_s": round(float(part["time_s"].max()), 3),
            "peak_acc_mag_m_s2": round(float(part["acc_mag"].max()), 3),
            "peak_acc_time_s": round(float(peak_acc["time_s"]), 3),
            "peak_gyro_mag_rad_s": round(float(part["gyro_mag"].max()), 3),
            "peak_gyro_time_s": round(float(peak_gyro["time_s"]), 3),
            "acc_threshold_crossed": bool((part["acc_mag"] >= args.acc_threshold).any()),
            "gyro_threshold_crossed": bool((part["gyro_mag"] >= args.gyro_threshold).any()),
            "status": "CANDIDATE_HIGH_MOTION_EVENT"
        })

    out_path = path.with_name(path.stem + "_event_demo.csv")
    pd.DataFrame(event_rows, columns=[
        "event_id", "start_time_s", "end_time_s", "peak_acc_mag_m_s2",
        "peak_acc_time_s", "peak_gyro_mag_rad_s", "peak_gyro_time_s",
        "acc_threshold_crossed", "gyro_threshold_crossed", "status"
    ]).to_csv(out_path, index=False)

    print("\nCARESAFE CSV EVENT DEMO")
    print("----------------------")
    print(f"Recording: {path.name}")
    print(f"Usable samples: {len(df)}")
    print(f"Duration: {df['time_s'].max():.2f} seconds")
    print(f"Acceleration threshold: {args.acc_threshold:.2f} m/s^2")
    print(f"Gyroscope threshold: {args.gyro_threshold:.2f} rad/s")
    print(f"Flagged samples: {int(df['candidate_sample'].sum())}")
    print(f"Candidate event groups: {len(event_rows)}")
    if event_rows:
        for e in event_rows:
            print(f"  Event {e['event_id']}: {e['start_time_s']:.2f}-{e['end_time_s']:.2f}s | "
                  f"peak acc={e['peak_acc_mag_m_s2']:.2f} m/s^2 | "
                  f"peak gyro={e['peak_gyro_mag_rad_s']:.2f} rad/s")
        print("DEMO ALERT: Potential high-motion event flagged. Check the person/context.")
    else:
        print("No candidate event crossed the selected thresholds.")
        print("For a demo only, you can try lower thresholds, e.g. --acc-threshold 16 --gyro-threshold 2.")
    print(f"Event report saved: {out_path}")
    print("\nNOTE: Threshold crossings are not proof of a fall. Validate thresholds with safe, labeled recordings.")

if __name__ == "__main__":
    main()
