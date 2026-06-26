const data = require("../../utils/data.js");
const store = require("../../utils/store.js");

Page({
  data: { product: null, qty: 1 },
  onLoad(opts) {
    this.setData({ product: data.get(opts.id) });
  },
  dec() {
    this.setData({ qty: Math.max(1, this.data.qty - 1) });
  },
  inc() {
    this.setData({ qty: this.data.qty + 1 });
  },
  add() {
    store.add(this.data.product.id, this.data.qty);
    wx.showToast({ title: "已加入购物车", icon: "success" });
  },
  buyNow() {
    store.add(this.data.product.id, this.data.qty);
    wx.switchTab({ url: "/pages/cart/cart" });
  }
});
