"""Ein Modul, das die Eingabe-Ausgabe-Module für den Raspberry Pi
netzwerkfähig macht.

Der Server kann mit den folgenden Zeilen einfach gestartet werden:

  from eapi.net import EAModulServer

  easerver = EAModulServer("localhost", 9999)
  easerver.serve_forever()

Nun wartet der Server auf dem Port 9999 auf UDP-Pakete. Ein an den Server
gesendeter Request besteht aus genau einem Byte. Die letzen drei Bit der Zahl
(0 oder 1), werden als Werte für die rote, gelbe oder grüne LED
interpretiert. Die Bitsequenz ?????010 (? bedeutet 'beliebig') schaltet die
gelbe LED an und die rote und grüne LED aus.

Mit Netcat und echo kann ein Byte einfach an einen Testserver wie folgt
gesendet werden:

  $ echo -en '\\x02' | nc -4u localhost 9999

Hex 2 (\\x02) entspricht der Bitfolge 010. Mit der Option -e wird eine
Escapesequenz ohne Zeilenumbruch (-n) verschickt - also nur das eine Byte. Die
Option -4 von nc senden eine IPv4-Paket, das als UDP-Paket (-u) verschickt
werden soll.
"""

import socketserver
from eapi.eapi import EAModul

class EAModulUDPHandler(socketserver.BaseRequestHandler):
    """Ein Handler für UDP requests an den EAModulServer."""

    eamodul = EAModul()

    def handle(self):
        """Der UDP-Handler bearbeitet UDP-Requests gemäß der Modulbeschreibung 
        (s.o.)."""

        # Der Request besteht aus einem Tupel aus Daten und Socket des
        # Senders. Wir greifen die Daten heraus.
        #
        data = self.request[0]

        # Erwarte mindestens ein Byte im Request
        if len(data) < 1:
            return

        byte = int(data[0])
        print("Byte empfangen:", byte)
        self.eamodul.schalte_led(EAModul.LED_ROT, byte & 1 == 1)
        self.eamodul.schalte_led(EAModul.LED_GELB, byte & 2 == 2)
        self.eamodul.schalte_led(EAModul.LED_GRUEN, byte & 4 == 4)


class EAModulServer(socketserver.UDPServer):
    """Ein UDPServer für ein EA-Modul.

    Ein an den Server gesendeter Request wird vom EAModulUDPHandler
    verarbeitet.
    """

    def __init__(self, host, port, eamodul=None):
        """Starte einen Server auf dem angegebnen hostname, oder IP-Adresse - 
        lokale Server können hier auch 'localhost' als Name verwenden.

        Über den Parameter eamodul kann ein EAModul übergeben werden. Wird
        kein Modul übergeben, wird ein Standardmodul selbst erstellt.
        """

        super().__init__((host,port), EAModulUDPHandler)

        if eamodul:
            EAModulUDPHandler.eamodul = eamodul
