import MySQLdb
from flask import request, make_response
from flask_mysqldb import MySQL
from flask import Flask, jsonify,render_template, session, redirect, url_for
#from clss import UserSignUp, Products,portfo,portfoli
import hashlib
import datetime
import jwt
import time
import socket
import json
from flask_cors import CORS




import re
from flask import jsonify


class UserSignUp:
    def __init__(self, json):
        self.FULL_NAME = json.get('FULL_NAME')
        self.EMAIL = json.get('EMAIL')
        self.PHONE_NUMBER = json.get('PHONE_NUMBER')
        self.PASSWORD = json.get('PASSWORD')
        self.CONFIRM_PASSWORD = json.get('CONFIRM_PASSWORD')

    def validatepassword(self):
        return self.PASSWORD == self.CONFIRM_PASSWORD

    def user_number_req(self):
        reg = "^[+]+(91)+[0-9]{10}$"
        pat = re.compile(reg)
        mat = re.search(pat, self.PHONE_NUMBER)
        if not mat:
            return jsonify("ph_no is invalid.@!"), 400
        else:
            print("ph_no is valid")

    def useremail_req(self):
        reg = r"(^[a-zA-Z0-9_.+-]+@([a-zA-Z])+\.(com)+$)"
        pat = re.compile(reg)
        mat = re.search(pat, self.EMAIL)
        if not mat:
            return jsonify("email is invalid.@!"), 400
        else:
            print(" email is valid")


class Products:
    def __init__(self, json):
        self.opportunity_name = json.get('opportunity_name')
        self.Opportunity_Image = json.get('Opportunity_Image')
        self.Investment_Amount = json.get('Investment_Amount')
        self.ROI = json.get('ROI')
        self.Opportunity_Type = json.get('Opportunity_Type')
        self.Opportunity_Desc = json.get('Opportunity_Desc')
        self.Area_Name = json.get('Area_Name')
        self.Area_Standard = json.get('Area_Standard')
        self.Revenue = json.get('Revenue')
        self.Expenses = json.get('Expenses')
        self.Tax = json.get('Tax')
        self.Tenant_Name = json.get('Tenant_Name')
        self.Tenant_Country = json.get('Tenant_Country')
        self.Tenant_Desc = json.get('Tenant_Desc')
        self.upload_file = json.get('upload_file')
        self.Contract_Duration = json.get('Contract_Duration')
        self.Starting_Date = json.get('Starting_Date')
        self.Ending_Date = json.get('Ending_Date')
        self.STATUS = json.get('STATUS')


class portfo:
    def __init__(self, json):
        self. TOTAL_REVENUE = json.get(' TOTAL_REVENUE')
        self.TOTAL_INVESTED_AMOUNT = json.get('TOTAL_INVESTED_AMOUNT')
        self.PROFIT = json.get('PROFIT')
        self.TOTAL_NO_OF_INVESTMENTS = json.get('TOTAL_NO_OF_INVESTMENTS')
        self.OUTLET_NAME = json.get('OUTLET_NAME')


class portfoli:
    def __init__(self, json):
        self. CL_PRODUCT_ID = json.get(' CL_PRODUCT_ID')
        self.INVESTMENT_PRODUCT_NAME = json.get('INVESTMENT_PRODUCT_NAME')
        self.LOCATION = json.get('LOCATION')
        self.INVESTMENT_AMOUNT = json.get('INVESTMENT_AMOUNT')
        self.AMOUNT = json.get('AMOUNT')
        self.GROWTH = json.get('GROWTH')
        self.PROFIT_LOSS = json.get('PROFIT_LOSS')
        self.REVENUE = json.get('REVENUE')
        self.EXPENSES = json.get('EXPENSES')





app = Flask(__name__)
CORS(app)
app.secret_key = 'SECRET KEY'
app.config['MYSQL_HOST'] = 'firstpharmcy.com'
app.config['MYSQL_USER'] = 'ukxgt8komtdul'
app.config['MYSQL_PASSWORD'] = 'uko0lgpgejnx'
app.config['MYSQL_DB'] = 'dbgg9quqi6ditx'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)




