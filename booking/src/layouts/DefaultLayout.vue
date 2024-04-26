<script lang="ts" setup>
import { Drawer } from "@/components";
</script>

<template>
  <v-app id="app" style="background-color: #ecf0f1">
    <!-- Use a Vuetify material color -->
    <v-main>
      <Drawer></Drawer>
      <div>
        <router-view></router-view>
      </div>
    </v-main>
  </v-app>
</template>
