import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/LoginView.vue"),
  },
  {
    path: "/register",
    name: "register",
    component: () => import("../views/RegisterView.vue"),
  },
  {
    path: "/newpost",
    name: "newpost",
    component: () => import("../views/NewPostView.vue"),
  },
  {
    path: "/group/:group",
    name: "Groups",
    props: true,
    component: () => import("../views/GroupView.vue"),
  },
  {
    path: "/user/:user",
    name: "Users",
    props: true,
    component: () => import("../views/UserView.vue"),
  },
  {
    path: "/post/:post",
    name: "Post",
    props: true,
    component: () => import("../views/PostView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;