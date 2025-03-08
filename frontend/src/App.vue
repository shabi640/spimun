<template>
  <div id="app" class="glass-bg">
    <!-- 背景装饰元素 -->
    <div class="glass-decoration circle1"></div>
    <div class="glass-decoration circle2"></div>
    <div class="glass-decoration circle3"></div>

    <GlassMenu v-if="showNavBar" :default-active="activeIndex" class="el-menu-demo glass-navbar" mode="horizontal"
      :ellipsis="false" @select="handleSelect">
      <!-- Left side nav items -->
      <div class="nav-left">
        <GlassMenuItem index="0">Home</GlassMenuItem>

        <GlassSubMenu index="1">
          <template #title>Uploads</template>
          <GlassMenuItem index="1-1">Clauses</GlassMenuItem>
          <GlassMenuItem index="1-2">Amendments</GlassMenuItem>
        </GlassSubMenu>

        <GlassSubMenu index="2">
          <template #title>
            <span @click.stop="delegate && goToCommitteePage('debating')">Debating</span>
          </template>
          <GlassMenuItem index="2-1" @click="goToCommitteePage('debating', 'senior')">Senior</GlassMenuItem>
          <GlassMenuItem index="2-2" @click="goToCommitteePage('debating', 'junior')">Junior</GlassMenuItem>
          <GlassMenuItem index="2-3" @click="goToCommitteePage('debating', 'security-council')">Security
            Council</GlassMenuItem>
        </GlassSubMenu>

        <GlassSubMenu index="3">
          <template #title>
            <span @click.stop="delegate && goToCommitteePage('resolution')">Resolution</span>
          </template>
          <GlassMenuItem index="3-1" @click="goToCommitteePage('resolution', 'senior')">Senior</GlassMenuItem>
          <GlassMenuItem index="3-2" @click="goToCommitteePage('resolution', 'junior')">Junior</GlassMenuItem>
          <GlassMenuItem index="3-3" @click="goToCommitteePage('resolution', 'security-council')">Security
            Council</GlassMenuItem>
        </GlassSubMenu>

        <GlassMenuItem index="4">Chat</GlassMenuItem>
      </div>

      <!-- Right side nav items -->
      <div class="nav-right">
        <GlassMenuItem index="5">Chair</GlassMenuItem>

        <!-- Delegate Info or Sign-In -->
        <GlassMenuItem v-if="!delegate" index="sign-in">
          <GlassButton @click="showLoginForm" class="glass-button" text>Sign In</GlassButton>
        </GlassMenuItem>

        <GlassSubMenu v-if="delegate" index="6">
          <template #title>
            <img :src="`https://flagcdn.com/24x18/${countryCode}.png`" class="flag-icon" alt="flag" />
            {{ delegate.name }}
          </template>
          <GlassMenuItem index="6-1" @click="signOut">Sign Out</GlassMenuItem>
        </GlassSubMenu>
      </div>
    </GlassMenu>

    <!-- Login Form -->
    <login-form :visible="isLoginFormVisible" @login="handleLogin" @refuse-login="isLoginFormVisible = false"
      @update:visible="val => isLoginFormVisible = val" />

    <router-view v-slot="{ Component }">
      <transition :name="$route.path === '/' ? 'fade' : slideDirection" mode="out-in">
        <div :key="$route.fullPath" class="content-wrapper" :class="{ 'home-content': $route.path === '/' }">
          <component :is="Component" />
        </div>
      </transition>
    </router-view>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, provide, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import LoginForm from '@/components/LoginForm.vue';
import { GlassMessage } from './components/ui';
import '@/assets/glassmorphism.css';

const activeIndex = ref('1');
const router = useRouter();
const delegate = ref(JSON.parse(localStorage.getItem('delegate') || 'null'));
const isLoginFormVisible = ref(false);
const showNavBar = ref(true);

const routeOrder = {
  'home': 0,
  'clauses_upload': 1,
  'amendments_upload': 2,
  'debating': 3,
  'resolution': 4,
  'chat': 5,
  'chair': 6
};

const slideDirection = ref('');

