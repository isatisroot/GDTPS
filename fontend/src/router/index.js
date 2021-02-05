import Vue from 'vue'
import Router from 'vue-router'
import axios from 'axios'
Vue.prototype.axios = axios
Vue.prototype.host = 'http://172.30.0.126:8000/'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/form'
    },
    {
      path: '/',
      component: () => import(/* webpackChunkName: "home" */ '../components/common/Home.vue'),
      meta: { title: '自述文件' },
      children: [
        {
          path: '/form',
          name: 'form',
          component: () => import(/* webpackChunkName: "form" */ '../components/page/BaseForm.vue'),
          meta: { title: '股东登记' }
        },
        {
          path: '/tabs',
          component: () => import(/* webpackChunkName: "tabs" */ '../components/page/Tabs.vue'),
          meta: { title: '统计结果' }
        },
        {
          // 富文本编辑器组件
          path: '/editor',
          component: () => import(/* webpackChunkName: "editor" */ '../components/page/VueEditor.vue'),
          meta: { title: '表决统计' }
        },
        {
          path: '/dashboard',
          component: () => import(/* webpackChunkName: "dashboard" */ '../components/page/Dashboard.vue'),
          meta: { title: '会议信息' }
        },

        // {
        //     path: '/table',
        //     component: () => import(/* webpackChunkName: "table" */ '../components/page/BaseTable.vue'),
        //     meta: { title: '股东统计' }
        // },

        // {
        //     // markdown组件
        //     path: '/markdown',
        //     component: () => import(/* webpackChunkName: "markdown" */ '../components/page/Markdown.vue'),
        //     meta: { title: 'markdown编辑器' }
        // },
        // {
        //     // 图片上传组件
        //     path: '/upload',
        //     component: () => import(/* webpackChunkName: "upload" */ '../components/page/Upload.vue'),
        //     meta: { title: '文件上传' }
        // },
        {
            // vue-schart组件
            path: '/charts',
            component: () => import(/* webpackChunkName: "chart" */ '../components/page/BaseCharts.vue'),
            meta: { title: '图表统计' }
        },
        // {
        // 	path:'/shareholders',
        // 	component:()=> import(/* webpackChunkName: "shareholders" */'../components/page/ShareHolder.vue'),
        // 	meta:{title:'股东信息维护'}
        // },

      ]
    },
    {
      path: '/login',
      component: () => import(/* webpackChunkName: "login" */ '../components/page/Login.vue'),
      meta: { title: '登录' }
    },
    {
      path: '*',
      redirect: '/404'
    }
  ]
})
