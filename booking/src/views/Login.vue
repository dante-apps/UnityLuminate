<template>
  <div>
    <v-img
      class="mx-auto my-6"
      max-width="228"
      src="@/icons/withoutbg.png"
    ></v-img>

    <v-card
      class="mx-auto pa-12 pb-8"
      elevation="8"
      max-width="448"
      rounded="lg"
    >
      <template #title>
        <div class="text-h6 font-emphasis-bold text-center mb-4">Log In to</div>
        <div class="text-h6 text-weight-emphasis text-center">
          Afsanah Guest House
        </div>
      </template>
      <div class="text-subtitle-1 text-medium-emphasis">Account</div>

      <v-text-field
        v-model="email"
        density="compact"
        placeholder="Email address"
        prepend-inner-icon="mdi-email-outline"
        variant="outlined"
      ></v-text-field>

      <div
        class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between"
      >
        Password
      </div>

      <v-text-field
        v-model="password"
        :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
        :type="visible ? 'text' : 'password'"
        density="compact"
        placeholder="Enter your password"
        prepend-inner-icon="mdi-lock-outline"
        variant="outlined"
        @click:append-inner="visible = !visible"
        @keyup.enter="login"
      ></v-text-field>

      <v-btn
        block
        class="mb-8"
        color="indigo"
        size="large"
        variant="tonal"
        @click="login"
      >
        Log In
      </v-btn>
    </v-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
      visible: false,
    };
  },
  inject: ["$auth"],
  async mounted() {
    if (this.$route?.query?.route) {
      this.redirect_route = this.$route.query.route;
      this.$router.replace({ query: null });
    }
  },
  methods: {
    async login() {
      if (this.email && this.password) {
        let res = await this.$auth.login(this.email, this.password);
        if (res) {
          this.$router.push({ name: "Home" });
        }
      }
    },
  },
};
</script>
