from datetime import date
from db import *
import json


def main():
    the_file = open('card_prices.txt')
    inventory = json.loads(the_file.read())
    with db_session:
        cur_list = []
        # set of cards in db
        names = set(select(c.name for c in Card))
        for key, value in inventory.items():
            print(key)
            # adds to db if not already there
            if key not in names:
                Card(name=key, num=value['inventory'], foil=value['foil'])
            # changes inventory name in db if different
            this_name = Card.get(name=key)
            if this_name.num != value['inventory']:
                update_num(key, value['inventory'])
            # adds card to a list for next step
            cur_list.append(key)
            # adds prices
            if value['foil'] is True:
                add_pricing((key, value['median']['foil'], value['date']))
            else:
                add_pricing((key, value['median']['normal'], value['date']))
        # deletes card if not there anymore
        delete(c for c in Card if c.name not in cur_list)


@db_session
def update_num(card, new_num):
    this_name = Card.get(name=name)
    this_name.num = new_num


@db_session
def add_pricing(a_tuple):
    c = Card.get(name=a_tuple[0])
    Pricing(card=c, price=a_tuple[1], date=a_tuple[2])


if __name__ == '__main__':
    main()
