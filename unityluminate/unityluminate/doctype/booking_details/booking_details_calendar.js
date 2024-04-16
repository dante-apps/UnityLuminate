frappe.views.calendar["Booking Details"] = {
  field_map: {
    start: "starts_on",
    end: "ends_on",
    id: "title",
    room: "room",
    customer: "customer",
    // allDay: "all_day",
    title: "title",
    // status: "event_type",
    // color: "color",
  },
  style_map: {
    Public: "success",
    Private: "info",
  },
  get_events_method:
    "bookmyroom.bookmyroom.doctype.booking_details.booking_details.get_events",
};
