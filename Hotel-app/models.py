# models.py
class Hotel:
    sortParam = 'name'

    def __init__(self, name, roomAvl, location, rating, pricePr, id=None):
        self.id = id
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

# New: simple in-memory store for hotels with sample data and CRUD helpers
class HotelStore:
    def __init__(self):
        self._hotels = []
        self._next_id = 1
        self._seed_sample()

    def _seed_sample(self):
        if self._hotels:
            return
        samples = [
            ("Executive Room", 5, "Downtown", 4.5, 120),
            ("Deluxe Room", 3, "Seaside", 4.7, 200),
            ("Presidential Suite", 1, "Penthouse", 5.0, 450),
        ]
        for name, rooms, loc, rating, price in samples:
            self.add(name, rooms, loc, rating, price)

    def list(self):
        return list(self._hotels)

    def add(self, name, roomAvl, location, rating, pricePr):
        h = Hotel(name, roomAvl, location, rating, pricePr, id=self._next_id)
        self._hotels.append(h)
        self._next_id += 1
        return h

    def get(self, id):
        return next((h for h in self._hotels if h.id == int(id)), None)

    def update(self, id, **kwargs):
        h = self.get(id)
        if not h:
            return None
        for k, v in kwargs.items():
            if hasattr(h, k):
                setattr(h, k, v)
        return h

    def delete(self, id):
        h = self.get(id)
        if h:
            self._hotels.remove(h)
            return True
        return False

# expose a module-level store instance
hotel_store = HotelStore()
