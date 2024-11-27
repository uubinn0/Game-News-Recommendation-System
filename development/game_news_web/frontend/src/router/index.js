import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

// 인증 가드
const authGuard = (to, from, next) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: "Login" }); // 인증이 필요하지만 인증되지 않은 경우
  } else {
    next(); // 인증이 필요 없거나 인증 상태가 확인된 경우
  }
};

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/", // 기본 경로
      name: "Dashboard",
      component: () => import("../components/DashBaordView.vue"),
      meta: { requiresAuth: true }, // 인증 필요
      beforeEnter: authGuard, // 경로별 가드 적용
    },
    {
      path: "/login",
      name: "Login",
      component: () => import("../components/HelloWorld.vue"), // 로그인 페이지
    },
  {
    path: "/article/",
    name: "ArticleDetail",
    component: () => import("../components/ArticleDetail.vue"),
	meta: { requiresAuth: true }, // 인증 필요
    beforeEnter: authGuard, // 경로별 가드 적용
    props: true,
  },
{
      path: "/myPage",
      name: "myPage",
      component: () => import("../components/MyPage.vue"), // 로그인 페이지
    },
  ],
});

// 전역 가드로도 인증 처리 가능
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  console.log('Auth state:', authStore.isAuthenticated);
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: "Login" }); // 인증 필요 시 로그인 페이지로 이동
  } else {
    next(); // 진행
  }
});

export default router;
