'''
A Feladat:
Osztályok Létrehozása
* Hozz létre egy Szoba absztrakt osztályt, amely alapvető attribútumokat definiál (ár, szobaszám). (5 pont)
* Hozz létre az Szoba osztályból EgyagyasSzoba és KetagyasSzoba származtatott osztályokat, amelyek különböző attributumai vannak, és az áruk is különböző.(5 pont)
* Hozz létre egy Szalloda osztályt, ami ezekből a Szobákból áll, és van saját attributuma is (név pl.) (10 pont)
* Hozz létre egy Foglalás osztályt, amelybe a Szálloda szobáinak foglalását tároljuk (elég itt, ha egy foglalás csak egy napra szól) (10 pont)
Foglalások Kezelése
* Implementálj egy metódust, ami lehetővé teszi szobák foglalását dátum alapján, visszaadja annak árát. (15 pont)
* Implementálj egy metódust, ami lehetővé teszi a foglalás lemondását. (5 pont)
* Implementálj egy metódust, ami listázza az összes foglalást. (5 pont)
Felhasználói Interfész és adatvalidáció
* Készíts egy egyszerű felhasználói interfészt, ahol a felhasználó kiválaszthatja a kívánt műveletet (pl. foglalás, lemondás, listázás). (20 pont)
* A foglalás létrehozásakor ellenőrizd, hogy a dátum érvényes (jövőbeni) és a szoba elérhető-e akkor. (10 pont)
* Biztosítsd, hogy a lemondások csak létező foglalásokra lehetségesek. (5 pont)
* Töltsd fel az futtatás után a rendszert 1 szállodával, 3 szobával és 5 foglalással, mielőtt a felhasználói adatbekérés megjelenik. (10 pont)
'''

from datetime import date, datetime, timedelta

# Osztályok definiálása

class Szoba:
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, furdo, ar):
        super().__init__(szobaszam, ar)
        self.furdo = furdo

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, furdo, extra, ar):
        super().__init__(szobaszam, ar)
        self.furdo = furdo
        self.extra = extra

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    # szalloda osztály funkciói

    def szoba_letrehozas(self, szoba):
        self.szobak.append(szoba)
    
    def foglalas(self, szobaszam, datum):
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                print("A választott szoba foglalt az adott napon. Kérem válasszon másik szobát, vagy másik dátumot.")
                return
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                self.foglalasok.append(Foglalas(szoba, datum))
                return szoba.ar

    def lemondas(self, szobaszam, datum):
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                return True
        return False
    
    def rendben_levo_foglalasok(self):
        for foglalas in self.foglalasok:
            print(f"Szoba: {foglalas.szoba.szobaszam}, Időpont: {foglalas.datum}")

# Szalloda létrehozása
szalloda = Szalloda("Az öt csillagos")

# Szobák létrehozása
szalloda.szoba_letrehozas(EgyagyasSzoba("1","Kád",10000))
szalloda.szoba_letrehozas(EgyagyasSzoba("10","Zuhany",11000))
szalloda.szoba_letrehozas(KetagyasSzoba("100","Jacuzzi","Minibár",20000))

# Foglalások létrehozása
szalloda.foglalas("1", date.today() + timedelta(days=2))
szalloda.foglalas("10", date.today() + timedelta(days=3))
szalloda.foglalas("100", date.today() + timedelta(days=4))
szalloda.foglalas("1", date.today() + timedelta(days=5))
szalloda.foglalas("10", date.today() + timedelta(days=6))

# Menü
while True:

    print("Kérem válasszon az alábbi menüpontok közül:")
    print("1. Választható szobák listája")
    print("2. Foglalás")
    print("3. Meglévő foglalások listázása")
    print("4. Foglalás lempondása")
    print("5. Kilépés")
    case = input("Kérem válasszon a fenti menüpontokból. Használja a menü sorszámát: ")

    if case == "1":
            print("Szobák száma:")
            print(len(szalloda.szobak))
            print("Egyágyas szobák:")
            for szoba in szalloda.szobak:
                if isinstance(szoba, EgyagyasSzoba):
                    print(f"Szobaszám: {szoba.szobaszam}, Ár: {szoba.ar} Ft, (Fürdő: {szoba.furdo})")
            print("Kétágyas szobák:")
            for szoba in szalloda.szobak:
                if isinstance(szoba, KetagyasSzoba):
                    print(f"Szobaszám: {szoba.szobaszam}, Ár: {szoba.ar} Ft, (Fürdő: {szoba.furdo}, Extra: {szoba.extra})")
    elif case == "2":
        szobaszam = input("Kérem adja meg a foglalni kívánt szoba számát (1,10,100): ")
        datum = input("Kérem adja meg, mikor szeretne nálunk megszállni, ennek formátuma ÉÉÉÉ-HH-NN, napi foglalás lehetséges csak: ")
        try:
            datum = datetime.strptime(datum, "%Y-%m-%d")
            if datum < datetime.now():
                print("Hibás dátum! Kérem olyan dátumot adjon meg, ami nem a mai és nem régebbi a mainál.")
            else:
                ar = szalloda.foglalas(szobaszam, datum)
                if ar:
                    print(f"Köszönjük foglalását! Az ár: {ar} Ft")
                else:
                    print("Hibás szobaszám!")
        except ValueError:
            print("Hibásan adta meg a dátumot! Engedélyezett formátum ÉÉÉÉ-HH-NN")
    elif case == "3":
        szalloda.rendben_levo_foglalasok()
    elif case == "4":
        szobaszam = input("Kérem adja meg a lemondani kívánt foglaláshoz tartozó szoba számát: ")
        datum = input("Kérem adja meg a foglalásához tartozó dátumot, ennek formátuma ÉÉÉÉ-HH-NN:")
        try:
            datum = datetime.strptime(datum, "%Y-%m-%d")
            siker = szalloda.lemondas(szobaszam, datum)
            if siker:
                print("Foglalását töröltük.")
            else:
                print("A megegadott adatokkal nem található foglalás.")
        except ValueError:
            print("Hibásan adta meg a dátumot! Engedélyezett formátum ÉÉÉÉ-HH-NN")
    elif case == "5":
        break
    else:
        print("Hibás választás!")