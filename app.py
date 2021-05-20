from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from sendemail import sendgridmail
import os
import requests
import json
import re

from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
app = Flask(__name__)

authenticator = IAMAuthenticator('API')

app.secret_key = 'a'


app.config['MYSQL_HOST'] = "remotemysql.com"   
app.config['MYSQL_USER'] = "USERID"          
app.config['MYSQL_PASSWORD'] = "PASSWORD"       
app.config['MYSQL_DB'] = "DATABASE"     
   
mysql = MySQL(app)
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/forgot',methods=['GET', 'POST'])
def forget():
    msg = ''
    if request.method =='POST':
        email = request.form["email"]
        mycursor = mysql.connection.cursor()
        mycursor.execute('SELECT * FROM nutrition WHERE email = % s', (email, ))
        account = mycursor.fetchone()
        print (account)
        if account:
            msg = "!!!!!!  We have sent your credentils to your mail  !!!!!!"
            name1 = account[1]
            password1 = account[3]
            print(name1,password1)
            TEXT = "Hello "+name1 + ",\n\n"+ "Thanks for using Prajwal's Nutrition Assistant"
            CONTACT ="Your User Name = " + name1 +",\n\n"
            VALUE="Your Password = "+ password1
            #sendmail(TEXT,email)
            sendgridmail(email,TEXT,CONTACT,VALUE)
            #mycursor = cursor = mysql.connection.cursor()
            #cursor.execute('SELECT * FROM nutrition WHERE email = % s', (email, ))
           
        
            return render_template('forget.html', msg = msg)
        else:
            msg = '!!!!!!   Incorrect email/You have not registered  !!!!!!'
            return render_template("forget.html",msg = msg)
            
    return render_template("forget.html",msg = msg)


@app.route('/covid')
def covid():
    return render_template("covid.html")

@app.route('/about')
def homeq():
    return render_template("about.html")

@app.route('/subscribe',methods=['GET', 'POST'])
def subscribe():
    msg="Enter your email"
    if request.method =='POST':
        email=request.form['email']
        msg = "~~~You are successfully subscribed~~~"
        TEXT="Thankyou for subscribing"
        CONTACT="Register to accesses other srvices "
        VALUE=""
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO subscribe VALUES (NULL, % s)', (email,))
        mysql.connection.commit()
        sendgridmail(email,TEXT,CONTACT,VALUE)
    return render_template("index.html",msg=msg)

@app.route('/services')
def homesz():
    return render_template("services.html")


@app.route('/contact',methods=['GET', 'POST'])
def contact():
    if request.method =='POST':
        contactname = request.form['YourName']
        contactmail = request.form['Email']
        contactphone = request.form['PhoneNumber']
        contactmsg = request.form['Message']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO contact VALUES (NULL, % s, % s, % s, % s)', (contactname, contactmail,contactphone,contactmsg))
        mysql.connection.commit()
        msg ="!!!!!Your message has been received!!!!!! "
        TEXT ="Hello "+contactname + ",\n\n"
        CONTACT = "We have received your message we will consider your request and process it soon.Do register our services."
        #sendmail(TEXT,contactmail)
        VALUE =""
        sendgridmail(contactmail,TEXT,CONTACT,VALUE)
        return render_template("index.html",msg=msg)
    
@app.route('/contact1',methods=['GET', 'POST'])
def contact1():
    if request.method =='POST':
        contactname = request.form['YourName']
        contactmail = request.form['Email']
        contactphone = request.form['PhoneNumber']
        contactmsg = request.form['Message']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO contact VALUES (NULL, % s, % s, % s, % s)', (contactname, contactmail,contactphone,contactmsg))
        mysql.connection.commit()
        msg ="!!!!!Your message has been received!!!!!! "
        
        TEXT = "Hello "+contactname + ",\n\n"
        CONTACT="We have received your message we will consider your request and process it soon.Do register our services."
        VALUE=""
        #sendmail(TEXT,contactmail)
        sendgridmail(contactmail,TEXT,CONTACT,VALUE)
        return render_template("index1.html",msg1=msg)
    

