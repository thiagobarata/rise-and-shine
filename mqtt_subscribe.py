import paho.mqtt.client as mqtt
import alarm_sound

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("delgado/state")
    
    client.message_callback_add("delgado/state", on_message_from_state)

def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

def on_message_from_state(client, userdata, message):
   print("Custom callback  - State Message: " + message.payload.decode())

   if message.payload.decode() == "asleep":
      print("User is asleep. Playing alarm.")
      alarm_sound.play_sound('mixkit-morning-clock-alarm-1003.wav')
    
   if message.payload.decode() == "awake":
      print("User is awake. Disabling alarm.")
      alarm_sound.stop_sound()


if __name__ == '__main__':
    
    client = mqtt.Client()
    
    client.on_message = on_message
    
    client.on_connect = on_connect

    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)

    client.loop_forever()