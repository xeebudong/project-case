# nordic-brand-site · 北欧极简轻奢品牌官网

> 对应猿急送需求 **159765「企业全套官网 UI 框架定制设计（极简轻奢北欧风）」** 的可运行 Demo。

对标 COS / coslus 风格：低饱和中性色、大面积留白、建筑感排版、轻量无多余装饰。

## 特点
- 纯静态、零依赖，`index.html` + `styles.css` 直接打开即可。
- **完全响应式**：桌面 4 列 → 平板 2 列 → 手机 1 列（见 `styles.css` 媒体查询）。
- 设计系统用 CSS 变量集中管理（配色 / 圆角 / 字体 / 栅格），改主题只动 `:root`。
- 覆盖官网核心区块：导航 / Hero / 产品系列 / 品牌故事 / 订阅 CTA / 页脚，可平滑接入电商购物车与多语言。

## 预览
```bash
# 任意静态服务器
python -m http.server 5500
# 打开 http://localhost:5500
```

## 交付时的扩展
- 接入真实商品数据 + 购物车（Snipcart / Shopify Buy Button / 自建）
- i18n 多语言（默认英文，可扩展中文等）
- CMS 内容管理（Sanity / Strapi）
