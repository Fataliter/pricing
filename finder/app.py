from finder.platforms.steam import Steam
from finder.platforms.gog import Gog
from finder.platforms.fanatical import Fanatical
from finder.platforms.humble import Humble
from finder.platforms.gamersgate import Gamersgate

def run():
    steam = Steam().run()
    # gog = Gog().run()
    # fanatical = Fanatical().run()
    # humble = Humble().run()
    # gamersgate = Gamersgate().run()

    print(steam)
    # print(gog)
    # print(fanatical)
    # print(humble)
    # print(gamersgate)
