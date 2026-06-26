const data = require("../../utils/data.js");
const store = require("../../utils/store.js");

Page({
  data: { products: [] },
  onLoad() {
    this.setData({ products: data.list() });
  },
  onShow() {
    store.updateTabBadge();
  },
  goDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({ url: `/pages/detail/detail?id=${id}` });
  },
  addToCart(e) {
    store.add(e.currentTarget.dataset.id, 1);
    wx.showToast({ title: "已加入购物车", icon: "success" });
  }
});
