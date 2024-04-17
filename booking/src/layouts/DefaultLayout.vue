<script lang="ts" setup>
import { Drawer } from "@/components";
</script>

<template>
  <v-app>
    <v-main>
      <Drawer></Drawer>
      <div>
        <router-view></router-view>
      </div>
    </v-main>
  </v-app>
</template>
