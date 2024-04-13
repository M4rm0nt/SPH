import configparser


class SpielKonfiguration:
    def __init__(self, dateipfad):
        self.config = None
        self.dateipfad = dateipfad
        self.hubschrauber_geschwindigkeit = None
        self.lkw_geschwindigkeit = None
        self.lade_konfiguration()

    def lade_konfiguration(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.dateipfad)

        self.lkw_geschwindigkeit = float(self.config['LKW']['geschwindigkeit'])
        self.hubschrauber_geschwindigkeit = float(self.config['Hubschrauber']['geschwindigkeit'])

    def speichern(self):
        self.config.set('LKW', 'geschwindigkeit', str(self.lkw_geschwindigkeit))
        self.config.set('Hubschrauber', 'geschwindigkeit', str(self.hubschrauber_geschwindigkeit))
        with open(self.dateipfad, 'w') as configdatei:
            self.config.write(configdatei)
