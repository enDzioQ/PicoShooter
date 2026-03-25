import network
import time

class WiFi:
    """Klasa do obsługi połączenia z WiFi."""

    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def connect(self, ssid, password):
        """Połącz się z WiFi."""
        print(f"Łączenie z WiFi: {ssid}...")
        self.wlan.connect(ssid, password)

        # Czekaj na połączenie (max 10 sekund)
        timeout = 0
        while not self.wlan.isconnected() and timeout < 10:
            print(".", end="")
            timeout += 1
            time.sleep(1)

        if self.wlan.isconnected():
            print("\nPołączono z WiFi!")
            print(f"IP: {self.wlan.ifconfig()[0]}")
            return True
        else:
            print("\nNie udało się połączyć z WiFi")
            return False