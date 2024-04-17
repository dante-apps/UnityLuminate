# Copyright (c) 2024, BRB and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Room(Document):
	pass


@frappe.whitelist()
def create_room(room):
    print("++++++++++++++++", room)
    doc = frappe.new_doc("Room")
    doc.room_name = room.get("room_name")
    doc.room1 = room.get("room_name")
    doc.room_type = room.get("room_type")
    doc.status = room.get("status")
    doc.save()

    return doc.name


@frappe.whitelist()
def get_room_list():
    room = frappe.qb.DocType("Room")
    
    q = (
		frappe.qb.from_(room)
			.select(
				room.room_name,
				room.room_type,
				room.status
			)
	)
    
    return q.run(as_dict=True) or []
