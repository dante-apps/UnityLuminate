import { createRouter, createWebHistory } from "vue-router";
import authRoutes from "./auth";
import { Home, RoomView, Billing, Calendar, Guests, Booking } from "@/views";
import DefaultLayout from "../layouts/DefaultLayout.vue";
// import Guests from "../views/Guests.vue";
// import Booking from "../views/Booking.vue";
const routes = [
  {
    path: "/",
    component: DefaultLayout,
    children: [
      {
        path: "",
        name: "Home",
        component: Home,
      },
    ],
  },
  {
    path: "/room",
    component: DefaultLayout,
    children: [
      {
        path: "",
        name: "Room",
        component: RoomView,
      },
    ],
  },
  {
    path: "/calendar",
    component: DefaultLayout,
    children: [
      {
        path: "",
        name: "Calendar",
        component: Calendar,
      },
    ],
  },
  {
    path: "/billing",
    component: DefaultLayout,
    children: [
      {
        path: "",
        name: "Billing",
        component: Billing,
      },
    ],
  },
  {
    path: "/guests",
    component: DefaultLayout,
    children: [
      {
        path: "",
        name: "Guests",
        component: Guests,
      },
    ],
  },
  {
    path: "/booking",
    component: DefaultLayout,
    children: [
      {
        path: "",
        name: "Booking",
        component: Booking,
      },
    ],
  },
  ...authRoutes,
  // {
  //   path: "/room",
  //   name: "Room",
  //   component: Room,
  // },
];

const router = createRouter({
  base: "/booking/",
  history: createWebHistory(),
  routes,
});

export default router;
