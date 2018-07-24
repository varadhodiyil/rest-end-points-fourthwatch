import requests
from fourthwatch.auth_core.models import Customer, BankEmployee
from django.conf import settings
BASE_URL = getattr(settings, "COMPOSER_REST_ENDPOINT",
                   "http://localhost:3000/api/")


class InitialLOC:
    def __init__(self):
        self.api_url = BASE_URL + "LetterOfCredit"

    def get(self, id=None):
        if id is not None:
            self.api_url += "/%s" % id
        return requests.get(self.api_url).json()

    def create(self, letter_id, applicant, beneficiary, rules, product, locFile,applicant_bank,beneficiary_bank):
		data = {
			"$class": "org.fourthwatch.LetterOfCredit",
			"letterId": "%s" % letter_id,
			"applicant": "resource:org.fourthwatch.Customer#%s" % applicant,
			"beneficiary": "resource:org.fourthwatch.Customer#%s" % beneficiary,
			"issuingBank": "resource:org.fourthwatch.Bank#%s" % applicant_bank,
			"exportingBank" : "resource:org.fourthwatch.Bank#%s" % beneficiary_bank,
			"rules": rules,
			"productDetails": {
				"$class": "org.fourthwatch.ProductDetails",
				"productType": product['type'],
				"quantity": product['quantity'],
				"pricePerUnit": product['pricePerUnit']
			},
			"locFile": locFile,
			"approval": [
				"resource:org.fourthwatch.Customer#%s" % applicant
			],
			"status": "AWAITING_APPROVAL"
		}

		return requests.post(self.api_url, json=data).json()


class Approve:
	def __init__(self):
		self.api_url = BASE_URL + "Approve"
		
	def create(self, letter_id, Customer, customer_type):
		if type(customer_type) == BankEmployee:
			party = "resource:org.fourthwatch.BankEmployee#%s" % Customer
		else:
			party = "resource:org.fourthwatch.Customer#%s" % Customer
		data = {
			"$class": "org.fourthwatch.Approve",
			"loc": "resource:org.fourthwatch.LetterOfCredit#%s" %letter_id,
			"approvingParty": party
		}
		
		return requests.post(self.api_url, json=data).json()

class Reject:
	def __init__(self):
		self.api_url = BASE_URL + "Reject"
		
	def create(self, letter_id, Customer, customer_type,closeReason):
		if type(customer_type) == BankEmployee:
			party = "resource:org.fourthwatch.BankEmployee#%s" % Customer
		else:
			party = "resource:org.fourthwatch.Customer#%s" % Customer
		data = {
			"$class":"org.fourthwatch.Reject",
			"loc": "resource:org.fourthwatch.LetterOfCredit#%s" %letter_id,
			"approvingParty": party,
			"closeReason":closeReason
		}
		
		return requests.post(self.api_url, json=data).json()



class ShipProduct:
	def __init__(self):
		self.api_url = BASE_URL + "ShipProduct"
		
	def create(self, letter_id, Customer, customer_type,evidence):
		if type(customer_type) == BankEmployee:
			party = "resource:org.fourthwatch.BankEmployee#%s" % Customer
		else:
			party = "resource:org.fourthwatch.Customer#%s" % Customer
		data = {
			"$class":"org.fourthwatch.ShipProduct",
			"loc": "resource:org.fourthwatch.LetterOfCredit#%s" %letter_id,
			"approvingParty": party,
			"evidence":evidence
		}
		
		return requests.post(self.api_url, json=data).json()


class ReceiveProduct:
	def __init__(self):
		self.api_url = BASE_URL + "ReceiveProduct"
		
	def create(self, letter_id, Customer, customer_type):
		if type(customer_type) == BankEmployee:
			party = "resource:org.fourthwatch.BankEmployee#%s" % Customer
		else:
			party = "resource:org.fourthwatch.Customer#%s" % Customer
		data = {
			"$class":"org.fourthwatch.ShipProduct",
			"loc": "resource:org.fourthwatch.LetterOfCredit#%s" %letter_id,
			"approvingParty": party
		}
		
		return requests.post(self.api_url, json=data).json()


class ReadyForPayment:
	def __init__(self):
		self.api_url = BASE_URL + "ReadyForPayment"
		
	def create(self, letter_id, Customer, customer_type):
		if type(customer_type) == BankEmployee:
			party = "resource:org.fourthwatch.BankEmployee#%s" % Customer
		else:
			party = "resource:org.fourthwatch.Customer#%s" % Customer
		data = {
			"$class":"org.fourthwatch.ReadyForPayment",
			"loc": "resource:org.fourthwatch.LetterOfCredit#%s" %letter_id,
			"approvingParty": party
		}
		
		return requests.post(self.api_url, json=data).json()

class PaymentReceived:
	def __init__(self):
		self.api_url = BASE_URL + "Close"
		
	def create(self, letter_id, Customer, customer_type,closeReason):
		if type(customer_type) == BankEmployee:
			party = "resource:org.fourthwatch.BankEmployee#%s" % Customer
		else:
			party = "resource:org.fourthwatch.Customer#%s" % Customer
		data = {
			"$class":"org.fourthwatch.Close",
			"loc": "resource:org.fourthwatch.LetterOfCredit#%s" %letter_id,
			"approvingParty": party,
			"closeReason": closeReason
		}
		
		return requests.post(self.api_url, json=data).json()