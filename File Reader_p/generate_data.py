"""
Utility – generate a sample employee CSV for testing.

Usage:
    python generate_data.py                          # generates employee_data.csv (100 rows)
    python generate_data.py my_file.csv 200          # custom name and row count
"""
import csv
import random
import sys

NAMES       = ["Arjun", "Meena", "Rahul", "Sneha", "Kiran", "Anjali", "Vikram", "Divya"]
DEPARTMENTS = ["Engineering", "HR", "Finance", "Marketing", "Sales"]
CITIES      = ["Chennai", "Bangalore", "Mumbai", "Delhi", "Hyderabad"]


def generate_data(file_name: str = "employee_data.csv", num_records: int = 100):
    with open(file_name, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["employee_id", "name", "department", "age", "salary", "city", "experience_years"])
        for i in range(1, num_records + 1):
            writer.writerow([
                100 + i,
                random.choice(NAMES),
                random.choice(DEPARTMENTS),
                random.randint(21, 45),
                random.randint(30000, 90000),
                random.choice(CITIES),
                random.randint(1, 10),
            ])
    print(f"✅ {num_records} records generated → {file_name}")


if __name__ == "__main__":
    out_file    = sys.argv[1] if len(sys.argv) > 1 else "employee_data.csv"
    num_records = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    generate_data(out_file, num_records)
