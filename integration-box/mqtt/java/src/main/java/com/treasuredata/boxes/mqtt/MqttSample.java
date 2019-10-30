package com.treasuredata.boxes.mqtt;

import com.treasuredata.boxes.mqtt.ssl.SSLUtils;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Collections;

public class MqttSample {

  private static JSONObject parseJSON(final String filename) throws IOException {
    InputStream stream = new FileInputStream(filename);
    BufferedReader br = new BufferedReader(new InputStreamReader(stream));
    StringBuilder builder = new StringBuilder();
    for (String line = br.readLine(); line != null; line = br.readLine()) {
        builder.append(line);
    }
    return new JSONObject(builder.toString());
  }

  public static void main(String[] args) throws Exception {
    Path currentPath = Paths.get(System.getProperty("user.dir"));
    Path filePath = Paths.get(currentPath.getParent().toString(), "config.json");
    JSONObject config = parseJSON(filePath.toString());

    String accountId = config.getString("apikey").split("/")[0];

    String uri = String.format("ssl://%s", config.getString("broker"));
    MqttClient client = new MqttClient(uri, "td-mqtt-sample");
    MqttConnectOptions connOpts = SSLUtils.loadMqttConnectOptions(
            accountId,
            config.getString("apikey"),
            config.getString("certfile"),
            config.getString("keyfile"));
    client.connect(connOpts);

    String target = String.format("%s:%s", config.getString("database"), config.getString("table"));
    String topic = "mqtt-ingest";
    int qos = 1;

    JSONObject headers = new JSONObject()
            .put("time", System.currentTimeMillis() / 1000L)
            .put("auth", config.getString("apikey"))
            .put("target", target);
    JSONObject content = new JSONObject()
            .put("id", 1)
            .put("name", "John Doe")
            .put("age", 25)
            .put("comment", "hello, world")
            .put("object", Collections.singletonMap("lang", "java"))
            .put("array", new String[] {"hello", "world"});
    JSONObject payload = new JSONObject()
            .put("headers", headers)
            .put("content", content);

    client.publish(topic, payload.toString().getBytes(), qos, false);

    Thread.sleep(10000);

    headers.put("time", System.currentTimeMillis() / 1000L);
    content.put("id", 2);
    content.put("name", "Jane Doe");
    content.put("age", 23);
    content.put("comment", "good morning");
    content.put("object", Collections.singletonMap("lang", "java"));
    content.put("array", new String[] {"good", "morning"});

    client.publish(topic, payload.toString().getBytes(), qos, false);

    Thread.sleep(10000);

    client.disconnect();
  }
}
