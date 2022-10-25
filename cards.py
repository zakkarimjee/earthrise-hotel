
## module 1: getting card images from netrunnerdb
# I mean - uuuhhh - running NISEI R&D to steal their assets
import requests
import shutil
import os
import json
import pandas as pd



def get_cards_json(url_cards = "https://netrunnerdb.com/api/2.0/public/cards", cache_file = "cards.json"):
    if os.path.exists(cache_file):
        print("Using cached card data")
        data_cards = open(cache_file,"r",encoding='utf-8')
        json_cards = json.load(data_cards)
    else:
        print("Running remote: " + url_cards)
        response_cards = requests.get(url_cards)
        json_cards = response_cards.json()
        data_cards = response_cards.content
        with open(cache_file,"wb") as out_file:
            out_file.write(data_cards)
    return json_cards

def get_cards_dataframe():
    json = get_cards_json()["data"]
    df = pd.DataFrame(json)
    df.set_index("code",inplace=True)
    return df

def get_card_info(id):
    cards = get_cards_dataframe()
    return cards.loc["{:05d}".format(id)]



def get_card_image(id):
    # pad it to a 5 digit string
    id_string = "{:05d}".format(id)

    # get card json
    json_cards = get_cards_json()
    # get the url of the card
    url_card_image = json_cards["imageUrlTemplate"].format(code=id_string)
    # generate a filename for the card
    output_filename = "cards/" + url_card_image.split("/")[-1]
    # find the name of the card
    card_info = get_card_info(id)
    print(card_info["title"])
    # check if we already have the card downloaded
    if os.path.exists(output_filename):
        print("Cached at: " + output_filename)
        return True
    else:
        print("Running remote: " + url_card_image)
        try:
            response_image = requests.get(url_card_image, stream=True)
            with open(output_filename, 'wb') as out_file:
                shutil.copyfileobj(response_image.raw, out_file)
        except:
            return False
        return True

if __name__ == "__main__":
    print("Getting card 60")
    get_card_image(60)


