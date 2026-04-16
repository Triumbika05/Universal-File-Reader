# import csv
# import random

# names = ["Arjun", "Meena", "Rahul", "Sneha", "Kiran", "Anjali", "Vikram", "Divya"]
# departments = ["Engineering", "HR", "Finance", "Marketing", "Sales"]
# cities = ["Chennai", "Bangalore", "Mumbai", "Delhi", "Hyderabad"]

# with open("employee_data.csv", "w", newline="") as file:
#     writer = csv.writer(file)

#     # Header
#     writer.writerow(["employee_id", "name", "department", "age", "salary", "city", "experience_years"])

#     # Generate 100 rows
#     for i in range(1, 101):
#         writer.writerow([
#             100 + i,
#             random.choice(names),
#             random.choice(departments),
#             random.randint(21, 45),
#             random.randint(30000, 90000),
#             random.choice(cities),
#             random.randint(1, 10)
#         ])

# print("✅ 100 employee records generated!")

import csv
import random

names = ["Arjun", "Meena", "Rahul", "Sneha", "Kiran", "Anjali", "Vikram", "Divya"]
departments = ["Engineering", "HR", "Finance", "Marketing", "Sales"]
cities = ["Chennai", "Bangalore", "Mumbai", "Delhi", "Hyderabad"]

def generate_data(file_name, num_records=100):
    with open(file_name, "w", newline="") as file:
        writer = csv.writer(file)

        # Header
        writer.writerow([
            "employee_id", "name", "department",
            "age", "salary", "city", "experience_years"
        ])

        # Generate data
        for i in range(1, num_records + 1):
            writer.writerow([
                100 + i,
                random.choice(names),
                random.choice(departments),
                random.randint(21, 45),
                random.randint(30000, 90000),
                random.choice(cities),
                random.randint(1, 10)
            ])

    print(f"✅ {num_records} employee records generated in {file_name}")


# Example run
if __name__ == "__main__":
    generate_data("employee_data.csv", 100)

