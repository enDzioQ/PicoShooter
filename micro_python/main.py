import network
import socket
import sys

def read_config(filename='config.txt'):
    """Odczytaj konfigurację z pliku config.txt"""
    config = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
        return config
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {filename}")
        return None

def connect_wifi(ssid, password):
    """Połącz się z WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    print(f"Łączenie z WiFi: {ssid}...")
    wlan.connect(ssid, password)
    
    # Czekaj na połączenie (max 10 sekund)
    timeout = 0
    while not wlan.isconnected() and timeout < 10:
        print(".", end="")
        timeout += 1
        import time
        time.sleep(1)
    
    if wlan.isconnected():
        print("\nPołączono z WiFi!")
        print(f"IP: {wlan.ifconfig()[0]}")
        return wlan
    else:
        print("\nNie udało się połączyć z WiFi")
        return None

def send_to_server(sock, message):
    """Wyślij wiadomość na serwer"""
    try:
        sock.sendall((message + '\n').encode())
        return True
    except Exception as e:
        print(f"Błąd wysyłania: {e}")
        return False

def receive_from_server(sock):
    """Otrzymaj wiadomość z serwera"""
    try:
        data = sock.recv(2000)
        if data:
            return data.decode()
        return None
    except Exception as e:
        print(f"Błąd odbierania: {e}")
        return None

def main():
    # Odczytaj konfigurację
    config = read_config()
    if not config or 'ssid' not in config or 'password' not in config:
        print("Błąd: Nieprawidłowy plik config.txt")
        print("Wymagane pola: ssid, password, server_ip, server_port")
        return
    
    ssid = config.get('ssid')
    password = config.get('password')
    server_ip = config.get('server_ip')
    server_port = int(config.get('server_port', 5000))
    
    # Połącz się z WiFi
    wlan = connect_wifi(ssid, password)
    if not wlan:
        print("Nie mogę kontynuować bez połączenia WiFi")
        return
    
    # Połącz się z serwerem
    print(f"\nŁączenie z serwerem {server_ip}:{server_port}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect((server_ip, server_port))
        print("Połączono z serwerem!")
        
        # Otrzymaj wiadomości powitalnes
        for _ in range(3):
            response = receive_from_server(sock)
            if response:
                print(response, end="")
        
        # Główna pętla - czytanie ze wejścia i wysyłanie na serwer
        print("\nWpisz wiadomość (pusta linia aby zakończyć):")
        while True:
            try:
                message = input("> ")
                
                if not message:  # Pusta linia - zamknij połączenie
                    print("Zamykanie połączenia...")
                    break
                
                # Wyślij wiadomość
                if send_to_server(sock, message):
                    # Otrzymaj odpowiedź (echo)
                    response = receive_from_server(sock)
                    if response:
                        print(f"Serwer: {response}")
                    else:
                        print("Brak odpowiedzi z serwera")
                        break
                        
            except KeyboardInterrupt:
                print("\nPrzerwano!")
                break
            except Exception as e:
                print(f"Błąd: {e}")
                break
        
    except Exception as e:
        print(f"Błąd połączenia z serwerem: {e}")
    finally:
        sock.close()
        print("Połączenie zamknięte")

if __name__ == '__main__':
    main()
