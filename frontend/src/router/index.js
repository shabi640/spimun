import { createRouter, createWebHashHistory } from 'vue-router';
import Home from '../views/home.vue';
import Clauses from '../views/upload_clauses.vue';
import DocumentViewer from '../components/document_viewer.vue';
import AmendmentsUpload from '../views/upload_amendments.vue';
import Debating from '../views/Debating.vue'
import Resolution from '../views/resolution.vue'
import ChatComponent from '../views/ChatComponent.vue'


const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/debating/:group',
        name: 'Debating',
        component: Debating,
    },
    {
        path: '/resolution/:committee',
        name: 'Resolution',
        component: Resolution,
    },
    {
        path: '/clauses_upload',
        name: 'Clauses',
        component: Clauses
    },
    {
  path: '/clauses_upload/view/:id',
  name: 'document_viewer',
  component: () => import('@/components/document_viewer.vue')
},
    {
        path: '/amendments_upload/:committee',
        name: 'AmendmentsUpload',
        component: AmendmentsUpload
    },
    {
        path: '/chat',
        name: 'ChatComponent',
        component: ChatComponent
    },
    {
        path: '/chair',
        name: 'ChairView',
        component: () => import('../views/chair.vue'), // Lazy loaded
        meta: { requiresAuth: true } // Protected route
    }
];

const router = createRouter({
    history: createWebHashHistory(),
    routes
});


export default router;
