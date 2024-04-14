import configparser


class SpielKonfiguration:
    def __init__(self, dateipfad):
        self.konfiguration = None
        self.dateipfad = dateipfad
        self.hubschrauber_geschwindigkeit = None
        self.lkw_geschwindigkeit = None
        self.lade_konfiguration()

    def lade_konfiguration(self):
        self.konfiguration = configparser.ConfigParser()
        self.konfiguration.read(self.dateipfad)

        self.lkw_geschwindigkeit = float(self.konfiguration['LKW']['geschwindigkeit'])
        self.hubschrauber_geschwindigkeit = float(self.konfiguration['Hubschrauber']['geschwindigkeit'])

    def speichern(self):
        self.konfiguration.set('LKW', 'geschwindigkeit', str(self.lkw_geschwindigkeit))
        self.konfiguration.set('Hubschrauber', 'geschwindigkeit', str(self.hubschrauber_geschwindigkeit))
        with open(self.dateipfad, 'w') as konfiguration_datei:
            self.konfiguration.write(konfiguration_datei)
