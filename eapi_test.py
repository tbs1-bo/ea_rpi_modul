from eapi.eapi import EAModul

if __name__ == "__main__":
    ea_modul = EAModul(1, 2, 3, 4, 5)

    ea_modul.schalte_led(1, False)
    try:
        for i in range(5):
            ea_modul.schalte_led(0, True)
            if ea_modul.taster_gedrueckt(0):
                ea_modul.schalte_led(0, False)

    except KeyboardInterrupt:
        ea_modul.cleanup()
    finally:
        ea_modul.cleanup()
