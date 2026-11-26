from syotto import Syote

def main():
    print("LaTeX-based citation application!\n \n" \
    "Commands you can use:\n \n" \
    "help   - Lists all available commands\n"
    "         You can type help [command] for help with specific command\n" \
    "list   - Gives list of all existing citations\n" \
    "types  - Gives a list of the available types of citations\n"
    "new    - Start adding a new citation (new TYPE)\n" \
    "edit   - Edit an existing citaton (edit [reference code])\n" \
    "delete - Delete a citation (delete MITEN TOIMII?)\n"
    "exit   - Closes and shuts down the application,\n         all additions are automatically saved. \n \n")

    s = Syote()
    s.lataa_viitteet()
    s.kysy_syotetta()

if __name__ == "__main__":
    main()