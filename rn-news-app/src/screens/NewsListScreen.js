import React, { useState } from "react";
import { View, Text, FlatList, TouchableOpacity, StyleSheet, ScrollView } from "react-native";
import { ARTICLES, CATEGORIES } from "../data";

export default function NewsListScreen({ navigation }) {
  const [cat, setCat] = useState("全部");
  const data = cat === "全部" ? ARTICLES : ARTICLES.filter((a) => a.cat === cat);

  return (
    <View style={styles.wrap}>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.tabs}>
        {CATEGORIES.map((c) => (
          <TouchableOpacity key={c} onPress={() => setCat(c)} style={[styles.tab, cat === c && styles.tabOn]}>
            <Text style={[styles.tabText, cat === c && styles.tabTextOn]}>{c}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <FlatList
        data={data}
        keyExtractor={(item) => item.id}
        contentContainerStyle={{ padding: 16 }}
        renderItem={({ item }) => (
          <TouchableOpacity style={styles.card} onPress={() => navigation.navigate("Article", { id: item.id })}>
            <Text style={styles.title}>{item.title}</Text>
            <Text style={styles.meta}>{item.cat} · {item.source} · {item.time}</Text>
          </TouchableOpacity>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { flex: 1, backgroundColor: "#f6f8fa" },
  tabs: { flexGrow: 0, paddingHorizontal: 12, paddingVertical: 10 },
  tab: { paddingHorizontal: 16, paddingVertical: 8, borderRadius: 999, marginRight: 8, backgroundColor: "#fff", borderWidth: 1, borderColor: "#e6e2da" },
  tabOn: { backgroundColor: "#2e8b57", borderColor: "#2e8b57" },
  tabText: { color: "#26251f", fontSize: 14 },
  tabTextOn: { color: "#fff" },
  card: { backgroundColor: "#fff", borderRadius: 12, padding: 16, marginBottom: 12 },
  title: { fontSize: 16, fontWeight: "500", color: "#26251f" },
  meta: { marginTop: 6, fontSize: 12, color: "#8a877d" }
});
