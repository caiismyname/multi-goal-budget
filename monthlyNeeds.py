import csv
from dateutil.parser import parse
from datetime import date
from monthdelta import monthdelta

# doesn't matter order of dates
def monthDiff(d1, d2):
    return abs((12 * (d2.year - d1.year) + (d2.month - d1.month)))

expenses = []
costs = {}
start = date(2022, 3, 1)
end = date.today()

with open("forecast.csv", "r") as f:
    data = csv.reader(f, delimiter=',')
    for row in data:
        dueDate = parse(row[2], default=date(2022,1,1)) # default to set the day to 1 for consistency
        if dueDate > end:
            end = dueDate
        expenses.append({
            "name": row[0],
            "cost": int(row[1]),
            "dueDate": dueDate
        })

cur = start
while cur <= end:
    costs[cur] = 0
    cur += monthdelta(1)

for entry in expenses:    
    timespan = monthDiff(entry['dueDate'], start)
    for i in range(timespan):
        costs[start + monthdelta(i)] += (entry['cost'] / timespan)

year = start.year
print("----------- " + str(year) + " -----------")
for key in costs.keys():
    if key.year > year:
        year = key.year
        print("----------- " + str(year) + " -----------")
    print(key.strftime("%m/%Y: " + str(int(costs[key]))))
