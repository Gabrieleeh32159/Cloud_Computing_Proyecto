<template>
  <header class="site-header">
    <div class="container">
      <form @submit.prevent="handleSubmit">
        <h3>Edit {{ user.username }} Profile</h3>
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
          <label>Description</label>
          <textarea v-model="description" class="form-control"></textarea>
        </div>

        <div class="form-group">
          <label>Password</label>
          <input v-model="password" class="form-control" />
        </div>

        <div class="form-group">
          <label>Confirm Password</label>
          <input v-model="confirm_pass" class="form-control" />
        </div>

        <div class="form-group">
          <button class="btn btn-primary btn-block" v-on:click="handleSubmit()">
            Submit
          </button>
        </div>
      </form>
    </div>
    <div class="alert alert-danger" role="alert" v-if="error">
      {{ error_msg }}
    </div>
  </header>
</template>

<script>
import router from "@/router";
import store from "@/vuex";
import axios from "axios";
export default {
  name: "EditProfile",
  compontents: {},
  data() {
    return {
      username: "",
      email: "",
      description: "",
      password: "",
      confirm_pass: "",
      error: false,
      error_msg: "",
    };
  },
  props: {
    slug: {
      type: String,
      required: true,
    },
  },
  computed: {
    user() {
      return store.state.user;
    },
  },
  methods: {
    async handleSubmit() {
      this.error = false;
      if (this.password == this.confirm_pass) {
        await axios
          .patch("http://52.2.150.187:8000/users/" + this.slug, {
            username: this.username,
            email: this.email,
            description: this.description,
            password: this.password,
          })
          .catch((err) => {
            console.log(err);
            this.error = true;
            this.error_msg = "Invalid Form! Please try again.";
          });

        if (this.error == false) {
          await router.push("/user/" + this.slug);
        }
      } else {
        this.error = true;
        this.error_msg = "Passwords don't match!";
      }
    },
  },
};
</script>

<style scoped>
.form-group {
  margin-top: 20px;
}

.container {
  padding: 20px;
  margin-block: 40px;
  width: 100%;
  border: 1px solid #dddddd;
  display: flex;
  flex-direction: column;
  align-items: flex-startsssss;
}
</style>
