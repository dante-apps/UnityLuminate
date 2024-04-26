<script setup>
import { inject, onMounted, ref, computed } from "vue";
import { v4 as uuidv4 } from 'uuid';

const call = inject("$call");
const guests = ref([]);
const headers = [
  { title: "Name", value: "name1"},
  { title: "Gender", value: "gender" },
  { title: "Phone Number", value: "phone" },
  { title: "Email ID", value: "email_id" },
  { title: "Date Added", value: "date_added" },
  { title: "Address", value: "address" },
  { title: "Actions", value: "actions", sortable: false },
];

// Fetch guests on component mount
onMounted(async () => {
  await fetchGuest();
});

// Function to fetch guests
async function fetchGuest() {
  const url =
    "unityluminate.unityluminate.doctype.guests.guests.fetch_guests_list";

  try {
    const resp = await call(url);
    guests.value = resp;
    console.log(resp);
  } catch (e) {
    console.error(e);
  }
}

// Initialize ref values for guest details
const name = ref("");
const gender = ref("");
const phone = ref("");
const email = ref("");
const address = ref("");
const formatedDate = computed(() => {
  const year = date.value.getFullYear();
  const month = String(date.value.getMonth() + 1).padStart(2, "0"); // Months are 0-indexed
  const day = String(date.value.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
});
const date = ref(new Date());

// Variable to control the visibility of the dialog for adding a new guest
const dialog = ref(false);
const dialogDelete = ref(false);
const selectedGuest = ref(null); // Ref to store the selected guest for deletion
const isEditMode = ref(false);


const search = ref(""); // Search query
const filteredGuests = computed(() => {
  return guests.value.filter((guest) =>
    guest.name1.toLowerCase().includes(search.value.toLowerCase())
  );
});

const sortedByFormatedDate = computed(() => {
  return guests.value.map((guest) => ({
    formatedDate: formatedDate.value,
    order: 'desc', // Change 'desc' to 'asc' if you want to sort in ascending order
  }));
});
// Function to open the dialog for adding a new guest
function openDialog() {
  isEditMode.value = false;
  dialog.value = true;
}

function editItem(guest) {
  isEditMode.value = true; // Set to edit mode
  selectedGuest.value = guest; // Store the selected guest
  populateFields(guest); // Populate the form fields with guest data
  dialog.value = true; // Open the dialog
}

function populateFields(guest) {
  name.value = guest.name1;
  gender.value = guest.gender;
  phone.value = guest.phone;
  email.value = guest.email_id;
  formatedDate.value = new Date(guest.date_added);
  address.value = guest.address;
}

// Function to close the dialog
function close() {
  dialog.value = false;
  clearFields();
}

// Function to clear the input fields
function clearFields() {
  name.value = "";
  gender.value = "";
  phone.value = "";
  email.value = "";
  date.value = new Date();
  address.value = "";
}

// Function to create a new guest
async function createGuest() {
  const uniqueId = uuidv4();
  const url = "unityluminate.unityluminate.doctype.guests.guests.add_guest";
  const guest_detail = {
    name1: name.value,
    gender: gender.value,
    phone: phone.value,
    email_id: email.value,
    date_added: formatedDate.value,
    address: address.value,
    unique_id: uniqueId,
  };

  try {
    const resp = await call(url, { guest: guest_detail });
    console.log(resp);
    close();
    fetchGuest();
  } catch (e) {
    console.error(e);
    close();
  }
}
// Function to update an existing guest
async function updateGuest() {
  const url = "unityluminate.unityluminate.doctype.guests.guests.update_guest";
  const guest_detail = {
    name1: name.value,
    gender: gender.value,
    phone: phone.value,
    email_id: email.value,
    date_added: formatedDate.value,
    address: address.value,
    name: name.value
  };

  try {
    const resp = await call(url, {
      guest: guest_detail,
      guest_id: selectedGuest.value.unique_id, // Pass the unique ID instead of name1
    });
    console.log(resp);
    close();
    fetchGuest();
  } catch (e) {
    console.error(e);
    close();
  }
}

// Function to open the delete confirmation dialog
function deleteItemConfirm(guest) {
  // Log the guest details
  console.log(`Guest Details:
    Name: ${guest.name1}
    Gender: ${guest.gender}
    Phone: ${guest.phone}
    Email: ${guest.email_id}
    Address: ${guest.address}
  `);

  // Store the selected guest for deletion
  selectedGuest.value = guest;
  dialogDelete.value = true;
}

// Function to close the delete confirmation dialog
function closeDelete() {
  dialogDelete.value = false;
  selectedGuest.value = null; // Reset the selected guest
}

// Function to delete a guest
async function deleteGuest(guest) {
  if (!guest || !guest.name1) {
    console.error("Invalid guest object or guest name is undefined");
    return;
  }

  const url = "unityluminate.unityluminate.doctype.guests.guests.delete_guest";

  try {
    const resp = await call(url, { name1: guest.name1 });
    console.log(resp);
    closeDelete(); // Close the delete confirmation dialog
    fetchGuest(); // Refresh the guest list after deletion
  } catch (e) {
    console.error(e);
    closeDelete(); // Close the delete confirmation dialog
  }
}
</script>

<style>
.search-field {
  width: 250px;
}
.v-data-table {
  margin-top: 10px;
  border: 1px solid #120e0e; /* Add border to the table */
}
.container{
  margin-top: 100px;
  justify-content: center;
}
</style>

<template>
    <div class="container">
    <!-- Add Guest button -->
    <v-row>
      <v-col cols="12" sm="6" class=text-left>
        <!-- Field for autocomplete search -->
        <v-text-field
          v-model="search"
          label="Search Guests"
          variant="outlined"
          density="compact"
          single-line
          clearable
          prepend-inner-icon="mdi-magnify"
          class="search-field"
        ></v-text-field>
      </v-col>
      <v-col cols="12" sm="6" class="text-right">
        <v-btn @click="openDialog" color="primary" dark>+ Add Guest</v-btn>
      </v-col>
    </v-row>
    <!-- Data table for displaying guests -->
    <v-data-table
      :headers="headers"
      :items="filteredGuests"
      :sort-by="sortedByFormatedDate"
      :serach="search"
      class="elevation-1"
      
    >
   
      <!-- Template for actions on each guest -->
      <template v-slot:item.actions="{ item }">
        <v-icon class="me-2" size="small" @click="editItem(item)"
          >mdi-pencil</v-icon
        >
        <v-icon size="small" @click="deleteItemConfirm(item)">mdi-delete</v-icon>
      </template>
    </v-data-table>

    <!-- Dialog for adding/editing a guest -->
    <v-dialog v-model="dialog" max-width="850px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ isEditMode ? 'Edit Guest Details' : 'Enter Guest Details' }}</span>
        </v-card-title>
        <v-form class="px-3" ref="form">
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    hide-details
                    variant="outlined"
                    density="compact"
                    v-model="name"
                    label="Guest Name"
                    autofocus 
                    :rules="nameRules"
                  </v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-select
                    hide-details
                    variant="outlined"
                    density="compact"
                    :items="['Male', 'Female', ' Prefer Not To Say']"
                    v-model="gender"
                    label="Gender"
                  ></v-select>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    hide-details
                    variant="outlined"
                    density="compact"
                    v-model="phone"
                    label="Phone Number"
                  ></v-text-field>
                  
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                      hide-details
                      variant="outlined"
                      density="compact"
                      v-model="email"
                      label="Email ID"
                    ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" sm="6">
                <v-menu :close-on-content-click="false">
                    <template v-slot:activator="{ props }">
                      <v-col cols="14" sm="14">
                        <v-text-field
                          slot="activator"
                          label="Date Added"
                          prepend-inner-icon="mdi-calendar"
                          variant="outlined"
                          density="compact"
                          v-bind="props"
                          readonly
                          v-model="formatedDate"
                        ></v-text-field>
                      </v-col>
                    </template>
                    <v-date-picker color="primary" v-model="date" scrollable ></v-date-picker>
                  </v-menu>
                  </v-col>
                  <v-col cols="12" sm="6">
                <v-textarea
                    label="Address"
                    row-height="30"
                    rows="5"
                    variant="filled"
                    auto-grow
                    shaped
                    v-model="address"
                  ></v-textarea>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" variant="outlined" @click="close"
              >Cancel</v-btn
            >
            <v-btn
              color="blue darken-1"
              variant="elevated"
              @click="isEditMode ? updateGuest() : createGuest()"
              >{{ isEditMode ? 'Update' : 'Save' }}</v-btn
            >
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>

    <!-- Dialog for deleting a guest -->
    <v-dialog v-model="dialogDelete" max-width="500px">
      <v-card>
        <v-card-title class="text-h5" text-align-center
          >Are you sure you want to delete this guest?</v-card-title
        >
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1"  variant="outlined" @click="closeDelete"
            >Cancel</v-btn
          >
          <v-btn color="error" variant="elevated" @click="deleteGuest(selectedGuest)"
            >DELETE</v-btn
          >
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
