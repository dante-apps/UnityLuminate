// Copyright (c) 2024, Balamurugan R and contributors
// For license information, please see license.txt

frappe.ui.form.on("Guest List", {
  name1: function (frm) {
    frm.set_value("name2", frm.doc.name1);
  },
});
