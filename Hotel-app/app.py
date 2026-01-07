from flask import Flask, render_template, request

app = Flask(__name__)

# Hotel class
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

# User class
class User:
    def __init__(self, uname, uId, cost):
        self.uname = uname
        self.uId = uId
        self.cost = cost

# Sample data
hotels = [
    Hotel("H1", 4, "Bangalore", 5, 100),
    Hotel("H2", 5, "Bangalore", 5, 200),
    Hotel("H3", 6, "Mumbai", 3, 100),
]

users = [
    User("U1", 2, 1000),
    User("U2", 3, 1200),
    User("U3", 4, 1100),
]

# Routes
@app.route('/')
def index():
    sort_by = request.args.get('sort', 'name')

    if sort_by == 'name':
        Hotel.sortByName()
    elif sort_by == 'rating':
        Hotel.sortByRate()
    elif sort_by == 'room':
        Hotel.sortByRoomAvailable()

    sorted_hotels = sorted(hotels)
    location = request.args.get('location', None)
    if location:
        filtered_hotels = [h for h in sorted_hotels if h.location == location]
    else:
        filtered_hotels = sorted_hotels

    return render_template('index.html', hotels=filtered_hotels)

@app.route('/users')
def show_users():
    return render_template('users.html', users=users, hotels=hotels)

if __name__ == "__main__":
    app.run(debug=True)
