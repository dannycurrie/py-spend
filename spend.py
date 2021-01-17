from argparse import ArgumentParser
import csv
import os
from clean import clean

parser = ArgumentParser('pyspend')
parser.add_argument('-f', help="filename for csv, minus .csv extension")
parser.add_argument('-valueNegative', action='store_true')
parser.add_argument('-dateIndex', type=int)
parser.add_argument('-descIndex', type=int)
parser.add_argument('-valueIndex', type=int)
parser.add_argument('-startRow', type=int)
args = parser.parse_args()

file = args.f

clean(
    file,
    args.dateIndex,
    args.descIndex,
    args.valueIndex,
    args.startRow
)

categoryNames = os.listdir('./categories')
categories = {}
totals = {
    'none': 0
}

for category in categoryNames:
    with open(f'./categories/{category}') as f:
        categories[category] = list(map(str.strip, f.readlines()))
        totals[category] = 0


def getCategory(desc):
    for category in categories.keys():
        for term in categories[category]:
            if term in desc:
                return category
    return 'none'


def isExpenditure(row, negative):
    try:
        if(negative):
            return float(row[2]) < 0
        else:
            return float(row[2]) > 0
    except:
        return False


parsedRows = []
uncategorised = []


with open(f'./put-data-here/{file}_cleaned.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print(row)
        if(isExpenditure(row, args.valueNegative)):
            category = getCategory(row[1])
            value = float(row[2]) * -1
            parsedRows.append({
                'date': row[0],
                'desc': row[1],
                'value': float(row[2]),
                'category': category
            })
            totals[category] += value
            if(category == 'none'):
                uncategorised.append(row[1])

with open(f'./output/{file}_output.csv', mode='w') as output_file:
    csv_writer = csv.DictWriter(
        output_file,
        fieldnames=['date', 'desc', 'value', 'category']
    )
    csv_writer.writerows(parsedRows)

with open(f'./output/{file}_totals.csv', mode='w') as totals_file:
    csv_writer = csv.writer(
        totals_file,
        delimiter=',',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL
    )
    for category in totals.keys():
        csv_writer.writerow([category, totals[category]])


with open(f'./output/{file}_uncategorised.csv', mode='w') as uncategorised_file:
    csv_writer = csv.writer(
        uncategorised_file,
        delimiter=',',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL
    )
    for row in uncategorised:
        csv_writer.writerow([row])
