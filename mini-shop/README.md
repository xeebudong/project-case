# mini-shop · 极简商城微信小程序

原生微信小程序（无第三方框架）。三页闭环：**商品列表 → 商品详情 → 购物车**，
全局购物车状态 + 本地缓存持久化，导航 TabBar 角标实时更新。

## 页面

- `pages/index`：商品列表，点进详情
- `pages/detail`：商品详情，数量加减 + 加入购物车
- `pages/cart`：购物车，改数量 / 删除 / 结算，实时小计

## 运行

1. 用[微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)导入本目录
2. AppID 选「测试号」即可预览
3. 编译后在模拟器里走一遍下单流程

## 结构

```
app.js / app.json / app.wxss     全局逻辑 / 路由与 TabBar / 全局样式
utils/store.js                   购物车逻辑（wx.storage 持久化）
utils/data.js                    商品数据（可替换为云函数 / 后端接口）
pages/index|detail|cart          三个页面（wxml/wxss/js/json）
```

## 接真实后端

`utils/data.js` 换成 `wx.request` 拉取商品；下单接微信支付（`wx.requestPayment`）与自建订单服务即可。
