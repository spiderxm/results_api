from flask import Flask, jsonify
import json
import pymysql.cursors

app = Flask(__name__)
try:
    mydb = pymysql.connect(
        host='localhost',
        user='root',
        password='***',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
    mycursor = mydb.cursor()

except:
    print("Cannot connect to database and not able to create cursor")

try:
    query = "USE RESULTS"
    mycursor.execute(query)
    print("Using db RESULTS")
except:
    print("error using database")


@app.route('/')
def allrecords():
    query = "SELECT * FROM RESULT"
    try:
        mycursor.execute(query)
        answer = mycursor.fetchall()
        for i in range(len(answer)):
            answer[i]['cgpa'] = float(answer[i]['cgpa'])
            answer[i]['sgpa'] = float(answer[i]['cgpa'])
        return jsonify(answer)
    except:
        print("Error")
        return jsonify({
            "status_code": 200,
            "error": "error in retreiving records"
        })


@app.route('/average_results_per_branch')
def average_results():
    try:
        query = "SELECT AVG (sgpa) as avg_sgpa, AVG(cgpa) as avg_cgpa FROM RESULT"
        mycursor.execute(query)
        answer = mycursor.fetchall()
        answer[0]['avg_cgpa'] = float(answer[0]['avg_cgpa'])
        answer[0]['avg_sgpa'] = float(answer[0]['avg_sgpa'])
        query = "SELECT AVG (sgpa) as avg_sgpa, AVG(cgpa) as avg_cgpa, branch  FROM RESULT GROUP BY branch"
        mycursor.execute(query)
        answer1 = mycursor.fetchone()
        while answer1:
            string = "avg_sgpa_{}".format(answer1['branch'])
            string2 = "avg_cgpa_{}".format(answer1['branch'])
            answer[0][string] = float(answer1['avg_sgpa'])
            answer[0][string2] = float(answer1['avg_cgpa'])
            answer1 = mycursor.fetchone()
        return jsonify(answer)
    except:
        print("Error")
        return jsonify({
            "status_code": 200,
            "error": "error in retreiving records"
        })


@app.route('/average_results_per_year')
def average_results_per_year():
    query = "SELECT AVG (sgpa) as avg_sgpa, AVG(cgpa) as avg_cgpa, current_year FROM RESULT GROUP BY current_year"
    try:
        mycursor.execute(query)
        print("1")
        answer = mycursor.fetchall()
        print(answer)
        for i in range(len(answer)):
            answer[i]['avg_cgpa'] = float(answer[i]['avg_cgpa'])
            answer[i]['avg_sgpa'] = float(answer[i]['avg_cgpa'])
        print(answer)
        return jsonify(answer)
    except:
        print("Error")
        return jsonify({
            "status_code": 200,
            "error": "error in retreiving records"
        })


@app.route('/result/<string:name>')
def results_like_name(name):
    query = "Select * from RESULT where name like '{}%'".format(name)
    try:
        mycursor.execute(query)
        answer = mycursor.fetchall()
        for i in range(len(answer)):
            answer[i]['cgpa'] = float(answer[i]['cgpa'])
            answer[i]['sgpa'] = float(answer[i]['cgpa'])
        if len(answer) != 0:
            return jsonify(answer)
        else:
            return jsonify({
                "result": "no result found"
            })
    except:
        print("Error")
        return jsonify({
            "status_code": 200,
            "error": "error in retreiving records"
        })


@app.route('/result_roll/<string:roll>')
def results_like_roll(roll):
    query = "Select * from RESULT where rollno like '{}%'".format(roll)
    try:
        mycursor.execute(query)
        answer = mycursor.fetchall()
        for i in range(len(answer)):
            answer[i]['cgpa'] = float(answer[i]['cgpa'])
            answer[i]['sgpa'] = float(answer[i]['cgpa'])
        if len(answer) != 0:
            return jsonify(answer)
        else:
            return jsonify({
                "result": "no result found"
            })
    except:
        print("Error")
        return jsonify({
            "status_code": 200,
            "error": "error in retreiving records"
        })


@app.route('/per_batch')
def average_results_per_year_per_branch():
    query = "SELECT AVG (sgpa) as avg_sgpa, AVG(cgpa) as avg_cgpa, current_year, branch FROM RESULT GROUP BY current_year, branch"
    try:
        mycursor.execute(query)
        answer = mycursor.fetchall()
        print(answer)
        for i in range(len(answer)):
            answer[i]['avg_cgpa'] = float(answer[i]['avg_cgpa'])
            answer[i]['avg_sgpa'] = float(answer[i]['avg_cgpa'])
        print(answer)
        return jsonify(answer)
    except:
        print("Error")
        return jsonify({
            "status_code": 200,
            "error": "error in retreiving records"
        })


if __name__ == '__main__':
    app.run()
