# Copyright (c) 2023, Anwar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff
from frappe import _

class LeaveApplication(Document):
	
	def validate(self):
		self.set_total_leave_days()
		self.get_total_leaves_allocated()
		self.check_leave_balance()

	def on_submit(self):
		self.update_leave_on_submit()

	def on_cancel(self):
		self.update_leave_balance_after_cancel()


	def set_total_leave_days(self):
		if self.to_date and self.from_date:
			total_leave_days = date_diff(self.to_date, self.from_date)

			if total_leave_days >= 0:
				self.total_leave_days = total_leave_days

	
	def get_total_leaves_allocated(self):
		if self.employee and self.from_date and self.to_date and self.leave_type:
			leave_allocated = frappe.db.sql(""" SELECT total_leaves_allocated FROM `tabLeave Allocation`
				   	 WHERE employee = %s and from_date <= %s and to_date >= %s and leave_type = %s""", 
					 (self.employee, self.from_date, self.to_date, self.leave_type), as_dict=True)
			
			if leave_allocated:
				self.leave_balance_before_application = str(leave_allocated[0].total_leaves_allocated)
			
			
	def check_leave_balance(self):
		if self.total_leave_days and self.leave_balance_before_application:
			if float(self.total_leave_days) > float(self.leave_balance_before_application):
				frappe.throw(_("your balance is less than leave days you want for ",'ar') + self.leave_type)


	def update_leave_on_submit(self):
		new_leave_balance = float(self.leave_balance_before_application) - float(self.total_leave_days)

		frappe.db.sql("""
			UPDATE `tabLeave Allocation` SET total_leaves_allocated = %s
			WHERE employee = %s AND from_date <= %s AND to_date >= %s AND leave_type = %s
		""", (new_leave_balance, self.employee, self.from_date, self.to_date, self.leave_type))

		frappe.db.commit()


	def update_leave_balance_after_cancel(self):
		
		leave_allocated = frappe.db.sql(""" SELECT total_leaves_allocated FROM `tabLeave Allocation`
				   	 WHERE employee = %s and from_date <= %s and to_date >= %s and leave_type = %s""", 
					 (self.employee, self.from_date, self.to_date, self.leave_type), as_dict=True)
			
		if leave_allocated:
			leave_balance_Before_application = str(leave_allocated[0].total_leaves_allocated)

			new_balance = float(leave_balance_Before_application) + float(self.total_leave_days)

			frappe.db.sql("""
				UPDATE `tabLeave Allocation` SET total_leaves_allocated = %s
				WHERE employee = %s AND from_date <= %s AND to_date >= %s AND leave_type = %s
			""", (new_balance, self.employee, self.from_date, self.to_date, self.leave_type))

			frappe.db.commit()
