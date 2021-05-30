import csv
import mysql.connector

conn = mysql.connector.connect(user='root', password='', host='localhost', database='tiln')

cursor = conn.cursor()
file = open('dataset2.csv', encoding="utf8")
csv_data = csv.reader(file)

for row in csv_data:
    cursor.execute("""INSERT INTO tiln(id, nume, descriere, sentiment, expresii, polexpresii, nik2) VALUES(%s, %s, %s, %s, %s, %s, %s)""", row)

conn.commit()
cursor.close()
print ("Done")