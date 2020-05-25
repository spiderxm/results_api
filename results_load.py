import json
import pymysql.cursors

try:
    mydb = pymysql.connect(
        host='localhost',
        user='root',
        password='***',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
except:
    print("error")

mycursor = mydb.cursor()

with open('venv/full_college_sgpi.json') as f:
    data = json.load(f)

try:
    query = "CREATE DATABASE IF NOT EXISTS RESULTS"
    mycursor.execute(query)
except:
    print("error creating database")

try:
    query = "USE RESULTS"
    mycursor.execute(query)
except:
    print("error using database")

try:
    query = "CREATE TABLE IF NOT EXISTS RESULT(" \
            "branch varchar(20) not null ," \
            "cgpa decimal(4,2) not null," \
            "sgpa decimal(4,2) not null, " \
            "g_rank integer not null," \
            "name varchar(30) not null," \
            "points integer not null," \
            "rollno varchar(10) primary key," \
            "current_year int not null" \
            ")"
    mycursor.execute(query)
except:
    print("error creating database")

for i in range(len(data)):
    try:
        query = "INSERT INTO RESULT VALUES (" \
                "'{}',{},{},{},'{}',{},'{}',{} )".format(data[i]['Branch'],
                                                         float(data[i]['Cgpa']),
                                                         float(data[i]['Sgpa']),
                                                         int(data[i]['G_rank']),
                                                         data[i]['Name'],
                                                         int(data[i]['Points']),
                                                         data[i]['Rollno'],
                                                         int(data[i]['Year']))
        mycursor.execute(query)
        print("record {} entered".format(i + 1))
    except:
        print("Error")

