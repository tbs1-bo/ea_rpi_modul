# -*- coding: utf-8 -*-

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
werden ignoriert. Die letzen sechs Bit (0 oder 1) des gesendeten Bytes, werden
als Werte für die rote, gelbe und grüne LED interpretiert:

  ? ? 0 0 1 1 1 0
      ^   ^   ^
      |   |   |
      |   |   grün
      |   gelb
      rot

Für jede Farbe werden zwei Bit verwendet. Das erste Bit besagt, ob die
entsprechende LED geschaltet werden soll (1) oder nicht (0). Wenn die LED
geschalet werden soll, beschreibt das zweite Bit den Zustand, in den die LED
geschaltet werden soll: an (1) oder aus (0). Wenn die LED nicht geschaltet
werden soll, ist der Wert beliebig.

Die Bitsequenz ?? 0? 11 10 (? bedeutet 'beliebig') belässt die rote LED in
ihrem bisherigen Zustand, schaltet die gelbe LED an und die grüne LED aus.

Mit Netcat und echo kann ein Byte einfach an einen Testserver wie folgt
gesendet werden:

  $ echo -en '\\xE' | nc -4u localhost 9999

Der Hexwert E entspricht dem Binärwert 00001110. Mit der Option -e wird eine
Escapesequenz verschickt, die Option -n besagt, dass kein Zeilenumbruch
gesendet werden soll - also nur die angegebenen Bytes. Die Option -4 von nc
sendet ein IPv4-Paket, das als UDP-Paket (-u) verschickt werden soll.

Das Modul enthält einen einfachen Konsolenclient, der über die Konsole
gestartet werden kann:

  $ python3 -m eapi.net startclient

Mit dem Python-Modul socket kann ein Packet in Python selbst erstellt und an
den Server gesendet werden.

>>> import socket
>>> client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
>>> daten = bytes([0xe])

Die zu sendenen Daten bestehen aus nur einem Byte.

>>> client.sendto(daten, ("localhost", 9999))
1


"""

# TODO Modul sendet an MQTT-Broker: https://www.dinotools.de/2015/04/12/mqtt-mit-python-nutzen/

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
        print("request erhalten!", self.request)

        # statisches Modul initaisieren, falls noch nicht geschehen
        if EAModulUDPHandler.eamodul is None:
            EAModulUDPHandler.eamodul = EAModul()

        # Der Request besteht aus einem Tupel aus Daten und Socket des
        # Senders. Wir greifen die Daten heraus.
        data = self.request[0]

        # Erwarte mindestens ein Byte im Request
        if len(data) < 1:
            return

        # ?? ?? ??
        # ro ge gr
        # 31 84 21
        # 26
        #
        byte = int(data[0])
        if byte & 32 == 32:
            EAModulUDPHandler.eamodul.schalte_led(EAModul.LED_ROT,
                                                  byte & 16 == 16)
        if byte & 8 == 8:
            EAModulUDPHandler.eamodul.schalte_led(EAModul.LED_GELB,
                                                  byte & 4 == 4)
        if byte & 2 == 2:
            EAModulUDPHandler.eamodul.schalte_led(EAModul.LED_GRUEN,
                                                  byte & 1 == 1)


class EAModulServer(socketserver.UDPServer):
    """Ein UDPServer für ein EA-Modul.

    Er lässt sich unter Angabe von hostname und Portnummer erzeugen.

    >>> easerver = EAModulServer("localhost", 9999)

    Anschließend kann er mit dem folgenden Aufruf gestartet werden

      easerver.serve_forever()
    
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

    Nun kann er mit dem Server kommunizieren und die dortigen LEDs ansteuern.

    >>> client.sende(rot=1, gelb=0, gruen=1)
    >>> client.sende(rot=0, gelb=0, gruen=1)

    Die Methoden lassen sich auch kürzer aufrufen.

    >>> client.sende(1, 0, 1)
    >>> client.sende(0, 0, 1)    

    Wenn ein Wert ungleich 0 oder 1 gesendet wird, so wird er ignoriert und die
    LED behält ihren Wert bei.

    >>> client.sende(1, 9, 1)

    schaltet die rote und grüne LED ein und belässt die gelbe LED in ihrem
    bisherigen Zustand.
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

        Werte von 0 oder 1 für rot, gelb und grün schalten die LED aus bzw. an.
        Andere Werte werden ignoriert und belassen die LED in ihrem bisherigen
        Zustand.
        """

        # ? ?  ? ?  ? ?
        # r o  g e  g r
        # 3 1  8 4  2 1
        # 2 6
        #
        byte = 0
        if gruen == 0 or gruen == 1:
            byte += 2
            if gruen:
                byte += 1
        if gelb == 0 or gelb == 1:
            byte += 8
            if gelb:
                byte += 4
        if rot == 0 or rot == 1:
            byte += 32
            if rot:
                byte += 16

        self.client.sendto(bytes([byte]), (self.servername, self.serverport))


def main():
    """Hauptprogramm, über das Client und Server gestartet werden können, wenn
    das Modul ausgeführt wird.
    """
    import sys

    if len(sys.argv) >= 2:
        hostname = input("Hostname (Enter für localhost):")
        if hostname == '':
            hostname = 'localhost'
        port = input("Port (Enter für 9999):")
        if port == '':
            port = '9999'

        if sys.argv[1] == "startserver":
            print("Starte Server auf", hostname, "auf Port", port)
            easerver = EAModulServer(hostname, int(port))
            easerver.serve_forever()

        elif sys.argv[1] == "startclient":
            print("Starte Client")
            client = EAModulClient(hostname, int(port))

            print("""
            Welche LEDs sollen angeschaltet werden? Gib drei Werte (0 oder 1)
            ein (erst rot, dann gelb, dann grün)
            Beispiel: 010 schaltet gelb an und rot und grün aus.

            Wenn Werte ungleich 0 der 1 verwendet werden, so bleibt die LED in
            ihrem bisherigen Zustand: 050 schaltet rot und grün aus und belässt
            gelb im bisherigen Zustand.

            'q' beendet das Programm""")

            while True:
                eingabe = input()
                if eingabe == 'q':
                    exit(0)

                try:
                    rot = int(eingabe[0])
                    gelb = int(eingabe[1])
                    gruen = int(eingabe[2])
                    client.sende(rot, gelb, gruen)

                except IndexError:
                    print("Eingabe fehlerhaft. Erwarte genau drei Zahlen (0 oder 1).")
                    print("Bitte wiederholen!")
                    
    else:
        print("Befehl angeben: startserver oder startclient")


# Main
#
if __name__ == "__main__":
    main()
