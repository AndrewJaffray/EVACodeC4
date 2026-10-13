import json
from datetime import datetime
import matplotlib.pyplot as plt

start_year = int(input("Start year: "))
end_year = int(input("End year: "))

with open("eva-data.json", "r", encoding="utf-8") as file:
    eva_data = json.load(file)

records = []

for eva in eva_data:
    date_text = eva.get("date")
    duration_text = eva.get("duration")
    country_text = eva.get("country")
    crew_text = eva.get("crew", "")

    if not date_text or not duration_text or not country_text:
        continue

    date = datetime.fromisoformat(date_text)
    if not (start_year <= date.year <= end_year):
        continue

    hours, minutes = map(int, duration_text.split(":"))
    duration_hours = hours + minutes / 60

    records.append((date, duration_hours, country_text, crew_text))

records.sort(key=lambda record: record[0])

dates = []
cumulative_hours = []
total_hours = 0
USA_hours = 0
Russia_hours = 0

for date, duration_hours, country_text, crew_text in records:
    total_hours += duration_hours
    dates.append(date)
    cumulative_hours.append(total_hours)
    if country_text == "USA":
        USA_hours += duration_hours
    elif country_text == "Russia":
        Russia_hours += duration_hours


def classify_duration(duration_hours):
    if duration_hours < 4:
        return "Short"
    elif duration_hours < 7:
        return "Standard"
    return "Long"


category_counts = {"Short": 0, "Standard": 0, "Long": 0}
for date, duration_hours, country_text, crew_text in records:
    category_counts[classify_duration(duration_hours)] += 1

total_evas = len(records)
print(f"\nEVA duration categories ({total_evas} EVAs):")
for category, count in category_counts.items():
    percentage = (count / total_evas * 100) if total_evas else 0
    print(f"  {category} {count}  ({percentage:.1f}%)")

crew_hours = {}
for date, duration_hours, country_text, crew_text in records:
    for name in crew_text.split(";"):
        name = name.strip()
        if name:
            crew_hours[name] = crew_hours.get(name, 0) + duration_hours

print("\nTop 5 astronauts by EVA time:")
top_crew = sorted(crew_hours.items(), key=lambda item: item[1], reverse=True)[:5]
for name, hours in top_crew:
    print(f"  {name} {hours:.1f} hours")

plt.plot(dates, cumulative_hours)
plt.title(f"USA: {USA_hours:.1f} Hours      Russia: {Russia_hours:.1f} Hours")
plt.xlabel("Year")
plt.ylabel("Cumulative EVA duration (hours)")
plt.tight_layout()
plt.savefig("cumulative_duration.png")
plt.show()
