import { createApp } from 'vue'
import { createPinia } from 'pinia';
import App from './App.vue'
import vuetify from './plugins/vuetify'
import VideoBackground from 'vue-responsive-video-background-player' // 추가
import router from "./router";
import { useAuthStore } from "@/stores/auth";
const pinia = createPinia();

createApp(App)
  .use(router)
  .use(pinia)
  .use(vuetify)
  .component('video-background', VideoBackground)
  .mount('#app')

const authStore = useAuthStore();
authStore.initializeAuth();