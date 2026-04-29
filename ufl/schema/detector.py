def detect_schema(data):

    # ✅ Ensure list
    if not isinstance(data, list):
        raise Exception(f"Expected list, got {type(data)}")

    # ✅ Convert bad data → safe format
    clean_data = []

    for row in data:
        if isinstance(row, dict):
            clean_data.append(row)
        else:
            # 🔥 FIX: wrap non-dict into dict
            clean_data.append({"value": str(row)})

    if len(clean_data) == 0:
        return {
            "columns": [],
            "row_count": 0
        }

    first_row = clean_data[0]

    columns = []

    for key in first_row.keys():

        values = [row.get(key) for row in clean_data]

        col_type = type(values[0]).__name__ if values else "unknown"

        nulls = sum(1 for v in values if v is None)

        columns.append({
            "name": key,
            "type": col_type,
            "nulls": nulls
        })

    return {
        "columns": columns,
        "row_count": len(clean_data)
    }