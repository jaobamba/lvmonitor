import requests
import lxml
import json
import time
import datetime
from colored import fg, bg, attr
from discord_webhooks import DiscordWebhooks
from bs4 import BeautifulSoup


webhookURL = ""
webhook = DiscordWebhooks(webhookURL)
ts = datetime.datetime.now()

class Monitor():
	def __init__(self):
		self.s = requests.Session()
		self.headers = {
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
		}
		self.proxies = {
		
		}

	def isProductInStock(self):
		try:
			response = self.s.get("https://secure.louisvuitton.com/ajaxsecure/getStockLevel.jsp?storeLang=eng-us&pageType=storelocator_section&skuIdList=M40712&null&_=1600213949066", headers=self.headers)

			stock = json.loads(response.text)
			ts = time.gmtime()

			return stock
		except Exception as e:
			print("A connection error has occurred.")
			raise e


	def monitorChanges(self):
		v1 = self.isProductInStock()

		while(True):
			time.sleep(5)

			v2 = self.isProductInStock()

			if(v1 == v2):
				print(v2)
				print(time.strftime("%Y-%m-%d [%H:%M:%S] ") + '%sNo Changes!%s' % (fg(1), attr(0)) + " Monitoring . . .")
				
			else:
				v1 = v2
				self.sendWebhook(v2)
				print(v2)
				print(time.strftime("%Y-%m-%d [%H:%M:%S] ") + '%sStock Change!%s' % (fg(2), attr(0)) + ' Sending Webhook . . .')
				


	def sendWebhook(self, content):
		webhook.set_content(title='POCHETTE ACCESSOIRES',description=("Bag in Stock, SKU: M40712"), url='https://us.louisvuitton.com/eng-us/products/pochette-accessoires-monogram-005656', color=0xde00ff)
		webhook.set_footer(text='JaoMonitors')
		webhook.set_thumbnail(url = 'https://i.pinimg.com/564x/0c/6e/71/0c6e71c2c293c565c49d8316259307f9.jpg')
		webhook.send()

print("Starting Monitor")
monitor = Monitor()
monitor.isProductInStock()
monitor.monitorChanges()
