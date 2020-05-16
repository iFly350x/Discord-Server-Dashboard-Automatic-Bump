from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import schedule
from pathlib import Path
from typing import *

class DiscordBump:

	DRIVER_PATH = Path('D:\WEB\web\chromedriver.exe')
	SERVER_URL = 'https://discord.com/channels/688209977583862054/688226442588454912'

	def __init__(self) :
		self.browser = webdriver.Chrome(self.DRIVER_PATH)

	def login(self) -> None:
		"""
		Navigate to discord link, fill login form
		:return: None
		"""
		email, password = credentials()
		self.browser.get(self.SERVER_URL)
		WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'form')))
		email_field = self.browser.find_element_by_xpath('.//*[@name="email"]')
		email_field.send_keys(email)
		password_field = self.browser.find_element_by_xpath('.//*[@name="password"]')
		password_field.send_keys(password)
		time.sleep(.1)
		password_field.send_keys(Keys.RETURN)
		self.send_bump()

	def send_bump(self) -> None:
		"""Send command in the channel"""
		time.sleep(5)
		text_box = self.browser.find_element_by_css_selector('.textArea-12jD-V > .markup-2BOw-j')
		text_box.send_keys('!d bump')
		# text_box.send_keys(Keys.RETURN)
		time.sleep(2)
		self.browser.close()

	# def count_bumps(self, i=[0]):   #COUTNS NUMBER OF BUMPS
	# 	i[0] += 1
	# 	print(f"Times Bumped: {i}")

	def schedule_bumps(self):
		schedule.every(2).hours.do(self.send_bump)
		schedule.every(2).hours.do(self.count_bumps)

def credentials() -> Tuple[str,str]:
		'''Taking discord  credentials'''
		with open('info.txt', 'r') as f:
			contents = f.readlines()
			return contents[0].strip(), contents[1].strip()


def main() -> None:
	bot = DiscordBump()
	bot.login()

if __name__ == '__main__':
	record = {'count': 0}

	def tracker(data):
		data['count'] += 1
		print('Number of Bumps:', data['count'])

	schedule.every(2).seconds.do(tracker, record)
	schedule.every(2).seconds.do(main)

	while True:
		schedule.run_pending()

