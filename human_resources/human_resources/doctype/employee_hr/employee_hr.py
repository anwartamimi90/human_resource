# Copyright (c) 2023, Anwar and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class EmployeeHR(Document):
	def validate(self):
		self.cv_valuation_()


	def after_insert(self):
		self.cv_valuation_()


	def cv_valuation_(self):
		if 'English' in self.cv:
			self.cv_valuation = 'Good'
		else:
			self.cv_valuation = 'Bad'
