import csv
import os
from datetime import datetime


def generate_sales_report_task(report_name: str) -> None:
    os.makedirs("generated_reports", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    file_path = f"generated_reports/{report_name}_{timestamp}.csv"

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["metric", "value"])
        writer.writerow(["total_orders", 10])
        writer.writerow(["total_sales", 125000])
        writer.writerow(["generated_at", datetime.utcnow()])

    with open("logs/reports.log", "a") as log_file:
        log_file.write(
            f"[{datetime.utcnow()}] Report generated: {file_path}\n"
        )