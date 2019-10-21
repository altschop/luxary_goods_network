from twitter.twitter_client import TwitterClient
from solelinks.solelink_info_scraper import ShoeInfoScraper
from image_scraper.google_scraper import GoogleScraper


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
    shoe_info_scraper = ShoeInfoScraper()
    shoes = shoe_info_scraper.getShoeInfos()
    shoe_names = [shoe.name for shoe in shoes]
    print(len(shoe_names))
    print(shoe_names)

    image_scraper = GoogleScraper()
    image_scraper.scrape_images(shoe_names)


if __name__ == '__main__':
    main()
