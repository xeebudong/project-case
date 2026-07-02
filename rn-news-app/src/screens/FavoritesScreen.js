import React, { useState, useEffect } from "react";
import { View, Text, FlatList, TouchableOpacity, StyleSheet } from "react-native";
import { ARTICLES } from "../data";
import { subscribe, favIds } from "../store";

export default function FavoritesScreen({ navigation }) {
  const [ids, setIds] = useState(favIds());
  useEffect(() => subscribe(() => setIds(favIds())), []);

  const data = ARTICLES.filter((a) => ids.includes(a.id));

  if (!data.length) {
    return (
      <View style={styles.empty}>
        <Text style={styles.emptyText}>还没有收藏</Text>
      </View>
    );
  }

  return (
    <FlatList
      style={styles.wrap}
      data={data}
      keyExtractor={(item) => item.id}
      contentContainerStyle={{ padding: 16 }}
      renderItem={({ item }) => (
        <TouchableOpacity style={styles.card} onPress={() => navigation.navigate("Article", { id: item.id })}>
          <Text style={styles.title}>{item.title}</Text>
          <Text style={styles.meta}>{item.cat} · {item.source}</Text>
        </TouchableOpacity>
      )}
    />
  );
}

const styles = StyleSheet.create({
  wrap: { flex: 1, backgroundColor: "#f6f8fa" },
  card: { backgroundColor: "#fff", borderRadius: 12, padding: 16, marginBottom: 12 },
  title: { fontSize: 16, fontWeight: "500", color: "#26251f" },
  meta: { marginTop: 6, fontSize: 12, color: "#8a877d" },
  empty: { flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: "#f6f8fa" },
  emptyText: { color: "#8a877d", fontSize: 15 }
});
