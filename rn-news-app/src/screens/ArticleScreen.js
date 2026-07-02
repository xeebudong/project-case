import React, { useState, useEffect } from "react";
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from "react-native";
import { ARTICLES } from "../data";
import { isFav, toggle, subscribe } from "../store";

export default function ArticleScreen({ route }) {
  const { id } = route.params;
  const article = ARTICLES.find((a) => a.id === id);
  const [fav, setFav] = useState(isFav(id));

  useEffect(() => subscribe(() => setFav(isFav(id))), [id]);

  if (!article) return null;

  return (
    <ScrollView style={styles.wrap} contentContainerStyle={{ padding: 20 }}>
      <Text style={styles.cat}>{article.cat}</Text>
      <Text style={styles.title}>{article.title}</Text>
      <Text style={styles.meta}>{article.source} · {article.time}</Text>
      <Text style={styles.body}>{article.body}</Text>

      <TouchableOpacity style={[styles.fav, fav && styles.favOn]} onPress={() => toggle(id)}>
        <Text style={[styles.favText, fav && styles.favTextOn]}>
          {fav ? "★ 已收藏" : "☆ 收藏"}
        </Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  wrap: { flex: 1, backgroundColor: "#fff" },
  cat: { color: "#2e8b57", fontSize: 13, letterSpacing: 1 },
  title: { fontSize: 24, fontWeight: "600", color: "#26251f", marginTop: 8 },
  meta: { color: "#8a877d", fontSize: 13, marginTop: 8 },
  body: { fontSize: 16, lineHeight: 26, color: "#3a382f", marginTop: 20 },
  fav: { marginTop: 30, borderWidth: 1, borderColor: "#2e8b57", borderRadius: 999, paddingVertical: 12, alignItems: "center" },
  favOn: { backgroundColor: "#2e8b57" },
  favText: { color: "#2e8b57", fontSize: 15 },
  favTextOn: { color: "#fff" }
});
