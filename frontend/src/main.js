//import './assets/main.css'

import { createApp } from 'vue'
import { CkeditorPlugin } from '@ckeditor/ckeditor5-vue'
import App from './App.vue'
import router from './router'
// import 'element-plus/dist/index.css';
import './assets/glassmorphism.css';
import GlassUI from './components/ui';

const app = createApp(App);

// 应用路由器和插件
app.use(router)
   .use(CkeditorPlugin)
   .use(GlassUI)  // 使用我们的自定义UI库
   .mount('#app')
