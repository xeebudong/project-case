// 收藏状态：AsyncStorage 持久化 + 简单订阅
import AsyncStorage from "@react-native-async-storage/async-storage";

const KEY = "rn_news_favorites";
let favorites = {}; // { [id]: true }
const listeners = new Set();

export async function init() {
  try {
    const raw = await AsyncStorage.getItem(KEY);
    favorites = raw ? JSON.parse(raw) : {};
  } catch (e) {
    favorites = {};
  }
  emit();
}

async function persist() {
  await AsyncStorage.setItem(KEY, JSON.stringify(favorites));
  emit();
}

function emit() {
  listeners.forEach((fn) => fn(favorites));
}

export function subscribe(fn) {
  listeners.add(fn);
  fn(favorites);
  return () => listeners.delete(fn);
}

export function isFav(id) {
  return !!favorites[id];
}

export function toggle(id) {
  if (favorites[id]) delete favorites[id];
  else favorites[id] = true;
  persist();
}

export function favIds() {
  return Object.keys(favorites);
}
