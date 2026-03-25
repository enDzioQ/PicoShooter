import socket

class Client:
    """Klasa do obsługi połączenia z serwerem."""

    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = None

    def connect(self):
        """Połącz się z serwerem."""
        print(f"\nŁączenie z serwerem {self.server_ip}:{self.server_port}...")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.server_ip, self.server_port))
            print("Połączono z serwerem!")
            return True
        except Exception as e:
            print(f"Błąd połączenia z serwerem: {e}")
            return False

    def send(self, message):
        """Wyślij wiadomość na serwer."""
        try:
            self.sock.sendall((message + '\n').encode())
            return True
        except Exception as e:
            print(f"Błąd wysyłania: {e}")
            return False

    def receive(self):
        """Otrzymaj wiadomość z serwera."""
        try:
            data = self.sock.recv(2000)
            if data:
                return data.decode()
            return None
        except Exception as e:
            print(f"Błąd odbierania: {e}")
            return None

    def close(self):
        """Zamknij połączenie."""
        if self.sock:
            self.sock.close()
            print("Połączenie zamknięte")