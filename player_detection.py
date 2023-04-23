import speech_recognition as sr
import cv2
import pyttsx3
import numpy as np

class start():
	def play(self):
		vidcap = cv2.VideoCapture('cutvideo.mp4')
		success, image = vidcap.read()
		count = 0
		success = True
		idx = 0
		while success:
			hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
			lower_green = np.array([40, 40, 40])
			upper_green = np.array([70, 255, 255])
			lower_red = np.array([160, 100, 20])
			upper_red = np.array([176, 255, 255])
			lower_white = np.array([0, 0, 212])
			upper_white = np.array([100, 255, 255])

			mask = cv2.inRange(hsv, lower_green, upper_green)
			res = cv2.bitwise_and(image, image, mask=mask)
			res_bgr = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
			res_gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

			kernel = np.ones((13, 13), np.uint8)
			thresh = cv2.threshold(res_gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
			thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

			contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

			prev = 0
			font = cv2.FONT_HERSHEY_SIMPLEX

			for c in contours:
				x, y, w, h = cv2.boundingRect(c)

				if (h >= (1.5) * w):
					if (w > 15 and h >= 15):
						idx = idx + 1
						player_img = image[y:y + h, x:x + w]
						player_hsv = cv2.cvtColor(player_img, cv2.COLOR_BGR2HSV)
						#Zamalik
						mask1 = cv2.inRange(player_hsv, lower_white, upper_white)
						res1 = cv2.bitwise_and(player_img, player_img, mask=mask1)
						res1 = cv2.cvtColor(res1, cv2.COLOR_HSV2BGR)
						res1 = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
						nzCount = cv2.countNonZero(res1)
						# Ahly
						mask2 = cv2.inRange(player_hsv, lower_red, upper_red)
						res2 = cv2.bitwise_and(player_img, player_img, mask=mask2)
						res2 = cv2.cvtColor(res2, cv2.COLOR_HSV2BGR)
						res2 = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)
						nzCountred = cv2.countNonZero(res2)

						if (nzCount >= 20):
							cv2.putText(image, 'Zamalek', (x - 2, y - 2), font, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
							cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 3)
						else:
							pass
						if (nzCountred >= 20):
							cv2.putText(image, 'Ahly', (x - 2, y - 2), font, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
							cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 3)
						else:
							pass

			print(('Read a new frame: '), success)
			count += 1
			cv2.imshow('Match Detection', image)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			success, image = vidcap.read()

		vidcap.release()
		cv2.destroyAllWindows()

if __name__ == '__main__':
	engine = pyttsx3.init()
	rate = engine.getProperty("rate")
	engine.setProperty("rate", 110)
	engine.say("welcome , sir")
	engine.runAndWait()
	lis = sr.Recognizer()
	a=1
	while(a==1):
		with sr.Microphone() as source:
			print("Listen...")
			voice = lis.listen(source)
			command = lis.recognize_google(voice)
			command = command.lower()
			print(command)
			if ("open") in command:
				command = command.replace("open", '')
				obj = start()
				obj.play()
				break
			else:
				engine = pyttsx3.init()
				rate2 = engine.getProperty("rate")
				engine.setProperty("rate", 110)
				engine.say("call open")
				print("call open")
				engine.runAndWait()