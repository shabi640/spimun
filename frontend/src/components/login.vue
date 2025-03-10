<template>
    <div v-if="visible" class="modal-overlay" @click.self="closeModal">
        <div class="modal">
            <h2>Login</h2>
            <form @submit.prevent="submitLogin">
                <div class="form-item">
                    <label for="username">Username</label>
                    <input id="username" type="text" v-model="loginForm.username" required />
                </div>
                <div class="form-item">
                    <label for="password">Password</label>
                    <input id="password" type="password" v-model="loginForm.password" required />
                </div>
                <div class="form-item">
                    <button type="submit">Login</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { defineEmits } from 'vue';

const emit = defineEmits(['login-success']); // Define the custom event

const visible = ref(true);
const loginForm = ref({
    username: '',
    password: ''
});
const router = useRouter();

const submitLogin = async () => {
    try {
        const response = await axios.post('http://127.0.0.1:8000/login', loginForm.value);
        const token = response.data.access_token;
        localStorage.setItem('token', token);
        visible.value = false;
        alert('Login successful');
        emit('login-success'); // Emit the event when login is successful
        router.push('/chair'); // Redirect to the protected route after login
    } catch (error) {
        alert('Invalid username or password');
    }
};

const resetForm = () => {
    loginForm.value.username = '';
    loginForm.value.password = '';
};

const closeModal = () => {
    resetForm();
    visible.value = false;
};
</script>

<style scoped>
/* Same styles as before */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal {
    background: white;
    padding: 20px;
    border-radius: 8px;
    width: 300px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    color: black;
}

.form-item {
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 5px;
}

input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
}

button {
    padding: 10px;
    background-color: #007bff;
    color: black;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: 100%;
}

button:hover {
    background-color: #0056b3;
}
</style>
