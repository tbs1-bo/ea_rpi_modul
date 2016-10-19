# -*- coding: utf-8 -*-

"""Visualisierungen für die LEDs des EAModuls.

Dieses Paket stellt verschiedene Visualisierungen für die LEDs auf dem EAModul
zur Verfügung gestellt.

Die Klasse EAModulGui visualisiert das EAModul in einem Fenster, die Klasse
EAModulCLI visualisiert es in der Konsole.

Damit die Visualisierer zum Einsatz kommen können, wird ein EAModul benötigt,
dessen LEDs sie darstellen sollen. Daher erstellt man zunächst ein übliches
EAModul.

>>> from eapi.gui import EAModulGui
>>> from eapi.hw import EAModul

>>> ea = EAModul()

Nun kann z.B. eine GUI für das EA-Modul erstellt werden. Der Aufruf ist
blockierend und zeigt ein Fenster mit drei LEDs (rot, gelb und grün) an.

   gui = EAModulGui(ea)

Änderungen an den LEDs am Modul werden nun ebenfalls in der GUI dargestellt.

Als weitere Option bietet sich eine Anzeige auf der Konsole an. Hier wird das
EAModul in der Klasse EAModulCLI verpackt.

>>> ea_konsole = EAModulKonsole(ea)

Nun würde ein Schalten der LEDs nicht nur auf dem Modul, sondern auch in der
Konsole angezeigt werden.

   ea.schalte_led(EAModul.LED_ROT, 1)   
"""

from tkinter import Tk, Label, StringVar, YES, BOTH
from eapi.hw import EAModul


class EAModulVisualisierer:
    """
    Klasse, die zum Visualisieren des EAModuls dient.
    """
    def __init__(self, eamodul):
        self._ea = eamodul
        self._ea.led_event_registrieren(EAModul.LED_ROT,
                                        self._rote_led_update)
        self._ea.led_event_registrieren(EAModul.LED_GELB,
                                        self._gelbe_led_update)
        self._ea.led_event_registrieren(EAModul.LED_GRUEN,
                                        self._gruene_led_update)

    def _rote_led_update(self, neuer_wert):
        """Die Methode wird bei Änderungen der roten LED aufgerufen und muss
        von Unterklasse überschrieben werden."""
        raise NotImplementedError(
            "Muss von einer Unterklasse überschrieben werden!")

    def _gelbe_led_update(self, neuer_wert):
        """siehe _rote_led_update"""
        raise NotImplementedError(
            "Muss von einer Unterklasse überschrieben werden!")

    def _gruene_led_update(self, neuer_wert):
        """siehe _gruene_led_update"""
        raise NotImplementedError(
            "Muss von einer Unterklasse überschrieben werden!")


