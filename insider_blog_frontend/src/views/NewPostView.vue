<template>
  <header class="site-header">
    <form @submit.prevent="handleSubmit">
      <h3>Crear Post</h3>
      <div class="content-section">
        <div class="form-group">
          <label>Title</label>
          <input
            type="title"
            class="form-control form-control-lg"
            v-model="title"
          />
        </div>

        <div class="form-group">
          <label>Content</label>
          <textarea
            class="form-control form-control-lg"
            v-model="content"
          ></textarea>
        </div>

        <div class="form-group">
          <label>Group</label>
          <select class="form-control form-control-lg" v-model="selected_group">
            <option
              v-for="group_name in user.groups_ids"
              v-bind:key="group_name"
            >
              {{ group_name }}
            </option>
          </select>
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
import router from "@/router";
import store from "@/vuex";
import axios from "axios";
export default {
  name: "NewPost",
  data() {
    return {
      title: "",
      content: "",
      group_id: 0,
      selected_group: "",
      error: false,
      error_msg: "",
    };
  },
  computed: {
    user() {
      return store.state.user;
    },
    search_groups() {
      return this.current_groups;
    },
  },
  methods: {
    async handleSubmit() {
      this.error = false;
      if (this.selected_group != "") {
        await axios
          .post("http://52.2.150.187:8002/posts", {
            title: this.title,
            content: this.content,
            user_id: store.state.user.id,
            group_id: store.state.groups.find(
              (g) => g.group_name == this.selected_group
            ).id,
          })
          .catch((err) => {
            console.log(err);
            this.error = true;
            this.error_msg = "Invalid Form! Please try again.";
          });
        if (this.error == false) {
          await router.push("/");
        }
      } else {
        console.log("Error");
        this.error = true;
        this.error_msg = "Please select a group.";
      }
    },
  },
};
</script>

<style>
@import "../assets/styles.css";
</style>
