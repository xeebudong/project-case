// 全局逻辑
App({
  globalData: {
    cartKey: "mini_shop_cart"
  },
  onLaunch() {
    // 冷启动时同步一次购物车角标
    const store = require("./utils/store.js");
    store.updateTabBadge();
  }
});
