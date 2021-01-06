import csv
import os

categoryNames = os.listdir('./categories')
categories = {}

for category in categoryNames:
    with open('./categories/' + category) as f:
        categories[category] = list(map(str.strip, f.readlines()))


def getCategory(desc):
    for category in categories.keys():
        for term in categories[category]:
            if term in desc:
                return category
    return 'none'


def isExpenditure(row):
    try:
        return int(row[2]) < 0
    except:
        return False


parsedRows = []


with open('./put-data-here/data-cleaned.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if(isExpenditure(row)):
            parsedRows.append({
                'date': row[0],
                'desc': row[1],
                'value': int(row[2]),
                'category': getCategory(row[1])
            })

with open('./output/output.csv', mode='w') as output_file:
    csv_writer = csv.DictWriter(
        output_file,
        fieldnames=['date', 'desc', 'value', 'category']
    )
    csv_writer.writerows(parsedRows)
