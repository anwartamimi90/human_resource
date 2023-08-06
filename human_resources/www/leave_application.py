import frappe

def get_context(context):
    context['leave_applications'] = get_leave_applications()


def get_leave_applications():
    return frappe.db.sql(""" SELECT employee_name, leave_type, total_leave_days FROM
                          `tabLeave Application` WHERE status='Open' """, as_dict=True)
