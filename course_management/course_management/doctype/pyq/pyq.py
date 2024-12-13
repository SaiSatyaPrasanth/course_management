# Copyright (c) 2024, Prasanth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PYQ(Document):
	pass

@frappe.whitelist(allow_guest=True)
def get_all_pyq():
	try:
		# Replace 'Record Name' with the actual record identifier
		parent_docs = frappe.get_all('PYQ', fields=['name', 'exam_name'])

		result = []

		for parent in parent_docs:

			child_records = frappe.get_all('PYQ Subjects', fields=['subject_name', 'download','file_type',"file_size"], filters={'parent': parent['name']})

			parent['subjects'] = child_records

			result.append(parent)
			
		return result
	except frappe.DoesNotExistError:
		frappe.throw("PYQ record not found")


import requests

