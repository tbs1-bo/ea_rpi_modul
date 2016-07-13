ea_rpi_modul
============

Bei dem Projekt handelt es sich um eine Python Bibliothek für ein E/A-Modul (Eingabe-Ausgabe-Modul) für den Raspberry Pi.

Klasse EAModul
==============

![Klassendiagramm (automatisch generiert mit pyreverse)](./klassendiagramm.png)

Mit Hilfe der Klasse `EAModul` können die Taster und LED einfach angesteuert bzw. ausgelesen werden. 

    ea = EAModul(1,2,3,4,5)    #1
    ea.schalte_led(0, True)    #2
    ea.schalte_led(0, False)   #3
    
    if ea.taster_gedrueckt(0): #4
        print("Taster 0 gedrückt")
        
    ea.cleanup()               #5



**#1** Bei der Initialisierung müssen die auf dem RaspberryPi verwendeten PINs angegeben werden: zuerst die beiden Pins für die Taster, es folgen drei Pins für die LED.

**#2 und #3** Die Led sind durchnummeriert (beginnend bei 0) und können ein oder ausgeschaltet werden. Hier wird die LED mit der Nummer 0 erst ein- und dann wieder ausgeschaltet.

**#4** Der Zustand des Tasters mit der Nummer 0 wird abgefragt. Die Taster sind nummeriert (beginnend bei 0).

**#5** Mit der Methode `cleanup()` werden die Pins des Pi wieder auf den Ausgangszustand zurückgesetzt.


Verwendung ohne Raspberry Pi
============================

Die Bibliothek ist für die Verwendung mit dem Raspberry Pi konzipiert. Wenn jedoch kein Pi angeschlossen ist, wird eine Bibliothek mit Dummyfunktionen geladen. Diese gibt für die Eingänge (Taster) zufällige Werte zurück. Bei Ausgaben (LED) auf den Ausgängen erfolgt eine Textausgabe auf der Konsole.