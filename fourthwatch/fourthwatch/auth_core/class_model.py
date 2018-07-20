import requests
from django.conf import settings

BASE_URL = getattr(settings,"COMPOSER_REST_ENDPOINT","http://localhost:3000/api/")

class Bank:
	def create(self,bank_id,bank_name):
		data = {
			"$class": "org.fourthwatch.Bank",
			"bankID": bank_id,
			"name": bank_name
			}
		api_url = BASE_URL + "Bank"
		return requests.post(api_url,json=data).json()

	def get(self,id=None):
		api_url = BASE_URL + "Bank"
		if id is not None:
			api_url += "/" + id
		return requests.get(api_url).json()



class BankEmployee:
	def __init__(self):
		self.api_url =  BASE_URL + "BankEmployee"

	def create(self,bank_id,emp_id,first_name,last_name):
		data = {
			"$class": "org.fourthwatch.BankEmployee",
			"personId": emp_id,
			"name": first_name,
			"lastName": last_name,
			"bank": "resource:org.fourthwatch.Bank#%s" % bank_id
		}
		return requests.post(self.api_url,json=data).json()

	def get(self,id=None):
		if id is not None:
			self.api_url += "/" + id
		return requests.get(self.api_url).json()

class Customer:
	def __init__(self):
		self.api_url =  BASE_URL + "Customer"

	def create(self,bank_id,cust_id, company, first_name,last_name):
		data = {
			"$class": "org.fourthwatch.Customer",
			"companyName": company,
			"personId": cust_id,
			"name": first_name,
			"lastName": last_name,
			"bank": "resource:org.fourthwatch.Bank#%s" % bank_id
  		}
		return requests.post(self.api_url,json=data).json()

	def get(self,id=None):
		if id is not None:
			self.api_url += "/" + id
		return requests.get(self.api_url).json()