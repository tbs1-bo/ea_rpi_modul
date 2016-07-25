"""Ein Modul, das die Eingabe-Ausgabe-Module für den Raspberry Pi
netzwerkfähig macht.

Der Server kann mit folgenden Zeilen einfach gestartet werden:

  from eapi.net import EAModulServer

  easerver = EAModulServer("localhost", 9999)
  easerver.serve_forever()

Ebenso kann der Server über die Kommandozeile mit dem folgenden Befehl
gestartet werden.

  $ python3 -m eapi.net startserver

Nun wartet der Server auf dem Port 9999 auf UDP-Pakete. Ein an den Server
gesendeter Request besteht aus genau drei Bytes - für jede LED ein Byte: erst
rot, dann gelb zuletzt grün. Der Wert des Bytes gibt in Prozent (0-100) die
Helligkeit der LED an. Werte außerhalb dieses Bereiches werden ignoriert.

Mit Netcat und echo können drei Bytes einfach an einen Testserver wie folgt
gesendet werden:

  $ echo -en '\\x02\\x64\\x00' | nc -4u localhost 9999

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
from eapi.eapi import EAModul

class EAModulUDPHandler(socketserver.BaseRequestHandler):
    """Ein Handler für UDP requests an den EAModulServer."""

    eamodul = EAModul()

    def handle(self):
        """Der UDP-Handler bearbeitet UDP-Requests gemäß der Modulbeschreibung 
        (s.o.)."""

        # Der Request besteht aus einem Tupel aus Daten und Socket des
        # Senders. Wir greifen die Daten heraus.
        data = self.request[0]

        # Erwarte mindestens drei Bytes im Request
        # Für jede LED ein Byte (rot, gelb, grün)
        if len(data) < 3:
            return

        #print("Bytes empfangen:", data)
        if 0 <= data[0] <= 100:
            self.eamodul.schalte_led(EAModul.LED_ROT, data[0]/100)
        if 0 <= data[1] <= 100:
            self.eamodul.schalte_led(EAModul.LED_GELB, data[1]/100)
        if 0 <= data[2] <= 100:
            self.eamodul.schalte_led(EAModul.LED_GRUEN, data[2]/100)


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

class EAModulClient:
    """Client, um von der Konsole aus auf den EAModulServer zuzugreifen."""

    def __init__(self, servername, serverport):
        """Starte den Client für einen laufenden Server.

        Der angegebene servername ist eine IP-Adresse oder ein Domainname -
        für ein lokal laufenden Server kann auch localhost verwendet
        werden. Mit serverport wird die Portnummer angegeben, über die der
        Server ansprechbar ist.
        """
        self.servername = servername
        self.serverport = serverport
        self.client = socket.socket(socket.AF_INET, # Address Family Internet
                                    socket.SOCK_DGRAM) # UDP

    def sende(self, rot_an, gelb_an, gruen_an):
        """Sende an den Server die Information, welche LEDs an- bzw. 
        ausgeschaltet werden sollen."""
        
        data = [0,0,0]
        if gruen_an:
            data[0] = 100
        if gelb_an:
            data[1] = 100
        if rot_an:
            data[2] = 100

        #print("Sende bytes", data)
        self.client.sendto(bytes(data), (self.servername, self.serverport))


# Main
#
if __name__ == "__main__":
    import sys
    import re

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

            print("Welche LEDs sollen angeschaltet werden?")
            print("(0=aus, 1=an, erst rot, dann gelb, dann grün)")
            print("Beispiel: 010 schaltet gelb an und rot und grün aus.")
            print("'q' beendet das Programm")

            while True:
                __eingabe = input()
                if re.match("^[01]{3}$", __eingabe): # Eingabe besteht aus drei 0 oder 1
                    __rot_an = __eingabe[0] == "1"
                    __gelb_an = __eingabe[1] == "1"
                    __gruen_an = __eingabe[2] == "1"
                    __client.sende(__rot_an, __gelb_an, __gruen_an)
                elif __eingabe == 'q':
                    exit(0)
                else:
                    print("Eingabe fehlerhaft. Erwarte genau drei Zeichen, nur 0 oder 1.")
                    print("Bitte wiederholen!")
    else:
        print("Befehl angeben: startserver oder startclient")