@app.route('/register', methods =['GET', 'POST'])
def registet():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM nutrition WHERE email = % s', (email,))
        account = cursor.fetchone()
        mycursor = mysql.connection.cursor()
        mycursor.execute('SELECT * FROM nutrition WHERE username = % s', (username,))
        account1 = mycursor.fetchone()
        print(account)
        if account:
        
            msg = 'Account already exists on this email!'
            
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            if account1:
                msg = "this user name is alredy taken by someone try other user name"
            else:
                cursor.execute('INSERT INTO nutrition VALUES (NULL, % s, % s, % s)', (username, email, password))
                mysql.connection.commit()
                msg = 'You have successfully registered !'
                TEXT = "Hello "+username + ",\n\n"
                CONTENT="""Thanks for registering Prajwal's Nutrition Assistant """
                #sendmail(TEXT,email)
                VALUE=""
                sendgridmail(email,TEXT,CONTENT,VALUE)
            
                cursor.execute("CREATE TABLE "+username+" (id INT AUTO_INCREMENT PRIMARY KEY, date VARCHAR(255), time VARCHAR(255), food VARCHAR(255), Protein FLOAT, lipid FLOAT, Carbohydrate FLOAT, Energy FLOAT, Sugars FLOAT, Iron FLOAT, Sodium FLOAT, Vitamin_A FLOAT, Vitamin_C FLOAT, Cholesterol FLOAT, Fatty_acids_trans FLOAT, Fatty_acids_saturated FLOAT, Calcium FLOAT, Fiber FLOAT)")
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register12.html', msg = msg)
'''
@app.route('/track')
def track():
    return render_template("contact.html")
'''

