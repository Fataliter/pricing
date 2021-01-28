import requests
from bs4 import BeautifulSoup as bs

GAMES = {
    'Trine 3': ['319910/Trine_3_The_Artifacts_of_Power/'],
    'Trine 4': ['690640/Trine_4_The_Nightmare_Prince/', '1444560/Trine_4_Melody_of_Mystery/'],
    'Portal 2': ['620/Portal_2/'],
    'Grim Dawn': ['219990/Grim_Dawn/']
}


class Steam:

    def __init__(self):
        self.url = 'https://store.steampowered.com/app/'

    def run(self):
        prices = {}
        for game, game_urls in GAMES.items():
            prices[game] = {}
            for url in game_urls:
                response = requests.get(self.url + url)
                bs_content = bs(response.text, "html.parser")
                content = bs_content.find('div', { 'class': 'page_content_ctn' })
                name_from_site = content.find('div', { 'class': 'apphub_AppName' }).getText().strip()
                prices[game][name_from_site] = {}

                purchases = content.find_all('div', { 'class': 'game_area_purchase_game_wrapper' })

                purchase = purchases[0]
                for p in purchases:
                    name = p.find('h1').getText().strip()
                    if len(name.replace('Buy ', '')) <= len(name_from_site):
                        purchase = p
                        break

                discount_block = purchase.find('div', { 'class': 'game_purchase_discount' })

                if discount_block is not None:
                    prices[game][name_from_site]['dsc'] = {
                        'pct': discount_block.find('div', { 'class': 'discount_pct' }).getText().strip(),
                        'original_price': discount_block.find('div', { 'class': 'discount_original_price' }).getText().strip(),
                        'final_price': discount_block.find('div', {'class': 'discount_final_price'}).getText().strip()
                    }
                else:
                    prices[game][name_from_site]['orig'] = {
                        'original_price': purchase.find('div', { 'class': 'game_purchase_price price' }).getText().strip()
                    }

        return prices
