import { StatusBar } from "expo-status-bar";
import React from "react";
import { Button, StyleSheet, Text, View } from "react-native";

const server_url = "http://192.168.4.66:1234/";

export default function App() {
  const [enabled, setEnabled] = React.useState(null);
  React.useEffect(() => {
    fetch(server_url + "enabled/")
      .then((response) => response.json())
      .then((json) => setEnabled(json.enabled))
      .catch((error) => console.error(error));
  }, []);
  return (
    <View style={styles.container}>
      <StatusBar style="auto" />
      <Text style={[styles.text, enabled ? styles.enabled : styles.disabled]}>
        {enabled ? "Enabled" : "Disabled"}
      </Text>
      <Button
        title={enabled ? "Disable" : "Enable"}
        onPress={() => {
          if (enabled) {
            fetch(server_url + "disable/");

            fetch(server_url + "enabled/")
              .then((response) => response.json())
              .then((json) => setEnabled(json.enabled))
              .catch((error) => console.error(error));
          } else {
            fetch(server_url + "enable/");
            fetch(server_url + "enabled/")
              .then((response) => response.json())
              .then((json) => setEnabled(json.enabled))
              .catch((error) => console.error(error));
          }
        }}
      />

      <Button
        title="Reset dispenser 1"
        onPress={() => {
          fetch(server_url + "reset1/");
        }}
      />
      <Button
        title="Reset dispenser 2"
        onPress={() => {
          fetch(server_url + "reset2/");
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
  text: {
    fontSize: 50,
  },
  enabled: {
    color: "green",
  },
  disabled: {
    color: "red",
  },
});
