from requests import get
from bs4 import BeautifulSoup
from time import sleep
import string
import re
from random import uniform
from datetime import date
import json
import ast
the_file = open('inventory.txt')
inventory = ast.literal_eval(the_file.read())


def get_card_set():
    formatted = []
    # remove punctuation pattern for slugification
    remove = string.punctuation
    remove = remove.replace("-", "")
    pattern = r"[{}]".format(remove)
    for each in inventory:
        card = re.sub(pattern, '', each[1]).lower().split()
        card = '-'.join(ch for ch in card)
        card_set = each[2].lower()
        if 'prerelease' in card_set:
            card_set = 'prerelease-cards'
        elif 'core' in card_set:
            card_set = card_set.split()
            card_set = "{0}-{1}-{2}{3}".format(card_set[0],
                                               card_set[1],
                                               card_set[0][0],
                                               card_set[1][2:])
        elif ('magic' in card_set and
              ('2012' in card_set or
               '2013' in card_set or
               '2011' in card_set or
               '2010' in card_set)):
            card_set = card_set.split()
            card_set = "{0}-{1}-{2}{3}".format(card_set[0],
                                               card_set[1],
                                               card_set[0][0],
                                               card_set[1][2:])
        elif 'event deck' in card_set:
            card_set = 'magic-modern-event-deck'
        elif 'game day' in card_set:
            card_set = 'game-day-promos'
        elif ('wpn' in card_set or
              'gateway' in card_set):
            try:
                card_set = 'wpn-promos'
            except ValueError:
                card_set = 'gateway-promos'
        elif 'friday' in card_set:
            card_set = 'fnm-promos'
        elif ('promos' in card_set or
              'intro pack' in card_set):
            card_set = 'unique-and-miscellaneous-promos'
        elif '2015 edition' in card_set:
            card_set = 'modern-masters-2015'
        elif 'sixth' in card_set:
            card_set = '6th-edition'
        elif 'seventh' in card_set:
            card_set = '7th-edition'
        elif 'eighth' in card_set:
            card_set = '8th-edition'
        elif 'ninth' in card_set:
            card_set = '9th-edition'
        elif 'tenth' in card_set:
            card_set = '10th-edition'
        else:
            card_set = re.sub(pattern, '', card_set).split()
            card_set = '-'.join(ch for ch in card_set)
        formatted.append((card_set, card, each[0], each[3], each[1]))
    return formatted


def price(table):
    names = [d.text.strip().lower() for d in table.select(
        '.priceGuidePricePointName')]
    prices = [float(d.text.strip('$')) for d in table.select(
        '.priceGuidePricePointData') if d.text.strip() != 'N/A']
    return dict(zip(names, prices))


def get_prices(card_tuple):
    sleep(uniform(0.5, 2))
    url = "http://shop.tcgplayer.com/magic/{0}/{1}".format(card_tuple[0],
                                                           card_tuple[1])
    page = get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    market_div, _, _, median_div = soup.select('.priceGuidePricePointDiv')
    prices = {
        'market': price(market_div),
        'median': price(median_div),
        'inventory': card_tuple[2],
        'date': str(date.today()),
        'foil': card_tuple[3]
    }
    print(card_tuple[1], prices)
    return prices


def main():
    with open('card_prices.txt') as f:
        try:
            result = json.load(f)
        except json.JSONDecodeError:
            result = {}
    for card in get_card_set():
        if card[4] not in result:
            result[card[4]] = get_prices(card)
            with open('card_prices.txt', 'w') as f:
                f.write(json.dumps(result))


if __name__ == '__main__':
    main()
