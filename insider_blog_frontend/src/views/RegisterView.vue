<template>
  <header class="site-header">
    <form @submit.prevent="handleSubmit">
      <h3>Sign Up</h3>
      <div class="content-section">
        <div class="form-group">
          <label>Username</label>
          <input
            type="text"
            name="username"
            v-model="username"
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label>Email</label>
          <input
            type="email"
            name="email"
            v-model="email"
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input
            type="password"
            name="password"
            v-model="password"
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label>Confirm Password</label>
          <input
            type="password"
            name="confirm_pass"
            v-model="confirm_pass"
            class="form-control"
          />
        </div>

        <div class="form-group">
          <button class="btn btn-primary btn-block" v-on:click="handleSubmit()">
            Sign Up
          </button>
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
  name: "Register",
  compontents: {},
  data() {
    return {
      username: "",
      email: "",
      password: "",
      confirm_pass: "",
      error: false,
    };
  },
  methods: {
    async handleSubmit() {
      this.error = false;
      await axios
        .post("http://52.2.150.187:8000/users", {
          username: this.username,
          email: this.email,
          password: this.password,
        })
        .catch((err) => {
          console.log(err);
          this.error = true;
          this.error_msg = "Invalid Form! Please try again.";
        });
      if (this.error == false) {
        this.$router.push("/login");
      }
    },
  },
};
</script>

<style>
@import "../assets/styles.css";
</style>
