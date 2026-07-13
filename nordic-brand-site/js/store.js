// 购物车逻辑（localStorage 持久化）+ 共享交互
(function () {
  const CART_KEY = "aurelia_cart";
  const SHIPPING = 6; // flat rate
  const FREE_OVER = 60;

  function byId(id) {
    return (window.PRODUCTS || []).find((p) => p.id === id);
  }
  function load() {
    try { return JSON.parse(localStorage.getItem(CART_KEY)) || {}; }
    catch (e) { return {}; }
  }
  function save(cart) {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
    updateBadges();
  }
  function count() {
    return Object.values(load()).reduce((a, b) => a + b, 0);
  }
  function items() {
    const cart = load();
    return Object.keys(cart).map((id) => {
      const p = byId(id);
      return p ? { product: p, qty: cart[id], line: p.price * cart[id] } : null;
    }).filter(Boolean);
  }
  function subtotal() {
    return items().reduce((a, it) => a + it.line, 0);
  }
  function shipping() {
    const s = subtotal();
    return s === 0 || s >= FREE_OVER ? 0 : SHIPPING;
  }
  function total() { return subtotal() + shipping(); }

  function add(id, qty) {
    qty = qty || 1;
    const cart = load();
    cart[id] = (cart[id] || 0) + qty;
    save(cart);
    toast(byId(id).name + " added to cart");
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
  function clear() { save({}); }

  function money(n) { return "$" + Number(n).toFixed(0); }

  function updateBadges() {
    const c = count();
    document.querySelectorAll("[data-cart-count]").forEach((el) => {
      el.textContent = c;
    });
    document.querySelectorAll("[data-cart-label]").forEach((el) => {
      el.textContent = "Cart · " + c;
    });
  }

  let toastTimer;
  function toast(msg) {
    let el = document.querySelector(".toast");
    if (!el) {
      el = document.createElement("div");
      el.className = "toast";
      document.body.appendChild(el);
    }
    el.textContent = msg;
    el.classList.add("toast--show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove("toast--show"), 2200);
  }

  // 事件委托：任何 [data-add] 按钮点击即加购
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-add]");
    if (!btn) return;
    e.preventDefault();
    const qtyInput = document.querySelector("[data-qty-input]");
    const qty = qtyInput ? Math.max(1, parseInt(qtyInput.value, 10) || 1) : 1;
    add(btn.getAttribute("data-add"), qty);
  });

  document.addEventListener("DOMContentLoaded", updateBadges);

  window.Store = {
    byId, items, subtotal, shipping, total, add, setQty, remove, clear,
    count, money, FREE_OVER
  };
})();
