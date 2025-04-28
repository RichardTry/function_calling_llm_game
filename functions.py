def get_weather(city: str):
    """
    Функция, которая возвращает погоду в заданном городе.
    
    Args:
        city: Город, для которого надо узнать погоду.
    """
    import random
    
    return "sunny" if random.random() > 0.5 else "rainy"


def get_sunrise_sunset_times(city: str):
    """
    Функция, которая возвращает время восхода и заката для заданного города для текущей даты (дата от пользователя не требуется), в формате списка: [sunrise_time, sunset_time].
    
    Args:
        city: Город, в котором можно узнать время восхода и захода солнца.
    """

    return ["6:00", "18:00"]

FUNCTIONS = [get_weather, get_sunrise_sunset_times]
