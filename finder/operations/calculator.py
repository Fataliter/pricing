class Calculator:

    def __init__(self, prices):
        self.prices = prices

    def run(self):
        dsc = self.discounted()
        print(dsc)

    def discounted(self):
        dsc = {}
        for game, platforms in self.prices.items():
            for p_game in platforms:
                if 'dsc' in p_game:
                    if game not in dsc: dsc[game] = []
                    dsc[game].append(p_game)

        return dsc