@app.route('/login01', methods=['GET', 'POST'])
def login1():
    try:
        if request.method == 'POST':
            user_details = request.json
            user_mail_id = user_details['user_mail_id']
            user_password = user_details['user_password']
           # h = hashlib.md5(password.encode())
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM invested WHERE user_mail_id = % s AND user_password= % s',
                        (user_mail_id,user_password))
            user = cur.fetchone()
            print(user)
            if not user:
                return make_response('User Not There Could not verify', 401)
            if user:
                session['Login_user_mail'] = user['user_mail_id']
                session['Login_user_id'] = user['user_id']
                session['Login_opportunity_id'] = user['opportunity_id']

                login_time = datetime.datetime.now()
                logout_time = '0000-00-00'
                insert_query = " INSERT INTO login_data VALUES(%s,%s,%s,%s)"
                cur.execute(insert_query,(session['Login_user_mail'], login_time, logout_time,session['Login_user_id']),)
                mysql.connection.commit()
                cur.close()
                token = jwt.encode({'opportunity_id': user['opportunity_id'],'user_id': user['user_id']}, "secret", algorithm="HS256")
                data = jwt.decode(token, "secret", algorithms=["HS256"])
                return data
                #return redirect(url_for('ses'))
            else:
                return 'Incorrect username / password !'
    except Exception as e:
        print(e)
    return 'out of login'


@app.route('/logout')
def logout():
    session.pop('user_mail_id', None)
    return redirect(url_for('login1'))



@app.route('/in', methods=['POST', 'GET'])
def aad():
    if request.method =='POST':
        user_id = request.json['user_id']
        cur = mysql.connection.cursor()
        resultVal = cur.execute("select * FROM invested where user_id=%s", (user_id,))

        if resultVal > 0:
            userDetails = cur.fetchall()
            return json.dumps(userDetails, default=str)

@app.route('/add', methods=['POST', 'GET'])
def naga():
    if request.method =='POST':
        user_id = request.json['user_id']
        cur = mysql.connection.cursor()
        resultVal = cur.execute("select count(OPPORTUNITY_NAME) as OPPORTUNITY_NAME from invested where user_id=%s", (user_id,))

        if resultVal > 0:
            userDetails = cur.fetchall()
            return json.dumps(userDetails, default=str)


@app.route('/som', methods=['POST', 'GET'])
def som():
    if request.method =='POST':
        user_id = request.json['user_id']
        cur = mysql.connection.cursor()
        resultVal = cur.execute("select sum(INVESTMENT_AMOUNT) as INVESTMENT_AMOUNT  from invested where user_id=%s", (user_id,))

        if resultVal > 0:
            userDetails = cur.fetchall()
            return json.dumps(userDetails, default=str)

@app.route('/rev', methods=['POST', 'GET'])
def rev():
    if request.method =='POST':
        user_id = request.json['user_id']
        cur = mysql.connection.cursor()
        resultVal = cur.execute("select sum(REVENUE) as REVENUE  from invested where user_id=%s", (user_id,))

        if resultVal > 0:
            userDetails = cur.fetchall()
            return json.dumps(userDetails, default=str)

@app.route('/prof', methods=['POST', 'GET'])
def prof():
    if request.method =='POST':
        user_id = request.json['user_id']
        cur = mysql.connection.cursor()
        resultVal = cur.execute("select sum(PROFIT_LOSS) as PROFIT_LOSS  from invested where user_id=%s", (user_id,))

        if resultVal > 0:
            userDetails = cur.fetchall()
            return json.dumps(userDetails, default=str)

@app.route('/inv', methods=['POST', 'GET'])
def aads():
    if request.method =='POST':
        opportunity_id = request.json['opportunity_id']
        cur = mysql.connection.cursor()
        resultVal = cur.execute("select * from invested where opportunity_id=%s",(opportunity_id,))

        if resultVal > 0:
            userDetails = cur.fetchall()
            return json.dumps(userDetails, default=str)

@app.route('/signup', methods=['POST','GET'])
def user_signup():
    try:
        if request.method == 'POST' and (request.json or request.form):
            ob1 = None
            print(request.json)

            if request.json:
                ob1 = UserSignUp(request.json)

            if ob1.useremail_req():
                return "invalid mail"

            if ob1.user_number_req():
                return "invalid phone number"


            if not ob1.validatepassword():
                return 'Password and confirm_password  does not match'
            else:
                print("password=confirm_password")
                h = hashlib.md5(ob1.PASSWORD.encode())
                print(h.hexdigest())
                h1 = hashlib.md5(ob1.CONFIRM_PASSWORD.encode())
                print(h.hexdigest())

                user_ip = get_ip()
                print(user_ip)
                user_date = get_date()
                print(user_date)
                user_device = get_device()
                print(user_device)
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO signup(FULL_NAME,EMAIL,PHONE_NUMBER,PASSWORD,CONFIRM_PASSWORD,USER_IP,USER_DATE_CREATED,USER_DEVICE) VALUES '
                               '(%s,%s, %s, %s,%s, %s,%s,%s)',
                               (ob1.FULL_NAME,
                                ob1.EMAIL,
                                ob1.PHONE_NUMBER,
                                h.hexdigest(),
                                h1.hexdigest(),
                                user_ip,
                                user_date,
                                user_device))
                mysql.connection.commit()
                cursor.close()
                return ({"message": "successfully created"})

    except:
        return ({"message": "user exists"})
    #return render_template('signup.html')



