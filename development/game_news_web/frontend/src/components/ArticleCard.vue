<!-- src/components/NewsCard.vue -->
<template>
	<vue-flip
        :active-hover="true"
		class="card"
        width="400px"
        height="400px"
      >
		
		
        <template #front>
          <v-card class="mb-4 pa-5" outlined >
      <v-card-title>
        <div class="d-flex justify-space-between align-center w-100">
          <span class="text-h6" style="width:250px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{{ news.title }}</span>
          <v-chip small color="primary">{{ news.category }}</v-chip>
        </div>
      </v-card-title>
      <v-card-subtitle style="width:400px; height:200px;">
        <span>{{ news.company }}</span>
      </v-card-subtitle>
<!-- <v-chip v-for="keyword in news.keywords.slice(0,4)" :key="keyword">{{ keyword }}</v-chip> -->
      <v-card-text>
        <div class="d-flex justify-space-between">
          <div>
            <v-icon left>mdi-thumb-up</v-icon>{{ news.likes.split(',').length - 1 }}
          </div>
          <div>
            <v-icon left>mdi-eye</v-icon>{{ news.views }}
          </div>
        </div>
      </v-card-text>
    </v-card>
        </template>



        <template #back>
          <v-card class="mb-4 pa-5" outlined>
      <v-card-title>
        <v-chip small color="secondary">{{ news.category }}</v-chip>
      </v-card-title>
      <v-card-text style="width:350px; height:200px; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 8; -webkit-box-orient: vertical;">
  {{ news.content }}
</v-card-text>
      <v-card-actions>
        <div class="d-flex justify-space-between w-100">
          <div @click="likeUp">
            <v-icon left>mdi-thumb-up</v-icon>{{ news.likes.split(',').length - 1}}
          </div>
          <div>
            <v-icon left>mdi-eye</v-icon>{{ news.views }}
          </div>
        </div>
      </v-card-actions>
    </v-card>
        </template>
      </vue-flip>
</template>

<script>
import axios from 'axios';
import { VueFlip } from "vue-flip";
export default {
  name: "NewsCard",
  data() {
    return {
		likeList: [],
    };
  },
  components: {
    "vue-flip": VueFlip,
	// "news-card": NewsCard,
  },
  methods:{
	async likeUp(tmpURL) {  
	this.likeList = this.news.split(',')
	// var email = localStorage.getItem("email");
	const email = "tbvjekgus@naver.com"
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
  },
  props: {
    news: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
.text-truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
