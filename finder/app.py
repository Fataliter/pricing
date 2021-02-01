from finder.platforms.steam import Steam
from finder.platforms.gog import Gog
from finder.platforms.fanatical import Fanatical
from finder.platforms.humble import Humble
from finder.platforms.gamersgate import Gamersgate

from finder.operations.calculator import Calculator

def run():
    prices = {}
    prices = Steam(prices).run()
    prices = Gog(prices).run()
    prices = Gamersgate(prices).run()

    # prices = Fanatical(prices).run()
    # prices = Humble(prices).run()

    # print(prices)
    Calculator(prices).run()

