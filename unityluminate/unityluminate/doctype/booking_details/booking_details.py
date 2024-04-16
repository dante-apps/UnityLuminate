# Copyright (c) 2024, BRB and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class BookingDetails(Document):
	pass

# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE


import json

import frappe
from frappe import _
from frappe.contacts.doctype.contact.contact import get_default_contact
from frappe.desk.doctype.notification_settings.notification_settings import (
	is_email_notifications_enabled_for_type,
)
from frappe.desk.reportview import get_filters_cond
from frappe.model.document import Document
from frappe.utils import (
	add_days,
	add_months,
	cint,
	cstr,
	date_diff,
	format_datetime,
	get_datetime_str,
	getdate,
	now_datetime,
	nowdate,
)
from frappe.utils.user import get_enabled_system_users

weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
communication_mapping = {
	"": "Event",
	"Event": "Event",
	"Meeting": "Meeting",
	"Call": "Phone",
	"Sent/Received Email": "Email",
	"Other": "Other",
}


class Event(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.desk.doctype.event_participants.event_participants import EventParticipants
		from frappe.types import DF

		add_video_conferencing: DF.Check
		all_day: DF.Check
		color: DF.Color | None
		description: DF.TextEditor | None
		ends_on: DF.Datetime | None
		event_category: DF.Literal["Event", "Meeting", "Call", "Sent/Received Email", "Other"]
		event_participants: DF.Table[EventParticipants]
		event_type: DF.Literal["Private", "Public"]
		friday: DF.Check
		google_calendar: DF.Link | None
		google_calendar_event_id: DF.Data | None
		google_calendar_id: DF.Data | None
		google_meet_link: DF.Data | None
		monday: DF.Check
		pulled_from_google_calendar: DF.Check
		repeat_on: DF.Literal["", "Daily", "Weekly", "Monthly", "Yearly"]
		repeat_this_event: DF.Check
		repeat_till: DF.Date | None
		saturday: DF.Check
		send_reminder: DF.Check
		sender: DF.Data | None
		starts_on: DF.Datetime
		status: DF.Literal["Open", "Waiting", "Reserved", "Booked", "Completed", "Closed", "Cancelled"]
		subject: DF.SmallText
		sunday: DF.Check
		sync_with_google_calendar: DF.Check
		thursday: DF.Check
		tuesday: DF.Check
		wednesday: DF.Check


@frappe.whitelist()
def get_events(start, end, user=None, for_reminder=False, filters=None) -> list[frappe._dict]:
	if not user:
		user = frappe.session.user

	if isinstance(filters, str):
		filters = json.loads(filters)

	filter_condition = get_filters_cond("Event", filters, [])

	tables = ["`tabBooking Details`"]
	if "`tabBooking Details Participants`" in filter_condition:
		tables.append("`tabBooking Details Participants`")

	events = frappe.db.sql(
		"""
		SELECT `tabBooking Details`.name,
				`tabBooking Details`.title,
				`tabBooking Details`.customer,
				`tabBooking Details`.room,
				`tabBooking Details`.color,
				`tabBooking Details`.starts_on,
				`tabBooking Details`.ends_on,
				`tabBooking Details`.owner,
				`tabBooking Details`.all_day,
				`tabBooking Details`.event_type,
				`tabBooking Details`.repeat_this_event,
				`tabBooking Details`.repeat_on,
				`tabBooking Details`.repeat_till,
				`tabBooking Details`.monday,
				`tabBooking Details`.tuesday,
				`tabBooking Details`.wednesday,
				`tabBooking Details`.thursday,
				`tabBooking Details`.friday,
				`tabBooking Details`.saturday,
				`tabBooking Details`.sunday
		FROM {tables}
		WHERE (
				(
					(date(`tabBooking Details`.starts_on) BETWEEN date(%(start)s) AND date(%(end)s))
					OR (date(`tabBooking Details`.ends_on) BETWEEN date(%(start)s) AND date(%(end)s))
					OR (
						date(`tabBooking Details`.starts_on) <= date(%(start)s)
						AND date(`tabBooking Details`.ends_on) >= date(%(end)s)
					)
				)
				OR (
					date(`tabBooking Details`.starts_on) <= date(%(start)s)
					AND `tabBooking Details`.repeat_this_event=1
					AND coalesce(`tabBooking Details`.repeat_till, '3000-01-01') > date(%(start)s)
				)
			)
		 {reminder_condition}
        {filter_condition}
        AND `tabBooking Details`.status != 'Cancelled'  -- Remove status filter
        ORDER BY `tabBooking Details`.starts_on""".format(
            tables=", ".join(tables),
            filter_condition=filter_condition,
            reminder_condition="AND coalesce(`tabBooking Details`.send_reminder, 0)=1" if for_reminder else "",
        ),
        {
            "start": start,
            "end": end,
            "user": user,
        },
        as_dict=1,
	)

	# process recurring events
	start = start.split(" ", 1)[0]
	end = end.split(" ", 1)[0]
	add_events = []
	remove_events = []

	def add_event(e, date):
		new_event = e.copy()

		enddate = (
			add_days(date, int(date_diff(e.ends_on.split(" ", 1)[0], e.starts_on.split(" ", 1)[0])))
			if (e.starts_on and e.ends_on)
			else date
		)

		new_event.starts_on = date + " " + e.starts_on.split(" ")[1]
		new_event.ends_on = new_event.ends_on = enddate + " " + e.ends_on.split(" ")[1] if e.ends_on else None

		add_events.append(new_event)

	for e in events:
		if e.repeat_this_event:
			e.starts_on = get_datetime_str(e.starts_on)
			e.ends_on = get_datetime_str(e.ends_on) if e.ends_on else None

			event_start, time_str = get_datetime_str(e.starts_on).split(" ")

			repeat = "3000-01-01" if cstr(e.repeat_till) == "" else e.repeat_till

			if e.repeat_on == "Yearly":
				start_year = cint(start.split("-", 1)[0])
				end_year = cint(end.split("-", 1)[0])

				# creates a string with date (27) and month (07) eg: 07-27
				event_start = "-".join(event_start.split("-")[1:])

				# repeat for all years in period
				for year in range(start_year, end_year + 1):
					date = str(year) + "-" + event_start
					if (
						getdate(date) >= getdate(start)
						and getdate(date) <= getdate(end)
						and getdate(date) <= getdate(repeat)
					):
						add_event(e, date)

				remove_events.append(e)

			if e.repeat_on == "Monthly":
				# creates a string with date (27) and month (07) and year (2019) eg: 2019-07-27
				year, month = start.split("-", maxsplit=2)[:2]
				date = f"{year}-{month}-" + event_start.split("-", maxsplit=3)[2]

				# last day of month issue, start from prev month!
				try:
					getdate(date)
				except Exception:
					date = date.split("-")
					date = date[0] + "-" + str(cint(date[1]) - 1) + "-" + date[2]

				start_from = date
				for i in range(int(date_diff(end, start) / 30) + 3):
					if (
						getdate(date) >= getdate(start)
						and getdate(date) <= getdate(end)
						and getdate(date) <= getdate(repeat)
						and getdate(date) >= getdate(event_start)
					):
						add_event(e, date)

					date = add_months(start_from, i + 1)
				remove_events.append(e)

			if e.repeat_on == "Weekly":
				for cnt in range(date_diff(end, start) + 1):
					date = add_days(start, cnt)
					if (
						getdate(date) >= getdate(start)
						and getdate(date) <= getdate(end)
						and getdate(date) <= getdate(repeat)
						and getdate(date) >= getdate(event_start)
						and e[weekdays[getdate(date).weekday()]]
					):
						add_event(e, date)

				remove_events.append(e)

			if e.repeat_on == "Daily":
				for cnt in range(date_diff(end, start) + 1):
					date = add_days(start, cnt)
					if (
						getdate(date) >= getdate(event_start)
						and getdate(date) <= getdate(end)
						and getdate(date) <= getdate(repeat)
					):
						add_event(e, date)

				remove_events.append(e)

	for e in remove_events:
		events.remove(e)

	events = events + add_events

	for e in events:
		# remove weekday properties (to reduce message size)
		for w in weekdays:
			del e[w]

	return events



# Close events if ends_on or repeat_till is less than now_datetime
def set_status_of_events():
	events = frappe.get_list("Event", filters={"status": "Open"}, fields=["name", "ends_on", "repeat_till"])
	for event in events:
		if (event.ends_on and getdate(event.ends_on) < getdate(nowdate())) or (
			event.repeat_till and getdate(event.repeat_till) < getdate(nowdate())
		):
			frappe.db.set_value("Event", event.name, "status", "Closed")


@frappe.whitelist()
def get_room_details():
    rooms = frappe.get_all("Room", fields=["name"])
    return rooms
