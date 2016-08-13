"""
GUI, die als Dummy für ein fehlendes EAModul dient.

Die Klasse ist noch in Entwicklung und sollte noch nicht verwendet werden.

Mit einem EAModul kann kann die GUI initialisiert werden.

>>> from eapi.gui import EAModulGui
>>> from eapi.hw import EAModul

>>> ea = EAModul()

Nun kann eine GUI für das EA-Modul erstellt werden.

   gui = EAModulGui(ea)

"""

from tkinter import Tk, Button, Label, StringVar
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

        btn_taster0 = Button(fenster, text="Taster 0",
                             command=self.__taster0_gedrueckt)
        btn_taster0.pack()

        btn_taster1 = Button(fenster, text="Taster 1",
                             command=self.__taster1_gedrueckt)
        btn_taster1.pack()

        # LEDs erzeugen
        self.var_rot = StringVar(value="0")
        lbl_led_rot = Label(fenster, textvariable=self.var_rot, bg='red')
        lbl_led_rot.pack()

        self.var_gelb = StringVar(value="0")
        lbl_led_gelb = Label(fenster, textvariable=self.var_gelb, bg='yellow')
        lbl_led_gelb.pack()

        self.var_gruen = StringVar(value="0")
        lbl_led_gruen = Label(fenster, textvariable=self.var_gruen, bg='green')
        lbl_led_gruen.pack()

        fenster.mainloop()

    def __taster0_gedrueckt(self):
        self.ea.schalte_led(EAModul.LED_ROT, True)

    def __taster1_gedrueckt(self):
        self.ea.schalte_led(EAModul.LED_ROT, False)

    def __rote_led_update(self, neuer_wert):
        self.var_rot.set(neuer_wert)

    def __gelbe_led_update(self, neuer_wert):
        self.var_gelb.set(neuer_wert)

    def __gruene_led_update(self, neuer_wert):
        self.var_gruen.set(neuer_wert)


def main():
    EAModulGui(EAModul())


if __name__ == '__main__':
    main()
