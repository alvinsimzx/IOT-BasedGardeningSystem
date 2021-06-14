# IOT-BasedGardeningSystem

This was an IOT-based project for the unit SWE30011 IOT PROGRAMMING, which is a gardening system built with the Arduino microcontroller and the Raspberry Pi.

Materials:
1. Arduino Uno Board
2. Raspberry Pi 4
3. Breadboard
4. Servo Motor
5. 28BYJ-48 Stepper Motor
6. ULN2003 Driver
7. Soil Moisture Sensor
8. LCD Display Screen 16x2 I2C
9. DHT22 Humidity and Temperature Sensor
10. LDR Resistor
11. Jumper Wires

## Explanation on the System

The proposed solution is an IOT-based system for monitoring the condition of a plant and its surroundings, which is reported back to the web server. For this solution, the IOT node would be built around the Arduino microcontroller, which would be connected to various sensing devices for collecting data as well as the actuators for performing the maintenance processes, such as watering the plant. These IOT nodes are then connected to the Raspberry Pi, which act as the main edge device to collect sensor data sent by the Arduino and stores the information in a database table. 

The type of database would be MySQL database, which stores a simple database table for data collection purposes. Aside from storing data, the Pi would use information stored in the database to decide any actions that needs to be taken, such as triggering the actuator for watering the plant. Therefore, the Pi would receive data from the IOT nodes to be stored in the database, which in turn helps with the evaluation for triggering the actuators in the IOT nodes. Aside from being an Edge device, the Pi would host a web server, which contains a web application built on Django, for the user to interact with the system.

## Arduino Set Up
![image](https://user-images.githubusercontent.com/24734828/121903569-04bac880-cd5b-11eb-8cd0-7d381fee61a6.png)

## Overall System Architecture
![image](https://user-images.githubusercontent.com/24734828/121903876-506d7200-cd5b-11eb-9511-e1df11a8cd05.png)

## Database Design
![image](https://user-images.githubusercontent.com/24734828/121903732-2b78ff00-cd5b-11eb-8fb5-2dad7d157edb.png)

## Software Block Diagram
![image](https://user-images.githubusercontent.com/24734828/121903794-3af84800-cd5b-11eb-8c94-1c66834c0b68.png)

## Real-life scenario Set Up
![image](https://user-images.githubusercontent.com/24734828/121904033-70049a80-cd5b-11eb-8f97-a93130b68338.png)
![image](https://user-images.githubusercontent.com/24734828/121904169-8ad70f00-cd5b-11eb-8d1c-9a97ae7d7ab1.png)
![image](https://user-images.githubusercontent.com/24734828/121904187-8f032c80-cd5b-11eb-842e-d04c2984fc32.png)

