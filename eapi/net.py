"""Ein Modul, das die Eingabe-Ausgabe-Module für den Raspberry Pi
netzwerkfähig macht.

Der Server kann mit folgenden Zeilen einfach erstellt werden:

>>> from eapi.net import EAModulServer
>>> easerver = EAModulServer("localhost", 9999)

Anschließend wird er mit einem Aufruf gestartet.

  easerver.serve_forever()

Ebenso kann der Server über die Kommandozeile mit dem folgenden Befehl
gestartet werden.

  $ python3 -m eapi.net startserver

Nun wartet der Server auf dem Port 9999 auf UDP-Pakete. Ein an den Server
gesendeter Request besteht aus genau einem Byte - weitere gesendete Bytes
werden ignoriert. Die letzen drei Bit (0 oder 1) des gesendeten Bytes, werden
als Werte für die rote, gelbe und grüne LED interpretiert:

  ? ? ? ? ? 0 1 0
            ^ ^ ^
            | | |
            | | grün
            | gelb
            rot

Die Bitsequenz ?????010 (? bedeutet 'beliebig') schaltet die gelbe LED an und
die rote und grüne LED aus.

Mit Netcat und echo kann ein Byte einfach an einen Testserver wie folgt
gesendet werden:

  $ echo -en '\\x02' | nc -4u localhost 9999

Hex 2 (\\x02) entspricht dem Hexwert 2. Mit der Option -e wird eine
Escapesequenz verschickt, die Option -n besagt, dass kein Zeilenumbruch
gesendet werden soll - also nur die angegebenen Bytes. Die Option -4 von nc
sendet ein IPv4-Paket, das als UDP-Paket (-u) verschickt werden soll.

Das Modul enthält auch einen einfachen Konsolenclient, der über die Konsole
gestartet werden kann:

  $ python3 -m eapi.net startclient

"""

import socket
import socketserver
from eapi.hw import EAModul


class EAModulUDPHandler(socketserver.BaseRequestHandler):
    """Ein Handler für UDP requests an den EAModulServer."""

    # eamodul als Klassenattribut, da für jeden Request auf den Server
    # eine neue Handlerinstanz erzeugt wird.
    eamodul = None

    def handle(self):
        """Der UDP-Handler bearbeitet UDP-Requests gemäß der Modulbeschreibung 
        (s.o.)."""

        # statisches Modul initaisieren, falls noch nicht geschehen
        if EAModulUDPHandler.eamodul is None:
            EAModulUDPHandler.eamodul = EAModul()

        # Der Request besteht aus einem Tupel aus Daten und Socket des
        # Senders. Wir greifen die Daten heraus.
        data = self.request[0]

        # Erwarte mindestens ein Byte im Request
        if len(data) < 1:
            return

        byte = int(data[0])
        EAModulUDPHandler.eamodul.schalte_led(EAModul.LED_ROT, byte & 1 == 1)
        EAModulUDPHandler.eamodul.schalte_led(EAModul.LED_GELB, byte & 2 == 2)
        EAModulUDPHandler.eamodul.schalte_led(EAModul.LED_GRUEN, byte & 4 == 4)


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

        super().__init__((host, port), EAModulUDPHandler)

        if eamodul:
            EAModulUDPHandler.eamodul = eamodul


class EAModulClient:
    """Client, um auf den EAModulServer zuzugreifen.

    Der Client kann mit der Angabe eines Hostnamens oder einer IP-Adresse
    gestartet werden.

    >>> from eapi.net import EAModulClient
    >>> client = EAModulClient('localhost', 9999)

    Nun kann er über mit dem Server kommunizieren und die dortigen LEDs
    ansteuern.

    >>> client.sende(1, 0, 1)
    >>> client.sende(0, 0, 1)
    """

    def __init__(self, servername, serverport):
        """Starte den Client für einen laufenden Server.

        Der angegebene servername ist eine IP-Adresse oder ein Domainname -
        für ein lokal laufenden Server kann auch localhost verwendet
        werden. Mit serverport wird die Portnummer angegeben, über die der
        Server ansprechbar ist.
        """
        self.servername = servername
        self.serverport = serverport
        self.client = socket.socket(socket.AF_INET,     # Address Family Internet
                                    socket.SOCK_DGRAM)  # UDP

    def sende(self, rot, gelb, gruen):
        """Sende an den Server die Information, welche LEDs an- bzw. 
        ausgeschaltet werden sollen.

        Die Werte für rot, gelb und grün müssen 0 oder 1 sein.
        """

        byte = 0
        if gruen:
            byte += 1
        if gelb:
            byte += 2
        if rot:
            byte += 4

        self.client.sendto(bytes([byte]), (self.servername, self.serverport))


# Main
#
if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 2:
        __hostname = input("Hostname (Enter für localhost):")
        if __hostname == '':
            __hostname = 'localhost'
        __port = input("Port (Enter für 9999):")
        if __port == '':
            __port = '9999'

        if sys.argv[1] == "startserver":
            print("Starte Server auf", __hostname, "auf Port", __port)
            __easerver = EAModulServer(__hostname, int(__port))
            __easerver.serve_forever()

        elif sys.argv[1] == "startclient":
            print("Starte Client")
            __client = EAModulClient(__hostname, int(__port))

            print("""
            Welche LEDs sollen angeschaltet werden? Gib drei Werte (0 oder 1)
            ein (erst rot, dann gelb, dann grün)
            Beispiel: 010 schaltet gelb an und rot und grün aus.
            'q' beendet das Programm""")

            while True:
                __eingabe = input()                    
                if __eingabe == 'q':
                    exit(0)

                try:
                    __rot = int(__eingabe[0])
                    __gelb = int(__eingabe[1])
                    __gruen = int(__eingabe[2])
                    __client.sende(__rot, __gelb, __gruen)

                except IndexError:
                    print("Eingabe fehlerhaft. Erwarte genau drei Zahlen (0 oder 1).")
                    print("Bitte wiederholen!")
                    
    else:
        print("Befehl angeben: startserver oder startclient")
