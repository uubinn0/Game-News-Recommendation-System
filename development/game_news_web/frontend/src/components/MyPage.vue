
<template>
  <div>
    <vue-word-cloud
  style="
    height: 480px;
    width: 640px;
  "
  :words="game_data = [['블루 아카이브', 15],
    ['던전앤파이터 페스티벌', 12],
    ['서든어택 챔피언십', 10],
    ['마비노기', 8],
    ['장송의 프리렌', 7],
    ['슈퍼바이브', 6],
    ['레전드 오브 이미르', 5],
    ['데블위딘: 삿갓', 4],
    ['테일즈런너 RPG', 4],
    ['게임 저작권', 3],
    ['지스타 2024', 3],
    ['e스포츠 대학리그', 3],
    ['패스 오브 엑자일 2', 2],
    ['히트 2', 2],
    ['쓰론 앤 리버티', 2],
    ['신의 탑: 새로운 세계', 2],
    ['아케인 시즌 2', 2],
    ['리니지 M', 2],
    ['진 삼국무쌍 오리진', 1],
    ['신월동행', 1],
    ['게임 규제', 5],
    ['콘솔 게임', 4],
    ['인공지능', 3],
    ['게임 IP', 3],
    ['중국 시장', 2],
    ['게임쇼', 2],
    ['트위치 서비스 종료', 2],
    ['스튜디오 뿌리 논란', 1],
    ['챗GPT', 1],
    ['E3 폐지', 1]]
"
  :color="([, weight]) => weight > 10 ? 'DeepPink' : weight > 5 ? 'RoyalBlue' : 'Indigo'"
  font-family="Roboto"
/>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
// import { BarChart } from 'vue-chart-3';
import VueWordCloud from 'vuewordcloud';


export default defineComponent({
  name: 'BarChartComponent',
  components: {
    // BarChart,
[VueWordCloud.name]: VueWordCloud,
  },
  data() {
    return {
      chartData: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June'],
        datasets: [
          {
            label: 'Sales',
            data: [65, 59, 80, 81, 56, 55],
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
          },
        ],
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    };
  },
});
</script>

<style scoped>
div {
  width: 100%;
  height: 400px;
}
</style>