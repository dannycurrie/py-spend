import csv

parsed = [['date', 'desc', 'value']]


def cleanCell(data: str):
    return data.strip('£').replace(',', '')


def clean(filename, dateIndex, descIndex, valueIndex, startRow):
    print(filename, dateIndex, descIndex, valueIndex, startRow)
    with open(f'./put-data-here/{filename}.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        rowNum = 0
        for row in csv_reader:
            if(rowNum < startRow):
                rowNum += 1
            else:
                parsed.append(
                    [row[dateIndex], row[descIndex], row[valueIndex]]
                )

    with open(f'./put-data-here/{filename}_cleaned.csv', mode='w') as cleaned_file:
        csv_writer = csv.writer(
            cleaned_file,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL
        )
        for row in parsed:
            csv_writer.writerow(map(cleanCell, row))
