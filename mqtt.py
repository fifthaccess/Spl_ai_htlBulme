import paho.mqtt.client  as mqtt 
import time 
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")


myclient = mqtt.Client()
myclient.on_connect = on_connect
myclient.connect("192.168.1.118", 1883, 60)
for i in range(3):
    myclient.publish('testTopic', payload="Hello World", qos=0, retain=False)# schickt ab pyload = message 
    print(f"send {i} to a/b")
    time.sleep(1)


myclient.loop_forever()