class EAModulGui(EAModulVisualisierer):
    """
    Eine GUI für ein EAModul mit zwei Tastern und drei LEDs.
    """

    def __init__(self, eamodul):
        """
        Erstellt eine GUI für das gegebenen EAModul.
        """
        super().__init__(eamodul)

        # gui init
        fenster = Tk()
        fenster.title("EAModul - GUI")
        fenster.geometry('300x300')

        # TODO entfernen, wenn nicht mehr gebraucht
        """
        btn_taster0 = Button(fenster, text="Taster 0",
                             command=self.__taster0_gedrueckt)
        btn_taster0.pack()

        btn_taster1 = Button(fenster, text="Taster 1",
                             command=self.__taster1_gedrueckt)
        btn_taster1.pack()
        """

        # LEDs erzeugen
        # TODO Icons statt Text verwenden
        self.var_rot = StringVar(value="0")
        self.lbl_led_rot = Label(fenster, textvariable=self.var_rot,
                                 bg='lightgrey')
        self.lbl_led_rot.pack(expand=YES, fill=BOTH)

        self.var_gelb = StringVar(value="0")
        self.lbl_led_gelb = Label(fenster, textvariable=self.var_gelb,
                                  bg='lightgrey')
        self.lbl_led_gelb.pack(expand=YES, fill=BOTH)

        self.var_gruen = StringVar(value="0")
        self.lbl_led_gruen = Label(fenster, textvariable=self.var_gruen,
                                   bg='lightgrey')
        self.lbl_led_gruen.pack(expand=YES, fill=BOTH)

        fenster.mainloop()

    def __taster0_gedrueckt(self):
        self._ea.schalte_led(EAModul.LED_ROT, True)

    def __taster1_gedrueckt(self):
        self._ea.schalte_led(EAModul.LED_ROT, False)

    def __farbe_fuer_ledwert(self, led_wert, default_wert):
        """Bestimmt für den led_wert eine Farbe.

        Wenn der LED-Wert 1 ist, wird der default_wert zurückgegeben, sonst wird
        lightgrey als Farbe verwendet."""

        if led_wert == 1:
            return default_wert
        else:
            return "lightgrey"

    def _rote_led_update(self, neuer_wert):
        self.var_rot.set(neuer_wert)
        self.lbl_led_rot.configure(bg=self.__farbe_fuer_ledwert(neuer_wert,
                                                                "red"))

    def _gelbe_led_update(self, neuer_wert):
        self.var_gelb.set(neuer_wert)
        self.lbl_led_gelb.configure(bg=self.__farbe_fuer_ledwert(neuer_wert,
                                                                 "yellow"))

    def _gruene_led_update(self, neuer_wert):
        self.var_gruen.set(neuer_wert)
        self.lbl_led_gruen.configure(bg=self.__farbe_fuer_ledwert(neuer_wert,
                                                                  "green"))


class EAModulKonsole(EAModulVisualisierer):
    """Eine Klasse, die die LEDs eines EAModul in der Konsole visualisiert.

    >>> ea = EAModul()
    >>> ea_konsole = EAModulKonsole(ea)

    Wenn nun die LEDs geschaltet werden, wird dies durch eine bunte
    Visualisierung auf der Konsole angezeigt.
    """

    # nach http://ascii-table.com/ansi-escape-sequences.php
    ANSI_BG_BLACK = "\033[40m"
    ANSI_BG_RED = "\033[41m"
    ANSI_BG_GREEN = "\033[42m"
    ANSI_BG_YELLOW = "\033[43m"
    ANSI_FG_BLACK = "\033[30m"
    ANSI_FG_WHITE = "\033[37m"

    ANSI_ALL_ATTRIBUTES_OFF = "\033[0m"
    ANSI_ERASE_DISPLAY = "\033[2J"
    ANSI_CURSOR_HOME = "\033[;H"
    ANSI_BOLD = "\033[1m"
    ANSI_SAVE_CURSOR = "\033[s"
    ANSI_RESTORE_CURSOR = "\033[u"

    def __init__(self, eamodul):
        super().__init__(eamodul)

        self.__leds = [0, 0, 0]

    def _rote_led_update(self, neuer_wert):
        self.__leds[0] = neuer_wert
        self.__print_leds()

    def _gelbe_led_update(self, neuer_wert):
        self.__leds[1] = neuer_wert
        self.__print_leds()

    def _gruene_led_update(self, neuer_wert):
        self.__leds[2] = neuer_wert
        self.__print_leds()

    def __print_leds(self):
        farbnamen = [" rot  ", " gelb ", " grün "]
        ansifarben = [self.ANSI_BG_RED, self.ANSI_BG_YELLOW, self.ANSI_BG_GREEN]

        s = self.ANSI_ERASE_DISPLAY + self.ANSI_CURSOR_HOME + \
            "LEDs: " + self.ANSI_BOLD + self.ANSI_FG_WHITE

        for i in range(len(self.__leds)):

            if self.__leds[i] == 1:
                s += ansifarben[i]
            else:
                s += self.ANSI_BG_BLACK

            s += farbnamen[i]

        s += self.ANSI_ALL_ATTRIBUTES_OFF

        print(s)


