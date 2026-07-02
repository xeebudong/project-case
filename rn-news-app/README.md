# rn-news-app · React Native 资讯 App

Expo + React Navigation 的三屏移动端应用：**资讯列表 → 文章详情 → 我的收藏**，
收藏用 AsyncStorage 本地持久化，跨屏与重启后保持。

## 功能

- 列表：分类筛选 + 下拉刷新
- 详情：正文阅读 + 一键收藏 / 取消收藏
- 收藏：AsyncStorage 持久化，空态提示

## 运行

```bash
npm install
npx expo start          # 用 Expo Go 扫码，或按 i / a 打开 iOS / Android 模拟器
```

## 结构

```
App.js                  导航容器（Stack + 收藏入口）
src/data.js             资讯数据（可替换为后端接口）
src/store.js            收藏状态（AsyncStorage + 订阅）
src/screens/            NewsList / Article / Favorites
```

## 接真实后端

`src/data.js` 换成 `fetch` 拉取资讯 API；收藏可同步到账号（登录 + 服务端存储）。
