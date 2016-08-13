"""
GUI, die als Dummy für ein fehlendes EAModul dient.

Die Klasse ist noch in Entwicklung und sollte noch nicht verwendet werden.

Mit einem EAModul kann kann die GUI initialisiert werden. Daher benötigen wir
zunächst ein übliches EAModul.

>>> from eapi.gui import EAModulGui
>>> from eapi.hw import EAModul

>>> ea = EAModul()

Nun kann eine GUI für das EA-Modul erstellt werden.

   gui = EAModulGui(ea)

Änderungen an den LEDs am Modul werden nun ebenfalls in der GUI dargestellt.
"""

from tkinter import *  # Tk, Button, Label, StringVar
from eapi.hw import EAModul


class EAModulGui:
    """
    Eine GUI für ein EAModul mit zwei Tastern und drei LEDs.
    """

    def __init__(self, eamodul):
        """
        Erstellt eine GUI für das gegebenen EAModul.
        """
        self.ea = eamodul
        self.ea.led_event_registrieren(EAModul.LED_ROT,
                                       self.__rote_led_update)
        self.ea.led_event_registrieren(EAModul.LED_GELB,
                                       self.__gelbe_led_update)
        self.ea.led_event_registrieren(EAModul.LED_GRUEN,
                                       self.__gruene_led_update)
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
        self.ea.schalte_led(EAModul.LED_ROT, True)

    def __taster1_gedrueckt(self):
        self.ea.schalte_led(EAModul.LED_ROT, False)

    def __farbe_fuer_ledwert(self, led_wert, default_wert):
        """Bestimmt für den led_wert eine Farbe.

        Wenn der LED-Wert 1 ist, wird der default_wert zurückgegeben, sonst wird
        lightgrey als Farbe verwendet."""

        if led_wert == 1:
            return default_wert
        else:
            return "lightgrey"

    def __rote_led_update(self, neuer_wert):
        self.var_rot.set(neuer_wert)
        self.lbl_led_rot.configure(bg=self.__farbe_fuer_ledwert(neuer_wert,
                                                                "red"))

    def __gelbe_led_update(self, neuer_wert):
        self.var_gelb.set(neuer_wert)
        self.lbl_led_gelb.configure(bg=self.__farbe_fuer_ledwert(neuer_wert,
                                                                 "yellow"))

    def __gruene_led_update(self, neuer_wert):
        self.var_gruen.set(neuer_wert)
        self.lbl_led_gruen.configure(bg=self.__farbe_fuer_ledwert(neuer_wert,
                                                                  "green"))

__eamodul = None
def __eamodul_erzeugen():
    """Hilfsmethode, die ein EAModul erstellt, wenn noch keines vorhanden ist.
    """
    global __eamodul

    if __eamodul is None:
        __eamodul = EAModul()

    return __eamodul


def demo_taster():
    """
    Über den Taster 0 an dem Modul kann die gelbe LED gleichzeitig auf dem
    Board und in der GUI geschaltet werden. Mit dem Taster 1 kann die rote LED auf die
    gleichte Weise gesteuert werden.
    """
    input(str(demo_taster.__doc__) + "\n(Enter für Start)")

    def taster0_gedrueckt(_):
        ea = __eamodul_erzeugen()
        ea.schalte_led(EAModul.LED_GELB, ea.taster_gedrueckt(0))

    def taster1_gedrueckt(_):
        ea = __eamodul_erzeugen()
        ea.schalte_led(EAModul.LED_ROT, ea.taster_gedrueckt(0))

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
    demo = input("Welches Demo soll gestartet werden: demo_taster ")
    if demo == "demo_taster":
        demo_taster()


if __name__ == '__main__':
    main()
