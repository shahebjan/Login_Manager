import pymysql

# <<<------------------Importing flask and else------------------------>>>

from flask import Flask, render_template, redirect, request

app = Flask(__name__)

# <<<---------------Making database connection-------------------------->>>

try:
    conn = pymysql.connect(host='localhost', user='root', password='', database='mirza_mobile_store')
    print("Database connected")

# <<<-------------------------Pymysql queries--------------------------->>>

    # with conn.cursor() as cur:
    #     sql= '''
    #     CREATE TABLE users (
    #     name VARCHAR(50),
    #     username VARCHAR(50) UNIQUE,
    #     password VARCHAR(50)
    #     )
    #     '''
    #     cur.execute(sql)
    #     conn.commit()
    #     print("Table created")

    # with conn.cursor() as cur:
    #     query = '''
    #     DELETE FROM users
    #     '''
    #     cur.execute(query)
    #     conn.commit()
    #     print("deleted")


    # <<<-------------------This route will open login form------------------------->>>

    @app.route('/')
    def login():
        return render_template('login.html')

    # <<<------------------This route will take inputs from login form----------------------->>>

    @app.route('/login_validation', methods=['POST'])
    def login_validation():
        try:
            if request.method=='POST':
                l_mail=request.form.get('l_email')
                l_password=request.form.get('l_password')
                with conn.cursor() as cur:
                    query = "SELECT * FROM users WHERE username = %s AND password = %s"
                    cur.execute(query, (l_mail, l_password))
                    users = cur.fetchall()

                    if len(users)>0:
                        return render_template('home.html')
                    else:
                        return redirect('/?error=1')
        except Exception as e:
            print(e)
            return "An error occured"


    # <<<-----------------------This route will open Signup form--------------------------->>>

    @app.route('/signup')
    def signup():
        return render_template('signup.html')
    
    # <<<--------------------Thsi route will take inputs from signup page------------------->>>

    @app.route('/signup_validation', methods=['POST'])
    def signup_validation():
        with conn.cursor() as cur:
            if request.method=='POST':
                s_name = request.form.get('s_name')
                s_email = request.form.get('s_email')
                s_password = request.form.get('s_password')
                query = '''
                INSERT INTO users (name, username, password) values (%s, %s, %s)
                '''
                values = (s_name, s_email, s_password)
                cur.execute(query, values)
                conn.commit()
                return "Thanks for Signing Up"

    # <<<-------------------------This route will open home page-------------------------->>>
    @app.route('/home')
    def home():
        return render_template('home.html')

except Exception as e:
    print(e)


if __name__=="__main__":
    app.run(debug=True)

