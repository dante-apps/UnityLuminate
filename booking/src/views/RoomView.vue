<script setup>
import { inject, onMounted, ref } from "vue";

const call = inject("$call");
const rooms = ref([]);
const snackbar = ref(false);

onMounted(async () => {
  await fetchRooms();
});

async function fetchRooms() {
  const url = "unityluminate.unityluminate.doctype.room.room.get_room_list";

  try {
    const resp = await call(url);
    rooms.value = resp;
    console.log(resp);
  } catch (e) {
    console.error(e);
  }
}

const room_name = ref();
const room_type = ref();
const room_status = ref();
const single_price = ref();
const double_price = ref();
const description = ref();

async function createRoom(show) {
  const url = "unityluminate.unityluminate.doctype.room.room.create_room";
  const room_detail = {
    room_name: room_name.value,
    room_type: room_type.value,
    status: room_status.value,
    single_price: single_price.value,
    double_price: double_price.value,
    room_description: description.value,
  };

  try {
    const resp = await call(url, { room: room_detail });
    console.log(resp);
    show.value = false;
    snackbar.value = true;
    fetchRooms();
  } catch (e) {
    console.error(e);
    show.value = false;
  }
}
</script>

<template>
  <div>
    <v-snackbar
      v-model="snackbar"
      color="success"
      :timeout="3000"
      location="top right"
    >
      Room has been created successfully!
    </v-snackbar>
    <v-dialog max-width="700">
      <template v-slot:activator="{ props: activatorProps }">
        <v-btn
          v-bind="activatorProps"
          text="+ Add Room"
          class="ma-8"
          color="success"
        ></v-btn>
      </template>

      <template v-slot:default="{ isActive }">
        <v-card title="Enter Room Details">
          <v-card-text>
            <v-row>
              <v-col>
                <v-text-field
                  dense
                  hide-details
                  variant="outlined"
                  density="compact"
                  color="primary"
                  label="Room Name"
                  v-model="room_name"
                  :rules="['Required']"
                ></v-text-field>
              </v-col>
              <v-col>
                <v-select
                  dense
                  hide-details
                  variant="outlined"
                  density="compact"
                  :items="['Normal', 'Cottage']"
                  color="primary"
                  label="Room Type"
                  v-model="room_type"
                ></v-select>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-select
                  dense
                  hide-details
                  variant="outlined"
                  density="compact"
                  color="primary"
                  label="Room Status"
                  :items="['Available', 'Booked', 'Waitlisted', 'Maintenance']"
                  v-model="room_status"
                ></v-select>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  hide-details
                  variant="outlined"
                  density="compact"
                  color="primary"
                  label="Single Price"
                  v-model="single_price"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-text-field
                  dense
                  hide-details
                  variant="outlined"
                  density="compact"
                  color="primary"
                  label="Double Price"
                  v-model="double_price"
                ></v-text-field>
              </v-col>
              <v-col>
                <v-text-field
                  dense
                  hide-details
                  variant="outlined"
                  density="compact"
                  color="primary"
                  label="Description"
                  v-model="description"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-card-text>

          <!-- End of fields -->
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              text="Close Dialog"
              @click="isActive.value = false"
              color="error"
            ></v-btn>
            <v-btn
              text="Create Room"
              @click="createRoom(isActive)"
              color="primary"
            ></v-btn>
          </v-card-actions>
        </v-card>
      </template>
    </v-dialog>
  </div>
  <div class="d-flex flex-wrap">
    <v-card
      class="ms-10 my-8"
      elevation="16"
      min-width="344"
      min-height="165"
      v-for="(room, i) in rooms"
      :key="i"
    >
      <v-card-item>
        <v-card-title>{{ room.room_name }}</v-card-title>
        <v-card-subtitle>{{ room.room_type }}</v-card-subtitle>
      </v-card-item>
      <v-card-subtitle>Single Price - {{ room.single_price }}</v-card-subtitle>
      <v-card-subtitle>Double Price - {{ room.double_price }}</v-card-subtitle>
      <v-card-subtitle>{{ room.status }}</v-card-subtitle>
      <v-card-subtitle>{{ room.room_description }}</v-card-subtitle>
    </v-card>
  </div>
</template>
