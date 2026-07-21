import sqlite3

connection = sqlite3.connect('student.db')

cursor = connection.cursor()

# table_info = '''CREATE TABLE STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT)'''

# cursor.execute(table_info)

cursor.execute('''INSERT INTO STUDENT VALUES('AMIT','Data Science','C',94)''')
cursor.execute('''INSERT INTO STUDENT VALUES('PRIYA', 'Data Science', 'A', 98)''')
cursor.execute('''INSERT INTO STUDENT VALUES('ROHAN', 'Web Development', 'B', 85)''')
cursor.execute('''INSERT INTO STUDENT VALUES('ANANYA', 'Cyber Security', 'A', 92)''')
cursor.execute('''INSERT INTO STUDENT VALUES('KABIR', 'Data Science', 'C', 78)''')
cursor.execute('''INSERT INTO STUDENT VALUES('SNEHA', 'Machine Learning', 'A', 96)''')
cursor.execute('''INSERT INTO STUDENT VALUES('ARJUN', 'Cloud Computing', 'B', 88)''')
cursor.execute('''INSERT INTO STUDENT VALUES('DIYA', 'Data Science', 'B', 89)''')
cursor.execute('''INSERT INTO STUDENT VALUES('VIKRAM', 'Web Development', 'C', 74)''')
cursor.execute('''INSERT INTO STUDENT VALUES('MEERA', 'Machine Learning', 'A', 95)''')
cursor.execute('''INSERT INTO STUDENT VALUES('RAHUL', 'Cyber Security', 'B', 81)''')

print('The inserted Records are :')

data = cursor.execute('''SELECT * FROM STUDENT''')

for row in data:
    print(row)

connection.commit()
connection.close()