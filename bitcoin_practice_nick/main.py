from twitter.twitter_client import TwitterClient
from solelinks.solelink_info_scraper import ShoeInfoScraper
from image_scraper.google_scraper import GoogleScraper
from neural_network.cnn import CNN
from neural_network.image_processor import *
from os import listdir
import shutil


def getTwitterAnalysisMap():
    shoe_info_scraper = ShoeInfoScraper()
    shoes = shoe_info_scraper.getShoeInfos(0)

    twitter_client = TwitterClient()

    shoe_analysis_map = {}
    for shoe in shoes:
        sentiments = twitter_client.get_sentiments_for_query(shoe.name)
        if sentiments is not None:
            shoe_analysis_map.update(sentiments)

    return shoe_analysis_map


def get_and_collect_shoes(num_shoes):
    shutil.rmtree("./train_data")
    shutil.rmtree("./test_data")
    shutil.rmtree("./npy_data")

    shoe_info_scraper = ShoeInfoScraper()
    shoes = shoe_info_scraper.getShoeInfos(num_shoes)
    shoe_names = [shoe.name for shoe in shoes]
    print(len(shoe_names))
    print(shoe_names)

    image_scraper = GoogleScraper()
    image_scraper.scrape_images(shoe_names, 200)
    return shoe_names


def run_network(shoe_names):
    network = CNN(shoe_names)
    network.run_network()


def main():
    # shoe_names = get_and_collect_shoes(100)
    shoe_names = get_current_shoes_loaded()
    # print(len(shoe_names))
    run_network(shoe_names)


def get_current_shoes_loaded():
    shoe_names = []
    for filename in listdir("./train_data"):
        print(filename)
        shoe_names.append(filename)

    return shoe_names


if __name__ == '__main__':
    main()