const handleSelect = (key: string) => {
  const currentRoute = router.currentRoute.value.name as string;
  const currentOrder = routeOrder[currentRoute] || 0;

  let targetRoute;
  switch (key) {
    case '0':
      targetRoute = 'home';
      break;
    case '1-1':
      targetRoute = 'clauses_upload';
      break;
    case '1-2':
      targetRoute = 'amendments_upload';
      break;
    case '4':
      targetRoute = 'chat';
      break;
    case '5':
      targetRoute = 'chair';
      break;
    default:
      targetRoute = currentRoute;
  }

  // Only set slide direction for non-home routes or when not navigating to home
  if (targetRoute !== 'home' && currentRoute !== 'home') {
    const targetOrder = routeOrder[targetRoute] || 0;
    slideDirection.value = targetOrder > currentOrder ? 'slide-left' : 'slide-right';
  } else {
    // For home route transitions, just use fade
    slideDirection.value = 'fade';
  }

  switch (key) {
    case '0':
      router.push('/');
      break;
    case '1-1':
      router.push('/clauses_upload');
      break;
    case '1-2':
      const delegateInfo = JSON.parse(localStorage.getItem('delegate') || 'null');
      if (delegateInfo && delegateInfo.committee) {
        router.push(`/amendments_upload/${delegateInfo.committee}`);
      } else {
        GlassMessage({
          showClose: true,
          message: 'Please login first to submit amendments',
          type: 'warning',
        });
      }
      break;
    case '2-1':
      router.push('/debating/senior');
      break;
    case '2-2':
      router.push('/debating/junior');
      break;
    case '2-3':
      router.push('/debating/security-council');
      break;
    case '3-1':
      router.push('/resolution/senior');
      break;
    case '3-2':
      router.push('/resolution/junior');
      break;
    case '3-3':
      router.push('/resolution/security-council');
      break;
    case '4':
      const delegateid = (delegate.value ? delegate.value.id : '');
      if (delegateid) {
        router.push({ name: 'ChatComponent', state: { delegateid: JSON.stringify(delegateid) } });
      }
      else {
        GlassMessage({
          showClose: true,
          message: 'Please login first to chat',
          type: 'warning',
        })
      }
      break;
    case '5':
      router.push('/chair');
      break;
    default:
      break;
  }
};

const goToCommitteePage = (type: string, committee: string | null = null) => {
  const currentRoute = router.currentRoute.value.name as string;
  const currentOrder = routeOrder[currentRoute] || 0;
  const targetOrder = routeOrder[type] || 0;

  slideDirection.value = targetOrder > currentOrder ? 'slide-left' : 'slide-right';

  const targetCommittee = committee || (delegate.value ? delegate.value.committee : '');
  if (targetCommittee) {
    router.push(`/${type}/${targetCommittee}`);
  }
};

const showLoginForm = () => {
  console.log('showLoginForm called'); // Debug log
  isLoginFormVisible.value = true;
};

const handleLogin = (delegateInfo) => {
  console.log('handleLogin called', delegateInfo); // Debug log
  delegate.value = delegateInfo;
  localStorage.setItem('delegate', JSON.stringify(delegateInfo));
  isLoginFormVisible.value = false;

  // Navigate to home to force re-render
  router.push({ path: '/', query: { t: Date.now() } });
};

const signOut = () => {
  console.log('signOut called'); // Debug log
  localStorage.removeItem('delegate');
  delegate.value = null;
  router.push('/');
};

const countryCode = computed(() => {
  if (!delegate.value || !delegate.value.country) return '';
  return delegate.value.country.toLowerCase();
});

// Function to control navigation bar visibility
const setNavBarVisibility = (visible: boolean) => {
  showNavBar.value = visible;
};

provide('setNavBarVisibility', setNavBarVisibility);
</script>

<style>
/* Add these global resets at the top */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
}

.el-menu--horizontal>.el-menu-item:nth-child(5) {
  margin-right: auto;
}

a {
  text-decoration: none;
}

.flag-icon {
  width: 24px;
  height: 18px;
  margin-right: 5px;
}

/* 背景装饰元素 */
.glass-decoration {
  position: fixed;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  box-shadow: 0 0 60px rgba(79, 236, 184, 0.2);
  z-index: -1;
}

.circle1 {
  width: 500px;
  height: 500px;
  top: 0%;
  left: 10%;
  background: linear-gradient(45deg, rgba(0, 150, 136, 0.05), rgba(32, 178, 170, 0.1));
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: float-slow 15s ease-in-out infinite;
}

.circle2 {
  width: 300px;
  height: 300px;
  bottom: 5%;
  right: 10%;
  background: linear-gradient(45deg, rgba(30, 144, 255, 0.05), rgba(0, 128, 128, 0.1));
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: float-slow 12s ease-in-out infinite;
  animation-delay: -3s;
}

