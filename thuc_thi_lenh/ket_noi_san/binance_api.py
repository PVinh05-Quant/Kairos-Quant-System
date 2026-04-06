import ccxt
from utils.doc_cau_hinh import lay_cau_hinh_api
from utils.log import logger

class BinanceAPI:
    def __init__(self):
        configs = lay_cau_hinh_api()
        if 'binance' in configs:
            self.exchange = ccxt.binance(configs['binance'])
            self.exchange.load_markets()
        else:
            self.exchange = None

    def doi_don_bay(self, symbol, leverage):
        try:
            return self.exchange.set_leverage(leverage, symbol)
        except Exception as e:
            logger.error(f"Lỗi set leverage Binance: {e}")
            return None

    def dat_lenh(self, symbol, side, amount, price=None):
        if not self.exchange: return None
        type = 'limit' if price else 'market'
        return self.exchange.create_order(symbol, type, side, amount, price)

binance_connector = BinanceAPI()