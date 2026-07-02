import React, { useEffect } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { Text, TouchableOpacity } from "react-native";

import NewsListScreen from "./src/screens/NewsListScreen";
import ArticleScreen from "./src/screens/ArticleScreen";
import FavoritesScreen from "./src/screens/FavoritesScreen";
import { init } from "./src/store";

const Stack = createNativeStackNavigator();
const GREEN = "#2e8b57";

export default function App() {
  useEffect(() => {
    init();
  }, []);

  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerStyle: { backgroundColor: GREEN },
          headerTintColor: "#fff",
          headerTitleStyle: { fontWeight: "600" }
        }}
      >
        <Stack.Screen
          name="News"
          component={NewsListScreen}
          options={({ navigation }) => ({
            title: "资讯",
            headerRight: () => (
              <TouchableOpacity onPress={() => navigation.navigate("Favorites")}>
                <Text style={{ color: "#fff", fontSize: 16 }}>收藏</Text>
              </TouchableOpacity>
            )
          })}
        />
        <Stack.Screen name="Article" component={ArticleScreen} options={{ title: "详情" }} />
        <Stack.Screen name="Favorites" component={FavoritesScreen} options={{ title: "我的收藏" }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
