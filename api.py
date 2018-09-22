#for generating random public Id
import uuid
import psycopg2
import datetime
import json
from config import config
from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from werkzeug.security import generate_password_hash ,check_password_hash


app = Flask(__name__)

@app.route('/user', methods=['GET'])
def get_all_users():
    """ query data from the vendors table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # cur.execute("SELECT vendor_id, vendor_name FROM vendors WHERE vendor_id=%s ORDER BY vendor_name", (id, ))
        cur.execute("SELECT * FROM users ORDER BY user_id")
        returned_data = cur.fetchall()
        columns = ('user_id','public_id', 'name', 'password', 'admin')
        results = []
        for row in returned_data:
            results.append(dict(zip(columns, row)))
        return jsonify({'Users':results})

        row = cur.fetchone()
 
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return ''
@app.route('/user/<int:user_id>',methods=['GET'])
def get_one_user(user_id):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # cur.execute("SELECT vendor_id, vendor_name FROM vendors WHERE vendor_id=%s ORDER BY vendor_name", (id, ))
        cur.execute("SELECT * FROM users WHERE user_id=%s",(user_id, ))
        returned_data = cur.fetchall()
        columns = ('user_id','public_id', 'name', 'password', 'admin')
        results = []
        number_of_rows = cur.rowcount
        if number_of_rows == 0:
            return jsonify({'message':'No User Found!'})
        for row in returned_data:
            results.append(dict(zip(columns, row)))
        return jsonify({'User':results})
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    user_public_id =str(uuid.uuid4())
    """ insert a new user into the users table """
    sql = """INSERT INTO users(public_id,name,password,admin)
             VALUES(%s,%s,%s,%s) RETURNING user_id;"""
    conn = None
    # user_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (user_public_id,data['name'],hashed_password,False,))
        # get the generated id back
        # user_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return jsonify({'Message':'New User Created'})
@app.route('/user/<int:user_id>', methods=['PUT'])
def promote_user(user_id):
    conn = None
    user_status = True
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id=%s",(user_id, ))
        user_exist = cur.rowcount
        if user_exist == 0:
            return jsonify({'Messsage':'No user Found!'})
        cur.execute("UPDATE users SET admin=%s WHERE user_id=%s",(user_status,user_id,))
        conn.commit()
        cur.close()
        return jsonify({'Message':"The user has been promoted!"})
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id=%s",(user_id, ))
        user_exist = cur.rowcount
        if user_exist == 0:
            return jsonify({'Messsage':'No user Found!'})
        cur.execute("DELETE FROM users WHERE user_id=%s",(user_id,))
        conn.commit()
        cur.close()
        return jsonify({'Message':"The user has been deleted!"})
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not  auth.password  or not auth.username:
        return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})
    
        token = jwt.encode({'user':auth.username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(seconds=15)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token})
    
if __name__ == '__main__':
    app.run(debug=True)