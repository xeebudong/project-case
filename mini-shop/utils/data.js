// 商品数据（可替换为 wx.request / 云函数）
const PRODUCTS = [
  { id: "p1", name: "无线蓝牙耳机", price: 199, tagline: "降噪 · 30h 续航", emoji: "🎧" },
  { id: "p2", name: "便携充电宝", price: 129, tagline: "20000mAh · 双向快充", emoji: "🔋" },
  { id: "p3", name: "机械键盘", price: 359, tagline: "87 键 · 热插拔", emoji: "⌨️" },
  { id: "p4", name: "智能手表", price: 499, tagline: "运动版 · 血氧监测", emoji: "⌚" },
  { id: "p5", name: "无线鼠标", price: 89, tagline: "静音 · 人体工学", emoji: "🖱️" },
  { id: "p6", name: "桌面支架", price: 69, tagline: "铝合金 · 可升降", emoji: "🧱" }
];

module.exports = {
  list: () => PRODUCTS,
  get: (id) => PRODUCTS.find((p) => p.id === id)
};
