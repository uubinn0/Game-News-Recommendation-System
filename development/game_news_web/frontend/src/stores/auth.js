import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("authToken") || null,
    isAuthenticated: !!localStorage.getItem("authToken"),
  }),
  actions: {
    login(token) {
      this.token = token;
      this.isAuthenticated = !!token;
    },
    logout() {
      this.token = null;
      this.isAuthenticated = false;
      localStorage.removeItem("token");
    },
	initializeAuth() {
      const token = localStorage.getItem('authToken');
      if (token) {
        this.login(token); // 토큰이 있으면 인증 상태 복원
      }
    },
  },
});