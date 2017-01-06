from datetime import date
from db import *
import pickle


def main():
    print('Putting gathered data into database...')
    with open('card_prices.txt', 'rb') as f:
        inventory = pickle.load(f)
    with db_session:
        cur_list = []
        # set of cards in db
        names = set(select((c.name, c.cardset, c.foil) for c in Card))
        for key, value in inventory.items():
            print(key, value)
            # adds to db if not already there
            if (key[0], key[1], key[2]) not in names:
                Card(name=key[0],
                     num=value['inventory'],
                     foil=key[2],
                     cardset=key[1])
            # changes inventory num in db if different
            this_name = Card.get(
                name=key[0], cardset=key[1], foil=key[2])
            if (this_name.num != value['inventory'] and
                    this_name.foil != key[2]):
                        update_num(key[0], value['inventory'])
            # adds card to a list for next step
            cur_list.append(key[0])
            # adds prices
            # key[1] is cardset
            # value['foil'] is foil
            if key[2]:
                try:
                    add_pricing(
                        (key[0], value['median']['foil'],
                         value['date'], key[1], key[2]))
                except KeyError:
                    add_pricing(
                        (key[0], value['median']['normal'],
                         value['date'], key[1], key[2]))
            else:
                try:
                    add_pricing(
                        (key[0], value['median']['normal'],
                         value['date'], key[1], key[2]))
                except KeyError:
                    add_pricing(
                        (key[0], value['median']['foil'],
                         value['date'], key[1], key[2]))
        # deletes card if not there anymore
        delete(c for c in Card if c.name not in cur_list)


@db_session
def update_num(card, new_num):
    this_name = Card.get(name=name)
    this_name.num = new_num


@db_session
def add_pricing(a_tuple):
    c = Card.get(name=a_tuple[0], cardset=a_tuple[3], foil=a_tuple[4])
    Pricing(card=c, price=a_tuple[1], date=a_tuple[2])


if __name__ == '__main__':
    main()
