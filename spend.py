import csv
import os

categoryNames = os.listdir('./categories')
categories = {}
totals = {
    'none': 0
}

for category in categoryNames:
    with open('./categories/' + category) as f:
        categories[category] = list(map(str.strip, f.readlines()))
        totals[category] = 0


def getCategory(desc):
    for category in categories.keys():
        for term in categories[category]:
            if term in desc:
                return category
    return 'none'


def isExpenditure(row):
    try:
        return float(row[2]) < 0
    except:
        return False


parsedRows = []


with open('./put-data-here/data-cleaned.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if(isExpenditure(row)):
            category = getCategory(row[1])
            value = float(row[2]) * -1
            parsedRows.append({
                'date': row[0],
                'desc': row[1],
                'value': float(row[2]),
                'category': category
            })
            totals[category] += value

with open('./output/output.csv', mode='w') as output_file:
    csv_writer = csv.DictWriter(
        output_file,
        fieldnames=['date', 'desc', 'value', 'category']
    )
    csv_writer.writerows(parsedRows)

with open('./output/totals.csv', mode='w') as totals_file:
    csv_writer = csv.writer(
        totals_file,
        delimiter=',',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL
    )
    for category in totals.keys():
        csv_writer.writerow([category, totals[category]])
