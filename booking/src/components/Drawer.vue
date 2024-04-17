<template>
  <v-navigation-drawer
    expand-on-hover
    rail
    style="background-color: #8cd5e4"
    class="flex-grow-0 flex-shrink-0"
  >
    <!-- User info section -->
    <v-list>
      <v-list-item
        :prepend-avatar="userImage"
        :subtitle="userEmail"
        :title="userName"
      ></v-list-item>
    </v-list>

    <!-- Navigation items -->
    <v-divider></v-divider>
    <v-list dense nav>
      <router-link to="/room">
        <v-list-item value="room">
          <v-layout align-center>
            <v-icon class="my-files-icon">
              <img src="@/icons/bed.png" alt="Room" />
            </v-icon>
            <v-list-item-title class="rooms-text font-weight-bold">
              Room
            </v-list-item-title>
          </v-layout>
        </v-list-item>
      </router-link>
      <router-link to="/calendar">
        <v-list-item value="calendar">
          <v-layout align-center>
            <v-icon class="calendar-icon">
              <img src="@/icons/calendar.png" alt="Calendar" />
            </v-icon>
            <v-list-item-title class="shared-text font-weight-bold">
              Calendar
            </v-list-item-title>
          </v-layout>
        </v-list-item>
      </router-link>
      <router-link to="/billing">
        <v-list-item value="billing">
          <v-layout align-center>
            <v-icon class="billing-icon">
              <img src="@/icons/bill.png" alt="Billing" />
            </v-icon>
            <v-list-item-title class="billing-text font-weight-bold">
              Billing
            </v-list-item-title>
          </v-layout>
        </v-list-item>
      </router-link>
    </v-list>

    <!-- Logout button -->
    <v-divider></v-divider>
    <v-spacer></v-spacer>
    <v-btn
      value="logout"
      class="logout-button"
      style="background-color: whitesmoke"
      @click="logoutDialog = true"
    >
      <v-layout align-center>
        <v-icon class="logout-icon">
          <img src="@/icons/logout.png" alt="Logout" />
        </v-icon>
        <span class="logout-text font-weight-bold"> Logout </span>
      </v-layout>
    </v-btn>

    <!-- Logout Dialog -->
    <v-dialog v-model="logoutDialog" max-width="500px">
      <v-card>
        <v-card-title>Logout Confirmation</v-card-title>
        <v-card-text>Are you sure you wanna logout?</v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="$auth.logout()">Yes</v-btn>
          <v-btn @click="logoutDialog = false">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-navigation-drawer>
</template>

<script>
export default {
  inject: ["$auth"],
  data() {
    return {
      userImage: "https://randomuser.me/api/portraits/women/85.jpg",
      userEmail: "sandra_a88@gmailcom",
      userName: "Sandra Adams",
      logoutDialog: false,
    };
  },
};
</script>

<style scoped>
.v-navigation-drawer {
  width: 100%;
}

@media (min-width: 768px) {
  .v-navigation-drawer {
    width: 256px;
  }
}

.my-files-icon img,
.calendar-icon img,
.billing-icon img {
  width: 24px;
  height: 24px;
}

.logout-icon img {
  width: 23px;
  height: 23px;
}

.rooms-text,
.shared-text,
.billing-text,
.logout-text {
  margin-left: 1rem;
  line-height: 1.5rem;
  font-size: 1rem;
}

@media (min-width: 768px) {
  .rooms-text,
  .shared-text,
  .billing-text,
  .logout-text {
    font-size: 1.2rem;
  }
}

.logout-button {
  margin-top: 620px;
  margin-bottom: 16px;
  width: 100%;
  justify-content: start;
}
</style>
