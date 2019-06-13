import RPi.GPIO as GPIO
import time
import logging
import traceback
import sqlite3

class Feeder(object):
	feedTime = 0
        __pinOne = 11
        __pinTwo = 13
        __pinPwm = 12
        __frequency = 5
        __dutyCycle = 10
	__outcome = ""

        def __init__(self, feedTime=4):
                self.feedTime = feedTime
		logging.basicConfig(format="%(asctime)s\t%(levelname)s\t%(message)s",filename="\home\pi\robot\feeder\feeder.log", level=logging.INFO)

        def feed(self):
		try:
              		logging.info("Feeding for " + str(self.feedTime) + " seconds")

		  	GPIO.setwarnings(False)
                	GPIO.setmode(GPIO.BOARD)
 
	               	GPIO.setup(self.__pinOne,GPIO.OUT) #motor control PIN 1
                	GPIO.setup(self.__pinTwo,GPIO.OUT) #motor control PIN 2
                	GPIO.setup(self.__pinPwm,GPIO.OUT) #PWM PIN

			logging.info("Starting Motor...")

                	GPIO.output(self.__pinOne,0)
                	GPIO.output(self.__pinTwo,1)
			GPIO.output(self.__pinPwm,GPIO.HIGH)

			logging.info("Motor Started Successfully")
			logging.info("Starting PWM...")

                	GPIO.output(self.__pinPwm, True)          ## enable motor PWM
                	p=GPIO.PWM(self.__pinPwm, self.__frequency)          ## frequency

                	p.start(1)

                	p.ChangeDutyCycle(self.__dutyCycle)

			logging.info("PWM Started Successfully")

			logging.info("Feeding...")
	
                	time.sleep(self.feedTime)

			logging.info("Done Feeding")	
			logging.info("Stopping PWM")

			p.stop()

			logging.info("PWM Stopped")
			logging.info("Feed Completed Successfully")
			self.__outcome = "OK"

		except:
			logging.error("An Error Has Occured. Feeding was not completed!")
			logging.error(traceback.print_exc())
			logging.error("Feed Completed with Errors")
			self.__outcome = "Error Feeding: " + traceback.print_exc()
		finally:
			logging.info("Cleaning Up, clearing pins")
			GPIO.cleanup()

		try:
			if (self.__outcome == "OK"):
				self.__updateDate()
				self.getDate()
		except:
			logging.error(traceback.print_exc())
		finally:
			return self.__outcome

	def __updateDate(self):
		conn = sqlite3.connect('/home/pi/robot/feeder/CatFeeder.db')
		c = conn.cursor()
		c.execute("UPDATE feedLog SET lastFeed = datetime('now');")
		conn.commit()
		conn.close()
	
	@staticmethod
	def getDate():
		updateDate = ""		

		conn = sqlite3.connect('/home/pi/robot/feeder/CatFeeder.db')
                c = conn.cursor()
		c.execute("SELECT datetime(lastfeed, 'localtime')  FROM feedLog;")
				
		for row in c:
			updateDate = row[0]

		conn.close()

		return updateDate
