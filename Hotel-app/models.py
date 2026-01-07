# models.py
class Hotel:
    sortParam = 'name'

    def __init__(self, name, roomAvl, location, rating, pricePr):
        self.name = name
        self.roomAvl = roomAvl
        self.location = location
        self.rating = rating
        self.pricePr = pricePr

    def __lt__(self, other):
        return getattr(self, Hotel.sortParam) < getattr(other, Hotel.sortParam)

    @classmethod
    def sortByName(cls):
        cls.sortParam = 'name'

    @classmethod
    def sortByRate(cls):
        cls.sortParam = 'rating'

    @classmethod
    def sortByRoomAvailable(cls):
        cls.sortParam = 'roomAvl'


class User:
    def __init__(self, uname, uId, cost):
        self.uname = uname
        self.uId = uId
        self.cost = cost
