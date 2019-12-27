import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends



def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = get_friends(user_id, 'bdate')
    if friends is not None:
        ages = []
        for i in range(len(friends)):
            try:
                birthday = friends[i]['bdate']
            except KeyError:
                pass
            else:
                fulldate = birthday.split('.')
                if len(fulldate) == 3:
                    day = dt.datetime.now().day
                    month = dt.datetime.now().month
                    year = dt.datetime.now().year
                    if month > int(fulldate[1]) or month == int(fulldate[1]) and day >= int(fulldate[0]):
                        ages.append(year - int(fulldate[2]))
                    else:
                        ages.append(year - int(fulldate[2]) - 1)
        if len(ages) == 0:
            return None
        else:
            return median(ages)
    return None