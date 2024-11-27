<template>
  <video-background
    :src="videoSource"
    style="height: 100vh; width: 100vw">
    <v-container fluid fill-height class=" justify-center align-center align-content-center">
      <v-row class="d-flex justify-center align-center" no-gutters>
        <!-- Left Image -->
        <v-col cols="1" class="pa-0">
          <img
            :src="loginLeft" 
            alt="Image 1">
        </v-col>
        <!-- Center Content with Login Form -->
        <v-col cols="5" class="pa-0 justify-center align-center" style="position: relative;">
          <img :src="loginCenter" alt="Image 2" class="w-100">
          <div class="login-text" style="text-align:-webkit-center;">
            <v-text-field
				style="width:70%;"
				class="idpsw"
              v-model="username" 
              label="ID" 
              outlined></v-text-field>
            <v-text-field 
			style="width:70%;"
              v-model="password" 
              label="PASSWORD" 
              type="password" 
              outlined></v-text-field>
            <v-btn variant="outlined" class="signINorUP mt-6" color="white" v-if="!signUp" @click="handleLogin">로그인</v-btn>
			<v-btn variant="outlined" class="signINorUP mt-6" color="white" v-else @click="handleSignup">회원가입</v-btn>
          </div>
        </v-col>
        
        <!-- Right Image -->
        <v-col cols="1" class="pa-0">
          <img
            :src="loginRight" 
            alt="Image 3"
			@click="handleClick">
			<div 
      v-for="(effect, index) in effects" 
      :key="index" 
      class="click-effect" 
      :style="{ left: `${effect.x}px`, top: `${effect.y}px` }"
    ></div>
        </v-col>
      </v-row>
	<v-row class="d-flex justify-center align-center" no-gutters style="height: 20vh;">
        <!-- Left Image -->
        <v-col cols="12" class="pa-0">
			<p class="loginDescription text-h2">
				PRESS A = Sign In
	</p>
			<p class="loginDescription text-h2">
				PRESS B = Sign Up
			</p>
        </v-col>
	</v-row>
    </v-container>
  </video-background>
</template>

<script>
import videoSource from '@/assets/gaming_news_background.mp4';
import loginLeft from '@/assets/login_left.png';
import loginRight from '@/assets/login_right.png';
import loginCenter from '@/assets/login_center.png';
import { signup, login } from '@/api/auth';
import { useAuthStore } from "@/stores/auth";
	
export default {
  data() {
    return {
		effects: [],
      videoSource,
      loginLeft,
      loginRight,
      loginCenter,
      username: '',
      password: '',
      signUp : false, // 초기 상태에서 right가 그레이스케일
    };
  },
  methods: {
async handleSignup() {
      try {
        const userData = {
          username: this.username,
          email: this.username,
          password: this.password,
          password_confirm: this.password
        };
        const response = await signup(userData);
        this.message = response.message;
      } catch (error) {
        this.message = error.error || '회원가입 중 오류가 발생했습니다.';
      }
    },
	async handleLogin() {
		const authStore = useAuthStore()
      try {
        const userData = {
          username: this.username,
          password: this.password
        };
        const response = await login(userData);
        this.message = '로그인 성공!';
        // 로그인 상태 갱신
        this.$emit('login', response.token);
		const tmpToken = localStorage.getItem('authToken');
		authStore.login(tmpToken);
		this.$router.push({ name: "Dashboard" });
      } catch (error) {
		
        this.message = error.error || '로그인 중 오류가 발생했습니다.';
      }
    },
	handleClick(event) {
	const container = event.currentTarget;

	// 이미지 컨테이너의 크기와 위치 정보 가져오기
	const rect = container.getBoundingClientRect();

	// 클릭한 위치의 상대적인 비율 계산
	const xPercent = ((event.clientX - rect.left) / rect.width) * 100;
	const yPercent = ((event.clientY - rect.top) / rect.height) * 100;
	

	// 특정 위치에 따라 이벤트 트리거
	if (xPercent > 35 && xPercent < 55 && yPercent > 30 && yPercent < 36) {
		this.signUp = true;
		const a = event.clientX, b = event.clientY;
			const newEffect = { x:a, y:b };
			console.log("B")
			this.effects.push(newEffect);
			// 일정 시간 후 효과 제거
			setTimeout(() => {
			this.effects.shift(); // 첫 번째 효과 제거
			}, 700); // 효과 지속 시간
	} else if (xPercent > 58 && xPercent < 78 && yPercent > 22 && yPercent < 28) {
		this.signUp = false;
		const a = event.clientX, b = event.clientY;
			const newEffect = { x:a, y:b };
			console.log("A")
			this.effects.push(newEffect);
			// 일정 시간 후 효과 제거
			setTimeout(() => {
			this.effects.shift(); // 첫 번째 효과 제거
			}, 700); // 효과 지속 시간
	} else {
		// alert(`클릭한 위치: X(${xPercent.toFixed(2)}%), Y(${yPercent.toFixed(2)}%)`);
	}
	}
  }
};
</script>

<style scoped>
/* 비디오 배경 및 텍스트 스타일 */
video-background {
  position: relative;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

h1 {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 3rem;
  color: white;
}

.v-container {
  height: 100vh;
}

.v-row {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.v-col {
  padding: 0 !important; /* Remove padding from columns to avoid spacing between images */
}

img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: filter 0.3s;
}

.grayscale {
  filter: grayscale(100%);
}

.login-text {
  position: absolute;
  color: white;
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  width: 100%;
  top: 50%;
  transform: translateY(-50%);
}

v-btn {
  margin-top: 20px;
}

	
@font-face {
    font-family: 'pixeboy-font';
    src: url('@/assets/pixeboy-font.ttf') format('truetype');
}

@font-face {
    font-family: 'pixelon-font';
    src: url('@/assets/Pixelon-font.ttf') format('truetype');
}
@font-face {
    font-family: 'galmuri-font';
    src: url('@/assets/galmuri-font.ttf') format('truetype');
}
	.signINorUP{
		font-family: 'galmuri-font', sans-serif;
		color: white;
		font-size:22px;
		text-align:center;
	}

	
.loginDescription {
    font-family: 'pixeboy-font', sans-serif;
	color:white;
	text-align:center;
	font-size:32px;
}
	
.idpsw {
    font-family: 'pixelon-font', sans-serif;
	color:white;
	text-align:center;
}

.click-effect {
	position: absolute;
  width: 40px;
  height: 40px;
  background-color: rgba(0, 150, 255, 0.7);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: pop 0.5s ease-out forwards;
}

@keyframes pop {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(2);
    opacity: 0;
  }
}
</style>
