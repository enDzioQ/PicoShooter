class Config:
    """Klasa do obsługi konfiguracji."""

    def __init__(self, filename='config.txt'):
        self.filename = filename
        self.config = {}

    def load(self):
        """Odczytaj konfigurację z pliku."""
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line:
                        key, value = line.split('=', 1)
                        self.config[key.strip()] = value.strip()
            return self.config
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku {self.filename}")
            return None