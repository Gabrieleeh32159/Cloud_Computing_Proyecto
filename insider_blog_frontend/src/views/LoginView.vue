<template>
  <header class="site-header horizontal">
    <form @submit.prevent="handleSubmit">
      <h3>Login</h3>
      <div class="content-section">
        <div class="form-group">
          <label>Username</label>
          <input
            type="username"
            class="form-control form-control-lg"
            v-model="username"
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input
            type="password"
            class="form-control form-control-lg"
            v-model="password"
          />
        </div>

        <div class="form-group">
          <button class="btn btn-primary btn-block">Login</button>
        </div>
      </div>
    </form>
    <div class="alert alert-danger" role="alert" v-if="error">
      {{ error_msg }}
    </div>
  </header>
</template>

<script>
import axios from "axios";

export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      error: false,
    };
  },
  methods: {
    async handleSubmit() {
      const login_response = await axios
        .post(
          "http://52.2.150.187:8000/login",
          {},
          {
            auth: {
              username: this.username,
              password: this.password,
            },
          }
        )
        .catch((err) => {
          console.log(err);
          this.error = true;
          this.error_msg = "Invalid Login! Please try again.";
        });
      localStorage.setItem("token", login_response.data.token);
      this.$store.dispatch("user", login_response.data.user);
      this.$router.push("/");
    },
  },
};
</script>

<style>
@import "../assets/styles.css";
</style>
