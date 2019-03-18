'''
Sensehat Dashboard
--------------------
Author: Owen De Waele
Modified: 03-12-2019
--------------------
Installation:
sudo pip3 -U Flask
Docs: http://flask.pocoo.org/docs/1.0/
'''
# Import the libraries
from flask import Flask, jsonify, render_template, request
from sense_hat import SenseHat
import sys
import os
import pyrebase
import time

config = {
  "apiKey": "AIzaSyBYCO3HevrkCz38GZHpdH7JShA17Kd39B4",
  "authDomain": "iotlabo5.firebaseapp.com",
  "databaseURL": "https://iotlabo5.firebaseio.com",
  "projectId": "iotlabo5",
  "storageBucket": "iotlabo5.appspot.com",
  "messagingSenderId": "7052501175"
}
firebase = pyrebase.initialize_app(config)

try:
  db = firebase.database()
  # Create an instance of flask
  app = Flask(__name__)

  # Create an instance of the sensehat
  sense = SenseHat()

  # Define the root route
  @app.route('/', methods=['GET'])
  def colorpicker():
	  while True:
		color = db.child('ambilight').get();
		pickedColor = color.val().lstrip('#');
		RGBColor = tuple(int(pickedColor[i:i+2], 16) for i in (0,2,4));
		print(RGBColor);
		for x in range(0,8):
			for y in range (0,8):
				sense.set_pixel(x,y,RGBColor);
		time.sleep(1)

  # Main method for Flask server
  if __name__ == '__main__':
    app.run(host = '192.168.0.156', port = 8080, debug = True)
    #app.run(host = '10.5.128.6', port = 8080, debug = True
    
  while True:
    pass
    
except (KeyboardInterrupt, SystemExit):
	sense.clear()
	print('\n' + 'Stopped ColorPicker')
	sys.exit(0)
