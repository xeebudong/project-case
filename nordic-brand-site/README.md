# nordic-brand-site · 北欧极简轻奢品牌官网 + 电商

品牌 **AURELIA**（北欧个护）。对标 COS / coslus 风格：低饱和中性色、大面积留白、
建筑感排版、轻量无多余装饰。一套**可完整走通购物流程**的纯静态电商站。

## 功能

- **首页**：Hero、商品列表（数据驱动渲染）、品牌故事、订阅 CTA。
- **商品详情页** `product.html?id=`：主图、简介、成分要点、数量加减、加入购物车 / 立即购买、相关推荐。
- **购物车** `cart.html`：增删改数量、小计 / 运费（满 $60 免运）/ 合计，实时计算。
- **结算** `checkout.html`：收货 + 支付表单校验 → 下单 → 订单确认页（自动清空购物车）。
- **购物车状态**：`localStorage` 持久化，导航角标全站实时同步；加购有 toast 提示。

## 技术

- 纯静态、零依赖（无框架、无构建），原生 HTML/CSS/JS，双击或任意静态服务器即可运行。
- 设计系统用 CSS 变量集中管理（配色 / 圆角 / 字体 / 栅格），改主题只动 `:root`。
- **完全响应式**：桌面 4 列 → 平板 2 列 → 手机 1 列，购物车/详情/结算均适配移动端。
- 商品图为内联生成的 SVG，无外部图片依赖。

## 结构

```
index.html         首页 + 商品列表
product.html       商品详情
cart.html          购物车
checkout.html      结算 + 下单确认
js/data.js         商品目录（可替换为后端 API / CMS）
js/store.js        购物车逻辑（localStorage）
img/*.svg          商品图
styles.css         设计系统与全部样式
```

## 预览

```bash
python -m http.server 5500   # 打开 http://localhost:5500
```

## 扩展方向

- 商品数据接后端 / CMS（Sanity / Strapi），`js/data.js` 换成 API 拉取
- 接真实支付（Stripe / Shopify Buy Button）与库存、订单系统
- i18n 多语言（默认英文，可扩展中文等）