__eamodul = None
def __eamodul_erzeugen():
    """Hilfsmethode, die ein EAModul erstellt, wenn noch keines vorhanden ist.
    """
    global __eamodul

    if __eamodul is None:
        __eamodul = EAModul()

    return __eamodul


def demo_cli():
    """
    Über den Taster 0 an dem Modul kann die gelbe LED gleichzeitig auf dem
    Board und in der Konsole geschaltet werden. Mit dem Taster 1 kann die rote
    LED auf die gleichte Weise gesteuert werden.
    """
    import time
    input(str(demo_taster.__doc__) + "\n(Enter für Start)")

    def taster0_gedrueckt(_):
        ea = __eamodul_erzeugen()
        ea.schalte_led(EAModul.LED_GELB, ea.taster_gedrueckt(0))

    def taster1_gedrueckt(_):
        ea = __eamodul_erzeugen()
        ea.schalte_led(EAModul.LED_ROT, ea.taster_gedrueckt(1))

    ea = __eamodul_erzeugen()
    ea.taster_event_registrieren(0, taster0_gedrueckt)
    ea.taster_event_registrieren(1, taster1_gedrueckt)

    EAModulKonsole(ea)

    try:
        while True:
            time.sleep(0.2)

    except KeyboardInterrupt:
        ea.cleanup()


def demo_cli_blinken():
    """
    Das Demo lässt die LEDs kurz blinken und visualisiert dies zusätzlich auf
    der Konsole.
    """
    import time

    input(str(demo_cli_blinken.__doc__) + "\n(Enter)")
    ea = EAModul()
    EAModulKonsole(ea)

    ea.schalte_led(EAModul.LED_ROT, 1)
    time.sleep(0.5)
    ea.schalte_led(EAModul.LED_ROT, 0)
    time.sleep(0.5)
    ea.schalte_led(EAModul.LED_ROT, 1)
    time.sleep(0.5)
    ea.schalte_led(EAModul.LED_GELB, 1)
    time.sleep(0.5)
    ea.schalte_led(EAModul.LED_GELB, 0)
    time.sleep(0.5)
    ea.schalte_led(EAModul.LED_GELB, 1)
    time.sleep(0.5)
    ea.schalte_led(EAModul.LED_GRUEN, 1)

    ea.cleanup()


def demo_taster():
    """
    Über den Taster 0 an dem Modul kann die gelbe LED gleichzeitig auf dem
    Board und in der GUI geschaltet werden. Mit dem Taster 1 kann die rote LED
    auf die gleichte Weise gesteuert werden.
    """
    input(str(demo_taster.__doc__) + "\n(Enter für Start)")

    def taster0_gedrueckt(_):
        _ea = __eamodul_erzeugen()
        _ea.schalte_led(EAModul.LED_GELB, ea.taster_gedrueckt(0))

    def taster1_gedrueckt(_):
        _ea = __eamodul_erzeugen()
        _ea.schalte_led(EAModul.LED_ROT, ea.taster_gedrueckt(1))

    ea = __eamodul_erzeugen()
    ea.taster_event_registrieren(0, taster0_gedrueckt)
    ea.taster_event_registrieren(1, taster1_gedrueckt)

    # GUI startet und blockiert bis zum Ende
    EAModulGui(ea)

    ea.cleanup()


def main():
    """
    Hauptfunktion, die bei Start des Moduls ausgeführt wird.
    """
    demo = input("Welches Demo soll gestartet werden?: " +
                 "demo_taster, demo_cli, demo_cli_blinken\n")

    if demo == "demo_taster":
        demo_taster()
    elif demo == "demo_cli":
        demo_cli()
    elif demo == "demo_cli_blinken":
        demo_cli_blinken()


if __name__ == '__main__':
    main()