@app.route('/userdetails', methods=['GET', 'POST'])
def userdetail():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM signup")
        data = cur.fetchall()
        users = json.dumps(data, default=str)
        data_s = json.loads(users)
        return jsonify({'users': data_s})
    return 'Unsuccess'


@app.route('/product', methods=['POST', 'GET'])
def product():
    if request.method == 'POST' and (request.json or request.form):
        ob1 = None
        print(request.json)

        if request.json:
            ob1 = Products(request.json)

            OPPORTUNITY_ID = "IN" + fillzero().zfill(4)
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO opportunity(OPPORTUNITY_NAME,OPPORTUNITY_IMAGE,INVESTMENT_AMOUNT,ROI,OPPORTUNITY_TYPE,"
                           "OPPORTUNITY_DESC,AREA_NAME,AREA_STANDARD,REVENUE,EXPENSES,TAX,TENANT_NAME,TENANT_COUNTRY,"
                           "TENANT_DESC,UPLOAD_FILE,CONTRACT_DURATION, STARTING_DATE,ENDING_DATE,OPPORTUNITY_ID,STATUS) VALUES"
                           "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (ob1.opportunity_name,
                            ob1.Opportunity_Image,
                            ob1.Investment_Amount,
                            ob1.ROI,
                            ob1.Opportunity_Type,
                            ob1.Opportunity_Desc,

                            ob1.Area_Name,
                            ob1.Area_Standard,
                            ob1.Revenue,
                            ob1.Expenses,
                            ob1.Tax,
                            ob1.Tenant_Name,
                            ob1.Tenant_Country,
                            ob1.Tenant_Desc,

                            ob1.upload_file,
                            ob1.Contract_Duration,
                            ob1.Starting_Date,
                            ob1.Ending_Date,
                            OPPORTUNITY_ID,
                            ob1.STATUS))
            mysql.connection.commit()
            cursor.close()
            return ({"message": "successfully created"})
        return ({"message": "user exists"})


def get_ip():
    hostName = socket.gethostname()
    ipaddr = socket.gethostbyname(hostName)
    return ipaddr


def get_device():
    hostName = socket.gethostname()
    return hostName


def get_date():
    date = datetime.datetime.now()
    return date


def fillzero():
    cur = mysql.connection.cursor()
    resultVal = cur.execute("select OPPORTUNITY_ID from opportunity")
    if resultVal >= 0:
        resultVal = resultVal + 1
        mysql.connection.commit()
        use = cur.fetchall()
        cur.close()
        return json.dumps(resultVal, default=str)


@app.route('/users')
def user():
    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT * FROM opportunity")
    if resultVal > 0:
        userDetails = cur.fetchall()
        return json.dumps(userDetails,default=str)
    return "No Data Present"


@app.route('/type')
def type():
    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT TYPE FROM opportunity_type")
    if resultVal > 0:
        userDetails = cur.fetchall()
        return json.dumps(userDetails, default=str)


@app.route('/standard')
def stnd():
    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT STANDARD FROM invetment_standard")
    if resultVal > 0:
        userDetails = cur.fetchall()
        return json.dumps(userDetails, default=str)


@app.route('/country')
def cntry():
    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT COUNTRY_CODE FROM country")
    if resultVal > 0:
        userDetails = cur.fetchall()
        return json.dumps(userDetails, default=str)


@app.route('/city')
def city():
    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT CITY_NAME FROM city")
    if resultVal > 0:
        userDetails = cur.fetchall()
        return json.dumps(userDetails, default=str)


@app.route('/contract')
def con():
    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT DURATION FROM contract")
    if resultVal > 0:
        userDetails = cur.fetchall()
        return json.dumps(userDetails, default=str)


@app.route('/OPPORTUNITY_NAME')
def NAME():
    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT OPPORTUNITY_NAME FROM opportunity_name")
    if resultVal > 0:
        userDetails = cur.fetchall()
        return json.dumps(userDetails, default=str)


@app.route('/preview')
def pre():
    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT ID,OPPORTUNITY_NAME,OPPORTUNITY_IMAGE ,STARTING_DATE,AREA_NAME,OPPORTUNITY_TYPE,STATUS FROM opportunity")
    if resultVal > 0:
        userDetails = cur.fetchall()
        return json.dumps(userDetails, default=str)


@app.route('/status')
def stat():
    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT status FROM status")
    if resultVal > 0:
        userDetails = cur.fetchall()
        return json.dumps(userDetails, default=str)


