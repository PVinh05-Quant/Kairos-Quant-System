from thuc_thi_lenh.bo_may_thuc_thi import quan_ly_san
from utils.log import logger

def kiem_tra_trang_thai_vi_the(san, symbol):
    exchange = quan_ly_san.lay_san(san)
    if not exchange: return None

    try:
        positions = exchange.fetch_positions([symbol])
        for pos in positions:
            # Kiểm tra size > 0 để đảm bảo là vị thế đang mở
            size = float(pos['contracts']) if 'contracts' in pos else float(pos['info'].get('size', 0))
            if size > 0 and pos['symbol'] == symbol:
                return {
                    'pnl_percent': float(pos['percentage']),
                    'pnl_amount': float(pos['unrealizedPnl']),
                    'side': pos['side'],
                    'entry_price': float(pos['entryPrice']),
                    'amount': size
                }
        return None # Không có vị thế
    except Exception as e:
        logger.error(f"Lỗi theo dõi vị thế {symbol}: {e}")
        return None