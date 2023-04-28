import time 
import serial
import telepot
import sys
import threading
from threading import Thread
import os
import Adafruit_IO
from Adafruit_IO import Client

ser = serial.Serial("/dev/ttyACM0", baudrate=9600)#Modificar el puerto serie de ser necesarioser = serial.Serial("/dev/ttyACM0", baudrate=9600)#Modificar el puerto serie de ser necesario
bot= telepot.Bot('6202600533:AAECtlBNcMdXKC0Xw8uu4fIqG1-Jwsjox50')

aoi = Client('Puppango','aio_diIF265GloMVnhK53wwUEgJJGOPl')
feeds_temperature = aoi.feeds('temperature')
feeds_humidity = aoi.feeds('humidity')
feeds_brightness = aoi.feeds('brightness')

def sendRecieve(command):
	ser.write((command+ '\n').encode())
	time.sleep(0.1)
	read = ser.readline().decode('utf-8') 
	read = read.rstrip(read[-1])
	return read

def handle (msg):
	userName = msg['from']['first_name']
	
	content_type, chat_type, chat_id = telepot.glance(msg)
	
	if content_type == 'text':
		command =msg['text']
		print('Comando obtenido: %s' % command)
		
		if 'start' in command:
			bot.sendMessage(chat_id, "Hola, " + userName + "\nMi nombre es: Q SED bot, Te muestro la lista de comandos que puedo reconocer:\n")
			
		elif 'temperature' in command:
			recieved = sendRecieve(command)
			aoi.send_data(feeds_temperature.key,float(recieved))
			bot.sendMessage(chat_id, "The temperature is: " + recieved + "ºC")
			
		elif 'humidity' in command:
			recieved = sendRecieve(command)
			aoi.send_data(feeds_humidity.key,float(recieved))
			bot.sendMessage(chat_id, "The humidity is: " + recieved + "%")
		elif 'hot' or 'cold' or 'off' or 'light_came_on' or 'light_came_off' in command:
			recieved = sendRecieve(command)
			bot.sendMessage(chat_id, recieved)
		elif 'light' in command:
			recieved = sendRecieve(command)
			aoi.send_data(feeds_brightness.key,float(recieved))
			bot.sendMessage(chat_id, "The brightness is: " + recieved)
		else:
			bot.sendMessage(chat_id, "This command is not supported, please, try again")

class Station():
	
	def __init__(self):
		print('Bot activado')
		print('Esperando comandos...')
		self.inicialize()

	def inicialize(self):

		def run(self):
			threading.Thread(target = commands, args = (self,)).start()
			threading.Thread(target = automatic, args = (self,)).start()
            
		def commands(self):
			
			
			
			bot.message_loop(handle)
			
			while True:
				time.sleep(20)

		def automatic(self):
			flagT = False
			flagL = False
			time.sleep(3)
			while True:
				temperature = sendRecieve("/temperature")
				aoi.send_data(feeds_temperature.key,float(temperature))
				print("The temperature is: " + temperature)
				if (not flagT) and float(temperature) > 30:
					print(sendRecieve("/hot"))
					flagT = True
					
				elif (not flagT) and float(temperature) < 10:
					print(sendRecieve("/cold"))
					flagT = True
					
				elif flagT and float(temperature) > 15 and float(temperature) < 25:
					print(sendRecieve("/off"))
					flagT = False
				
				humidity = sendRecieve("/humidity")
				aoi.send_data(feeds_humidity.key,float(humidity))
				print("The humidity is: " + humidity)
				
				light = sendRecieve("/light")
				aoi.send_data(feeds_brightness.key,float(light))
				print("The brightness is: " + light)
				if (not flagL) and float(light) < 750:
					print(sendRecieve("/light_came_on"))
					flagL = True
				elif flagL and float(light) > 750:
					print(sendRecieve("/light_came_off"))
					flagL = False
				
				time.sleep(300)#Esto cambiarlo a 5 min

		run(self)

Station()
			