.circle3 {
  width: 200px;
  height: 200px;
  top: 40%;
  right: 25%;
  background: linear-gradient(45deg, rgba(32, 178, 170, 0.05), rgba(0, 191, 255, 0.1));
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: float-slow 10s ease-in-out infinite;
  animation-delay: -7s;
}

/* 覆盖Element Plus样式 */
.glass-navbar {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(10px) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important;
  position: relative;
  z-index: 1000;
  display: flex;
  justify-content: space-between;
}

.nav-left {
  display: flex;
}

.nav-right {
  display: flex;
  margin-left: auto;
}

.glass-navbar .el-menu-item,
.glass-navbar .el-sub-menu__title {
  background: transparent !important;
  color: white !important;
  border-bottom: none !important;
  transition: all 0.3s ease;
}

.glass-navbar .el-menu-item:hover,
.glass-navbar .el-sub-menu__title:hover,
.glass-navbar .el-menu-item.is-active {
  background: rgba(255, 255, 255, 0.15) !important;
  color: rgba(79, 236, 184, 1) !important;
}

.el-sub-menu__title:hover {
  background: rgba(255, 255, 255, 0.15) !important;
}

.el-menu--popup {
  background: rgba(30, 60, 90, 0.9) !important;
  backdrop-filter: blur(10px) !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  border-radius: 8px !important;
}

.el-menu--popup .el-menu-item {
  background: transparent !important;
  color: white !important;
}

.el-menu--popup .el-menu-item:hover,
.el-menu--popup .el-menu-item.is-active {
  background: rgba(255, 255, 255, 0.15) !important;
  color: rgba(79, 236, 184, 1) !important;
}

/* GlassUI 导航栏样式覆盖 */
.glass-menu--horizontal .glass-submenu__popup {
  min-width: 220px !important;
  /* 增加下拉菜单最小宽度 */
  padding: 8px 0;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3) !important;
}

.glass-submenu__title,
.glass-menu-item {
  padding: 0 20px !important;
  height: 40px !important;
  line-height: 40px !important;
  white-space: nowrap;
}

.glass-submenu__content {
  padding: 5px 0;
}

.glass-menu--horizontal .glass-submenu__content {
  width: 100%;
}

.glass-menu--horizontal .glass-submenu .glass-menu-item {
  text-align: left;
  padding: 0 20px !important;
  width: 100%;
  box-sizing: border-box;
}

.content-wrapper {
  padding: 0;
  height: calc(100vh - 80px);
  overflow-y: auto;
  width: 100%;
}

/* 继续保留其他原有样式 */
ol {
  list-style-type: decimal;
  margin-bottom: 1em;
}

ol ol {
  list-style-type: lower-alpha;
  margin-bottom: 1em;
}

ol ol ol {
  list-style-type: lower-roman;
  margin-bottom: 1em;
}

ol ol ol ol {
  list-style-type: upper-alpha;
}

ol ol ol ol ol {
  list-style-type: upper-roman;
}

li {
  margin-bottom: 1em;
}

/* Slide Transitions */
.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.3s ease-out;
}

.slide-left-enter-from {
  opacity: 0;
  transform: translateX(50px);
}

.slide-left-leave-to {
  opacity: 0;
  transform: translateX(-50px);
}

.slide-right-enter-from {
  opacity: 0;
  transform: translateX(-50px);
}

.slide-right-leave-to {
  opacity: 0;
  transform: translateX(50px);
}

/* Simple fade transition for home page */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Ensure components don't overlap during transition */
.slide-left-leave-active,
.slide-right-leave-active,
.fade-leave-active {
  position: absolute;
  width: 100%;
}

/* Add this to your container to handle absolute positioning during transitions */
#app {
  position: relative;
  overflow-x: hidden;
  min-height: 100vh;
  width: 100vw;
  color: white;
  margin: 0;
  padding: 0;
}

/* Ensure the router view container maintains height during transitions */
#app> :nth-child(2) {
  min-height: calc(100vh - 60px);
  /* Adjust based on your menu height */
}

/* Special styling for the home route */
.content-wrapper.home-content {
  height: 100vh; /* Full height for home */
  padding: 0;
  margin: 0;
  overflow: hidden; /* Prevent scrollbars during transitions */
  position: absolute; /* Ensure it's positioned absolutely */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
</style>