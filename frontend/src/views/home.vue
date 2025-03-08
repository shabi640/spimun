<template>
  <div class="fullscreen-glass">
    <!-- 内容卡片 -->
    <div class="content-card">
      <div class="glass-shine"></div>
      <h1 class="main-title">
        <span class="highlight">SPIMUN</span> 2025
      </h1>
      <div class="glass-divider"></div>
      <h2 class="subtitle">
        <span v-if="delegate">Welcome, {{ delegate.name }}</span>
        <span v-else>Please sign in to continue</span>
      </h2>

      <!-- Login button for non-logged in users -->
      <div v-if="!delegate" class="login-container">
        <GlassButton @click="showLoginForm" class="login-button">Sign In</GlassButton>
      </div>
    </div>
  </div>

  <!-- Login Form -->
  <login-form :visible="isLoginFormVisible" @login="handleLogin" @refuse-login="isLoginFormVisible = false"
    @update:visible="val => isLoginFormVisible = val" />
</template>

<script lang="ts" setup>
import { ref, onMounted, inject, watch, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import LoginForm from '@/components/LoginForm.vue';

const delegate = ref(JSON.parse(localStorage.getItem('delegate') || 'null'));
const route = useRoute();
const router = useRouter();
const isLoginFormVisible = ref(false);

// Inject the function to control navigation bar visibility
const setNavBarVisibility = inject('setNavBarVisibility') as (visible: boolean) => void;

// Only call setNavBarVisibility if it exists
onMounted(async () => {
  if (typeof setNavBarVisibility === 'function') {
    setNavBarVisibility(true); // Show navigation bar immediately
  }
  
  // Add a small delay to ensure smooth rendering
  await nextTick();
  document.querySelector('.fullscreen-glass')?.classList.add('ready');
});

// Watch for route changes and update nav bar visibility
watch(
  () => route.path,
  (newPath) => {
    if (typeof setNavBarVisibility === 'function') {
      if (newPath !== '/') {
        setNavBarVisibility(true); // Show on other pages
      } else {
        setNavBarVisibility(true); // Also show on home now
      }
    }
  },
  { immediate: true }
);

// Login functions
const showLoginForm = () => {
  isLoginFormVisible.value = true;
};

const handleLogin = (delegateInfo) => {
  console.log('handleLogin called', delegateInfo); // Debug log
  delegate.value = delegateInfo;
  localStorage.setItem('delegate', JSON.stringify(delegateInfo));
  isLoginFormVisible.value = false;

  // Force re-render without query parameter to avoid jittering
  router.push('/');
};
</script>

<style scoped>
.fullscreen-glass {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: linear-gradient(125deg, #1a4d6d, #2e8b57, #0f6e8c);
  background-size: 300% 300%;
  animation: gradient-shift 20s ease infinite;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 0;
  opacity: 0;
  transition: opacity 0.4s ease-in;
  will-change: opacity;
}

.fullscreen-glass.ready {
  opacity: 1;
}

@keyframes gradient-shift {
  0% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0% 50%;
  }
}

.content-card {
  position: relative;
  width: 80%;
  max-width: 500px;
  padding: 3rem;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.07);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 0 20px rgba(255, 255, 255, 0.05);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  transition: all 0.3s ease;
  z-index: 2;
  opacity: 0;
  transform: translateY(20px);
  animation: card-appear 0.6s forwards;
  animation-delay: 0.2s;
}

@keyframes card-appear {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.glass-shine {
  position: absolute;
  top: 0;
  left: -150%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg,
      transparent,
      rgba(255, 255, 255, 0.2),
      transparent);
  transform: skewX(-25deg);
  animation: shine 8s infinite;
}

@keyframes shine {
  0% {
    left: -150%;
  }

  20% {
    left: 150%;
  }

  100% {
    left: 150%;
  }
}

.glass-divider {
  width: 70%;
  height: 1px;
  background: linear-gradient(90deg,
      transparent,
      rgba(79, 236, 184, 0.4),
      transparent);
  margin: 1.5rem 0;
}

.main-title {
  font-size: 3.2em;
  margin-bottom: 0.2em;
  letter-spacing: 2px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
  font-weight: 800;
  color: rgba(255, 255, 255, 0.95);
}

.highlight {
  background: linear-gradient(to right, #4adede, #1ca7ec);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 5px 15px rgba(47, 201, 226, 0.5);
}

.subtitle {
  font-size: 1.8em;
  margin-bottom: 0.5em;
  font-weight: 500;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
  color: rgba(255, 255, 255, 0.9);
}

.login-container {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
}

.login-button {
  background: linear-gradient(45deg, var(--glass-accent, #4adede), var(--glass-accent-secondary, #1ca7ec)) !important;
  border: none !important;
  padding: 0.8rem 2.5rem;
  font-size: 1.1rem;
  letter-spacing: 1px;
  border-radius: 30px;
  color: white;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(26, 188, 156, 0.3);
  cursor: pointer;
}

.login-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(26, 188, 156, 0.4);
}
</style>
