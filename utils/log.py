import logging
import os
import sys
from datetime import datetime

class TimeContext:
    current_sim_time = None 

class DynamicTimeFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        if TimeContext.current_sim_time:
            if isinstance(TimeContext.current_sim_time, datetime):
                return TimeContext.current_sim_time.strftime(datefmt or '%Y-%m-%d %H:%M:%S')
            return str(TimeContext.current_sim_time)
        
        return super().formatTime(record, datefmt)

def thiet_lap_logger():
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'du_lieu')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    logger = logging.getLogger("CryptoBot")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        formatter = DynamicTimeFormatter('%(asctime)s - %(levelname)s - %(message)s')
        
        file_handler = logging.FileHandler(os.path.join(log_dir, 'nhat_ky_hoat_dong.log'), encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        
    return logger

def set_log_time(dt):
    """Goi ham nay dau moi vong lap nen de set thoi gian"""
    TimeContext.current_sim_time = dt

def reset_log_time():
    """Goi ham nay khi chay Realtime hoac ket thuc Backtest"""
    TimeContext.current_sim_time = None

logger = thiet_lap_logger()