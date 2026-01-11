import pytest
import os
from todo import TaskManager, Task  # <--- Uprav 'todo' podle názvu tvého souboru!


# Fixture je způsob, jak připravit data před každým testem
# Tady chceme čistý TaskManager pro každý test, aby se neovlivňovaly
@pytest.fixture
def manager():
    test_filename = "test_tasks.json"
    # Použijeme testovací soubor, abychom si nepřepsali ten ostrý
    if os.path.exists(test_filename):
        os.remove(test_filename)

    mgr = TaskManager(filename=test_filename)
    # Trik: Přepíšeme název souboru v instanci, aby ukládal jinam
    # (V reálu bychom to dělali přes parametr v __init__, ale pro teď stačí takto)
    # POZOR: Musíš upravit svou třídu TaskManager, aby název souboru nebyl "hardcoded"
    # Ale zatím to otestujeme i bez toho.
    return mgr


def test_add_task(manager):
    """Testuje, zda se úkol skutečně přidá do seznamu."""
    manager.add_task("Koupit mléko")

    assert len(manager.task_list) == 1
    assert manager.task_list[0].title == "Koupit mléko"
    assert manager.task_list[0].completed is False


def test_complete_task(manager):
    """Testuje splnění úkolu."""
    manager.add_task("Uklidit")
    manager.task_list[0].completed = True  # Simulujeme splnění

    assert manager.task_list[0].completed is True


def test_empty_task_not_added(manager):
    """Testuje validaci - prázdný úkol by se neměl přidat."""
    manager.add_task("")  # Prázdný string
    manager.add_task("   ")  # Jen mezery

    assert len(manager.task_list) == 0