from syotto import Syote

def main():
    print("Latekxi lähdeviittaus sovellus!\nSyötä komentoja:")

    s = Syote()
    s.lataa_viitteet()
    s.kysy_syotetta()

if __name__ == "__main__":
    main()