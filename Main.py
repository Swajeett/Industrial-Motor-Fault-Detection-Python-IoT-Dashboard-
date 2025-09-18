import network
import urequests
import machine
import time
from machine import Pin, SPI, I2C
import dht
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import mcp3008

# ---------- WiFi Setup ----------
SSID = "IOT PROJECT"
PASSWORD = "123123123"

# ---------- ThingSpeak ----------
API_KEY = "WFDF8EGNJAGC2842R"
SERVER = "http://api.thingspeak.com/update"

# ---------- MCP3008 SPI ----------
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
cs = Pin(17, Pin.OUT)
adc = mcp3008.MCP3008(spi, cs)

CT_CHANNEL = 0
PT_CHANNEL = 1
SWITCH1_CHANNEL = 3
SWITCH2_CHANNEL = 4
SWITCH3_CHANNEL = 5
SWITCH4_CHANNEL = 6

# ---------- DHT11 ----------
dht_sensor = dht.DHT11(Pin(15))

# ---------- Relay ----------
relay = Pin(4, Pin.OUT)

# ---------- Thresholds ----------
CT_SET = 5.0
PT_SET = 220.0
TEMP_SET = 30.0

# ---------- LCD Setup ----------
I2C_ADDR = 0x27
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# ---------- WiFi Connect ----------
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print("WiFi connected:", wlan.ifconfig())

connect_wifi()

lcd.putstr("IND MOTOR FLT")

while True:
    # --- Sensor Readings ---
    ct_value = (adc.read(CT_CHANNEL) / 2.0) * 20.0
    pt_value = (adc.read(PT_CHANNEL) / 2.0) * 50.0

    dht_sensor.measure()
    temp_value = dht_sensor.temperature()

    print("CT:", ct_value, "A, PT:", pt_value, "V, Temp:", temp_value, "C")

    # --- Relay Control ---
    if ct_value > CT_SET or pt_value > PT_SET or temp_value > TEMP_SET:
        relay.value(1)
        relay_status = "ON"
    else:
        relay.value(0)
        relay_status = "OFF"

    # --- LCD Display ---
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("CT:{:.1f}A PT:{:.1f}V".format(ct_value, pt_value))
    lcd.move_to(0, 1)
    lcd.putstr("T:{:.1f}C {}".format(temp_value, relay_status))

    # --- Send to ThingSpeak ---
    try:
        url = "{}?api_key={}&field1={}&field2={}&field3={}".format(
            SERVER, API_KEY, ct_value, pt_value, temp_value
        )
        response = urequests.get(url)
        response.close()
        print("Data sent to ThingSpeak")
    except:
        print("Error sending data")

    time.sleep(2)
