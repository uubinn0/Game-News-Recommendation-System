const { defineConfig } = require('@vue/cli-service');
const { VuetifyPlugin } = require('webpack-plugin-vuetify');

module.exports = defineConfig({
  transpileDependencies: true,

  devServer: {
    allowedHosts: "all",
    // proxy 설정은 필요할 때만 활성화
    // proxy: {
    //   '/picsum': {
    //     target: 'https://picsum.photos',
    //     changeOrigin: true,
    //     pathRewrite: { '^/picsum': '' },
    //   },
    // },
  },

  publicPath: process.env.NODE_ENV === 'production' ? '/static/' : '/',

  configureWebpack: {
    plugins: [new VuetifyPlugin()],
  },

  pluginOptions: {
    vuetify: {
      // 추가 옵션이 필요할 경우 여기에 작성
    },
  },
});
