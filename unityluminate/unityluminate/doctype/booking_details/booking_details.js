// Copyright (c) 2024, BRB and contributors
// For license information, please see license.txt

frappe.ui.form.on("Booking Details", {
  refresh: function (frm) {
    frm.add_custom_button(
      "Create C-Form",
      function () {
        createCForm(frm);
      },
      __("Create")
    );
    frm.add_custom_button(
      "Create Auroville Report",
      function () {
        createAurovilleReport(frm);
      },
      __("Create")
    );
  },

  status: function (frm) {
    // Update the color when the status changes
    assignStatusColor(frm);
  },
  validate: function (frm) {
    updateTitleField(frm);
  },
});
function updateTitleField(frm) {
  let customer = frm.doc.customer;
  let room = frm.doc.room;

  if (customer && room) {
    frm.set_value("title", customer + "-" + room);
    refresh_field("title");
  }
}
function createCForm(frm) {
  frappe.new_doc("C-Form Application", {
    first_name: frm.doc.customer,
    document_type: "Booking Details",
    reference_document: frm.doc.name,
  });
}
function createAurovilleReport(frm) {
  frappe.new_doc("Arrival Report", {
    first_name: frm.doc.customer,
    document_type: "Booking Details",
    reference_document: frm.doc.name,
  });
}
function assignStatusColor(frm) {
  const statusColors = {
    Open: "#FFA500", // Orange
    Waiting: "#FFFF00", // Yellow
    Reserved: "#0000FF", // Blue
    Booked: "#008000", // Green
    Completed: "#800080", // Purple
    Closed: "#FF0000", // Red
    Cancelled: "#A9A9A9", // Dark Grey
  };

  const status = frm.doc.status;
  const color = statusColors[status];

  if (color) {
    frm.set_value("color", color);
    frm.refresh_field("color");
  }
}
