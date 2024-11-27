import axios from "axios";

export const signup = async (userData) => {
  try {
    const response = await axios.post('https://saffy-pjt-news-kjyij.run.goorm.site/api/signup/', userData, {
      headers: { 'Content-Type': 'application/json' }
    });
    console.log('회원가입 성공:', response.data);
    return response.data; // 성공 메시지 반환
  } catch (error) {
    console.error('회원가입 실패:', error.response.data);
    throw error.response.data; // 오류 메시지 반환
  }
};

export const login = async (userData) => {
  try {
    const response = await axios.post('https://saffy-pjt-news-kjyij.run.goorm.site/api/login/', userData, {
      headers: { 'Content-Type': 'application/json' }
    });
    console.log('로그인 성공:', response.data);
    // 로그인 성공 시 토큰 저장
    localStorage.setItem('authToken', response.data.token);
	localStorage.setItem('email', userData.email)
    return response.data;
  } catch (error) {
    console.error('로그인 실패:', error.response.data);
    throw error.response.data; // 오류 메시지 반환
  }
};