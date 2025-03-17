# 🎮 맞춤형 게임 뉴스 추천 웹 서비스 📰

## 👥 프로젝트 팀원

- **팀장**: 김다현 (Front & Back 개발)
- **팀원**: 나유빈 (데이터 처리 및 분석)

## 💡 프로젝트 소개

맞춤형 게임 뉴스 추천 웹 서비스는 사용자에게 게임 관련 뉴스를 맞춤형으로 제공하는 플랫폼입니다. OpenAI 기반의 자연어 처리 모델을 활용하여 뉴스를 카테고리별로 분류하고, 사용자의 관심사를 분석하여 최적의 뉴스를 추천합니다.

- **프로젝트 기간**: 2024년 11월 20일 ~ 11월 26일

## 🔧 주요 기능

### 1. 사용자 관리

- **회원가입 및 로그인**
  - 이메일 및 비밀번호 기반 회원가입/로그인 지원

### 2. 뉴스 제공 및 분류

- **카테고리별 뉴스 분류 (총 8개)**:
  - **출시**: 게임 및 콘솔 기기 출시 관련 기사
  - **업데이트**: 게임 업데이트 및 패치 관련 기사
  - **게임 산업 동향**: 국내외 게임 업계 현황, 게임 관련 법률 및 기업 매출 등
  -  **행사(오프라인)**: 게임 관련 행사 및 IP 콜라보 행사, 굿즈 판매 등
  -  **리뷰**: 게임 혹은 업데이트에 대한 평가 및 분석
  -  **기술**: 게임 개발 관련 SW/HW 기술 발전 소식
  -  **e-sport**: e-sport 관련 기사
  -  **사건사고 및 기타**: 주요 사건사고 및 게임 관련 비게임 뉴스
- **뉴스 미리보기 및 상세보기**
  - 기사 제목, 본문 미리보기, 좋아요 수, 조회수 제공
  - 실제 기사 링크 포함
  - 주요 키워드 제공
  - 본문 기반 유사한 기사 Top 3 추천

### 4. 개인화된 대시보드 (My Page)

- 나의 관심 카테고리 Top5 (읽은 기사 기반 도넛 차트 제공)
- 좋아요 누른 기사 카테고리 Top5 (좋아요 수 기반 도넛 차트 제공)
- 주요 키워드 (워드클라우드 제공)
- 주간 읽은 기사 수 (요일별 막대그래프 제공)
- 오늘의 추천 기사 (개인 맞춤 뉴스 추천)
- 언론사별 좋아요 누른 수

## 📈 데이터 처리

- **크롤링**: 15,000개 이상의 기사 데이터 수집
- **데이터 전처리**
  - OpenAI API를 활용한 카테고리 분류, 임베딩, 키워드 추출
  - 중복 제거 후 parquet 파일로 저장
  - 기존 parquet 파일과 통합하여 관리
- **Hadoop HDFS 적재** (일부 테스트 데이터만 저장)

## 🛠️ 기술 스택
![Vue](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![Javascript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache_Spark-E25A1C?style=for-the-badge&logo=apache-spark&logoColor=white)
![Hadoop](https://img.shields.io/badge/Hadoop-66CCFF?style=for-the-badge&logo=apache-hadoop&logoColor=black)
![Gitlab](https://img.shields.io/badge/Gitlab-FCA121?style=for-the-badge&logo=gitlab&logoColor=white)

## 🚀 추가 과제 및 발전 방향

- **스팀 연동**: 사용자 라이브러리 기반 게임 뉴스 추천
- **해외 사이트 기사 연동**
- **이스터에그 기능 추가**
