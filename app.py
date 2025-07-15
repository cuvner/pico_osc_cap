import time
import board
import wifi
import socketpool
import microosc
import adafruit_mpr121


def init_wifi_status_label(display):
    # Initialize the WiFi status label with empty text
    wifi_status_label = label.Label(terminalio.FONT, text="", color=0xFFFFFF)
    display.show(wifi_status_label)
    return wifi_status_label

def update_wifi_status(display, wifi_status_label, text):
    # Update the text and adjust position for right justification
    wifi_status_label.text = text
    wifi_status_label.x = display.width - len(text) * 6  # 6 is an approximation for char width


def connect_to_wifi():
    ssid = "CodingWorkshop"
    password = "CodingWorkshop"
    try:
        wifi.radio.connect(ssid, password)
        # You can update the display within this function, if you wish
        return True
    except Exception as e:
        return False


def create_osc_client(socket_pool):
    try:
        osc_client = microosc.OSCClient(socket_pool, "224.0.0.1", 5000)
        return osc_client
    except Exception as e:
        return None      
    
def send_osc_message(osc_client, message):
    try:
        osc_client.send(message)
    except BrokenPipeError:
        # Attempt to reconnect and resend the message
        try:
            # Recreate the OSC client or reinitialize the connection
            osc_client = create_osc_client(socketpool.SocketPool(wifi.radio))
            osc_client.send(message)
        except Exception as e:
            print("Error re-establishing OSC connection:", e)

def check_wifi_connection():
    try:
        # Attempt to get the current IP address as a way to check connectivity
        ip_address = wifi.radio.ipv4_address
        return ip_address is not None
    except Exception as e:
        # Handle exceptions if WiFi module is not responding
        return False  

def reconnect_to_wifi(display):
    try:
        ssid = "CodingWorkshop"
        password = "CodingWorkshop"
        wifi.radio.connect(ssid, password)
        return True
    except Exception as e:
        # Update the display with an error message if needed
        return False
          


def main():
    # check wifi
    wifi_connected = True  # Initial assumption
    last_check_time = time.monotonic()
    check_interval = 10  # Time in seconds between checks


    # Connect to WiFi and update WiFi status label
    ip_address = connect_to_wifi()
    while !ip_address:
        print("connecting......")

    on_connection="Connected" if ip_address else "No WiFi"
    print(on_connection)

    # Setup OSC client if connected to WiFi
    osc_client = create_osc_client(socketpool.SocketPool(wifi.radio)) if ip_address else None

    # Touch Pad Setup
    touch_pad = adafruit_mpr121.MPR121(board.STEMMA_I2C())
    last_touch_time = None
    last_wifi_check = time.monotonic()
    wifi_check_interval = 5  # Time in seconds to check WiFi status

    while True:

        current_time = time.monotonic()

        # Periodically check WiFi status
        if current_time - last_wifi_check > wifi_check_interval:
            wifi_connected = check_wifi_connection()
            if not wifi_connected:
                wifi_connected = reconnect_to_wifi(display)
            wifi_status_label = "W-Osc" if wifi_connected else "No WiFi"
            print(wifi_status_label)
            last_wifi_check = current_time
            
        # Touch pad detection logic
        touch_detected = False
        for i in range(12):
            if touch_pad[i].value:
                touch_detected = True
                print( f'Touched pad #{i + 1}!')
  
                if osc_client and touch_detected:
                    osc_message = microosc.OscMsg("/touch", [i], ("i",))
                    send_osc_message(osc_client, osc_message)

                last_touch_time = time.monotonic()
                break

        if not touch_detected and last_touch_time and (time.monotonic() - last_touch_time > 5):
            print( "Touch a pad!")
            last_touch_time = None


        time.sleep(0.2)

if __name__ == "__main__":
    main()