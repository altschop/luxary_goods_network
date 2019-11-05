from twitter.twitter_client import TwitterClient
from solelinks.solelink_info_scraper import ShoeInfoScraper
from image_scraper.google_scraper import GoogleScraper
from neural_network.cnn import CNN
from os import listdir
import shutil


def get_twitter_analysis_map():
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
    shoe_info_scraper = ShoeInfoScraper()
    shoes = shoe_info_scraper.get_shoe_infos(num_shoes)
    shoe_names = [shoe.name for shoe in shoes]

    image_scraper = GoogleScraper()
    image_scraper.scrape_images(shoe_names, 400)
    return shoe_names


def run_network(shoe_names):
    network = CNN(shoe_names)
    network.run_all_networks()


def clear_data():
    shutil.rmtree("./train_data")
    shutil.rmtree("./test_data")
    shutil.rmtree("./npy_data")


def main():
    # clear_data()
    # shoe_names = get_and_collect_shoes(1000)
    shoe_names = get_current_shoes_loaded()
    print(len(shoe_names))
    run_network(shoe_names)


def get_current_shoes_loaded():
    shoe_names = []
    for filename in listdir("./train_data"):
        shoe_names.append(filename)

    return shoe_names


if __name__ == '__main__':
    main()
