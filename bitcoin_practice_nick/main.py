from twitter.twitter_client import TwitterClient
from twitter.solelink_info_scraper import ShoeInfoScraper
from stockx.stockx_client import StockXClient


def getTwitterAnalysisMap():
    shoe_info_scraper = ShoeInfoScraper()
    shoes = shoe_info_scraper.getShoeInfos()

    return None
    twitter_client = TwitterClient()

    shoe_analysis_map = {}
    for shoe in shoes:
        sentiments = twitter_client.get_sentiments_for_query(shoe.name)
        if sentiments is not None:
            shoe_analysis_map.update(sentiments)

    return shoe_analysis_map


def main():
    shoe_analysis_map = getTwitterAnalysisMap()
    #stockx_client = StockXClient()
    #stockx_client.getShoes()


if __name__ == '__main__':
    main()
