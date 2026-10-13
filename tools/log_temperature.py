import argparse
import csv
import math
from datetime import datetime, timezone

import serial


def main():
    parser = argparse.ArgumentParser(description="Save Nano temperatures to CSV.")
    parser.add_argument("port", help="Nano serial port, for example COM3")
    args = parser.parse_args()

    filename = datetime.now().strftime("temperature_%Y%m%d_%H%M%S.csv")

    with serial.Serial(args.port, 9600, timeout=2) as nano:
        with open(filename, "x", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["time_utc", "uptime_ms", "temperature_c"])
            file.flush()

            print(f"Saving to {filename}. Press Ctrl+C to stop.")

            while True:
                raw = nano.readline()
                if not raw.endswith(b"\n"):
                    continue

                line = raw.decode("utf-8", errors="replace").strip()

                if line.startswith("#"):
                    print(line)
                    continue

                try:
                    uptime, temperature = line.split(",")
                    uptime = int(uptime)
                    temperature = float(temperature)
                except ValueError:
                    continue

                if uptime < 0 or not math.isfinite(temperature):
                    continue

                timestamp = datetime.now(timezone.utc).isoformat()
                writer.writerow([timestamp, uptime, temperature])
                file.flush()
                print(f"{temperature:.2f} C")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nLogging stopped.")
    except (serial.SerialException, OSError) as error:
        print(f"Could not log readings: {error}")
