//导入 进度条
import NProgress from "nprogress";
import "nprogress/nprogress.css";
import { createRouter, createWebHashHistory } from "vue-router";
import Layout from "@/components/Layout/index.vue";
import navPage from "@/views/index.vue";

NProgress.configure({ showSpinner: false }); // 进度条配置 NProgress 不显示加载旋转器
const routes = [
  {
    path: "/",
    name: "Nav",
    meta: {
      name: "导航",
    },
    redirect: "/home", // 重定向到首页
    component: navPage, // 该路由匹配时渲染的 Vue 组件
  },
  {
    path: "/",
    name: "Layout",
    meta: {
      name: "Layout",
    },
    component: Layout,
    redirect: "/home",
    children: [
      // 子路由
      {
        path: "/home",
        name: "Home",
        meta: {
          name: "首页",
        },
        component: () => import("@/views/home/home.vue"), // 异步加载组件，提高加载速度
      },
      {
        path: "/archives",
        name: "Archives",
        meta: {
          name: "时间轴",
        },
        component: () => import("@/views/archives/archives.vue"),
      },
      {
        path: "/category",
        name: "Category",
        meta: {
          name: "分类",
        },
        component: () => import("@/views/category/category.vue"),
      },
      {
        path: "/tag",
        name: "Tag",
        meta: {
          name: "标签",
        },
        component: () => import("@/views/tag/tag.vue"),
      },
      {
        path: "/article",
        name: "Article",
        meta: {
          name: "文章",
        },
        component: () => import("@/views/article/article.vue"),
      },
      {
        path: "/articleList",
        name: "ArticleList",
        meta: {
          name: "文章列表",
        },
        component: () => import("@/views/article/article-list.vue"),
      },
      {
        path: "/photoAlbum",
        name: "PhotoAlbum",
        meta: {
          name: "相册",
        },
        component: () => import("@/views/photo/photo-album.vue"),
      },
      {
        path: "/photos",
        name: "Photos",
        meta: {
          name: "图库",
        },
        component: () => import("@/views/photo/photos.vue"),
      },
      {
        path: "/talk",
        name: "Talk",
        meta: {
          name: "说说",
        },
        component: () => import("@/views/talk/talk.vue"),
      },
      {
        path: "/link",
        name: "link",
        meta: {
          name: "友链",
        },
        children: [
          {
            path: "list",
            name: "LinkList",
            meta: {
              name: "友情链接",
            },
            component: () => import("@/views/links/link-list.vue"),
          },
        ],
      },
      {
        path: "/resources",
        name: "Resources",
        meta: {
          name: "资源导航",
        },
        children: [
          {
            path: "/resources/front",
            name: "Front",
            meta: {
              name: "前端",
            },
            component: () => import("@/views/resources/category-list.vue"),
          },
          {
            path: "/resources/back",
            name: "Back",
            meta: {
              name: "后端",
            },
            component: () => import("@/views/resources/category-list.vue"),
          },
        ],
      },
      {
        path: "/siteList",
        name: "SiteList",
        meta: {
          name: "网站列表",
        },
        component: () => import("@/views/resources/site-list.vue"),
      },
      {
        path: "/userCenter",
        name: "UserCenter",
        meta: {
          name: "个人中心",
        },
        component: () => import("@/views/user/user-center.vue"),
      },
      {
        path: "/message",
        name: "Message",
        meta: {
          name: "留言",
        },
        children: [
          {
            path: "list",
            name: "MessageList",
            meta: {
              keepAlive: true,
              name: "留言",
            },
            component: () => import("@/views/message/index.vue"),
          },
          {
            path: "publish",
            name: "PublishMessage",
            meta: {
              name: "编辑/新增留言",
            },
            component: () => import("@/views/message/publish.vue"),
          },
          {
            path: "detail",
            name: "MessageDetail",
            meta: {
              name: "留言详情",
            },
            component: () => import("@/views/message/detail.vue"),
          },
        ],
      },
    ],
  },
  {
    path: "/:pathMatch(.*)*", // 匹配所有未找到路径的路由，返回一个 404 组件
    name: "404",
    meta: {
      name: "404 not found",
    },
    component: () => import("@/views/404/index.vue"),
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  NProgress.start(); // 每次路由切换时，启动 NProgress 进度条
  next();
});

// 不滚动到顶部的路由名单
const whiteList = ["/message/list"];

router.afterEach((to) => {
  // 切换就滚动到顶部
  if (!whiteList.includes(to.path)) {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  }

  NProgress.done();
});

export default router;