@app.route('/update', methods=['GET', 'PUT'])
def up():
    if request.method == 'PUT':
        userDetails = request.json or request.form
        Id = userDetails['Id']
        opportunity_name = userDetails['opportunity_name']
        Investment_Amount = userDetails['Investment_Amount']
        ROI = userDetails['ROI']
        Opportunity_Type = userDetails['Opportunity_Type']
        Opportunity_Desc = userDetails['Opportunity_Desc']
        Area_Name = userDetails['Area_Name']
        Area_Standard = userDetails['Area_Standard']
        Revenue = userDetails['Revenue']
        Expenses = userDetails['Expenses']
        Tax = userDetails['Tax']
        Tenant_Name = userDetails['Tenant_Name']
        Tenant_Country = userDetails['Tenant_Country']
        Tenant_Desc = userDetails['Tenant_Desc']
        #upload_file = userDetails['upload_file']
        Contract_Duration = userDetails['Contract_Duration']
        Starting_Date = userDetails['Starting_Date']
        Ending_Date = userDetails['Ending_Date']
        STATUS = userDetails['STATUS']

        cur = mysql.connection.cursor()
        cur.execute("update opportunity set OPPORTUNITY_NAME=%s,INVESTMENT_AMOUNT=%s,ROI=%s,OPPORTUNITY_TYPE=%s,OPPORTUNITY_DESC=%s,"
                        "AREA_NAME=%s,AREA_STANDARD=%s,REVENUE=%s,EXPENSES=%s,TAX=%s,TENANT_NAME=%s,"
                        "TENANT_COUNTRY=%s,TENANT_DESC=%s,CONTRACT_DURATION=%s,STARTING_DATE=%s,"
                        "ENDING_DATE=%s,STATUS=%s where ID=%s",
                        (opportunity_name,Investment_Amount,ROI,Opportunity_Type,Opportunity_Desc,Area_Name,Area_Standard,
                         Revenue,Expenses,Tax,Tenant_Name,Tenant_Country,Tenant_Desc,Contract_Duration,
                         Starting_Date,Ending_Date,STATUS,Id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "REQUIREMENT UPDATED"})
    return "updated successfully!"


@app.route('/delete', methods=['POST','GET'])
def remove():
    if request.method == 'POST':
        Id = request.json['Id']
        cur = mysql.connection.cursor()
        cur.execute("delete FROM opportunity where ID=%s", (Id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Deleted Successfully"})
    return "unsuccessful!"


@app.route('/edit', methods=['POST','GET'])
def ide():
    if request.method == 'POST':
        ID = request.json['ID']
        cur = mysql.connection.cursor()
        resultVal = cur.execute("select * FROM opportunity where ID=%s", (ID,))

        if resultVal > 0:
            userDetails = cur.fetchall()
            return json.dumps(userDetails, default=str)




@app.route('/display')
def disp():
    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT ID,ROI,OPPORTUNITY_NAME,INVESTMENT_AMOUNT,AREA_NAME,OPPORTUNITY_TYPE,STATUS FROM opportunity")
    if resultVal > 0:
        userDetails = cur.fetchall()
        return json.dumps(userDetails, default=str)




@app.route('/play',methods=['GET'])
def play():
    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT ID,OPPORTUNITY_NAME FROM opportunity")
    if resultVal > 0:
        userDetails = cur.fetchall()
        return json.dumps(userDetails, default=str)




@app.route('/inves', methods=['POST', 'GET'])
def inves():
    if request.method == 'POST':
        ID = request.json['ID']
        cur = mysql.connection.cursor()
        resultVal = cur.execute("select * FROM opportunity where ID=%s", (ID,))

        if resultVal > 0:
            userDetails = cur.fetchall()
            return json.dumps(userDetails, default=str)



@app.route('/revenue', methods=['POST', 'GET'])
def revenue():
    if request.method =='POST':
        user_id = request.json['user_id']
        cur = mysql.connection.cursor()
        resultVal = cur.execute("select REVENUE  from INVESTED where user_id=%s", (user_id,))

        if resultVal > 0:
            userDetails = cur.fetchall()
            return json.dumps(userDetails, default=str)




@app.route('/first_chart', methods=['POST', 'GET'])
def userdetailsfirst():
    if request.method =='POST':
        opportunity_id = request.json['opportunity_id']
        cur = mysql.connection.cursor()
        resultVal = cur.execute("select first_chart.opportunity_id,first_chart.revenues,first_chart.months,first_chart.expenses from invested inner join first_chart on invested.opportunity_id=first_chart.opportunity_id where invested.opportunity_id=%s",(opportunity_id,))

        if resultVal > 0:
            userDetails = cur.fetchall()
            return json.dumps(userDetails, default=str)


if __name__ == "__main__":
    app.run(debug=True)
