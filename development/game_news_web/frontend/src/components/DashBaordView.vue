<template>
  <div id="app">
    <div class="main-buttons">
      <button
        v-if="isDeckShuffled"
        @click="displayInitialDeck"
        class="button is-primary is-outlined"
      >
        Reset <i class="fas fa-undo"></i>
      </button>
		<v-chip-group
		class="mx-7"
        selected-class="text-primary"
        column
      >
        <v-chip
		class="mx-2"
          v-for="category in categories"
          :key="category"
		@click="setCategory(category)"
        >
          {{ category }}
        </v-chip>
      </v-chip-group>
      <!-- <button @click="shuffleDeck" class="button is-primary">
        Shuffle <i class="fas fa-random"></i>
      </button> -->
    </div>
    <transition-group :name="shuffleSpeed" tag="div" class="deck">
	<news-card v-for="news in cards" :key=news.url :news=news @click="goDetailView(news)"></news-card>
      
    </transition-group>
  </div>
</template>
<script>
import { ref, onMounted } from "vue";
import axios from "axios"; // Import axios for API calls
import NewsCard from "@/components/ArticleCard.vue";

export default {
  name: "CardShuffling",
  components: {
	"news-card": NewsCard,
  },
  methods:{
	goDetailView(news){
		this.$router.push({ name: "ArticleDetail",
		query: {tmpURL: encodeURIComponent(news.url)}});
	},
	async setCategory(category) {
  if (this.category === category) {
    this.category = null;
    await this.fetchParquetData();
    return;
  }

  this.category = category; // 카테고리 변경
  this.loading = true; // 로딩 시작
  try {
    const response = await axios.get(
      `https://saffy-pjt-news-kjyij.run.goorm.site/api/article/list/${category}/`
    );

    if (response.data && response.data.status === "success") {
      this.cards = response.data.data || [];
    } else {
      this.error = response.data?.message || "Unexpected error.";
    }
  } catch (err) {
    this.error = err.response?.data?.message || "Error fetching data from the server.";
    console.error("Error details:", err);
  } finally {
    this.loading = false; // 로딩 종료
  }
}

  },
  setup() {
    const cards = ref([]); // Reactive list of cards
    const shuffleSpeed = ref("shuffleMedium");
    const shuffleTypes = ["Slow", "Medium", "Fast"];
    const isDeckShuffled = ref(false);
    const shuffleCount = ref(0);
    const error = ref(null);

    
// Fetch Parquet Data
    const fetchParquetData = async () => {
      try {
        const response = await axios.get(
          "https://saffy-pjt-news-kjyij.run.goorm.site/api/article/list/"
        );
        if (response.data.status === "success") {
          cards.value = response.data.data; // Update cards with fetched data
        } else {
          error.value = response.data.message;
        }
      } catch (err) {
        error.value = "Error fetching data from the server.";
        console.error(err);
      }
    };

    // Initialize deck
    const displayInitialDeck = () => {
      isDeckShuffled.value = false;
      shuffleCount.value = 0;
    };

    // Shuffle the deck
    const shuffleDeck = () => {
      for (let i = cards.value.length - 1; i > 0; i--) {
        const randomIndex = Math.floor(Math.random() * i);
        [cards.value[i], cards.value[randomIndex]] = [
          cards.value[randomIndex],
          cards.value[i],
        ];
      }
      isDeckShuffled.value = true;
      shuffleCount.value++;
    };

    onMounted(() => {
      fetchParquetData(); // Fetch data when component is mounted
      displayInitialDeck();
    });

    return {
		categories:["출시", "업데이트", "게임 산업 동향", "행사", "리뷰", "기술", "e-sport", "사건사고 및 기타"],
		category:null,
		cards,
      shuffleSpeed,
      shuffleTypes,
      isDeckShuffled,
      shuffleCount,
      error,
      displayInitialDeck,
      shuffleDeck,
      fetchParquetData, // Return to expose in the template or hooks
    };
  },
};
</script>

<style scoped>
html,
body,
#app {
  height: 100%;
  background: ghostwhite;
}

.title {
  font-family: "Roboto Slab", sans-serif;
  text-align: center;
  padding-top: 30px;
  margin-bottom: 0;
  font-weight: 300;
  font-size: 3rem;
}

.vue-logo {
  height: 55px;
  position: relative;
  top: 10px;
}

.speed-buttons {
  text-align: center;
  padding-top: 30px;
}
.speed-buttons .button {
  height: 2.5em;
}

.main-buttons {
  text-align: center;
  padding-top: 30px;
}

.count-section {
  position: absolute;
  top: 10px;
  right: 10px;
}

.deck {
	display: flex;          /* Flexbox 활성화 */
  flex-wrap: wrap; 
  margin-left: 30px;
  padding-top: 30px;
}

.card-front,
.card-back {
  
  text-align: center;
  padding: 10px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.shuffleSlow-move {
  transition: transform 2s;
}

.shuffleMedium-move {
  transition: transform 1s;
}

.shuffleFast-move {
  transition: transform 0.5s;
}
	.card{
		margin:25px;
		margin-left:15px;
		margin-right:15px;
	}

</style>
