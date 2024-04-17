import { createRouter, createWebHistory } from "vue-router";
import authRoutes from "./auth";
import { Home, RoomView, Billing, Calendar } from "@/views";
import DefaultLayout from "../layouts/DefaultLayout.vue";
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
