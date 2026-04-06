import sys
import os
import pandas as pd
import ta
from datetime import datetime
# --- IMPORT RICH ---
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
from rich.live import Live


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

try:
    from utils.log import logger
    from utils.doc_cau_hinh import lay_cau_hinh_giao_dich, lay_cau_hinh_ao
    from lay_du_lieu.lay_ohlcv import gop_nen, tai_du_lieu_lich_su, chuan_bi_du_lieu_da_khung
    from ml.tool.data_filter import tao_log_can_bang
    from ml.trang_thai_thi_truong_ml.ml_model import huan_luyen_model
    from ml.trang_thai_thi_truong_ml.ml_predict import du_doan_trang_thai_ml, danh_gia_ml, STATE_MAP
    from ml.tool.trading_teacher import trang_thai_thi_truong_ky_thuat
except ImportError as e:
    print(f"❌ Lỗi Import: {e}")
    sys.exit(1)

def tao_model_lan_dau():
    config_backtest = lay_cau_hinh_ao()
    config_trading = lay_cau_hinh_giao_dich()
    
    START_DATE = config_backtest.get('ngay_bat_dau')
    END_DATE = config_backtest.get('ngay_ket_thuc')
    DS_SYMBOL = config_trading.get('cap_giao_dich')

    symbol = DS_SYMBOL[0] 

    df_goc = tai_du_lieu_lich_su(symbol, START_DATE, END_DATE)

    dfs = chuan_bi_du_lieu_da_khung(df_goc, END_DATE)

    df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d = dfs

    huan_luyen_model(df_1m, df_3m, df_5m, df_15m, df_30m, df_1h)

console = Console()
def chay_training_cap_toc():
    config_backtest = lay_cau_hinh_ao()
    config_trading = lay_cau_hinh_giao_dich()
    
    START_DATE = config_backtest.get('ngay_bat_dau', '2025-01-01')
    END_DATE = config_backtest.get('ngay_ket_thuc', '2025-01-31')
    DS_SYMBOL = config_trading.get('cap_giao_dich', ['BTC/USDT'])

    with Live(console=console, refresh_per_second=10) as live:
        
        for symbol in DS_SYMBOL:
            
            df_goc = tai_du_lieu_lich_su(symbol, START_DATE, END_DATE)
            if df_goc.empty: continue

            idx_start = 43200 
            if len(df_goc) < idx_start: continue
            timestamps = df_goc.index[idx_start:]
            
            # Khởi tạo bộ đếm
            stats = {'correct': 0, 'wrong': 0}
            class_stats = {k: {'correct': 0, 'total': 0} for k in STATE_MAP.keys()}

            
            for current_time in timestamps:
                dfs = chuan_bi_du_lieu_da_khung(df_goc, current_time)
                if not dfs: continue


                df_1m, df_3m, df_5m, df_15m, df_30m, df_1h, df_4h, df_1d = dfs

                packet = du_doan_trang_thai_ml(df_1m, df_3m, df_5m, df_15m, df_30m, df_1h)
                if packet is None: continue
                conf = packet['confidence']
                ai_state = packet['state_id']
                teacher_state, teacher_conf = trang_thai_thi_truong_ky_thuat(df_1m, df_3m, df_5m, df_15m, df_30m, df_1h)
                
                # Cập nhật thông tin để hiển thị
                class_stats[teacher_state]['total'] += 1
                
                if ai_state == teacher_state: #== 5 or ai_state == teacher_state == 3:
                    stats['correct'] += 1
                    class_stats[teacher_state]['correct'] += 1
                    danh_gia_ml(packet, 1, 0, teacher_state)
                else:
                    stats['wrong'] += 1
                    danh_gia_ml(packet, -0.5, 0, teacher_state)

                layout = hien_thi_dashboard(symbol, current_time, stats, class_stats, ai_state, teacher_state, teacher_conf, conf)
                live.update(layout)

            console.print(f"[bold green]✅ HOÀN TẤT TRAINING {symbol}![/]")

