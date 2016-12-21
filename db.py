from pony.orm import *
from datetime import date

db = Database()


class Pricing(db.Entity):
    card = Required('Card')
    price = Required(float)
    date = Required(date)
    composite_key(card, date)


class Card(db.Entity):
    name = Required(str)
    cardset = Required(str)
    num = Required(int)
    foil = Required(bool)
    pricings = Set(Pricing)
    composite_key(name, cardset, foil)

db.bind('sqlite', 'database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
sql_debug(True)
