<template>
  <TheNavigation />
  <div class="algo">
    <router-view v-bind:key="$route.path" />
  </div>
</template>

<script>
import TheNavigation from "./components/TheNavigation.vue";
//import TheGroups from "./components/TheGroups.vue";
import axios from "axios";
import store from "./vuex";

export default {
  name: "App",
  components: {
    TheNavigation,
    //TheGroups,
  },
  async created() {
    const users_response = await axios.get("http://52.2.150.187:8000/users");
    const users = await users_response.data.users;
    this.$store.dispatch("users", users);

    if (localStorage.getItem("token" !== null)) {
      const response = await axios.get("http://52.2.150.187:8000/user", {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      });
      this.$store.dispatch("user", response.data);
    }
    console.log(store.state.groups);
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
}
.algo {
  display: flex;
  justify-content: space-between;
  margin-right: 170px;
}

body {
  background: #fafafa;
  /*background-color: rgba(255, 255, 255, 0.814);*/
  color: #333333;
  margin-top: 5rem;
}

h1,
h2,
h3,
h4,
h5,
h6 {
  color: #444444;
}

.bg-steel {
  background-color: rgb(0, 187, 227);
}

.site-header .navbar-nav .nav-link {
  color: #ecf6fb;
  transition: 0.5s;
}

.site-header .navbar-nav .nav-link:hover {
  color: #ffffff;
  transform: scale(1.1);
}

.site-header .navbar-nav .nav-link.active {
  font-weight: 500;
}

.content-section {
  background: #ffffff;
  padding: 10px 20px;
  border: 1px solid #dddddd;
  border-radius: 3px;
  margin-bottom: 20px;
}

.article-title {
  color: #262626;
}

a.article-title:hover {
  color: #428bca;
  text-decoration: none;
}

.article-content {
  white-space: pre-line;
}

.article-img {
  height: 65px;
  width: 65px;
  margin-right: 16px;
}

.article-metadata {
  padding-bottom: 1px;
  margin-bottom: 4px;
  border-bottom: 1px solid #e3e3e3;
}

.article-metadata a:hover {
  text-decoration: underline;
}

.article-svg {
  width: 25px;
  height: 25px;
  vertical-align: middle;
}

.account-img {
  height: 125px;
  width: 125px;
  margin-right: 20px;
  margin-bottom: 16px;
}

.account-heading {
  font-size: 2.5rem;
}
</style>
