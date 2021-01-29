from finder.platforms.steam import Steam
from finder.platforms.gog import Gog
from finder.platforms.fanatical import Fanatical
from finder.platforms.humble import Humble
from finder.platforms.gamersgate import Gamersgate

def run():
    prices = {}
    prices['steam'] = Steam().run()
    prices['gog'] = Gog().run()
    prices['gamersgate'] = Gamersgate().run()

    # prices['fanatical'] = Fanatical().run()
    # prices['humble'] = Humble().run()

    print(prices)
