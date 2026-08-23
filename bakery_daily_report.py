import csv
from datetime import datetime
from pathlib import Path

SALES_FILE = "bakery_sales.csv"
REPORT_FOLDER = Path("reports")


def load_sales(filename):
    sales = []
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["quantity"] = int(row["quantity"])
            row["price"] = float(row["price"])
            sales.append(row)
    return sales


def build_report(sales):
    total_items = sum(item["quantity"] for item in sales)
    total_revenue = sum(item["quantity"] * item["price"] for item in sales)
    best_seller = max(sales, key=lambda item: item["quantity"])

    lines = [
        f"Daily Bakery Report - {datetime.now():%Y-%m-%d %H:%M}",
        "-" * 40,
        f"Total items sold: {total_items}",
        f"Total revenue: ${total_revenue:.2f}",
        f"Best seller: {best_seller['item']} ({best_seller['quantity']} sold)",
    ]
    return "\n".join(lines)


def save_report(report_text):
    REPORT_FOLDER.mkdir(exist_ok=True)
    filename = REPORT_FOLDER / f"report_{datetime.now():%Y-%m-%d}.txt"
    with open(filename, "w") as f:
        f.write(report_text)
    print(f"Report saved to {filename}")


if __name__ == "__main__":
    sales = load_sales(SALES_FILE)
    report = build_report(sales)
    save_report(report)