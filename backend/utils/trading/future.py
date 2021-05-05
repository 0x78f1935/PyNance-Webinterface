from backend.utils.trading import Trading

class Futures(Trading):
    def __init__(self):
        Trading.__init__(self)

    @property
    def get_active_symbols(self):
        target_symbols = []
        for item in self.bot.orders:
            if item.symbol in self.bot.config.symbols and item.active and not item.spot:
                target_symbols.append(item.symbol)
        return list(set([i for i in self.bot.config.symbols] + target_symbols))