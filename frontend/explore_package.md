# 基本信息

- **name**: 项目的名称。
- **version**: 项目的版本号。
- **private**: 设置为 true，表示这是一个私有项目，防止意外发布到 npm。
- **type**: 设置为 module，表示使用 ES 模块。

# 脚本

- **dev**: 启动开发服务器，使用 Vite。
- **build**: 打包项目，生成生产环境代码。
- **preview**: 预览打包后的项目。
- **lint**: 使用 ESLint 检查代码风格和语法错误，支持 .vue、.js、.jsx 等文件类型，并自动修复。
- **format**: 使用 Prettier 格式化 src 目录中的代码。

# 依赖项 (dependencies)

- **@vueuse/core**: Vue 的组合式 API 工具库，提供了多种实用的组合函数。
- **animate.css**: CSS 动画库，提供了多种常用的 CSS 动画效果。
- **autoprefixer**: 自动为 CSS 添加浏览器前缀的工具，确保更好的跨浏览器兼容性。
- **axios**: 基于 Promise 的 HTTP 客户端，用于发送 HTTP 请求。
- **core-js**: 提供了 ECMAScript 标准库的 polyfill，支持更老的浏览器。
- **crypto-js**: 提供加密和解密功能的 JavaScript 库，支持多种加密算法。
- **element-plus**: Vue 3 的 UI 组件库，提供了一套高质量的组件，适用于快速构建现代网页。
- **express**: 快速、开放、极简的 Node.js Web 框架，通常用于构建后端服务。
- **gsap**: 动画库，提供强大的动画控制和效果，适用于前端动画。
- **md-editor-v3**: Markdown 编辑器，支持实时预览，适用于博客和文档编辑。
- **mint-filter**: 可能是一个用于过滤和排序数据的工具库。
- **nprogress**: 页面加载进度条，提供用户友好的加载反馈。
- **pinia**: Vue 3 的状态管理库，类似于 Vuex，但更加简单和灵活。
- **pinia-plugin-persist**: Pinia 的持久化插件，用于将状态持久化到本地存储。
- **postcss**: CSS 处理工具，支持插件，可以用来处理 CSS 代码。
- **sass-loader**: 将 Sass 转换为 CSS 的 Webpack 加载器。
- **tailwindcss**: 一个功能类优先的 CSS 框架，提供了一系列的实用类来构建 UI。
- **unplugin-auto-import**: 自动导入模块的工具，减少重复的导入语句。
- **unplugin-vue-components**: 自动导入 Vue 组件的工具，简化组件使用。
- **vite-plugin-compression**: Vite 插件，用于对打包后的文件进行压缩，减少文件大小。
- **vite-plugin-require-transform**: 支持 CommonJS 的 Vite 插件，允许使用 require 语法。
- **vite-plugin-svg-icons**: Vite 插件，支持将 SVG 图标转化为 Vue 组件。
- **vue**: Vue.js 框架，用于构建用户界面。
- **vue-router**: Vue.js 的路由管理库，提供 SPA 应用的路由功能。
- **vue3-danmaku**: Vue 3 的弹幕组件库，用于实现弹幕效果。

# 开发依赖项 (devDependencies)

- **@rollup/plugin-commonjs**: Rollup 插件，用于支持 CommonJS 模块。
- **@rushstack/eslint-patch**: 解决 ESLint 的一些问题的补丁库。
- **@vitejs/plugin-vue**: Vite 的 Vue 插件，支持 Vue 单文件组件（SFC）。
- **@vue/eslint-config-prettier**: Vue 项目的 ESLint 和 Prettier 兼容配置，确保两者的规则不冲突。
- **eslint**: JavaScript 和 Vue 项目的代码质量和风格检查工具。
- **eslint-plugin-vue**: ESLint 的 Vue 插件，提供 Vue 特有的代码检查规则。
- **prettier**: 代码格式化工具，确保代码风格一致。
- **sass**: Sass 的核心库，用于编写样式。
- **sass-embedded**: 用于支持 Sass 的嵌入式实现，提供更好的编译速度和功能。
- **vite**: 前端构建工具，提供快速的开发和构建体验。
