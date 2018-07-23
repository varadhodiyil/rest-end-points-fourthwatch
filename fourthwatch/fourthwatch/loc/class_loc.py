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
		print data
		return requests.post(self.api_url, json=data).json()


class Approve:

    def approve(self, letter_id, Customer, customer_type):
        if type(customer_type) == BankEmployee:
            party = "resource:org.fourthwatch.BankEmployee#%s" % Customer
        else:
            party = "resource:org.fourthwatch.Customer#%s" % Customer
        data = {
            "$class": "org.fourthwatch.Approve",
            "loc": "resource:org.fourthwatch.LetterOfCredit#5160",
            "approvingParty": party
        }
