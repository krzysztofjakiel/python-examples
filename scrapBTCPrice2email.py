#!/usr/bin/env python
# coding: utf-8

import datetime
import locale
import urllib2
import sys
from bs4 import BeautifulSoup

import smtplib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate

web_charset = "utf-8"
mail_charset = "ISO-2022-JP"

targeturl = "https://coinmarketcap.com/currencies/bitcoin/" # Target URL for scraping
targetclass = "#quote_price .text-large2" # Target element for scraping

from_address = "x@gmail.com" # Sender address (Gmail address)
from_password = "x" # Sender server password (Gmail password)
to_address   = "krzysztof.jakiel@gmail.com" # Recipient address

statusOK = u"Found / "
statusNG = u"Not Found"

def scraping(url):
	try:
		html = urllib2.urlopen(url).read()
		# f1=open('./testfile', 'w+')
		# f1.write(html)
		# f1.close()

		soup = BeautifulSoup(html, "lxml")
		target = soup.select(targetclass)[0].renderContents()
		# target = soup.find(id=targetclass).renderContents()

		if len(target) == 0:
			return statusNG
		else:
			return "Price for BTCUSD: " + target.decode(web_charset)
	except Exception as e:
		s = str(e)
		return statusNG + "Ex: " + s

def create_message(from_addr, to_addr, subject, body, encoding):
	msg = MIMEText(body, 'plain', encoding)
	msg['From'] = from_addr
	msg['To'] = to_addr
	msg['Subject'] = Header(subject, encoding)
	msg["Date"] = formatdate(localtime=True)
	return msg

def sendmail(subject, text):
	msg = create_message(from_address, to_address, subject, text, mail_charset)
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login(from_address, from_password)
	s.sendmail(from_address, to_address, msg.as_string())
	s.close()

if __name__ == "__main__":
	d = datetime.datetime.today()
	time = d.strftime("%Y-%m-%d %H:%M:%S")
	mailsubject = u"Bitcoin price at " + time
	mailmessage = scraping(targeturl)
	sendmail(mailsubject, mailmessage)
