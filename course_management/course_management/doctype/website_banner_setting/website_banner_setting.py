# Copyright (c) 2024, Prasanth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WebsiteBannerSetting(Document):
	pass


@frappe.whitelist(allow_guest=True)
def get_home_page_banners():
    try:
        # Replace 'Record Name' with the actual record identifier
        parent_doc = frappe.get_doc('Website Banner Setting', 'mh82vhi8us')
        return parent_doc
    except frappe.DoesNotExistError:
        frappe.throw("Website Banner Setting record not found")
