from eapi.net import EAModulServer

if __name__ == "__main__":
    host = "localhost"
    port = 9999

    print("Starte Server auf host", host, "und Port", port)
    easerver = EAModulServer(host, port)
    easerver.serve_forever()
