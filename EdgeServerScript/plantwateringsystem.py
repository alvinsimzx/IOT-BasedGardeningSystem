import serial
import RPi.GPIO as GPIO
import time
import MySQLdb
import datetime
import sys
from firebase import firebase
from google.cloud import pubsub_v1
import json

arduino = serial.Serial('/dev/ttyACM0',9600)

project_id = "smarthomeiot-313717" # enter your project id here
topic_name = "gardeningdata" # enter the name of the topic that you created
 
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)
 
futures = dict()
 
def get_callback(f, data):
    def callback(f):
        try:
            # print(f.result())
            futures.pop(data)
        except:
            print("Please handle {} for {}.".format(f.exception(), data))
 
    return callback


def water_command(): #manually trigger watering system
    arduino.write(b"low_moisture\n")
    

def open_shade_command(): #manually open shade
    arduino.write(b"low_sunlight\n")
    shadeOpened = True

def close_shade_command(): #manually close shade
    arduino.write(b"high_sunlight\n")
    shadeOpened = False

def main():
    #fb= firebase.FirebaseApplication('https://smarthomeiot-eaf51-default-rtdb.firebaseio.com/')
    shadeOpened = True;
    #Default threshold values
    thresholdSunlight = 0
    thresholdSoil = 0
    thresholdTemperature = 0
    while futures:
        time.sleep(5)
    while True:
        
        #connect to MySQL Database
        dbConn = MySQLdb.connect("localhost","pi","","plant_db") or dle("Could not connect to database")
        print(dbConn)
        while(arduino.in_waiting == 0):
             pass
        
        #Read Serial data sent by Arduino and split it
        line = arduino.readline()
        data = str(line).split(":")[1].split(",")
        Temp = int(data[0])
        Hum = int(data[1])
        Soil = int(data[2])
        Sunlight = int(data[3].split("\\r\\n")[0])
        print(Temp,Hum,Soil,Sunlight)# for debugging purposes
        thresholdResult = None
        
        with dbConn:#Insert received Arduino data into Database table "sensorInfor"
            cursor = dbConn.cursor()
            cursor.execute("INSERT INTO sensorInfor (temperature,humidity,SoilMoisture,Sunlight) VALUES (%s,%s,%s,%s)"%(Temp,Hum,Soil,Sunlight))
            cursor.execute("SELECT tempThresVal,sunThresVal,soilThresVal from thresholdVal WHERE thresholdID=1")
            thresholdResult = cursor.fetchone()
            dbConn.commit()
            cursor.close()
        
        thresholdTemperature = thresholdResult[0]
        thresholdSunlight = thresholdResult[1]
        thresholdSoil = thresholdResult[2]
        #result = fb.post('GardeningSystem', {'Temp':str(Temp),'HUM':str(Hum), 'Soil':str(Soil),'Sunlight':str(Sunlight)})
        datapublish = {"Temperature":Temp, "Humidity" : Hum,"SoilMoisture":Soil,"Sunlight":Sunlight}
        # When you publish a message, the client returns a future.
        future = publisher.publish(
            topic_path, data=(json.dumps(datapublish)).encode("utf-8")) # data must be a bytestring.
        # Publish failures shall be handled in the callback function.
        future.add_done_callback(get_callback(future, datapublish))
        
        #Automatically trigger actuators if fulfill condition
        if(Soil<thresholdSoil): #change the comparison operator later
            arduino.write(b"low_moisture\n")
        elif((Sunlight>=thresholdSunlight) and shadeOpened and Temp>=thresholdTemperature):
            arduino.write(b"high_sunlight\n") #if above sunlight and temperature threshold and shade was opened  
            shadeOpened = False
        elif((Sunlight<thresholdSunlight) and not shadeOpened and Temp<thresholdTemperature):
            arduino.write(b"low_sunlight\n") #if below sunlight and temperature threshold and shade was closed  
            shadeOpened = True
               
        
if __name__ == "__main__" :
    main()
    
    