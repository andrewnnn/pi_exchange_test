from flask import Flask, request, jsonify, Response
import sqlite3
import json
app = Flask(__name__)

# /customers?prefix="123"
@app.route("/customers", methods=['GET', 'POST'])
def customers():
    if request.method == 'GET':
        sql = """ SELECT * FROM Customers; """

        # check for prefix search
        prefix = request.args.get('prefix')
        if (prefix):
            sql = """ SELECT * FROM Customers 
                    WHERE phone_number LIKE '{}%'; """.format(prefix)
            
        conn = create_connection("sqlite.db")
        try:
            c = conn.cursor()
            c.execute(sql)

            data = c.fetchall()

            datajson = []
            # convert to json
            for d in data:
                j = {"id": d[0], "name": d[1], "phone_number": d[2]}
                datajson.append(j)

            return jsonify(datajson)

        except sqlite3.Error as e:
            print(e)
            return jsonify({"code": 500, "message": str(e)}), 500
        finally:
            conn.close()
    elif request.method == 'POST':
        code = 200
        response = {}
        sql = """ INSERT INTO customers(name, phone_number)
              VALUES(?,?); """
        name = request.form['name']
        phone_number = request.form['phone_number']

        print("form data", name, phone_number)

        conn = create_connection("sqlite.db")
        try:
            c = conn.cursor()
            c.execute(sql, (name, phone_number))
            conn.commit()
            print(c.lastrowid)

            response = {"code": 201, "message": "resources successfully created"}
            code = 201
        except sqlite3.Error as e:
            print(e)
            response = {"code": 500, "message": str(e)}
            code = 500
        finally:
            conn.close()

        return jsonify(response), code
    else:
        return jsonify({"code": 400, "message": "bad request"}), 400

# DATABASE HELPERS
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Sqlite Version: ", sqlite3.version)
    except:
        print("create connection erorr")
    
    return conn