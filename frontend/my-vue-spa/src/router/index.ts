import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/loginpage',
    name: 'LoginPage', // Updated name to match the route naming convention
    component: () => import('../views/LoginPage.vue') // Dynamically import the LoginPage component
  },
  {
    path: '/coursespage',
    name: 'CoursesPage', // Updated name to match the route naming convention
    component: () => import('../views/CorsesPage.vue') // Dynamically import the LoginPage component
  },
  {
    path: '/python',
    name: 'PythonPage', // Updated name to match the route naming convention
    component: () => import('../views/PythonPage.vue') // Dynamically import the LoginPage component
  },
  {
    path: '/english',
    name: 'EnglishPage', // Updated name to match the route naming convention
    component: () => import('../views/EnglishPage.vue') // Dynamically import the LoginPage component
  },
  {
    path: '/coding',
    name: 'CodingPage', // Updated name to match the route naming convention
    component: () => import('../views/CodingPage.vue') // Dynamically import the LoginPage component
  },
  {
    path: '/signup',
    name: 'SignUpPage', // Updated name to match the route naming convention
    component: () => import('../views/SignUpPage.vue') // Dynamically import the LoginPage component
  },
  {
    path: '/student-dashboard',
    name: 'StudentDashboard', // Updated name to match the route naming convention
    component: () => import('../views/StudentDashboard.vue') // Dynamically import the StudentDashboard component
  },
  {
    path: '/instructor-dashboard',
    name: 'InstructorDashboard', // Updated name to match the route naming convention
    component: () => import('../views/InstructorDashboard.vue') // Dynamically import the InstructorDashboard component
  },
  {
    path: '/python-grades',
    name: 'PythonGrades', // Updated name to match the route naming convention
    component: () => import('../views/PythonGrades.vue') // Dynamically import the LoginPage component
  },
  {
    path: '/english-grades',
    name: 'EnglishGrades', // Updated name to match the route naming convention
    component: () => import('../views/EnglishGrades.vue') // Dynamically import the LoginPage component
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
