import csv
import json

# Step 1: Detect file type
def detect_file_type(file_name):
    if file_name.endswith(".csv"):
        return "csv"
    elif file_name.endswith(".json"):
        return "json"
    else:
        return "unknown"

# Step 2: Process CSV
def process_csv(file_path):
    data = []

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    return data

# Step 3: Create final output
def create_output(file_name, data):
    output = {
        "file_name": file_name,
        "data": data
    }

    with open("output.json", "w") as f:
        json.dump(output, f, indent=4)

    print("✅ JSON output created")

# Step 4: Main function
def main():
    file_name = "employee_data.csv"

    file_type = detect_file_type(file_name)

    if file_type == "csv":
        data = process_csv(file_name)
        create_output(file_name, data)
    else:
        print("❌ Unsupported file type")

# Run
main()

