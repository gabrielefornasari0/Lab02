def carica_da_file(file_path):
    """
    Carica le foto dal file creando un dizionario con gli anni come chiavi.
    Salta l'intestazione e restituisce None in caso di FileNotFoundError.
    """
    album = {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # Salta la riga di intestazione (codice, titolo, ...)
            next(f)

            # Legge riga per riga
            for riga in f:
                riga = riga.strip()
                if not riga:
                    continue

                dati = [campo.strip() for campo in riga.split(",")]
                if len(dati) == 5:
                    codice, titolo, autore, mese, anno = dati
                    # anno e mese convertiti in intero per coerenza con il main
                    mese = int(mese)
                    anno = int(anno)

                    # Se l'anno non è ancora presente nell'album, crea la lista
                    if anno not in album:
                        album[anno] = []

                    # Aggiunge i dati della foto alla lista dell'anno
                    album[anno].append([codice, titolo, autore, mese])

        print("Album inserito correttamente!")
        return album

    except FileNotFoundError:
        # Se il file non esiste restituisce None come richiesto dalla traccia
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """
    Aggiunge una foto all'album e al file.
    Ritorna il riferimento alla foto aggiunta, oppure None se:
    - il mese non è compreso tra 1 e 12
    - il codice è già presente nell'album
    - il file non viene trovato
    """
    # Controllo validità mese
    if not (1 <= mese <= 12):
        return None

    # Controllo univocità del codice
    for a in album:
        for f in album[a]:
            if f[0] == codice:
                return None

    # Scrittura su file (append)
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
    except FileNotFoundError:
        return None

    # Aggiornamento struttura dati
    if anno not in album:
        album[anno] = []

    nuova_foto = [codice, titolo, autore, mese]
    album[anno].append(nuova_foto)

    # Restituisce il riferimento alla foto inserita
    return nuova_foto


def cerca_foto(album, codice):
    """
    Cerca una foto per codice.
    Ritorna una stringa formattata 'codice, titolo, autore, mese, anno',
    oppure None se non trovata.
    """
    codice = str(codice).strip()

    for anno in album:
        for foto in album[anno]:
            if foto[0] == codice:
                codice_foto, titolo, autore, mese = foto
                return f"{codice_foto}, {titolo}, {autore}, {mese}, {anno}"

    return None


def elenco_foto_anno_per_titolo(album, anno):
    """
    Ritorna la lista dei soli titoli ordinati alfabeticamente per un dato anno.
    Se l'anno non è mai comparso, ritorna None.
    """
    # anno è già un intero proveniente dal main
    if anno not in album:
        return None

    # Ordina le foto dell'anno in base al titolo (indice 1)
    foto_ordinate = sorted(album[anno], key=lambda foto: foto[1].lower())

    # Estrae solo i titoli
    titoli = []
    for foto in foto_ordinate:
        titoli.append(foto[1])

    return titoli


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()