def hien_thi_dashboard(symbol, current_time, stats, class_stats, ai_state, teacher_state, teacher_conf, conf):

    SHORT_NAMES = {
        0: "Noise",             #Nhiễu (hoặc "Rác")
        1: "Trend_following",   #Có xu hướng (Trending)
        2: "Mean_reversion",    #Đi ngang (Sideways / Ranging)
        3: "Squeeze",           #Tích lũy / Nén (Consolidation)
        4: "Breakout",          #Bùng nổ (Expansion)
        5: "Scalping"           #Biến động hỗn loạn (Choppy/Volatile)
    }

    total = stats['correct'] + stats['wrong']
    global_acc = (stats['correct'] / total * 100) if total > 0 else 0.0
    
    ai_text = SHORT_NAMES.get(ai_state, str(ai_state))
    tc_text = SHORT_NAMES.get(teacher_state, str(teacher_state))
    
    is_match = ai_state == teacher_state
    status_color = "bold green" if is_match else "bold red"
    icon = "✅ MATCH" if is_match else "❌ DIFF"

    table = Table(box=box.SIMPLE, expand=True, border_style="blue")
    table.add_column("Trạng Thái", style="cyan", no_wrap=True)
    table.add_column("Tỷ Lệ (Đ/T)", justify="center")
    table.add_column("Chính Xác", justify="right")
    table.add_column("Biểu Đồ", ratio=1) 

    for state_id in sorted(class_stats.keys()):
        val = class_stats[state_id]
        if val['total'] == 0: continue

        name = SHORT_NAMES.get(state_id, str(state_id))
        acc = (val['correct'] / val['total'] * 100)
        fraction = f"{val['correct']}/{val['total']}"
        
        # Thanh Bar
        bar_len = 20
        filled = int(acc / 100 * bar_len)
        bar_str = "█" * filled + "░" * (bar_len - filled)
        color_bar = "[green]" if acc > 50 else "[yellow]" if acc > 30 else "[red]"
        
        table.add_row(name, fraction, f"{acc:.1f}%", f"{color_bar}{bar_str}[/]")

    # B. Panel Thông tin Live
    live_info = Text()
    live_info.append("🤖 AI Dự Đoán : ", style="bold white")
    live_info.append(f"{ai_text:<8} : {conf * 100:.2f}%", style="cyan")
    live_info.append("  vs  ", style="dim")
    live_info.append("👨‍🏫 Thầy Phán : ", style="bold white")
    live_info.append(f"{tc_text:<8} : {teacher_conf:.2f}", style="magenta")
    live_info.append(f"\n\n   KẾT QUẢ: ", style="bold white")
    live_info.append(f"{icon}", style=status_color)

    live_panel = Panel(
        Align.center(live_info, vertical="middle"),
        title="⚡ LIVE FEED",
        border_style="yellow",
        height=8
    )

    stats_text = Text()
    stats_text.append(f"{global_acc:.2f}%", style="bold green" if global_acc > 50 else "bold red")
    stats_text.append("\nGlobal Accuracy", style="dim")
    stats_text.append(f"\n\nSample Size: {total}", style="white")

    stats_panel = Panel(
        Align.center(stats_text, vertical="middle"),
        title="🎯 PERFORMANCE",
        border_style="green",
        height=8
    )

    grid = Table.grid(expand=True)
    grid.add_column(ratio=1)
    grid.add_column(ratio=2)
    grid.add_row(stats_panel, live_panel)

    final_layout = Layout()
    final_layout.split_column(
        Layout(name="header", size=3),
        Layout(name="upper", size=8),
        Layout(name="lower")
    )
    
    final_layout["header"].update(
        Panel(Align.center(f"KAIROS QUANT SYSTEM - {symbol} - {current_time}", vertical="middle"), style="bold white on blue")
    )
    final_layout["upper"].update(grid)
    final_layout["lower"].update(Panel(table, title="📈 BREAKDOWN BY STATE", border_style="blue"))

    return final_layout


def main():
    print("=== CHỌN CHỨC NĂNG ===")
    print("1. Tạo model lần đầu")
    print("2. Chạy training cấp tốc")
    print("3. Tự động học từ log")
    print("4. Lọc dữ liệu lệnh thắng từ log")
    print("0. Thoát")

    choice = input("Nhập lựa chọn: ").strip()

    if choice == "1":
        tao_model_lan_dau()

    elif choice == "2":
        chay_training_cap_toc()

    elif choice == "3":
        from ml.trang_thai_thi_truong_ml.ml_model import tu_dong_hoc_tu_log
        tu_dong_hoc_tu_log()

    elif choice == "4":
        tao_log_can_bang()


    elif choice == "0":
        print("Thoát chương trình.")

    else:
        print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
