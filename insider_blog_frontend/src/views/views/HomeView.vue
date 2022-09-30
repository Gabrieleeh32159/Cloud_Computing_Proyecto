<template>
  <div class="container" v-if="user">
    <div class="posts">
      <div v-for="item in posts" v-bind:key="item.user_id">
        <article class="post-info">
          <router-link :to="{ name: 'Users', params: { slug: item.user_id } }">
            <img
              class="rounded-circle article-img"
              src="../assets/default.jpg"
              style="height: 65px; border-radius: 65px"
            />
          </router-link>

          <div class="media-body">
            <div class="article-metadata">
              <router-link
                :to="{ name: 'Users', params: { slug: item.user_id } }"
                >{{ item.author_name }}</router-link
              >
              <small class="text-muted"> 2022-06-28 </small>
            </div>
            <h2>
              <router-link
                :to="{ name: 'Posts', params: { slug: item.id } }"
                class="article-title"
              >
                {{ item.title }}
              </router-link>
            </h2>
            <p class="article-content">{{ item.content }}</p>
          </div>
        </article>
      </div>
    </div>
    <TheGroups />
  </div>
  <div v-else class="alert alert-danger" role="alert">
    You must first login to see this page.
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";
import store from "@/vuex";
import TheGroups from "@/components/TheGroups.vue";

export default {
  name: "Home",
  data() {
    return {
      groups: store.getters.groups,
    };
  },
  components: {
    TheGroups,
  },

  computed: {
    ...mapGetters(["user"]),
    ...mapGetters(["posts"]),
  },

  async created() {
    let post_response = await axios.get("http://52.2.150.187:8002/posts", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    });
    let posts = await post_response.data.posts;
    this.$store.dispatch("posts", posts);

    let groups_response = await axios.get(
      "http://52.2.150.187:8001/groups?page=0",
      {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      }
    );
    let groups = groups_response.data.grupos;
    this.$store.dispatch("groups", groups);
  },
};
</script>

<style scoped>
@import "../assets/styles.css";
</style>
