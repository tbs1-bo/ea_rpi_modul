import socketserver
from eapi.eapi import EAModul

class EAModulUDPHandler(socketserver.BaseRequestHandler):
    """Ein Handler für UDP request an den EAModulServer.

    Ein an den Server gesendeter Request besteht aus einem Byte. Die letzen
    drei Bit der Zahl (0 oder 1), werden als Werte für die rote, gelbe oder
    grüne LED interpretiert. Die Bitsequenz xxxxx010 (x bedeutet 'beliebig')
    schaltet die rote und grüne LED aus und die gelbe LED an.

    Mit Netcat kann ein einfacher Test wie folgt aussehen:
    $ echo -en '\x02' | nc -4u localhost 9998

    Hex 2 entspricht der Bitfolge 010, mit -e wird eine Escapesequenz ohne
    Zeilvorschub (-n) verschickt. Die Optionen -4 von nc senden eine
    IPv4-Paket, das als UDP-Paket (-u) verschickt werden soll.
    """

    eamodul = EAModul()

    def handle(self):
        # Der Request besteht aus einem Tupel aus Daten und Socket des
        # Senders. Wir greifen die Daten heraus.
        #
        # Erwarte genau ein Byte im Request
        data = self.request[0]
        if len(data) != 1:
            return

        byte = int(data[0])
        print("Byte empfangen", byte)
        self.eamodul.schalte_led(EAModul.LED_ROT, byte & 1 == 1)
        self.eamodul.schalte_led(EAModul.LED_GELB, byte & 2 == 2)
        self.eamodul.schalte_led(EAModul.LED_GRUEN, byte & 4 == 4)


class EAModulServer(socketserver.UDPServer):
    """Ein UDPServer für ein EA-Modul.

    Ein an den Server gesendeter Request wird vom EAModulUDPHandler
    verarbeitet.
    """

    def __init__(self, host, port, eamodul=None):
        super().__init__((host,port), EAModulUDPHandler)

        if eamodul:
            EAModulUDPHandler.eamodul = eamodul



if __name__ == "__main__":
    easerver = EAModulServer("localhost", 9998)
    easerver.serve_forever()
