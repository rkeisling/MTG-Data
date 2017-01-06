import scrape_deckbox
import get_prices
import put_in_db

if __name__ == '__main__':
    scrape_deckbox.main()
    get_prices.main()
    put_in_db.main()
