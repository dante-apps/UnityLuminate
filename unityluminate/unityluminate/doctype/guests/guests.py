# Copyright (c) 2024, Balamurugan R and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Guests(Document):
	pass


@frappe.whitelist()
def fetch_guests_list():
    guest = frappe.qb.DocType("Guests")
    
    q = (
		frappe.qb.from_(guest)
			.select(
				guest.name1,
				guest.gender,
				guest.phone,
                guest.email_id,
                guest.date_added,
                guest.address,
                guest.name,
                guest.unique_id,
                
			)
	)
    
    return q.run(as_dict=True) or []

# @frappe.whitelist()
# def add_guest(guest):
#     print("++++++++++++++++", guest)
#     doc = frappe.new_doc("Guests")
#     doc.name1 = guest.get("name1")
#     doc.gender = guest.get("gender")
#     doc.phone = guest.get("phone")
#     doc.email_id = guest.get("email_id")
#     doc.date_added = guest.get("date_added")
#     doc.address = guest.get("address")
#     doc.save()

#     return doc.name1

@frappe.whitelist()
def add_guest(guest):
    """
    Add a new guest record.
    """
    try:
        doc = frappe.new_doc("Guests")
        doc.name1 = guest.get("name1")  # Ensure name1 matches frontend
        # Assign other properties from the frontend
        doc.gender = guest.get("gender")
        doc.phone = guest.get("phone")
        doc.email_id = guest.get("email_id")
        doc.date_added = guest.get("date_added")
        doc.address = guest.get("address")
        doc.unique_id = guest.get("unique_id") 
        doc.save()

        frappe.db.commit()
        return doc.name1  # Return the name1 of the created guest
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Add Guest Failed"))
        frappe.db.rollback()
        return _("Failed to add guest: {0}").format(str(e))


@frappe.whitelist()
def delete_guest(name1):
    """
    Delete a guest record by name1.
    """
    try:
        frappe.delete_doc("Guests", name1)
        frappe.db.commit()
        return "Guest deleted successfully"
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Delete Guest Failed"))
        frappe.db.rollback()
        return _("Failed to delete guest: {0}").format(str(e))


@frappe.whitelist()
def update_guest(guest, guest_id):
    """
    Update an existing guest record.
    """
    try:
        guest_doc = frappe.get_doc("Guests", {"unique_id": guest_id})
        guest_doc.name1 = guest.get("name1")
        guest_doc.gender = guest.get("gender")
        guest_doc.phone = guest.get("phone")
        guest_doc.email_id = guest.get("email_id")
        guest_doc.date_added = guest.get("date_added")
        guest_doc.address = guest.get("address")
        guest_doc.save()
        frappe.db.commit()
        return "Guest updated successfully"
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Update Guest Failed"))
        frappe.db.rollback()
        return _("Failed to update guest: {0}").format(str(e))