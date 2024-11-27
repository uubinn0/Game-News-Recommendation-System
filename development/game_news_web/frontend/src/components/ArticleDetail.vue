<template>
  <div>
    <!-- 메인 기사 -->
    <div v-if="articles.length > 0" class="main-news">
      <v-card class="mb-4 pa-5" outlined>
        <v-card-title>
          <div class="d-flex justify-space-between align-center w-100">
            <span class="text-h6" style="width:250px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
              {{ articles[0].title }}
            </span>
            <v-chip small color="primary">{{ articles[0].category }}</v-chip>
          </div>
        </v-card-title>
        <v-card-subtitle style="width:400px; height:200px;">
          <span>{{ articles[0].company }}</span>
        </v-card-subtitle>
<v-card-text>
{{articles[0].content}}
	</v-card-text>
        <v-card-text>
          <div class="d-flex justify-space-between">
            <div @click="likeUp(articles[0].url)">
              <v-icon left>mdi-thumb-up</v-icon>{{ articles[0].likes.split(',').length - 1 }}
            </div>
            <div>
              <v-icon left>mdi-eye</v-icon>{{ articles[0].views }}
            </div>
          </div>
        </v-card-text>
      </v-card>
    </div>

    <!-- 나머지 기사 제목 -->
    <div v-if="articles.length > 1" class="other-news">
      <v-list>
        <v-list-item
          v-for="(news, index) in articles.slice(1)" 
          :key="index"
          class="other-news-item"
@click="goDetailView(news)"
        >
          <span @click="goDetailView(news)">{{ news.title }}</span>
        </v-list-item>
      </v-list>
    </div>
  </div>
</template>

<script>
import axios from "axios"; // Import axios for API calls

export default {
  name: "ArticleDetail",
	watch: {
    '$route.query.tmpURL': {
      immediate: true, // 컴포넌트 로드 시에도 실행
      handler(newVal, oldVal) {
        console.log(`tmpURL changed from "${oldVal}" to "${newVal}"`);
        this.getNews(newVal); // URL 변경에 따라 필요한 작업 실행
      },
    },
  },
  methods: {
goDetailView(news){
		console.log(news)
		this.$router.push({ name: "ArticleDetail",
		query: {tmpURL: encodeURIComponent(news.url)}});
	},
	async likeUp(tmpURL) {  
	this.likeList = this.articles[0].likes.split(',')
	var email = localStorage.getItem("email");
	// const email = "tbvjekgus@naver.com"
	if (this.likeList.includes(email)) {
  // email이 likeList에 있으면 제거
  this.likeList.splice(this.likeList.indexOf(email), 1);
} else {
  // email이 likeList에 없으면 추가
  this.likeList.push(email);
}
	const token = localStorage.getItem("access_token");
      this.loading = true; // 로딩 시작
      const url = `https://saffy-pjt-news-kjyij.run.goorm.site/api/article/list/like/${encodeURIComponent(tmpURL)}/`;
		console.log(url);
      try {
        const { data } = await axios.put(url,{},{headers: {
      Authorization: `Bearer ${token}`, // JWT 토큰
    },});
		console.log(data)
        if (data?.status === "success") {
          this.articles = data.data || [];
        } else {
          this.error = data?.message || "Unexpected error.";
        }
      } catch (err) {
        this.error =
          err.response?.data?.message || "Error fetching data from the server.";
        console.error("Error details:", err);
      } finally {
        this.loading = false; // 로딩 종료
      }
    },
    async getNews(tmpURL) {
      this.loading = true; // 로딩 시작
      const url = `https://saffy-pjt-news-kjyij.run.goorm.site/api/article/RAG/${encodeURIComponent(tmpURL)}/`;
console.log(url)
      try {
        const { data } = await axios.get(url);
		console.log(data)
        if (data?.status === "success") {
          this.articles = data.data || [];
        } else {
          this.error = data?.message || "Unexpected error.";
        }
      } catch (err) {
        this.error =
          err.response?.data?.message || "Error fetching data from the server.";
        console.error("Error details:", err);
      } finally {
        this.loading = false; // 로딩 종료
      }
    },
  },
  props: {
    id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      tmpURL: this.$route.query.tmpURL,
      articles: [],
      error: "",
      loading: false,
		likeList:[]
    };
  },
  created() {
    this.getNews(this.tmpURL);
  },
};
</script>

<style scoped>
.main-news {
  margin-bottom: 20px;
}

.other-news {
  display: flex;
  flex-direction: column;
  align-items: flex-end; /* 오른쪽 정렬 */
}

.other-news-item {
  margin-bottom: 10px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 1000px; /* 제목 최대 너비 설정 */
}
</style>
