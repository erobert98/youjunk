import csv

C = open('articles.csv')
csv_C = csv.reader(C)
H = open('happy.csv')
csv_H = csv.reader(H)

for rowC in csv_C:
    print(rowC)
    for rowH in csv_H:
        if rowC[0] in rowH[0]:
            print('match')
            print(rowC)
            print(rowH)
            continue
        if rowC[0] not in rowH[0]:
            print(rowC)
            print('nada')