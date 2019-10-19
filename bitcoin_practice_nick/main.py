from models.twitter_client import TwitterClient
from models.shoe_info_scraper import ShoeInfoScraper


def main():
    shoe_info_scraper = ShoeInfoScraper()
    shoes = shoe_info_scraper.getShoeInfos()

    twitter_client = TwitterClient()

    shoe_analysis_map = {}
    for shoe in shoes:
        sentiments = twitter_client.get_sentiments_for_query(shoe.name)
        print(sentiments)
        if sentiments is not None:
            shoe_analysis_map.update(sentiments)

    print(shoe_analysis_map)


if __name__ == '__main__':
    main()
