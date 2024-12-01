import random
import csv
import os

def create_data_files():
    data = {
        "imiona.txt": ["Anna", "Jan", "Marek", "Ewa", "Piotr", "Kasia", "Tomasz", "Monika"],
        "nazwiska.txt": ["Kowalski", "Nowak", "Wisniewski", "Zielinska", "Krawczyk", "Lewandowski"],
        "ulice.txt": ["Lipowa", "Akacjowa", "Sloneczna", "Chopina", "Kosciuszki"],
        "miasta.txt": ["Warszawa", "Krakow", "Gdansk", "Wroclaw", "Poznan"],
        "kraje.txt": ["Polska", "Niemcy", "Francja", "Hiszpania", "Wlochy"]
    }
    for file_name, values in data.items():
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write('\n'.join(values))
        print(f"Plik {file_name} zostal wygenerowany.")

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]
    else:
        print(f"Plik {file_path} nie istnieje.")
        return []

def generate_pesel():
    return ''.join(random.choices("0123456789", k=11))

def generate_data_row(imiona, nazwiska, ulice, miasta, kraje, existing_rows):
    while True:
        imie = random.choice(imiona)
        nazwisko = random.choice(nazwiska)
        pesel = generate_pesel()
        ulica = random.choice(ulice)
        nr_domu = random.randint(1, 50)
        miasto = random.choice(miasta)
        kraj = random.choice(kraje)
        
        new_row = [imie, nazwisko, pesel, ulica, nr_domu, miasto, kraj]
        # Konwertujemy wiersz na tuple dla łatwiejszego porównania
        row_tuple = tuple(new_row)
        
        # Sprawdzamy czy wiersz już istnieje
        if row_tuple not in existing_rows:
            return new_row

def save_to_csv(data, output_file):
    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['imie', 'nazwisko', 'pesel', 'ulica', 'nr_domu', 'miasto', 'kraj'])
        writer.writerows(data)
    print(f"Plik zapisano w: {os.path.abspath(output_file)}")

def display_csv(file_path):
    if not os.path.exists(file_path):
        print(f"Plik {file_path} nie istnieje.")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            
            # Wyświetl nagłówek
            headers = next(reader)
            header_format = "{:<15} {:<15} {:<12} {:<15} {:<8} {:<15} {:<15}"
            print("\n" + header_format.format(*headers))
            print("-" * 95)
            
            # Wyświetl dane
            for row in reader:
                print(header_format.format(*row))
    except Exception as e:
        print(f"Wystąpił błąd podczas odczytu pliku: {e}")

def main():
    create_data_files()
    imiona = load_data('imiona.txt')
    nazwiska = load_data('nazwiska.txt')
    ulice = load_data('ulice.txt')
    miasta = load_data('miasta.txt')
    kraje = load_data('kraje.txt')

    if not all([imiona, nazwiska, ulice, miasta, kraje]):
        print("Nie udalo sie wczytac wszystkich danych. Sprawdz pliki wejsciowe.")
        return

    liczba_wierszy = int(input("Podaj liczbe wierszy do wygenerowania: "))
    
    # Zbiór do przechowywania już wygenerowanych wierszy
    dane = set()
    max_attempts = liczba_wierszy * 100  # Zabezpieczenie przed nieskończoną pętlą
    attempts = 0
    
    while len(dane) < liczba_wierszy and attempts < max_attempts:
        new_row = generate_data_row(imiona, nazwiska, ulice, miasta, kraje, dane)
        dane.add(tuple(new_row))
        attempts += 1
    
    if attempts >= max_attempts:
        print("Ostrzeżenie: Osiągnięto maksymalną liczbę prób generowania unikalnych wierszy.")
    
    save_to_csv(dane, 'dane_osobowe.csv')
    
    # Wyświetl wygenerowane dane
    print("\nWygenerowane dane:")
    display_csv('dane_osobowe.csv')

if __name__ == "__main__":
    main()
