from requests import get
from bs4 import BeautifulSoup
from time import sleep
import string
import re
from random import uniform
from datetime import date
import pickle
import os
with open('inventory.txt', 'rb') as f:
    inventory = pickle.load(f)


def get_url(cardname, cardname_set):
    url = ''
    # remove punctuation pattern for slugification
    remove = string.punctuation
    remove = remove.replace("-", "")
    pattern = r"[{}]".format(remove)
    # begin cardname formatting
    cardname = cardname.lower()
    cardname_set = cardname_set.strip()
    if (cardname_set == 'Antiquities' or
        cardname_set == 'Chronicles' and
        "urza's power" in cardname):
            card = "urzas-power-plant-columns"
    elif (cardname_set == 'Antiquities' or
          cardname_set == 'Chronicles' and
          "urza's tower" in cardname):
            card = "urzas-tower-forest"
    elif (cardname_set == 'Antiquities' or
          cardname_set == 'Chronicles' and
          "urza's mine" in cardname):
            card = 'urzas-mine-mouth'
    else:
        card = re.sub(pattern, '', cardname).split()
        card = '-'.join(ch for ch in card)
        card = card.replace('æ', 'ae').replace('é', 'e').replace('á', 'a')
    # begin cardset formatting
    card_set = cardname_set.lower()
    if 'prerelease' in card_set:
        card_set = ['prerelease-cards']
    elif 'core' in card_set:
        card_set = card_set.split()
        card_set = ["{0}-{1}-{2}{3}".format(card_set[0],
                                            card_set[1],
                                            card_set[0][0],
                                            card_set[1][2:])]
    elif ('magic' in card_set and
          ('2012' in card_set or
           '2013' in card_set or
           '2011' in card_set or
           '2010' in card_set)):
        card_set = card_set.split()
        card_set = ["{0}-{1}-{2}{3}".format(card_set[0],
                                            card_set[1],
                                            card_set[0][0],
                                            card_set[1][2:])]
    elif 'event deck' in card_set:
        card_set = ['magic-modern-event-deck']
    elif 'ravnica:' in card_set:
        card_set = ['ravnica']
    elif 'game day' in card_set:
        card_set = ['game-day-promos']
    elif 'wpn' in card_set:
        card_set = ['wpn-promos', 'gateway-promos']
    elif 'friday' in card_set:
        card_set = ['fnm-promos']
    elif ('promos' in card_set or
          'intro pack' in card_set):
        card_set = ['unique-and-miscellaneous-promos']
    elif '2015 edition' in card_set:
        card_set = ['modern-masters-2015']
    elif 'sixth' in card_set:
        card_set = ['6th-edition']
    elif 'seventh' in card_set:
        card_set = ['7th-edition']
    elif 'eighth' in card_set:
        card_set = ['8th-edition']
    elif 'ninth' in card_set:
        card_set = ['9th-edition']
    elif 'tenth' in card_set:
        card_set = ['10th-edition']
    else:
        card_set = re.sub(pattern, '', card_set).split()
        card_set = ['-'.join(ch for ch in card_set)]
    if (card_set == 'fifth-edition' and card == 'urzas-power-plant-columns'):
        card = 'urzas-power-plant'
    elif (card_set == 'fifth-edition' and card == 'urzas-mine-mouth'):
        card = 'urzas-mine'
    elif (card_set == 'fifth-edition' and card == 'urzas-tower-forest'):
        card = 'urzas-tower'
    url_list = ["http://shop.tcgplayer.com/magic/{0}/{1}".format(
        each, card) for each in card_set]
    return url_list


def price(table):
    names = [d.text.strip().lower() for d in table.select(
        '.priceGuidePricePointName')]
    prices = [float(d.text.strip('$')) for d in table.select(
        '.priceGuidePricePointData') if d.text.strip() != 'N/A']
    return dict(zip(names, prices))


def get_prices(card):
    urls = get_url(card[1], card[2])
    try:
        return next(filter(None, map(try_get_prices, urls)))
    except:
        exit(urls)


def try_get_prices(url):
    sleep(uniform(0.5, 2))
    page = get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    try:
        market_div, _, _, median_div = soup.select('.priceGuidePricePointDiv')
    except ValueError:
        return None
    prices = {
        'market': price(market_div),
        'median': price(median_div),
        'date': str(date.today())
    }
    return prices


def main():
    print('Beginning gathering of prices...')
    if not os.path.exists('card_prices.txt'):
        open('card_prices.txt', 'w').close()
    with open('card_prices.txt', 'rb') as f:
        try:
            result = pickle.load(f)
        except:
            result = {}
        f.close()
    for card in inventory:
        if (card[1], card[2].strip()) not in result:
            cardset = card[2].strip()
            result[(card[1], cardset)] = get_prices(card)
            result[(card[1], cardset)]['foil'] = card[3]
            result[(card[1], cardset)]['inventory'] = card[0]
            print((card[1], cardset), result[card[1], cardset])
            with open('card_prices.txt', 'wb') as f:
                pickle.dump(result, f)
                f.close()
        elif ((card[1], card[2].strip()) in result and
              result[(card[1], card[2].strip())]['inventory'] != card[0] and
              result[(card[1], card[2].strip())]['foil'] == card[3]):
            cardset = card[2].strip()
            result[(card[1], cardset)]['inventory'] += card[0]
            print((card[1], cardset), result[card[1], cardset])
            with open('card_prices.txt', 'wb') as f:
                pickle.dump(result, f)


if __name__ == '__main__':
    main()
