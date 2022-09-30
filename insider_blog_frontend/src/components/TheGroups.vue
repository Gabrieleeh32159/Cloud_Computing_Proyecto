<template>
  <div class="groups">
    <h2>Grupos</h2>
    <p>Estos son los grupos a los que perteneces actualmente.</p>
    <div v-if="this.user">
      <li v-for="group in user.groups_ids" v-bind:key="group">
        <v-if></v-if>
        <router-link
          :to="{ name: 'Groups', params: { slug: group } }"
          class="group-title"
          >{{ group }}</router-link
        >
      </li>
    </div>
  </div>
</template>

<script>
import store from "@/vuex";
import axios from "axios";

export default {
  name: "TheGroups",
  data() {
    return {
      groups: store.getters.groups,
      user: store.getters.user,
    };
  },

  async created() {
    let groups_response = await axios.get(
      "http://52.2.150.187:8001/groups?page=0",
      {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      }
    );
    let groups = await groups_response.data.grupos;
    this.$store.dispatch("groups", groups);
  },
};
</script>

<style>
.groups {
  background: #ffffff;
  padding: 10px 20px;
  border: 1px solid #dddddd;
  border-radius: 3px;
  margin-top: 20px;
  width: auto;
}

.group-title {
  color: #1c1c1c;
  text-decoration: none;
  font-size: 20px;
}

.group-title:hover {
  color: #3295ed;
}
</style>
