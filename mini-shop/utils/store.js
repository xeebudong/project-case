// 购物车逻辑（wx.storage 持久化）
const KEY = "mini_shop_cart";
const data = require("./data.js");

function load() {
  return wx.getStorageSync(KEY) || {};
}
function save(cart) {
  wx.setStorageSync(KEY, cart);
  updateTabBadge();
}
function add(id, qty = 1) {
  const cart = load();
  cart[id] = (cart[id] || 0) + qty;
  save(cart);
}
function setQty(id, qty) {
  const cart = load();
  if (qty <= 0) delete cart[id];
  else cart[id] = qty;
  save(cart);
}
function remove(id) {
  const cart = load();
  delete cart[id];
  save(cart);
}
function items() {
  const cart = load();
  return Object.keys(cart).map((id) => {
    const p = data.get(id);
    return { ...p, qty: cart[id], line: p.price * cart[id] };
  });
}
function count() {
  return Object.values(load()).reduce((a, b) => a + b, 0);
}
function subtotal() {
  return items().reduce((a, it) => a + it.line, 0);
}
function clear() {
  save({});
}
function updateTabBadge() {
  const c = count();
  if (c > 0) {
    wx.setTabBarBadge({ index: 1, text: String(c) }).catch(() => {});
  } else {
    wx.removeTabBarBadge({ index: 1 }).catch(() => {});
  }
}

module.exports = { add, setQty, remove, items, count, subtotal, clear, updateTabBadge };
