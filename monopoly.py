import pickle
import random
from abc import ABC, abstractmethod

class GameObject(ABC):
    @abstractmethod
    def __init__(self, name):
        self.name = name

class Property(GameObject):
    def __init__(self, name, price, house_price, rent):
        super().__init__(name)
        self.price = price
        self.house_price = house_price
        self.rent = rent
        self.owner = None
        self.houses = 0

    def buy(self, player):
        if self.name == "Start":
            return False 
        if self.owner is None and player.balance >= self.price:
            player.balance -= self.price
            self.owner = player
            player.properties.append(self)
            return True
        return False

    def buy_house(self, player):
        if self.owner == player and player.balance >= self.house_price:
            player.balance -= self.house_price
            self.houses += 1
            return True
        return False

class Player:
    def __init__(self, name):
        self.name = name
        self.balance = 1500
        self.position = 0
        self.properties = []
        self.roll_count = 0  # Liczba rzutów kością

    def move(self, roll):
        self.position = (self.position + roll) % len(board)
        self.roll_count += 1  # Zwiększ liczbę rzutów

# Tworzenie planszy
board = [
    Property("Start", 0, 0, 0),
    Property("Brzeźno", 60, 2, 50),
    Property("Bielany", 60, 4, 50),
    Property("Las", 100, 6, 50),
    Property("Śluz", 100, 8, 50),
    Property("Wschodnia", 120, 10, 50),
    Property("Główna", 140, 12, 50),
    Property("Wola", 140, 14, 50),
    Property("Jana Pawła II", 160, 16, 50),
    Property("Przebudzenie", 180, 18, 50),
    Property("Pokój", 180, 20, 50),
    Property("Kosciuszki", 200, 22, 50),
    Property("Zgoda", 220, 24, 50),
    Property("Warszawska", 220, 26, 50),
    Property("Urok", 240, 28, 50),
    Property("Wilanów", 260, 30, 50),
    Property("Zamkowa", 260, 32, 50),
    Property("Złote Piaski", 280, 34, 50),
    Property("Niezależna", 300, 36, 50),
    Property("Na zdanie", 300, 38, 50),
]

def save_game(players, filename):
    with open(filename, 'wb') as file:
        pickle.dump(players, file)

def load_game(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

def display_menu():
    print("1. Nowa gra")
    print("2. Wczytaj grę")
    return input("Wybierz opcję: ")

def display_game_state(player):
    current_property = board[player.position]
    print("+---------------------+")
    print("|---------------------|")
    print("|---MONOPOLY-PYTHON---|")
    print("|---------------------|")
    print("+---------------------+")
    print("\nDane gracza:")
    print(f"- Nazwa gracza: {player.name}")
    print(f"- Stan konta: {player.balance}")
    print(f"- Ulica: {current_property.name}")
    
    print("\nMożliwe akcje:")
    print("1. Rzuć kością")
    if current_property.owner is None and current_property.name != "Start":
        print("2. Kup ulicę")
    if current_property.owner == player:
        print("3. Kup domek")
    
    print("\nZarządzanie grą:")
    print("4. Zapisz grę")
    print("5. Koniec bez zapisania")
    print("6. Wyświetl statystyki graczy")
    return input("Wybierz opcję: ")

def display_player_stats(players):
    print("\n--- Statystyki graczy ---")
    for player in players:
        print(f"\nGracz: {player.name}")
        print(f"Stan konta: {player.balance}")
        print(f"Liczba rzutów kością: {player.roll_count}")
        print("Posiadane ulice:")
        for prop in player.properties:
            print(f" - {prop.name} (Domek: {prop.houses})")
        print(f"Liczba domków: {sum(prop.houses for prop in player.properties)}")
    print("\n--- Koniec statystyk ---")

def main():
    players = []
    
    choice = display_menu()
    if choice == "1":
        num_players = int(input("Ilu graczy? "))
        players = [Player(input(f"Podaj nazwę gracza {i + 1}: ")) for i in range(num_players)]
    elif choice == "2":
        filename = input("Podaj nazwę pliku: ")
        players = load_game(filename)
    else:
        print("Nieprawidłowy wybór.")
        return

    current_player_idx = 0
    
    while True:
        player = players[current_player_idx]
        action = display_game_state(player)
        
        if action == "1":
            roll = random.randint(1, 6)
            print(f"Rzuciłeś: {roll}")
            player.move(roll)
            
            current_property = board[player.position]
            if current_property.owner and current_property.owner != player:
                rent = current_property.rent * (1 + current_property.houses)
                print(f"Płacisz czynsz: {rent}")
                player.balance -= rent
                current_property.owner.balance += rent

        elif action == "2":
            current_property = board[player.position]
            if current_property.buy(player):
                print(f"Kupiłeś ulicę {current_property.name}")
            else:
                print("Nie możesz kupić tej ulicy.")

        elif action == "3":
            current_property = board[player.position]
            if current_property.buy_house(player):
                print(f"Kupiłeś domek na ulicy {current_property.name}")
            else:
                print("Nie możesz kupić domku.")

        elif action == "4":
            filename = input("Podaj nazwę pliku do zapisu: ")
            save_game(players, filename)
            print("Gra została zapisana.")

        elif action == "5":
            print("Gra zakończona.")
            break

        elif action == "6":
            display_player_stats(players)
        
        else:
            print("Nieprawidłowy wybór.")

        current_player_idx = (current_player_idx + 1) % len(players)

if __name__ == "__main__":
    main()
