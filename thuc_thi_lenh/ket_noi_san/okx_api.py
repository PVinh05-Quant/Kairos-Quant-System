import ccxt
from utils.doc_cau_hinh import lay_cau_hinh_api
from utils.log import logger

class OkxAPI:
    def __init__(self):
        configs = lay_cau_hinh_api()
        if 'okx' in configs:
            self.exchange = ccxt.okx(configs['okx'])
            self.exchange.load_markets()
        else:
            self.exchange = None
        print(configs['okx'])


    def doi_don_bay(self, symbol, leverage):
        try:
            return self.exchange.set_leverage(leverage, symbol, params={'mgnMode': 'cross'})
        except Exception as e:
            logger.error(f"Lỗi set leverage OKX: {e}")
            return None

okx_connector = OkxAPI()

