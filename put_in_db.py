from datetime import date
from db import *
import pickle


def main():
    print('Putting gathered data into database...')
    with open('card_prices.txt', 'rb') as f:
        inventory = pickle.load(f)
        f.close()
    with db_session:
        cur_list = []
        # set of cards in db
        names = set(select(c.name for c in Card))
        for key, value in inventory.items():
            print(key)
            # adds to db if not already there
            if key[0] not in names:
                Card(name=key[0],
                     num=value['inventory'],
                     foil=value['foil'],
                     cardset=key[1])
            # changes inventory num in db if different
            this_name = Card.get(name=key[0])
            if this_name.num != value['inventory']:
                update_num(key[0], value['inventory'])
            # adds card to a list for next step
            cur_list.append(key[0])
            # adds prices
            if value['foil'] is True:
                try:
                    add_pricing(
                        (key[0], value['median']['foil'], value['date']))
                except KeyError:
                    add_pricing(
                        (key[0], value['median']['normal'], value['date']))
            else:
                try:
                    add_pricing(
                        (key[0], value['median']['normal'], value['date']))
                except KeyError:
                    add_pricing(
                        (key[0], value['median']['foil'], value['date']))
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
