
def read_file(filename):
    records = []
    try:
        f = open(filename, "r")
        records = f.readlines()
        f.close()
    except FileNotFoundError:
        print("ERROR: water_readings.txt not found.")
        print("Make sure the file is in the same folder as this program.")
    return records

def calculate_bill(consumption):
    bill = 0.0
    if consumption > 6:
        band2 = consumption - 6
        if band2 > 14:
            band2 = 14
        i = 0
        while i < band2:
            bill += 8.50
            i += 1
    if consumption > 20:
        band3 = consumption - 20
        i = 0
        while i < band3:
            bill += 12.00
            i += 1
    return bill

def classify(consumption):
    if consumption <= 20:
        return "LOW"
    elif consumption <= 50:
        return "MODERATE"
    else:
        return "HIGH"

def top_five(valid_records):
    indexes = []
    i = 0
    while i < len(valid_records):
        indexes.append(i)
        i += 1

    top = []
    count = 0
    while count < 5 and len(indexes) > 0:
        highest_pos = 0
        j = 0
        while j < len(indexes):
            current_idx = indexes[j]
            highest_idx = indexes[highest_pos]
            if valid_records[current_idx]["consumption"] > valid_records[highest_idx]["consumption"]:
                highest_pos = j
            j += 1
        top.append(valid_records[indexes[highest_pos]])
        new_indexes = []
        k = 0
        while k < len(indexes):
            if k != highest_pos:
                new_indexes.append(indexes[k])
            k += 1
        indexes = new_indexes
        count += 1
    return top

def main():
    print("Community Water Billing System")
    print("==============================")

    lines = read_file("water_readings.txt")
    if len(lines) == 0:
        return

    valid_records = []
    seen_meters = {}
    errors = []
    rejected = 0
    accepted = 0

    line_num = 0
    for line in lines:
        line_num += 1
        line = line.strip()

        if line == "":
            continue

        parts = line.split(",")
        cleaned = []
        for p in parts:
            cleaned.append(p.strip())

        if len(cleaned) != 5:
            rejected += 1
            msg = f"Line {line_num}: {line} - REJECTED: Expected 5 fields, got {len(cleaned)}"
            errors.append(msg)
            print(msg)
            continue

        meter = cleaned[0]
        name = cleaned[1]
        prev_str = cleaned[2]
        curr_str = cleaned[3]
        area = cleaned[4]

        if meter == "" or name == "" or prev_str == "" or curr_str == "" or area == "":
            rejected += 1
            msg = f"Line {line_num}: {line} - REJECTED: Missing field(s)"
            errors.append(msg)
            print(msg)
            continue

        if meter in seen_meters:
            rejected += 1
            msg = f"Line {line_num}: {line} - REJECTED: Duplicate meter number {meter}"
            errors.append(msg)
            print(msg)
            continue

        try:
            prev = int(prev_str)
            curr = int(curr_str)
        except ValueError:
            rejected += 1
            msg = f"Line {line_num}: {line} - REJECTED: Non-numeric reading"
            errors.append(msg)
            print(msg)
            continue

        if prev < 0 or curr < 0:
            rejected += 1
            msg = f"Line {line_num}: {line} - REJECTED: Negative reading"
            errors.append(msg)
            print(msg)
            continue

        if curr < prev:
            rejected += 1
            msg = f"Line {line_num}: {line} - REJECTED: Current reading below previous reading"
            errors.append(msg)
            print(msg)
            continue

        consumption = curr - prev

        bill = calculate_bill(consumption)
        category = classify(consumption)

        record = {
            "meter": meter,
            "name": name,
            "previous": prev,
            "current": curr,
            "area": area,
            "consumption": consumption,
            "bill": bill,
            "category": category
        }
        valid_records.append(record)
        seen_meters[meter] = name
        accepted += 1

    total_consumption = 0
    total_billed = 0.0
    for r in valid_records:
        total_consumption += r["consumption"]
        total_billed += r["bill"]

    top5 = top_five(valid_records)

    report = open("billing_report.txt", "w")
    report.write("COMMUNITY WATER BILLING REPORT\n")
    report.write("==============================\n\n")
    report.write(f"{'Meter':<8} {'Name':<20} {'Area':<18} {'Cons(kL)':<10} {'Bill(R)':<10} {'Category'}\n")
    report.write("-" * 85 + "\n")

    for r in valid_records:
        report.write(f"{r['meter']:<8} {r['name']:<20} {r['area']:<18} {r['consumption']:<10} {r['bill']:<10.2f} {r['category']}\n")

    report.write("\nTOP 5 HIGHEST CONSUMERS\n")
    report.write("-----------------------\n")
    rank = 1
    for r in top5:
        report.write(f"{rank}. {r['name']} ({r['meter']}) - {r['consumption']} kL - R{r['bill']:.2f}\n")
        rank += 1

    report.write("\nSUMMARY\n")
    report.write("-------\n")
    report.write(f"Accepted records: {accepted}\n")
    report.write(f"Rejected records: {rejected}\n")
    report.write(f"Total records processed: {accepted + rejected}\n")

    low = 0
    mod = 0
    high = 0
    for r in valid_records:
        if r["category"] == "LOW":
            low += 1
        elif r["category"] == "MODERATE":
            mod += 1
        else:
            high += 1
    report.write(f"LOW: {low}\nMODERATE: {mod}\nHIGH: {high}\n")
    report.write(f"Total consumption: {total_consumption} kL\n")
    report.write(f"Total billed: R{total_billed:.2f}\n")
    report.close()

    elog = open("errors.log", "w")
    elog.write("ERROR LOG - REJECTED RECORDS\n")
    elog.write("============================\n\n")
    for e in errors:
        elog.write(e + "\n")
    elog.close()

    print("\n==============================")
    print(f"Accepted: {accepted}")
    print(f"Rejected: {rejected}")
    print(f"Total consumption: {total_consumption} kL")
    print(f"Total billed: R{total_billed:.2f}")
    print("Reports created: billing_report.txt and errors.log")

main()