from flask import Flask
from flask import render_template, request, url_for, redirect, jsonify, json
import sqlite3
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from twilio.rest import Client

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/SignUp')
def sign_up():
    return render_template('SignUp.html')

@app.route('/adduser',methods = ['POST', 'GET'])
def adduser():
   print("test")
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         phone = request.form['phone']
         card = request.form['card']
         
         with sqlite3.connect("Siip.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users(name,phone,creditcard,Drinks) VALUES ('" + nm + "','" + phone + "','" + card + "', 0);")
            uID = cur.lastrowid
            con.commit()
      except:
         con.rollback()
         msg = "error in insert operation"
         return "failed"
      finally:
         con.close()
         return redirect(url_for('addtag', userID=uID))
         return "success 2"

'''@app.route('/', methods = ['POST', 'GET'])

   reader = SimpleMFRC522()

   try:
      text = input('New data:')
      print("Now place your tag to write")
      reader.write(text)
      print("written")
      return render_template('SignUp.html')
   finally:
      GPIO.cleanup()
'''
@app.route('/ScanCard/<userID>', methods = ['POST', 'GET'])
#def readtag():
def addtag(userID):

   reader = SimpleMFRC522()

   try:
      id, text = reader.read()
      with sqlite3.connect("Siip.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET tag = '"+ str(id) +"' WHERE userID = "+ userID +";")
            con.commit()
            return render_template('SignUp.html')
            return cur.execute("SELECT userID FROM users WHERE userID = "+ userID +";")
   finally:
      GPIO.cleanup()
      account_sid = "ACa4747fb78875f8b1c9c5d8574372a3e3"
      auth_token = "6ff9c35c562146b820187d848eb22703"
      with sqlite3.connect("Siip.db") as con:
         cur = con.cursor()
         cur.execute("SELECT phone FROM users WHERE userID = "+ userID +";")
         PhoneNum = cur.fetchone()
         client = Client(account_sid, auth_token)
         client.messages.create(
            to= "+"+str(PhoneNum),
            from_="+12407248181",
            body="Welcome to Siip",
            media_url="https://climacons.herokuapp.com/clear.png")

@app.route('/Drinks', methods = ['POST', 'GET'])
#its adding drinks, like it says.
def drinks():
   return render_template('drinks.html')

@app.route('/AddDrink')
def AddDrink():
   reader = SimpleMFRC522()
   try:
         id, text = reader.read()
         with sqlite3.connect("Siip.db") as con:
               cur = con.cursor()
               cur.execute("UPDATE users SET Drinks = Drinks + 1 WHERE tag = '"+ str(id) +"';")
               con.commit()
               return jsonify(results = {"success": "true"})
               #return render_template('drinks.html')
   finally:
      GPIO.cleanup()
      account_sid = "ACa4747fb78875f8b1c9c5d8574372a3e3"
      auth_token = "6ff9c35c562146b820187d848eb22703"
      with sqlite3.connect("Siip.db") as con:
         cur = con.cursor()
         cur.execute("SELECT phone FROM users WHERE tag = '"+ str(id) +"';")
         PhoneNum = cur.fetchone()
         cur = con.cursor()
         cur.execute("SELECT Drinks FROM users WHERE tag = '"+ str(id) +"';")
         DrinkAmount = cur.fetchone()
         client = Client(account_sid, auth_token)
         client.messages.create(
            to= "+"+str(PhoneNum),
            from_="+12407248181",
            body="You've had " +str(DrinkAmount)+ " drinks",
            media_url="https://climacons.herokuapp.com/clear.png")

#@app.route('/', methods = ['POST', 'GET'])
#Grabs from SQLite and sends text over twillio
'''   # put your own credentials here
   account_sid = "ACa4747fb78875f8b1c9c5d8574372a3e3"
   auth_token = "6ff9c35c562146b820187d848eb22703"
   with sqlite3.connect("Siip.db") as con:
      cur = con.cursor()
      PhoneNum = cur.execute("SELECT phone FROM users Where userID = "+ userID +";")
      con.close()
   
   client = Client(account_sid, auth_token)
   client.messages.create(
      to= "+"+PhoneNum,
      from_="+12407248181",
      body="BAAAAAALLLLLLLLSSSSSSS",
      media_url="https://climacons.herokuapp.com/clear.png")
'''