@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM nutrition WHERE username = % s AND password = % s', (username, password ),)
        account = cursor.fetchone()
        print (account)
        if account:
            #session['loggedin'] = True
            #session['id'] = account[0]
            #userid =  account[0]
            #session['username'] = account[1]
            
            msg = 'Logged in successfully !'
        
            return render_template('index1.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
            
    
    return render_template('login2.html', msg = msg)
    


@app.route('/dashboard',methods =['GET', 'POST'])
def homee():
    
    return render_template('index1.html')


@app.route('/track',methods= ['GET','Post'])
def trackimage():
    msg = ""
    v = ""
    x = 0
    
    session.clear()
    if request.method == 'POST':
        username= request.form['username']
        password = request.form['password']
        date = request.form['date']
        time= request.form['Time']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM nutrition WHERE username = % s AND password = % s', (username, password ),)
        account = cursor.fetchone()
        if account:
            if request.files['image']:
                if request.method == 'POST':
                    f = request.files['image']
                    visual_recognition = VisualRecognitionV3(
                        version='2018-03-19',
                        authenticator=authenticator)
                    visual_recognition.set_service_url('URL') 
                    classes = visual_recognition.classify(images_filename=f.filename, 
                                              images_file=f ,classifier_ids='food').get_result() 
                    data=json.loads(json.dumps(classes,indent=4))

                    x=data["images"][0]['classifiers'][0]["classes"][0]["class"]
        
                    if x:
                   
                        def call_API_2(foodName, apiKey):
                            data = {"query" : foodName}
                            url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={apiKey}'
                            r = requests.post(url, json=data)
                            return r.json()
        
                        ans = call_API_2(x, "API")
        
                        v1 = ans["foods"][0]['description']
                        
                        v = "Food you had is = "+ x
                        session['food']= x
                        session['username'] = username
                        session['date'] = date
                        session['time'] = time
                        print(session['date'])
                        print(session['time'])
                        ans = call_API_2(v, "API")
                        y={"a":"a"}
                        print(ans["foods"][0]['description'])
                        
                        y['Protein']=y['Total lipid (fat)']=y['Carbohydrate, by difference']=y['Energy']=y['Sugars, total including NLEA']=y['Fiber, total dietary']=y['Calcium, Ca']=y['Calcium, Ca']=y['Sodium, Na']=y['Vitamin A, IU']=y['Vitamin C, total ascorbic acid']=y['Cholesterol']=y['Fatty acids, total saturated']=y['Fatty acids, total trans']=0.0
                        for concept in ans["foods"][0]["foodNutrients"]:
                            y.update({concept["nutrientName"]: concept["value"]})
                        print(y)
                        session['Protein']=y['Protein']
                        session['fat']=y['Total lipid (fat)']
                        session['carbohydrate']=y['Carbohydrate, by difference']
                        session['Energy']=y['Energy']
                        session['sugar']=y['Sugars, total including NLEA']
                        session['fiber']=y['Fiber, total dietary']
                        session['calcium']=y['Calcium, Ca']
                        session['iron']=y['Calcium, Ca']
                        session['sodium']=y['Sodium, Na']
                        session['vitamin_a']=y['Vitamin A, IU']
                        session['vitamin_c']=y['Vitamin C, total ascorbic acid']
                        session['cholesterol']=y['Cholesterol']
                        session['trans_fat']=y['Fatty acids, total trans']
                        session['sat_fat']=y['Fatty acids, total saturated']
                        print(type(session['sat_fat']))
                        print(type(session['date']))
       
                        
                        msg = "!!!!!!!        scroll down             !!!!!!!!!!"
                        return render_template('contact.html',v=v,msg=msg,ans=ans["foods"][0]["foodNutrients"] )
                    else:
                        v = "We cannot find the proper food in the image.Please try again"
            else:
                v = "We cannot find the proper food in the image.Please try again"
            
        else:
            msg ="~~~~~~~Invalid user id and password~~~~~~~~~~"
            v = "Invalid user id and password"

    return render_template('contact.html',v=v,msg=msg )

@app.route('/submit',methods= ['GET','Post'])
def submit():
    msg = "~~~~~~we did not find any matching response please try again~~~~~~~~"
    if session:
        
        mcursor = mysql.connection.cursor()
        mcursor.execute('INSERT INTO '+session['username']+' VALUES (NULL,% s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', ( session['date'], session['time'],session['food'], session['Protein'], session['fat'], session['carbohydrate'], session['Energy'], session['sugar'], session['fiber'],session['calcium'], session['iron'], session['sodium'], session['vitamin_a'], session['vitamin_c'], session['cholesterol'], session['trans_fat'], session['sat_fat']))
        mysql.connection.commit()
        msg = "~~~~~~we have received your data~~~~~~~~"
        session.clear()
        return render_template('contact.html', msg=msg)
    return render_template('contact.html', msg=msg)
    

@app.route('/trackdata',methods= ['GET','Post'])
def trackdata():
    msg = "!!!!!!!        scroll down             !!!!!!!!!!"
    v = "Wrong spelling/Food not found"
    x = 0
    
    session.clear()
    if request.method == 'POST':
        username= request.form['username']
        password = request.form['password']
        date = request.form['date']
        time= request.form['Time']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM nutrition WHERE username = % s AND password = % s', (username, password ),)
        account = cursor.fetchone()
        if account:

                if request.method == 'POST':
                    x = request.form['data']

                    if x == "sweet":
                        x = "sugar"
        
                    if x:
                   
                        def call_API_2(foodName, apiKey):
                            data = {"query" : foodName}
                            url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={apiKey}'
                            r = requests.post(url, json=data)
                            return r.json()
        
                        ans = call_API_2(x, "API")
                        if x == "sugar":
                            x="sweet"
                        
                        if ans["totalHits"]:
                            v1 = ans["foods"][0]['description']
                            v = "Food you had is = "+ v1
                           
                            msg = "!!!!!!!        scroll down             !!!!!!!!!!"
                            session['username'] = username
                        
                            session['date'] = date
                            session['time'] = time
                            print(session['date'])
                            print(session['time'])
                            #ans = call_API_2(v, "API")
                            y={"a":"a"}
                            #print(ans["foods"][0]['description'])
                        
                            y['Protein']=y['Total lipid (fat)']=y['Carbohydrate, by difference']=y['Energy']=y['Sugars, total including NLEA']=y['Fiber, total dietary']=y['Calcium, Ca']=y['Calcium, Ca']=y['Sodium, Na']=y['Vitamin A, IU']=y['Vitamin C, total ascorbic acid']=y['Cholesterol']=y['Fatty acids, total saturated']=y['Fatty acids, total trans']=0.0
                            for concept in ans["foods"][0]["foodNutrients"]:
                                y.update({concept["nutrientName"]: concept["value"]})
                            #print(y)
                            session['food']=v1
                            session['Protein']=y['Protein']
                            session['fat']=y['Total lipid (fat)']
                            session['carbohydrate']=y['Carbohydrate, by difference']
                            session['Energy']=y['Energy']
                            session['sugar']=y['Sugars, total including NLEA']
                            session['fiber']=y['Fiber, total dietary']
                            session['calcium']=y['Calcium, Ca']
                            session['iron']=y['Iron, Fe']
                            session['sodium']=y['Sodium, Na']
                            session['vitamin_a']=y['Vitamin A, IU']
                            session['vitamin_c']=y['Vitamin C, total ascorbic acid']
                            session['cholesterol']=y['Cholesterol']
                            session['trans_fat']=y['Fatty acids, total trans']
                            session['sat_fat']=y['Fatty acids, total saturated']
                            #cursor.execute('INSERT INTO'+session['username']+' VALUES (NULL, % s, % s, %s, % f, % f, % f, % f, % f, % f, % f, % f, % f, % f, % f, % f, % f, % f)', ( session['date'], session['time'], session['food'], session['Protein'], session['fat'], session['carbohydrate'], session['Energy'], session['sugar'], session['fiber'],session['calcium'], session['iron'], session['sodium'], session['vitamin_a'], session['vitamin_c'], session['cholesterol'], session['trans_fat'], session['sat_fat']))
                            
                        
                            return render_template('contact.html',v=v,msg=msg,ans=ans["foods"][0]["foodNutrients"] )
                    else:
                        v = "Wrong spelling/Food not found"
                        return render_template('contact.html', v=v, msg=msg)

            
        else:
            msg ="~~~~~~~Invalid user id and password~~~~~~~~~~"
            v = "Invalid user id and password"

    return render_template('contact.html',v=v,msg=msg )
@app.route('/diary',methods =['GET', 'POST'])
def diary1():
    return render_template("display.html")

@app.route('/diarydata',methods =['GET', 'POST'])
def diary():
    msg = "~~~~Invalid Request~~~~"
    if request.method == 'POST':
        
        fromdate = request.form['fromdate']
        todate = request.form['todate']
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM nutrition WHERE username = % s AND password = % s', (username, password ),)
        account = cursor.fetchone()
        if account:
            msg = "View your data here"
            email=account[2]
            
            fromdate= fromdate
            todate= todate
            ncursor = mysql.connection.cursor()
            ncursor.execute('SELECT * FROM '+username+' WHERE date BETWEEN % s AND % s ',(fromdate,todate))
            naccount=ncursor.fetchall()
            x=('Protein','lipid','Carbohydrate','Energy','Sugars','Fiber','Calcium','Iron','Sodium','Vitamin_A','Vitamin_C','Cholesterol','Fatty_acids_trans','Fatty_acids_saturated')
            y=('g','g','g','kcal','g','g','mg','mg','mg','iu','iu','mg','g','g')
            i=0
            temp=[]
            while i!=14:
                ncursor.execute("SELECT SUM("+x[i]+") FROM "+username+" WHERE date BETWEEN % s AND % s ",(fromdate,todate))    
                zaccount=ncursor.fetchall()
                temp.append(str(round(zaccount[0][0],2)))
                
                i+=1
            temp1=tuple(temp)
            j=0
            temp2=[]
            while j!=14:
                
                temp2.append(x[j]+"    "+temp[j]+y[j])
                
                
                j+=1
            temp3=tuple(temp2)
            print(str(temp3))   
            TEXT = "Hello "+username + ",\n\n"
            CONTENT="You have consumed the following nutrients  From - "+fromdate+ "  "+"To-"+todate+ ",\n\n"
            VALUE=",\n\n".join(temp3)+""
            #sendmail(TEXT,email)
            sendgridmail(email,TEXT,CONTENT,VALUE)
            
            if naccount !=():
                msg = "Visit Us Again"
                return render_template("data.html",account=naccount,temp1=temp1,x=x,msg=msg)
            
            
            else:
                msg = "You have not entered any data between these dates"
        else:
            msg = "~~~~~Invalid data/ Account does not exist~~~~~"
       
    return render_template("display.html",msg=msg)
                
@app.route('/display',methods =['GET', 'POST'])
def gfg():
    msg = "!!!!!!!        scroll down             !!!!!!!!!!"
    v = "~~~~We cannot find the proper food in the image.Please try again~~~~~"
    x = 0
    if request.files['image']:
        if request.method == 'POST':
            f = request.files['image']
            
            visual_recognition = VisualRecognitionV3(
                        version='2018-03-19',
                        authenticator=authenticator)
            visual_recognition.set_service_url('URL') 
            classes = visual_recognition.classify(images_filename=f.filename, 
                                              images_file=f,classifier_ids='food').get_result() 
            data=json.loads(json.dumps(classes,indent=4))

            x=data["images"][0]['classifiers'][0]["classes"][0]["class"]
       
        
            
        
        
        
            if x:
                   
                def call_API_2(foodName, apiKey):
                    data = {"query" : foodName}
                    url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={apiKey}'
                    r = requests.post(url, json=data)
                    return r.json()
        
                ans = call_API_2(x, "API")
            
                v = ans["foods"][0]['description']
                v = "Your entered food is "+x
       
            
                msg = "!!!!!!!        scroll down             !!!!!!!!!!"
                return render_template('services.html',v=v,msg=msg,ans=ans["foods"][0]["foodNutrients"] )
        else:
            v = "~~~We cannot find the proper food in the image.Please try again~~~~"
        return render_template('services.html',v=v,msg=msg )
    else:
        return render_template('services.html',v=v,msg=msg )

@app.route('/url',methods =['GET', 'POST'])
def happy():
    msg = "!!!!!!!        scroll down             !!!!!!!!!!"
    v = "~~~Not entered Food image/Wrong spelling~~~"
    x = 0
    if request.method == 'POST':
        url1 = request.form["url1"]
        if url1:
            visual_recognition = VisualRecognitionV3(
                        version='2018-03-19',
                        authenticator=authenticator)
            visual_recognition.set_service_url('URL') 
            classes = visual_recognition.classify(url=url1 ,classifier_ids='food').get_result() 
            data=json.loads(json.dumps(classes,indent=4))

            x=data["images"][0]['classifiers'][0]["classes"][0]["class"]
        
        
        
        if x:
    
            def call_API_2(foodName, apiKey):
                data = {"query" : foodName}
                url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={apiKey}'
                r = requests.post(url, json=data)
                return r.json()

            ans = call_API_2(x, "API key")
        
            v = ans["foods"][0]['description']
            v = "Your entered food is "+x
            
            msg = "!!!!!!!        scroll down             !!!!!!!!!!"
            return render_template('services.html',v=v,msg=msg,ans=ans["foods"][0]["foodNutrients"] )
        else:
            v = "~~~invalid URL/Food not food~~~"
        return render_template('services.html',v=v,msg=msg )    
    else:
        return render_template('services.html',v=v,msg=msg )

@app.route('/data',methods =['GET', 'POST'])
def data():
    msg = "!!!!!!!        scroll down             !!!!!!!!!!"
    v = "~~~Wrong spelling/Food not found~~~"
    if request.method == 'POST':
        x = request.form["data"]
     
        if x == "sweet":
            x = "sugar"
        
        if x:        
            def call_API_2(foodName, apiKey):
                data = {"query" : foodName}
                url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={apiKey}'
                r = requests.post(url, json=data)
                return r.json()

            ans = call_API_2(x, "API key")
            if x=="sugar":
                x="sweet"
        
        
            if ans["totalHits"]:
                v = ans["foods"][0]['description']
                v = x
                v = "Your entered food is "+x
                msg = "!!!!!!!        scroll down             !!!!!!!!!!"
                return render_template('services.html',v = v,msg=msg,ans=ans["foods"][0]["foodNutrients"] )    
            else :
                v = "~~~Wrong spelling/Food not found~~~"
                return render_template('services.html',v=v,msg=msg )
        else:
            return render_template('services.html',v=v,msg=msg )
    else:
        return render_template('services.html',v=v,msg=msg )
    
@app.route('/read',methods =['GET', 'POST'])
def read():
    
    msg = "!!!!!!!        scroll down             !!!!!!!!!!"
    v = "~~~Wrong spelling/Food not found~~~"
    if request.method == 'POST':
        x = request.form["data"]
     
        if x == "sweet":
            x = "sugar"
        
                
        def call_API_2(foodName, apiKey):
            data = {"query" : foodName}
            url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={apiKey}'
            r = requests.post(url, json=data)
            return r.json()

        ans = call_API_2(x, "42d93mMY4R0b2Mt3RUAvt2bMqzbHRiOEhSCHHzOB")
        print(ans)
        if x=="sugar":
            x="sweet"
        v = x
        v = "Your entered food is "+x
        
        
        if ans["totalHits"]:
            v = ans["foods"][0]['description']
            msg = "!!!!!!!        scroll down             !!!!!!!!!!"
            return render_template('1.html',v = v,msg=msg,ans=ans["foods"][0]["foodNutrients"] )    
        else :
            v = "Wrong spelling/Food not found"
        return render_template('1.html',v=v,msg=msg )
    
    


@app.route('/logout')
    
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.clear()
    msg="!!! Successfully loged out !!!!"
    return render_template('index.html',msg=msg)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True,port = 8080)
