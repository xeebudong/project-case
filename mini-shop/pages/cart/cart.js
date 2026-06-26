const store = require("../../utils/store.js");

Page({
  data: { items: [], subtotal: 0 },
  onShow() {
    this.refresh();
    store.updateTabBadge();
  },
  refresh() {
    this.setData({ items: store.items(), subtotal: store.subtotal() });
  },
  inc(e) {
    const it = this.item(e);
    store.setQty(it.id, it.qty + 1);
    this.refresh();
  },
  dec(e) {
    const it = this.item(e);
    store.setQty(it.id, it.qty - 1);
    this.refresh();
  },
  remove(e) {
    store.remove(e.currentTarget.dataset.id);
    this.refresh();
  },
  item(e) {
    const id = e.currentTarget.dataset.id;
    return this.data.items.find((x) => x.id === id);
  },
  checkout() {
    if (!this.data.items.length) return;
    wx.showModal({
      title: "确认下单",
      content: `合计 ¥${this.data.subtotal}，确认结算？`,
      success: (r) => {
        if (r.confirm) {
          store.clear();
          this.refresh();
          wx.showToast({ title: "下单成功", icon: "success" });
        }
      }
    });
  }
});
