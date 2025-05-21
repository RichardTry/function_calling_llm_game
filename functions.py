def go_to(location: str):
    """
    Пойти в заданную локацию.
    
    Args:
        location: Название локации, куда надо отправиться игроку
    """
    
    return None


def move(side: str):
    """
    Начать движение в указанную сторону света.
    
    Args:
        side: Сторона света, в которую надо начать движение. Доступны значения: north, east, south, west.
    """

    return None

def stop():
    """
    Остановиться.
    """

    return None

def go_inside(location: str = None):
    """
    Войти внутрь локации.
    
    Args:
        location: Название локации, куда надо войти. Если не указано, то войти в ближайшую локацию.
    """

    return None

def take_quest(npc: str = None):
    """
    Взять квест у NPC.
    
    Args:
        npc: Имя NPC, у которого надо взять квест. Если не указано, то взять квест у ближайшего NPC.
    """

    return None

def fight(npc: str = None):
    """
    Начать бой с NPC.
    
    Args:
        npc: Имя NPC, с которым надо начать бой. Если не указано, то начать бой с ближайшим NPC.
    """

    return None

def give(item: str, amount: int = 1, npc: str = None):
    """
    Отдать предмет NPC.
    
    Args:
        item: Название предмета, который надо отдать.
        amount: Количество предметов, которое надо отдать. По умолчанию 1.
        npc: Имя NPC, которому надо отдать предмет. Если не указано, то отдать ближайшему NPC.
    """

    return None

def drop(item: str, amount: int = 1):
    """
    Выбросить предмет.
    
    Args:
        item: Название предмета, который надо выбросить.
        amount: Количество предметов, которое надо выбросить. По умолчанию 1.
    """

    return None

FUNCTIONS = [go_to, move, stop, go_inside, take_quest, fight, give, drop]
