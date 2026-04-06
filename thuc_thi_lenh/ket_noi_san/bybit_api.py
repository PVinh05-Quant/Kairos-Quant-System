import ccxt
from utils.doc_cau_hinh import lay_cau_hinh_api
from utils.log import logger

class BybitAPI:
    def __init__(self):
        configs = lay_cau_hinh_api()
        if 'bybit' in configs:
            self.exchange = ccxt.bybit(configs['bybit'])
            self.exchange.load_markets()
        else:
            self.exchange = None

    def doi_don_bay(self, symbol, leverage):
        try:
            # Bybit thường yêu cầu set leverage cho cả Buy và Sell side
            return self.exchange.set_leverage(leverage, symbol)
        except Exception as e:
            # Bybit hay báo lỗi nếu leverage đã được set giống như cũ, ta bỏ qua lỗi này
            if "leverage not modified" not in str(e).lower():
                logger.error(f"Lỗi set leverage Bybit: {e}")
            return None

bybit_connector = BybitAPI()