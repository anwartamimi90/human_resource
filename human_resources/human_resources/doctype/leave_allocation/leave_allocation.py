# Copyright (c) 2023, Anwar and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.utils import date_diff

class LeaveAllocation(Document):

	def validate(self):
		self.set_total_leaves_allocated()

	def set_total_leaves_allocated(self):
		if self.to_date and self.from_date:
			total_leaves_allocated = date_diff(self.to_date, self.from_date)

			if total_leaves_allocated >= 0:
				self.total_leaves_allocated = total_leaves_allocated

