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

    if not date_text or not duration_text or not country_text:
        continue

    date = datetime.fromisoformat(date_text)
    if not (start_year <= date.year <= end_year):
        continue

    hours, minutes = map(int, duration_text.split(":"))
    duration_hours = hours + minutes / 60

    records.append((date, duration_hours, country_text))

records.sort(key=lambda record: record[0])

dates = []
cumulative_hours = []
total_hours = 0
USA_hours = 0
Russia_hours = 0

for date, duration_hours, country_text in records:
    total_hours += duration_hours
    dates.append(date)
    cumulative_hours.append(total_hours)
    if country_text == "USA":
        USA_hours += duration_hours
    elif country_text == "Russia":
        Russia_hours += duration_hours

plt.plot(dates, cumulative_hours)
plt.title(f"USA: {USA_hours:.1f} Hours      Russia: {Russia_hours:.1f} Hours")
plt.xlabel("Year")
plt.ylabel("Cumulative EVA duration (hours)")
plt.tight_layout()
plt.savefig("cumulative_duration.png")
plt.show()
