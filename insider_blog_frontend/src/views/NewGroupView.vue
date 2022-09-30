<template>
  <header class="site-header">
    <form @submit.prevent="handleSubmit">
      <h3>Crear Grupo</h3>
      <div class="content-section">
        <div class="form-group">
          <label>Name</label>
          <input class="form-control form-control-lg" v-model="groupname" />
        </div>

        <div class="form-group">
          <button class="btn btn-primary btn-block">Create</button>
        </div>
      </div>
    </form>
    <div class="alert alert-danger" role="alert" v-if="error">
      {{ error_msg }}
    </div>
  </header>
</template>

<script>
//import router from "@/router";
import axios from "axios";
import { mapGetters } from "vuex";
//import store from "@/vuex";
export default {
  name: "NewGroup",
  data() {
    return {
      groupname: "",
      error: false,
      error_msg: "",
    };
  },
  computed: {
    ...mapGetters({
      user: "user",
    }),
  },
  methods: {
    async handleSubmit() {
      this.error = false;
      await axios
        .post("http://52.2.150.187:8001/groups", {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
          groupname: this.groupname,
          user_id: this.user.id,
        })
        .catch((err) => {
          console.log(err);
          this.error = true;
          this.error_msg = "Please enter a valid name.";
        });
      if (this.error == false) {
        this.$router.push("/");
      }
    },
  },
};
</script>

<style>
@import "../assets/styles.css";
</style>
