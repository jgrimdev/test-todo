from typing import List, Dict, Any
from dataclasses import dataclass, asdict
import json,os

@dataclass
class Task:
    title: str
    completed: bool = False

class TaskManager:
    def __init__(self,filename: str = "tasks.json") -> None:
        # Tady vzniká "vnitřní paměť" objektu
        self.task_list: List[Task] = []
        self.filename = filename
        self.load_from_file()

    # ZDE MAŽEME argument 'task_list'. Metoda potřebuje jen 'title'.
    def add_task(self, title: str) -> None:
        if not title.strip():
            print("⚠ Chyba: Název úkolu nesmí být prázdný.")
            return

        # new_task = {"title": title, "completed": False}
        new_task = Task(title=title)
        # Používáme SELF.task_list (naši vnitřní paměť)
        self.task_list.append(new_task)
        self.save_to_file()
        print(f"✅ Úkol '{title}' přidán.")

    def show_tasks(self) -> None:
        # Opět: pracujeme se self.task_list
        if not self.task_list:
            print("--- Seznam úkolů je prázdný ---")
            return

        print("\n--- Seznam úkolů ---")
        for index, task in enumerate(self.task_list):
            status_icon = "[x]" if task.completed else "[ ]"
            print(f"{index}. {status_icon} {task.title}")
        print("--------------------\n")

    def complete_task(self) -> None:
        # Voláme vlastní metodu přes self
        self.show_tasks()

        if not self.task_list:
            return

        try:
            user_input = input("Zadej číslo úkolu pro splnění: ")
            index = int(user_input)

            if 0 <= index < len(self.task_list):
                self.task_list[index].completed = True
                self.save_to_file()
                print(f"✅ Úkol '{self.task_list[index].title}' označen jako hotový.")
            else:
                print(f"⚠ Chyba: Úkol s číslem {index} neexistuje.")

        except ValueError:
            print("⚠ Chyba: Musíš zadat platné číslo.")

    def save_to_file(self):
        # 1. Převedeme objekty Task na seznam slovníků
        data_to_save = [asdict(task) for task in self.task_list]

        # 2. Otevřeme soubor pro ZÁPIS (w = write)
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=4)  # indent=4 udělá hezké odsazení
        print("💾 Uloženo.")

    def load_from_file(self):
        # Pokud soubor neexistuje, končíme (není co načítat)
        if not os.path.exists(self.filename):
            return

        # Otevřeme soubor pro ČTENÍ (r = read)
        with open("tasks.json", "r", encoding="utf-8") as f:
            data_loaded = json.load(f)  # To nám vrátí seznam slovníků

            # Musíme převést slovníky zpátky na objekty Task!
            self.task_list = [Task(**item) for item in data_loaded]
            # Vysvětlení **item: Rozbalí slovník {"title": "X", "completed": True}
            # na argumenty Task(title="X", completed=True)

def main() -> None:
    # Vytvoříme instanci. Ta už v sobě má prázdný list díky __init__
    manager = TaskManager()

    # POZOR: Proměnná 'tasks = []' už tu není potřeba!

    running = True
    while running:
        print("\n=== TODO APP 2026 ===")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Splnit úkol")
        print("4. Ukončit")

        choice = input("Vyber možnost: ")

        if choice == '1':
            title = input("Zadej název úkolu: ")
            # Voláme metodu BEZ seznamu, ten už je uvnitř 'manager'
            manager.add_task(title)
        elif choice == '2':
            manager.show_tasks()
        elif choice == '3':
            manager.complete_task()
        elif choice == '4':
            print("Ukončuji aplikaci. Ahoj!")
            running = False
        else:
            print("⚠ Neplatná volba, zkus to znovu.")


if __name__ == "__main__":
    main()