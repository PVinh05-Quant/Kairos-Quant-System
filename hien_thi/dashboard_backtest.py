import sys
import os
import random
import calendar
from datetime import datetime
import math
import polars as pl

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
try:
    from chuc_nang.backtest_donluong import chay_backtest
except ImportError:
    pass

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFrame, QDockWidget, QSizePolicy, 
                             QGraphicsDropShadowEffect, QScrollArea, QGridLayout, QToolBar)
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPolygonF, QPainterPath, QLinearGradient, QFontMetrics
from PyQt6.QtCore import Qt, QRectF, QPointF, QTimer, QThread, pyqtSignal
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QFileDialog, QMessageBox

def funny_quant_runner():
    # --- CẤU HÌNH LOGIC ---
    if not hasattr(funny_quant_runner, "frames"):
        frames = []
        WIDTH = 120  # Sân khấu rộng
        
        # --- HÀM TIỆN ÍCH ---
        def add_frame(content):
            frames.append(content)

        def add_static_scene(icon_list, pos, repeat=1):
            for _ in range(repeat):
                for icon in icon_list:
                    safe_pos = max(0, min(pos, WIDTH - len(icon)))
                    add_frame(" " * safe_pos + icon)

        def add_run(icon, start, end, step=2):
            if start < end:
                rng = range(start, end, step)
            else:
                rng = range(start, end, -step) if step > 0 else range(start, end, step)
            for x in rng:
                safe_x = max(0, min(x, WIDTH - len(icon)))
                add_frame(" " * safe_x + icon)

        zombie_morning = [
            "( 🧟‍♂️ ) ... não... cần... code...",
            "( 🕸️_🕸️ ) ... cà... phê... đâu...",
            "( 😵‍💫 ) ☕ *ực ực*",
            "( 😳 ) ⚡KÍCH HOẠT⚡"
        ]
        add_static_scene(zombie_morning, 10, repeat=2)
        add_run("🏃💨( >﹏<) Đợi em!!", 0, 90, step=4)
        boring_phase = [
            "( •_•) 📉 ...",
            "( -_-) 📉 buồn ngủ...",
            "( o_o) 📈 Ơ?"
        ]
        add_static_scene(boring_phase, 50, repeat=3)
        pump_phase = [
            "( 😲 ) 🚀 LÊN KÌA!!",
            "( 🤪 ) 🚀 TO THE MOON!!",
            "( 🤩 ) 💰 Tiền đè chết người!!"
        ]
        add_static_scene(pump_phase, 50, repeat=3)
        dump_phase = [
            "( 😨 ) 📉 Ủa...",
            "( 😱 ) 📉 RỚT MẠNG RỒI?!",
            "( 💀 ) 💸 Cháy tài khoản..."
        ]
        add_static_scene(dump_phase, 50, repeat=3)
        stress_icons = [
            "   ( 🤯 ) 🔥 BUG Ở ĐÂU???",
            " ( 🤯 )   🔥 TẠI SAO???",
            "   ( 🌋 ) 💣 BÙMMMM!!!!"
        ]
        for _ in range(5):
            for icon in stress_icons:
                 add_frame(" " * 48 + icon)
        holy_grail = [
            "( ¬‿¬ ) He he he...",
            "( ⌐■_■ ) Đã tìm ra Bug...",
            "( ✨‿✨ ) All-in lệnh này!"
        ]
        add_static_scene(holy_grail, 50, repeat=3)

        eating = [
            "( 🍜 ) sụp soạp...",
            "( 🤤 ) ngon vãi...",
            "( 🤢 ) ợ..."
        ]
        add_static_scene(eating, 80, repeat=3)

        add_run("🕺(⌐■_■)✨ Tối nay quẩy!", 100, 10, step=3)

        sleep_fail = [
            "( ◡‿◡ ) Nhà đây rồ...",
            "( x_x ) *RẦM* (Ngã sấp mặt)",
            "( 💤_💤 ) Zzzzz..."
        ]
        add_static_scene(sleep_fail, 10, repeat=4)

        funny_quant_runner.frames = frames
        funny_quant_runner.i = 0

    frame = funny_quant_runner.frames[funny_quant_runner.i]
    funny_quant_runner.i = (funny_quant_runner.i + 1) % len(funny_quant_runner.frames)
    
    return frame

# =================================================================================
# CẤU HÌNH THEME "PRO TERMINAL" (PHẦN BỊ THIẾU GÂY LỖI)
# =================================================================================
BG_COLOR = "#0e0e0e"        # Nền App siêu tối
CARD_BG = "#141414"         # Nền Card
BORDER_COLOR = "#2a2a2a"    # Viền tối tinh tế
TEXT_MAIN = "#E0E0E0"       # Trắng xám
TEXT_SUB = "#999999"        # Xám mờ
ACCENT_COLOR = "#C8AA6E"    # Vàng đồng
COLOR_WIN = "#4CAF50"       # Xanh lá
COLOR_LOSS = "#E53935"      # Đỏ
GRID_COLOR = "#2a2a2a"      # Lưới mờ

# Font Configuration
FONT_TITLE = QFont("Segoe UI", 10, QFont.Weight.Bold)
FONT_VAL_BIG = QFont("Segoe UI", 20, QFont.Weight.Bold)
FONT_VAL_NORM = QFont("Segoe UI", 11, QFont.Weight.Bold)
FONT_LABEL = QFont("Segoe UI", 9)
FONT_SUB = QFont("Segoe UI", 8)

# =================================================================================
# DRAGGABLE CARD (DOCK WIDGET)
# =================================================================================
class DraggableCard(QDockWidget):
    def __init__(self, title, widget, parent=None):
        super().__init__(title, parent)
        self.setWidget(widget)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | 
                         QDockWidget.DockWidgetFeature.DockWidgetFloatable |
                         QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        
        self.setWindowTitle(title.upper()) 
        self.setTitleBarWidget(None) 

        self.setStyleSheet(f"""
            QDockWidget {{
                border: 1px solid {BORDER_COLOR};
                border-radius: 4px;
                color: {TEXT_MAIN};
            }}
            QDockWidget::title {{
                background: {CARD_BG};
                text-align: left;
                padding-left: 12px;
                padding-top: 8px;
                padding-bottom: 8px;
                border-bottom: 1px solid {BORDER_COLOR};
                color: {TEXT_SUB};
                font-family: "Segoe UI";
                font-weight: bold;
                font-size: 11px;
            }}
            QDockWidget::close-button, QDockWidget::float-button {{
                border: none;
                background: transparent;
                padding: 0px;
                icon-size: 14px;
                subcontrol-position: right;
                subcontrol-origin: margin;
                right: 5px;
            }}
            QDockWidget::close-button:hover, QDockWidget::float-button:hover {{
                background: #333;
                border-radius: 3px;
            }}
        """)

# =================================================================================
# WORKER THREAD (CHẠY BACKTEST NGẦM)
# =================================================================================
class BacktestWorker(QThread):
    progress_signal = pyqtSignal(dict)
    finished_signal = pyqtSignal(dict)

    def run(self):
        def on_live_update(data):
            self.progress_signal.emit(data)

        try:
            result = chay_backtest(return_data=True, callback=on_live_update)
            self.finished_signal.emit(result)
        except Exception as e:
            print(f"Lỗi Backtest: {e}")
            self.finished_signal.emit({})

# =================================================================================
# Widget Biểu đồ Phân Phối
# =================================================================================
class DistributionChart(QWidget):
    bar_clicked = pyqtSignal(int, str)

    def __init__(self, chart_type="day"):
        super().__init__()
        self.chart_type = chart_type
        self.setMinimumHeight(150)
        self.selected_index = None 
        
        if self.chart_type == "day":
            self.labels = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
            self.data = [0.0] * 7
        else:
            self.labels = [f"{i}h" for i in range(24)]
            self.data = [0.0] * 24

        self.update_data()

    def update_data(self, df: pl.DataFrame = None, current_filter_idx=None):
        self.selected_index = current_filter_idx
        count = 7 if self.chart_type == "day" else 24
        
        # Reset data về 0
        if df is None or df.is_empty():
            self.data = [0.0] * count
            self.update()
            return

        try:
            col_name = "filter_weekday" if self.chart_type == "day" else "filter_hour"
            
            if col_name not in df.columns:
                self.update(); return

            grp = (
                df.group_by(col_name)
                .agg(pl.col("pnl_usd").sum().round(2).alias("sum_pnl"))
            )
            
            grp_dict = dict(zip(grp[col_name].to_list(), grp["sum_pnl"].to_list()))

            if self.chart_type == "day":
                self.data = [float(grp_dict.get(i + 1, 0.0)) for i in range(7)]
            else:
                self.data = [float(grp_dict.get(i, 0.0)) for i in range(24)]

        except Exception as e:
            print(f"Lỗi DistributionChart ({self.chart_type}): {e}")
            self.data = [0.0] * count
        
        self.update()

    def mousePressEvent(self, event):
        w = self.width()
        margin = 16
        draw_w = w - 2 * margin
        count = len(self.data)
        if count == 0: return

        col_w = draw_w / count
        mouse_x = event.position().x() - margin
        
        index = int(mouse_x // col_w)
        
        if 0 <= index < count:
            if self.selected_index == index:
                self.selected_index = None
                self.bar_clicked.emit(-1, self.chart_type) 
            else:
                self.selected_index = index
                self.bar_clicked.emit(index, self.chart_type)
            self.update()

    def paintEvent(self, event):
        if not hasattr(self, 'data') or not self.data:
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor(CARD_BG))
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(CARD_BG))

        w, h = self.width(), self.height()
        margin = 16
        draw_rect = QRectF(margin, margin, w - 2*margin, h - 2*margin - 10) 
        
        bar_count = len(self.data)
        if bar_count == 0: return

        bar_w_total = draw_rect.width() / bar_count
        bar_gap = 6 if self.chart_type == "day" else 2
        bar_w = bar_w_total - bar_gap
        
        max_abs_val = max([abs(x) for x in self.data]) or 1.0
        zero_y = draw_rect.center().y()

        painter.setPen(QPen(QColor(GRID_COLOR), 1, Qt.PenStyle.DashLine))
        painter.drawLine(int(draw_rect.left()), int(zero_y), int(draw_rect.right()), int(zero_y))

        for i, val in enumerate(self.data):
            x = draw_rect.left() + i * bar_w_total + bar_gap / 2
            h_val = (abs(val) / max_abs_val) * (draw_rect.height() / 2)
            
            # Chọn màu
            if val >= 0:
                color = QColor(COLOR_WIN)
                rect = QRectF(x, zero_y - h_val, bar_w, h_val)
            else:
                color = QColor(COLOR_LOSS)
                rect = QRectF(x, zero_y, bar_w, h_val)
            
            # Xử lý hiệu ứng Highlight / Dim
            if self.selected_index is not None:
                if self.selected_index == i:
                    color.setAlpha(255) # Sáng rõ
                    painter.setPen(QPen(QColor("#FFFFFF"))) # Viền trắng
                else:
                    color.setAlpha(50) # Mờ đi
                    painter.setPen(Qt.PenStyle.NoPen)
            else:
                color.setAlpha(200) # Mặc định
                painter.setPen(Qt.PenStyle.NoPen)

            painter.setBrush(color)
            painter.drawRect(rect)
            
            # Vẽ Label (Chỉ vẽ nếu i < len(labels))
            if self.chart_type == "day" or (self.chart_type == "hour" and i % 2 == 0):
                if i < len(self.labels): # Kiểm tra an toàn
                    painter.setPen(QColor(TEXT_SUB))
                    painter.setFont(FONT_SUB)
                    label = self.labels[i] 
                    text_rect = QRectF(x - 5, draw_rect.bottom() + 5, bar_w + 10, 15)
                    
                    if self.selected_index == i:
                        painter.setPen(QColor(ACCENT_COLOR))
                        f = QFont(FONT_SUB); f.setBold(True)
                        painter.setFont(f)

                    painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, label)

# =================================================================================
# Widget Backtest Summary
# =================================================================================
class BacktestSummaryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(250, 380)
        self.update_data()

    def update_data(self, data_packet=None):
        # data_packet có thể là result (khi xong backtest) hoặc dict chứa 'trades' (khi lọc)
        result = data_packet if data_packet else {}
        trades = result.get("trades", [])

        total_trades = len(trades)

        if total_trades > 0:
            df = pl.DataFrame(trades)

            # Ép kiểu để chắc chắn
            df = df.with_columns(
                pl.col("pnl_usd").cast(pl.Float64)
            )

            # ===== TÍNH TOÁN =====
            total_profit = df["pnl_usd"].sum()

            wins = df.filter(pl.col("pnl_usd") > 0)
            losses = df.filter(pl.col("pnl_usd") <= 0)

            win_rate = (wins.height / total_trades) * 100 if total_trades else 0

            avg_win = wins["pnl_usd"].mean() or 0.0
            avg_loss = abs(losses["pnl_usd"].mean() or 0.0)

            profit_factor = (
                wins["pnl_usd"].sum() / abs(losses["pnl_usd"].sum())
                if losses.height > 0 and losses["pnl_usd"].sum() != 0
                else 0.0
            )

            rr_ratio = avg_win / avg_loss if avg_loss > 0 else 0.0
            expectancy = df["pnl_usd"].mean() or 0.0

            # ===== MAX DRAWDOWN =====
            df = df.with_columns(
                pl.col("pnl_usd").cum_sum().alias("cumsum")
            ).with_columns(
                pl.col("cumsum").cum_max().alias("peak")
            ).with_columns(
                (pl.col("cumsum") - pl.col("peak")).alias("drawdown")
            )

            max_dd_val = df["drawdown"].min() or 0.0

        else:
            total_profit = 0.0
            win_rate = 0.0
            profit_factor = 0.0
            expectancy = 0.0
            avg_win = 0.0
            avg_loss = 0.0
            rr_ratio = 0.0
            max_dd_val = 0.0

        # ===== CẬP NHẬT HIỂN THỊ =====
        self.perf_data = [
            ("Tỷ lệ thắng", f"{win_rate:.1f}%", COLOR_WIN if win_rate > 50 else COLOR_LOSS),
            ("Hệ số lợi nhuận", f"{profit_factor:.2f}", TEXT_MAIN),
            ("Sụt giảm (PnL)", f"{max_dd_val:,.2f}$", COLOR_LOSS),
            ("Kỳ vọng / lệnh", f"{expectancy:+.2f}$", TEXT_MAIN),
            ("Lợi nhuận TB", f"{avg_win:+.2f}$", COLOR_WIN),
            ("Thua lỗ TB", f"-{avg_loss:.2f}$", COLOR_LOSS),
            ("Tỷ lệ R:R", f"{rr_ratio:.2f}", TEXT_MAIN),
        ]

        c_profit = COLOR_WIN if total_profit >= 0 else COLOR_LOSS
        self.summary_data = [
            ("TỔNG LỢI NHUẬN", f"{total_profit:+,.2f}$", c_profit),
            ("TỔNG SỐ LỆNH", f"{total_trades}", TEXT_MAIN),
        ]

        self.update()


    def paintEvent(self, event):
        if not hasattr(self, 'perf_data') or not self.perf_data:
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor(CARD_BG))
            painter.setPen(QColor(TEXT_SUB))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No Data Available")
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(CARD_BG))

        w, h = self.width(), self.height()
        margin = 14
        gap = 6

        box1_h = h * 0.62
        box2_h = h - box1_h - margin - gap

        self.draw_section(
            painter,
            QRectF(margin, margin, w - 2 * margin, box1_h),
            title=None,
            data=self.perf_data
        )

        self.draw_section(
            painter,
            QRectF(margin, margin + box1_h + gap, w - 2 * margin, box2_h),
            title="TỔNG KẾT",
            data=self.summary_data,
            is_summary=True
        )

    def draw_section(self, painter, rect, title, data, is_summary=False):
        header_h = 24 if title else 0

        if title:
            painter.setPen(QColor(TEXT_SUB))
            font_title = FONT_LABEL
            font_title.setBold(True)
            painter.setFont(font_title)
            painter.drawText(int(rect.left()), int(rect.top() + 15), title)

            line_y = rect.top() + header_h
            painter.setPen(QPen(QColor(GRID_COLOR), 1))
            painter.drawLine(int(rect.left()), int(line_y), int(rect.right()), int(line_y))
        else:
            line_y = rect.top()

        content_rect = QRectF(
            rect.left(),
            line_y + (8 if title else 0),
            rect.width(),
            rect.height() - header_h
        )

        row_h = min(34, content_rect.height() / len(data)) if len(data) > 0 else 34

        for i, (label, value, color_str) in enumerate(data):
            y = content_rect.top() + i * row_h
            row_rect = QRectF(content_rect.left(), y, content_rect.width(), row_h)

            painter.setPen(QColor(TEXT_SUB))
            painter.setFont(FONT_LABEL)
            painter.drawText(
                row_rect,
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                label
            )

            painter.setPen(QColor(color_str))
            painter.setFont(FONT_VAL_BIG if is_summary and i == 0 else FONT_VAL_NORM)
            painter.drawText(
                row_rect,
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight,
                value
            )

# =================================================================================
# Widget Daily PnL Bar Chart
# =================================================================================
class DailyPnLBarChart(QWidget):
    date_clicked = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setMinimumSize(300, 250)
        self.chart_data = []      
        self.intra_day_trades = [] 
        self.selected_index = None
        self.selected_date = None
        self.total_pnl_str = "$0.00"
        self.setMouseTracking(True)
        self.df_trades = pl.DataFrame() # Khởi tạo DF rỗng

    def update_data(self, df_trades: pl.DataFrame):
        if df_trades is None or df_trades.is_empty():
            self.chart_data = []; self.total_pnl_str = "$0.00"; self.update(); return

        self.df_trades = df_trades
        try:
            # Sửa logic: đưa biểu thức so sánh vào trong .filter()
            daily_stats = (
                self.df_trades.group_by("filter_date")
                .agg([
                    pl.col("pnl_usd").sum().round(2).alias("total_pnl"),
                    pl.col("pnl_usd").filter(pl.col("filter_side") == "long").sum().round(2).fill_null(0).alias("long_pnl"),
                    pl.col("pnl_usd").filter(pl.col("filter_side") == "short").sum().round(2).fill_null(0).alias("short_pnl"),
                    pl.len().alias("count") # Sử dụng pl.len() thay cho pl.count() đã bị loại bỏ
                ])
                .sort("filter_date")
            )

            # Map đúng key 'date' để paintEvent có dữ liệu vẽ
            self.chart_data = [
                {
                    "date": r["filter_date"],
                    "total_pnl": r["total_pnl"],
                    "long_pnl": r["long_pnl"],
                    "short_pnl": r["short_pnl"],
                    "count": r["count"]
                }
                for r in daily_stats.tail(50).to_dicts()
            ]

            total_pnl = self.df_trades["pnl_usd"].sum()
            self.total_pnl_str = f"{total_pnl:+,.2f}$"
            
        except Exception as e:
            print(f"Lỗi Daily PnL: {e}")
        self.update()

    def mousePressEvent(self, event):
        if not self.chart_data: return
        
        # Nếu đang ở chế độ xem chi tiết, click bất kỳ đâu để thoát
        if self.selected_date:
            self.selected_date = None
            self.selected_index = None
            self.date_clicked.emit(None)
            self.update()
            return

        margin = 16
        chart_w = self.width() - margin * 2
        slot_w = chart_w / len(self.chart_data)
        mouse_x = event.position().x() - margin
        index = int(mouse_x // slot_w)

        if 0 <= index < len(self.chart_data):
            self.selected_index = index
            self.selected_date = self.chart_data[index]["date"]
            
            # Trích xuất lệnh chi tiết cho ngày này (Dùng Polars filter)
            day_df = self.df_trades.filter(pl.col("filter_date") == self.selected_date).sort("time_close")
            self.intra_day_trades = day_df.to_dicts()
            
            self.date_clicked.emit(self.selected_date)
            self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(CARD_BG))

        w, h = self.width(), self.height()
        margin = 16
        chart_top = 85
        chart_h = h - chart_top - 30
        zero_y = chart_top + chart_h / 2

        # -------- HEADER --------
        painter.setFont(FONT_VAL_BIG)
        painter.setPen(QColor(COLOR_WIN if "+" in self.total_pnl_str else COLOR_LOSS))
        painter.drawText(margin, 40, self.total_pnl_str)

        # Nếu đang CHỌN NGÀY -> Vẽ biểu đồ đường chi tiết (Intraday)
        if self.selected_date and self.intra_day_trades:
            self.draw_intraday_line(painter, margin, chart_top, w - margin*2, chart_h)
        else:
            # Nếu KHÔNG CHỌN -> Vẽ biểu đồ cột như cũ
            self.draw_daily_bars(painter, margin, chart_top, w - margin*2, chart_h, zero_y)

    def draw_intraday_line(self, painter, x, y, w, h):
        # Header phụ cho ngày đang chọn
        painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        painter.setPen(QColor(ACCENT_COLOR))
        painter.drawText(x, 65, f"CHI TIẾT: {self.selected_date.strftime('%d/%m/%Y')} (Click để quay lại)")

        # Tính toán Equity Curve nội bộ ngày
        pnl_values = [t['pnl_usd'] for t in self.intra_day_trades]
        equity_points = [0]
        curr = 0
        for v in pnl_values:
            curr += v
            equity_points.append(curr)

        max_v = max(equity_points) if equity_points else 1
        min_v = min(equity_points) if equity_points else -1
        range_v = max(abs(max_v), abs(min_v)) or 1

        # Vẽ đường Zero
        zero_y = y + h/2
        painter.setPen(QPen(QColor(GRID_COLOR), 1, Qt.PenStyle.DotLine))
        painter.drawLine(x, int(zero_y), x + w, int(zero_y))

        # Vẽ Path
        path = QPainterPath()
        step_x = w / (len(equity_points) - 1) if len(equity_points) > 1 else w
        
        points = []
        for i, val in enumerate(equity_points):
            px = x + i * step_x
            # Scale theo range_v
            py = zero_y - (val / range_v * (h/2.2))
            points.append(QPointF(px, py))
            if i == 0: path.moveTo(px, py)
            else: path.lineTo(px, py)

        # Vẽ bóng mờ (Gradient fill)
        fill_path = QPainterPath(path)
        fill_path.lineTo(points[-1].x(), zero_y)
        fill_path.lineTo(points[0].x(), zero_y)
        painter.fillPath(fill_path, QColor(60, 180, 255, 30))

        # Vẽ đường chính
        painter.setPen(QPen(QColor("#3498db"), 2))
        painter.drawPath(path)
        
        # Vẽ điểm kết thúc
        painter.setBrush(QColor("#3498db"))
        painter.drawEllipse(points[-1], 3, 3)

    def draw_daily_bars(self, painter, margin, chart_top, chart_w, chart_h, zero_y):
        if not self.chart_data: return
        
        max_val = max(abs(d["total_pnl"]) for d in self.chart_data) or 1
        slot_w = chart_w / len(self.chart_data)
        bar_gap = 6
        bar_w = max(3, slot_w - bar_gap)

        painter.setPen(QPen(QColor(GRID_COLOR), 1, Qt.PenStyle.DashLine))
        painter.drawLine(margin, int(zero_y), margin + chart_w, int(zero_y))

        for i, d in enumerate(self.chart_data):
            x = margin + i * slot_w + bar_gap / 2
            
            l_height = (abs(d["long_pnl"]) / (max_val * 1.2)) * (chart_h / 2)
            s_height = (abs(d["short_pnl"]) / (max_val * 1.2)) * (chart_h / 2)

            # Vẽ Long
            l_rect = QRectF(x, zero_y - l_height if d["long_pnl"] >= 0 else zero_y, bar_w, l_height)
            painter.fillRect(l_rect, QColor(COLOR_WIN))

            # Vẽ Short
            s_rect = QRectF(x, zero_y - s_height if d["short_pnl"] >= 0 else zero_y, bar_w, s_height)
            painter.fillRect(s_rect, QColor(COLOR_LOSS))

            # Trade count text
            painter.setPen(QColor(TEXT_SUB))
            painter.setFont(QFont("Segoe UI", 7))
            painter.drawText(QRectF(x-5, zero_y + (chart_h/2) + 5, bar_w+10, 15), Qt.AlignmentFlag.AlignCenter, str(d["count"]))

# =================================================================================
# Widget Calendar
# =================================================================================
class CalendarWidget(QWidget):
    # Signal: Gửi object date ra ngoài
    date_selected = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setMinimumSize(250, 300)
        self.year, self.month = datetime.now().year, datetime.now().month
        self.selected_date = None # Ngày đang được chọn để highlight
        self.all_trades_df = pl.DataFrame() # Khởi tạo ngay lập tức
        self.pnl_data = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        
        # --- Nav Bar ---
        nav_container = QWidget()
        nav_container.setFixedHeight(30)
        nav_layout = QHBoxLayout(nav_container)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        
        self.btn_prev = QPushButton("<")
        self.btn_prev.setFixedSize(30, 30)
        self.btn_prev.clicked.connect(self.prev_month)
        self.btn_prev.setStyleSheet(f"QPushButton {{ color: {TEXT_SUB}; border: none; font-weight: bold; background: transparent; }} QPushButton:hover {{ background: #222; border-radius: 4px; }}")

        self.lbl_date = QLabel()
        self.lbl_date.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_date.setStyleSheet(f"color: {TEXT_MAIN}; font-family: 'Segoe UI'; font-weight: bold; font-size: 13px;")
        
        self.btn_next = QPushButton(">")
        self.btn_next.setFixedSize(30, 30)
        self.btn_next.clicked.connect(self.next_month)
        self.btn_next.setStyleSheet(f"QPushButton {{ color: {TEXT_SUB}; border: none; font-weight: bold; background: transparent; }} QPushButton:hover {{ background: #222; border-radius: 4px; }}")

        nav_layout.addWidget(self.btn_prev)
        nav_layout.addStretch()
        nav_layout.addWidget(self.lbl_date)
        nav_layout.addStretch()
        nav_layout.addWidget(self.btn_next)
        
        layout.addWidget(nav_container)
        
        # --- Grid ---
        self.grid = QWidget() 
        self.grid.paintEvent = self.grid_paint_event
        # Gán sự kiện mousePress cho Grid Widget
        self.grid.mousePressEvent = self.grid_mouse_press 
        layout.addWidget(self.grid)

        self.all_trades = []
        self.update_header_text()
        self.update_data()
        
    def update_header_text(self):
        self.lbl_date.setText(f"THÁNG {self.month:02d} / {self.year}")

    def set_trades(self, trades, current_date_filter=None):
        if not trades:
            self.all_trades_df = pl.DataFrame()
        else:
            # Convert list sang Polars
            df = pl.DataFrame(trades)
            
            # Ép kiểu thời gian nếu là String
            if df["time_close"].dtype == pl.Utf8:
                df = df.with_columns(
                    pl.col("time_close").str.strptime(pl.Datetime, strict=False)
                )
            self.all_trades_df = df

        self.selected_date = current_date_filter
        self.update_data()

    def update_data(self):
        # Kiểm tra an toàn: nếu DF chưa có dữ liệu hoặc chưa được tạo
        if not hasattr(self, 'all_trades_df') or self.all_trades_df.is_empty():
            self.pnl_data = {}
            if hasattr(self, 'grid'): self.grid.update()
            return

        try:
            # 1. Lọc dữ liệu trong tháng/năm đang hiển thị
            df = self.all_trades_df            
            monthly_stats = (
                df.filter(
                    (pl.col("time_close").dt.year() == self.year) &
                    (pl.col("time_close").dt.month() == self.month)
                )
                .group_by(pl.col("time_close").dt.day().alias("day"))
                .agg(
                    # Sử dụng .round(2) để làm tròn tổng PnL ngay tại đây
                    pl.col("pnl_usd").sum().round(2).alias("total_pnl")
                )
            )
            # 2. Chuyển kết quả thành dictionary
            self.pnl_data = {
                int(row["day"]): float(row["total_pnl"]) 
                for row in monthly_stats.to_dicts()
            }

        except Exception as e:
            print(f"Lỗi xử lý dữ liệu Calendar: {e}")
            self.pnl_data = {}

        if hasattr(self, 'grid'):
            self.grid.update()

    def prev_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.update_header_text()
        self.update_data()

    def next_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.update_header_text()
        self.update_data()

    def grid_mouse_press(self, event):
        w, h = self.grid.width(), self.grid.height()
        col_w = w / 7
        row_h = h / 7
        
        # Bỏ qua dòng tiêu đề thứ
        if event.position().y() < row_h: return

        cal = calendar.Calendar(firstweekday=6)
        matrix = cal.monthdayscalendar(self.year, self.month)
        
        # Tính toán row, col trong matrix
        r = int((event.position().y() - row_h) // row_h)
        c = int(event.position().x() // col_w)
        
        if 0 <= r < len(matrix) and 0 <= c < 7:
            day = matrix[r][c]
            if day != 0:
                clicked_date = datetime(self.year, self.month, day).date()
                
                # Logic Toggle
                if self.selected_date == clicked_date:
                    self.selected_date = None # Bỏ chọn
                else:
                    self.selected_date = clicked_date
                
                self.date_selected.emit(self.selected_date)
                self.grid.update()

    def grid_paint_event(self, event):
        painter = QPainter(self.grid)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.grid.width(), self.grid.height()
        
        cal = calendar.Calendar(firstweekday=6)
        matrix = cal.monthdayscalendar(self.year, self.month)
        
        col_w = w / 7
        row_h = h / 7 
        
        days = ["CN", "T2", "T3", "T4", "T5", "T6", "T7"]
        painter.setFont(FONT_SUB)
        painter.setPen(QColor(TEXT_SUB))
        for i, d in enumerate(days):
            painter.drawText(QRectF(i*col_w, 0, col_w, row_h), Qt.AlignmentFlag.AlignCenter, d)
            
        font_day = QFont("Segoe UI", 10, QFont.Weight.Bold)
        font_val = QFont("Segoe UI", 7)
        
        for r, week in enumerate(matrix):
            y = (r + 1) * row_h
            painter.setPen(QPen(QColor(GRID_COLOR), 1))
            painter.drawLine(0, int(y), w, int(y))

            for c, day in enumerate(week):
                if day == 0: continue
                x = c * col_w
                cell_rect = QRectF(x, y, col_w, row_h)

                # Vẽ Highlight nếu ngày được chọn
                current_date_obj = None
                try:
                    current_date_obj = datetime(self.year, self.month, day).date()
                except: pass

                if self.selected_date and current_date_obj == self.selected_date:
                    painter.fillRect(cell_rect.adjusted(2,2,-2,-2), QColor("#333"))
                    painter.setPen(QPen(QColor(ACCENT_COLOR), 1))
                    painter.drawRect(cell_rect.adjusted(2,2,-2,-2))

                # Vẽ số ngày
                painter.setPen(QColor(TEXT_MAIN))
                painter.setFont(font_day)
                painter.drawText(QRectF(x, y+2, col_w, row_h/2), Qt.AlignmentFlag.AlignHCenter, str(day))
                
                # Vẽ PnL
                if day in self.pnl_data:
                    pnl = self.pnl_data[day]
                    color = QColor(COLOR_WIN) if pnl > 0 else QColor(COLOR_LOSS)
                    painter.setPen(color)
                    painter.setFont(font_val)
                    painter.drawText(QRectF(x, y+18, col_w, 15), Qt.AlignmentFlag.AlignCenter, f"{pnl:+}")

# =================================================================================
# Widget Total Asset Chart
# =================================================================================
class TotalAssetChart(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(300, 200)
        self.chart_color = QColor("#2962FF") 
        
        # 1. Khởi tạo các giá trị mặc định TRƯỚC
        self.data = []
        self.total_val = 0.0
        self.pnl_val = 0.0
        self.pnl_pct = 0.0
        
        # 2. Gọi update ban đầu để vẽ khung rỗng
        self.update_data()

    def downsample_data(self, balances, max_points=300):
        """Hàm rút gọn dữ liệu để biểu đồ mượt hơn (Instance method)"""
        n = len(balances)
        if n <= max_points:
            return balances

        bucket_size = n / max_points
        result = []
        for i in range(max_points):
            start = int(i * bucket_size)
            end = int((i + 1) * bucket_size)
            chunk = balances[start:end]
            if not chunk: continue
            # Lấy cả min và max của chunk để giữ được độ biến động (Volatility)
            result.append(min(chunk))
            result.append(max(chunk))
        return result

    def update_data(self, equity_curve=None):
        if not equity_curve:
            self.data = []
            self.total_val = self.pnl_val = self.pnl_pct = 0.0
            self.update()
            return

        # Trích xuất balance từ list dictionary
        balances = [item["balance"] for item in equity_curve]
        
        if len(balances) > 0:
            # Gọi hàm downsample đã sửa tên
            self.data = self.downsample_data(balances, 300)

            start_val = balances[0]
            self.total_val = balances[-1]
            self.pnl_val = self.total_val - start_val
            self.pnl_pct = (self.pnl_val / start_val * 100) if start_val != 0 else 0.0
        
        self.update()

    def paintEvent(self, event):

        if not hasattr(self, 'data') or not self.data:
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor(CARD_BG))
            painter.setPen(QColor(TEXT_SUB))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No Data Available")
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(CARD_BG))
        w, h = self.width(), self.height()
        margin = 16

        painter.setPen(QColor(TEXT_MAIN))
        painter.setFont(FONT_VAL_BIG)
        str_balance = f"${self.total_val:,.2f}"
        painter.drawText(margin, margin + 25, str_balance)
        
        fm = QFontMetrics(FONT_VAL_BIG)
        balance_width = fm.horizontalAdvance(str_balance)
        
        painter.setFont(FONT_VAL_NORM)
        if self.pnl_val >= 0:
            color = QColor(COLOR_WIN)
            sign = "+"
        else:
            color = QColor(COLOR_LOSS)
            sign = ""
            
        painter.setPen(color)
        pnl_str = f"{sign}{self.pnl_val:,.2f}$ ({sign}{self.pnl_pct:.2f}%)"
        painter.drawText(margin + balance_width + 10, margin + 25, pnl_str)

        painter.setPen(QColor(TEXT_SUB))
        painter.setFont(FONT_SUB)

        chart_top = 60
        chart_h = h - chart_top
        
        if not self.data: return
        
        max_v = max(self.data)
        min_v = min(self.data)
        range_v = max_v - min_v if max_v != min_v else 1
        
        path = QPainterPath()
        step_x = w / (len(self.data) - 1) if len(self.data) > 1 else w
        points = []
        
        for i, val in enumerate(self.data):
            x = i * step_x
            y = h - ((val - min_v) / range_v * (chart_h - 10)) - 5 
            p = QPointF(x, y)
            points.append(p)
            if i == 0: path.moveTo(p)
            else: path.lineTo(p)

        fill_path = QPainterPath(path)
        fill_path.lineTo(points[-1].x(), h)
        fill_path.lineTo(points[0].x(), h)
        fill_path.closeSubpath()
        
        grad = QLinearGradient(0, chart_top, 0, h)
        c_base = QColor(COLOR_WIN) if self.pnl_val >= 0 else QColor(COLOR_LOSS)
        
        c1 = QColor(c_base); c1.setAlpha(80)
        c2 = QColor(c_base); c2.setAlpha(0)
        grad.setColorAt(0, c1); grad.setColorAt(1, c2)
        painter.fillPath(fill_path, QBrush(grad))
        
        painter.setPen(QPen(c_base, 2))
        painter.drawPath(path)

# =================================================================================
# COIN CONTENT WIDGET WITH COUNT (ĐÃ SỬA LỖI THỤT ĐẦU DÒNG)
# =================================================================================
class CoinContentWidget(QWidget):

    coin_clicked = pyqtSignal(str)

    def __init__(self, data=[]):
        super().__init__()
        self.data = data
        self.row_height = 40
        self.setMinimumHeight(len(data) * self.row_height)
        self.selected_coin = None # Khởi tạo biến này để tránh lỗi AttributeError

    def update_data(self, data, selected_coin=None):
        self.data = data or []
        self.selected_coin = selected_coin  # trạng thái highlight

        # Chỉ update height khi thực sự thay đổi
        new_height = len(self.data) * self.row_height
        if self.minimumHeight() != new_height:
            self.setMinimumHeight(new_height)

        self.update()


    def mousePressEvent(self, event):
        # Sửa: Dùng int() để tránh lỗi float index
        if self.row_height == 0: return 
        index = int(event.position().y() // self.row_height)
        
        if 0 <= index < len(self.data):
            # Lấy tên coin và gửi signal
            coin_name = self.data[index]['pair']
            self.coin_clicked.emit(coin_name)

    def paintEvent(self, event):

        if not hasattr(self, 'data') or not self.data:
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor(CARD_BG))
            painter.setPen(QColor(TEXT_SUB))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No Data Available")
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(CARD_BG))
        w = self.width()
        
        for i, item in enumerate(self.data):
            y = i * self.row_height
            
            # [QUAN TRỌNG] Vẽ Highlight nền nếu coin đang được chọn
            if self.selected_coin and self.selected_coin == item.get('pair'):
                painter.fillRect(QRectF(0, y, w, self.row_height), QColor("#333"))
                painter.setPen(QPen(QColor(ACCENT_COLOR), 3))
                painter.drawLine(0, int(y), 0, int(y + self.row_height))

            # 1. Tên Coin
            painter.setPen(QColor(ACCENT_COLOR))
            painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            painter.drawText(10, int(y), w//3, self.row_height, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, str(item['pair']))
            
            # 2. Số Lệnh
            count = item.get('count', 0)
            painter.setPen(QColor(TEXT_SUB))
            painter.setFont(QFont("Segoe UI", 9))
            painter.drawText(10, int(y), w - 20, self.row_height, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter, f"{count} lệnh")

            # 3. PnL
            pnl = item['pnl']
            color = QColor(COLOR_WIN) if pnl >= 0 else QColor(COLOR_LOSS)
            painter.setPen(color)
            painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            painter.drawText(w - 110, int(y), 100, self.row_height, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight, f"{pnl:+.2f}$")
            
            # Đường kẻ ngang
            painter.setPen(QPen(QColor(BORDER_COLOR), 1))
            painter.drawLine(10, int(y + self.row_height - 1), w - 10, int(y + self.row_height - 1))

class CoinResultWidget(QWidget):
    # Signal trung gian
    coin_selected_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet(f"background: {CARD_BG}; border: none;")
        self.scroll.verticalScrollBar().setStyleSheet(f"QScrollBar:vertical {{ background: {CARD_BG}; width: 6px; }} QScrollBar::handle:vertical {{ background: #333; border-radius: 3px; }}")
        
        self.content = CoinContentWidget([])
        # Kết nối signal nội bộ
        self.content.coin_clicked.connect(self.on_coin_clicked)
        
        self.scroll.setWidget(self.content)
        layout.addWidget(self.scroll)

    def on_coin_clicked(self, coin_name):
        self.coin_selected_signal.emit(coin_name)

    def update_data(self, df: pl.DataFrame | None = None, current_filter_coin=None):
        # [QUAN TRỌNG] Reset list nếu không có dữ liệu
        if df is None or df.is_empty():
            self.content.update_data([], current_filter_coin)
            return

        try:
            grp = (
                df.group_by("symbol")
                  .agg([
                      pl.sum("pnl_usd").alias("pnl"),
                      pl.len().alias("count"), # Dùng pl.len() thay pl.count()
                  ])
                  .sort("pnl", descending=True)
            )

            data = [
                {
                    "pair": r["symbol"],
                    "pnl": float(r["pnl"]),
                    "count": int(r["count"]),
                }
                for r in grp.to_dicts()
            ]
            
            # Cập nhật nội dung bên trong ScrollArea
            self.content.update_data(data, current_filter_coin)

        except Exception as e:
            print(f"Lỗi CoinResultWidget: {e}")
            self.content.update_data([], current_filter_coin)

# =================================================================================
# Widget Lịch Sử Lệnh Chi Tiết (Table)
# =================================================================================
class TradeHistoryWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Tạo bảng
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["THỜI GIAN", "CẶP", "VỊ THẾ", "ENTRY", "EXIT", "PNL ($)", "ROI (%)", "LÝ DO"])
        
        # Cấu hình giao diện bảng
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # Không cho sửa
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) # Chọn cả dòng
        
        # [QUAN TRỌNG] Tắt Focus Policy để hạn chế việc nhận tiêu điểm chuột
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setAlternatingRowColors(True)
        
        # [QUAN TRỌNG] Style Sheet đã thêm 'outline: 0' để tắt viền trắng
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {CARD_BG};
                border: none;
                gridline-color: {BORDER_COLOR};
                outline: 0; /* Tắt viền nét đứt/viền trắng khi focus toàn bảng */
            }}
            QHeaderView::section {{
                background-color: {BG_COLOR};
                color: {TEXT_SUB};
                padding: 5px;
                border: none;
                border-bottom: 1px solid {BORDER_COLOR};
                font-weight: bold;
                font-family: "Segoe UI";
            }}
            QTableWidget::item {{
                padding: 5px;
                border-bottom: 1px solid #1f1f1f;
                outline: none; /* Tắt outline cho từng item */
                border: none;
            }}
            QTableWidget::item:selected {{
                background-color: #333;
                border: none;
                outline: none;
                color: {TEXT_MAIN};
            }}
            QTableWidget::item:focus {{
                border: none;
                outline: none; /* Tắt viền focus khi click vào ô cụ thể */
                background-color: #333; 
            }}
        """)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) 
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addWidget(self.table)

    def update_data(self, trades=None):
        if not trades:
            self.table.setRowCount(0)
            return

        # CHỈ lấy 100 lệnh mới nhất. Nạp 500+ lệnh vào QTableWidget sẽ làm UI đứng hình.
        display_limit = 100 
        display_trades = trades[-display_limit:] if len(trades) > display_limit else trades
        reversed_trades = display_trades[::-1]
        
        self.table.setRowCount(len(reversed_trades))
        font_bold = QFont("Segoe UI", 9, QFont.Weight.Bold)

        for row, t in enumerate(reversed_trades):
            # 0. Thời gian
            item_time = QTableWidgetItem(str(t.get('time_close', '')))
            item_time.setForeground(QColor(TEXT_SUB))
            item_time.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, item_time)
            
            # 1. Cặp Coin
            item_pair = QTableWidgetItem(str(t.get('symbol', '')))
            item_pair.setForeground(QColor(ACCENT_COLOR))
            item_pair.setFont(font_bold)
            item_pair.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, item_pair)
            
            # 2. Vị thế
            side_str = str(t.get('side', '')).upper()
            item_side = QTableWidgetItem(side_str)
            if side_str in ["BUY", "LONG"]:
                item_side.setForeground(QColor("#4CAF50")) 
            else:
                item_side.setForeground(QColor("#FF5252")) 
            item_side.setFont(font_bold)
            item_side.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 2, item_side)
            
            # 3. Entry
            entry_val = t.get('entry', 0)
            self.table.setItem(row, 3, QTableWidgetItem(f"{entry_val:.4f}"))
            
            # 4. Exit
            exit_val = t.get('exit', 0)
            self.table.setItem(row, 4, QTableWidgetItem(f"{exit_val:.4f}"))
            
            # 5. PnL ($)
            pnl = t.get('pnl_usd', 0)
            item_pnl = QTableWidgetItem(f"{pnl:+.2f}$")
            item_pnl.setFont(font_bold)
            if pnl > 0: item_pnl.setForeground(QColor(COLOR_WIN))
            else: item_pnl.setForeground(QColor(COLOR_LOSS))
            item_pnl.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 5, item_pnl)
            
            # 6. ROI (%)
            roi = t.get('pnl_pct', 0) * 100
            item_roi = QTableWidgetItem(f"{roi:+.2f}%")
            if roi > 0: item_roi.setForeground(QColor(COLOR_WIN))
            else: item_roi.setForeground(QColor(COLOR_LOSS))
            item_roi.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 6, item_roi)
            
            # 7. Lý do
            full_text = str(t.get('reason', ''))
            display_text = full_text
            if len(full_text) > 30:
                display_text = full_text[:30] + "..."

            item_reason = QTableWidgetItem(display_text)
            item_reason.setForeground(QColor(TEXT_SUB))
            item_reason.setToolTip(full_text)

            self.table.setItem(row, 7, item_reason)

            # Chỉnh màu text mặc định
            for col in [3, 4]:
                it = self.table.item(row, col)
                if it: 
                    it.setForeground(QColor(TEXT_MAIN))
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

# =================================================================================
# WIDGET SCATTER PLOT (Sửa lỗi hiển thị thời gian & Tính toán Duration)
# =================================================================================
class TradeScatterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(300, 200)
        self.points = [] 
        self.max_duration = 1
        self.max_pnl_abs = 1
        
        # [CẤU HÌNH] Ngưỡng dưới thời gian (phút)
        # Tăng lên 0.5 (30 giây) để thu hẹp khoảng cách từ 0 đến 1m
        self.MIN_DURATION_DISPLAY = 1
        
        # Bật theo dõi chuột để hiện Tooltip
        self.setMouseTracking(True) 
        self.hover_point = None     

    def format_duration(self, minutes):
        """Format thời gian dễ đọc (vd: 5m, 2h 30m)"""
        if minutes < 1: return f"{int(minutes*60)}s"
        if minutes < 60: return f"{int(minutes)}m"
        hours = int(minutes // 60)
        mins = int(minutes % 60)
        if hours < 24: return f"{hours}h {mins}m"
        days = int(hours // 24)
        rem_hours = hours % 24
        return f"{days}d {rem_hours}h"

    def update_data(self, df: pl.DataFrame | None = None):
        self.points = []
        self.hover_point = None

        if df is None or df.is_empty():
            self.update()
            return

        try:
            # 1. Đảm bảo có đủ cột thời gian
            if "time_close" not in df.columns or "time_open" not in df.columns:
                print("ScatterPlot: Thiếu cột time_close hoặc time_open")
                self.update()
                return

            # 2. Tính toán Duration và PnL (Polars Vectorization)
            df_plot = df.select([
                pl.col("time_close"),
                pl.col("time_open"),
                pl.col("pnl_usd").cast(pl.Float64).alias("pnl"),
                pl.col("symbol").fill_null("Unknown").alias("pair")
            ]).with_columns(
                ((pl.col("time_close") - pl.col("time_open"))
                 .dt.total_minutes()
                 .fill_null(0)
                 # [SỬA] Clip dữ liệu theo ngưỡng mới để không bị lỗi scale
                 .clip(lower_bound=self.MIN_DURATION_DISPLAY) 
                ).alias("duration")
            )

            # 3. Tính Min/Max để scale biểu đồ
            max_dur = df_plot["duration"].max()
            max_pnl = df_plot["pnl"].abs().max()
            
            self.max_duration = max_dur if max_dur and max_dur > 1 else 1
            self.max_pnl_abs = max_pnl if max_pnl and max_pnl > 0 else 1

            # 4. Convert sang list dict nhẹ để vẽ
            rows = df_plot.select(["duration", "pnl", "pair"]).to_dicts()
            
            for r in rows:
                self.points.append({
                    "dur": r["duration"],
                    "pnl": r["pnl"],
                    "pair": r["pair"],
                    "color": QColor(COLOR_WIN) if r["pnl"] >= 0 else QColor(COLOR_LOSS),
                })

        except Exception as e:
            print(f"Lỗi logic Scatter Plot: {e}")

        self.update()

    def get_x_pos(self, duration, plot_width, margin_left):
        # [SỬA] Sử dụng ngưỡng MIN_DURATION_DISPLAY thay vì 0.1
        safe_dur = max(self.MIN_DURATION_DISPLAY, duration)
        
        min_log = math.log10(self.MIN_DURATION_DISPLAY) 
        
        # Đảm bảo max_log luôn lớn hơn min_log để tránh lỗi chia 0
        real_max = max(self.max_duration * 1.1, self.MIN_DURATION_DISPLAY * 2)
        max_log = math.log10(real_max)
        
        current_log = math.log10(safe_dur)
        
        range_log = max_log - min_log
        if range_log == 0: range_log = 1
        
        # Tỷ lệ % trên trục X
        ratio = (current_log - min_log) / range_log
        return margin_left + (ratio * plot_width)

    def mouseMoveEvent(self, event):
        """Xử lý hover chuột để hiện Tooltip"""
        if not self.points: return
        
        mx, my = event.position().x(), event.position().y()
        w, h = self.width(), self.height()
        
        m_left, m_bottom, m_top, m_right = 50, 30, 20, 20
        plot_w = w - m_left - m_right
        plot_h = h - m_top - m_bottom
        center_y = m_top + plot_h / 2
        scale_y = (plot_h / 2) / self.max_pnl_abs

        closest_dist = 15 # Pixel
        found = None

        for p in self.points:
            # Tính toạ độ điểm hiện tại
            px = self.get_x_pos(p['dur'], plot_w, m_left)
            py = center_y - (p['pnl'] * scale_y)
            
            dist = math.hypot(px - mx, py - my)
            if dist < closest_dist:
                closest_dist = dist
                found = p
                found['sx'] = px
                found['sy'] = py

        if self.hover_point != found:
            self.hover_point = found
            self.update()

    def paintEvent(self, event):
        if not hasattr(self, 'points') or not self.points:
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor(CARD_BG))
            painter.setPen(QColor(TEXT_SUB))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No Data Available")
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(CARD_BG))
        
        w, h = self.width(), self.height()
        m_left, m_bottom, m_top, m_right = 50, 30, 20, 20
        plot_w = w - m_left - m_right
        plot_h = h - m_top - m_bottom
        center_y = m_top + plot_h / 2
        
        # --- 1. VẼ TRỤC VÀ KHUNG ---
        painter.setPen(QPen(QColor(BORDER_COLOR), 1))
        painter.drawLine(m_left, m_top, m_left, h - m_bottom) # Trục Y
        painter.drawLine(m_left, h - m_bottom, w - m_right, h - m_bottom) # Trục X
        
        # Đường 0$
        painter.setPen(QPen(QColor("#444"), 1, Qt.PenStyle.DashLine))
        painter.drawLine(m_left, int(center_y), w - m_right, int(center_y))
        
        # --- 2. VẼ GRIDLINES THỜI GIAN (LOGARIT) ---
        time_markers = [1, 5, 15, 60, 240, 1440, 4320] 
        painter.setFont(FONT_SUB)
        
        for tm in time_markers:
            if tm > self.max_duration * 1.5: break 
            
            # [SỬA] Chỉ vẽ các mốc lớn hơn ngưỡng hiển thị
            if tm < self.MIN_DURATION_DISPLAY: continue

            # Tính vị trí X theo Logarit
            x_line = self.get_x_pos(tm, plot_w, m_left)
            
            # Vẽ đường dọc mờ
            painter.setPen(QPen(QColor(GRID_COLOR), 1, Qt.PenStyle.DotLine))
            painter.drawLine(int(x_line), m_top, int(x_line), h - m_bottom)
            
            # Vẽ nhãn
            painter.setPen(QColor(TEXT_SUB))
            label = self.format_duration(tm)
            painter.drawText(int(x_line) + 3, h - m_bottom - 5, label)

        # --- 3. VẼ NHÃN TRỤC Y ---
        painter.setFont(FONT_LABEL)
        painter.setPen(QColor(COLOR_WIN))
        painter.drawText(5, m_top + 10, f"+{self.max_pnl_abs:.1f}$")
        painter.setPen(QColor(COLOR_LOSS))
        painter.drawText(5, h - m_bottom, f"-{self.max_pnl_abs:.1f}$")
        painter.setPen(QColor(TEXT_SUB))
        painter.drawText(5, int(center_y) + 5, "0$")

        if not self.points:
            painter.drawText(w//2 - 20, h//2, "No Data")
            return

        # --- 4. VẼ CÁC ĐIỂM (POINTS) ---
        scale_y = (plot_h / 2) / self.max_pnl_abs
        painter.setPen(Qt.PenStyle.NoPen)
        
        for p in self.points:
            # Dùng hàm get_x_pos Logarit
            x = self.get_x_pos(p['dur'], plot_w, m_left)
            y = center_y - (p['pnl'] * scale_y)
            
            # Giới hạn vùng vẽ (Clip)
            if y < m_top: y = m_top
            if y > h - m_bottom: y = h - m_bottom
            
            is_hover = (self.hover_point == p)
            radius = 6 if is_hover else 4
            
            c = QColor(p['color'])
            c.setAlpha(255 if is_hover else 180)
            painter.setBrush(c)
            
            if is_hover:
                painter.setPen(QPen(QColor("white"), 1))
            else:
                painter.setPen(Qt.PenStyle.NoPen)
                
            painter.drawEllipse(QPointF(x, y), radius, radius)

        # --- 5. VẼ TOOLTIP ---
        if self.hover_point:
            hp = self.hover_point
            tip_text = f"{hp['pair']}\nPnL: {hp['pnl']:+.2f}$\nTime: {self.format_duration(hp['dur'])}"
            
            fm = painter.fontMetrics()
            lines = tip_text.split('\n')
            max_w = max([fm.horizontalAdvance(l) for l in lines]) + 20
            box_h = len(lines) * fm.height() + 15
            
            bx = hp['sx'] + 10
            by = hp['sy'] - 10
            
            # Đảo chiều tooltip nếu sát lề phải/dưới
            if bx + max_w > w: bx = hp['sx'] - max_w - 10
            if by + box_h > h: by = hp['sy'] - box_h - 10
            
            painter.setPen(QPen(QColor(ACCENT_COLOR), 1))
            painter.setBrush(QColor(20, 20, 20, 240))
            painter.drawRoundedRect(QRectF(bx, by, max_w, box_h), 5, 5)
            
            painter.setPen(QColor(TEXT_MAIN))
            for i, line in enumerate(lines):
                painter.drawText(int(bx + 10), int(by + 15 + i*fm.height()), line)

# =================================================================================
# Widget Long/Short (Phiên bản an toàn - Chấp nhận cả chữ hoa/thường)
# =================================================================================
class LongShortWidget(QWidget):
    # [QUAN TRỌNG] Đổi thành 'object' để có thể gửi giá trị None
    side_clicked = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setMinimumSize(250, 150)
        self.stats = {
            "long": {"win": 0, "total": 0, "pnl": 0}, 
            "short": {"win": 0, "total": 0, "pnl": 0}
        }
        self.selected_side = None # "long", "short" hoặc None

    def update_data(self, df: pl.DataFrame | None = None, current_filter_side=None):
        self.selected_side = current_filter_side
        self.stats = {
            "long": {"win": 0, "total": 0, "pnl": 0.0}, 
            "short": {"win": 0, "total": 0, "pnl": 0.0}
        }

        if df is None or df.is_empty():
            self.update(); return

        try:
            # Group theo cột filter_side đã chuẩn hóa ở Dashboard
            agg = (
                df.group_by("filter_side")
                   .agg([
                       pl.len().alias("total"),
                       pl.col("pnl_usd").sum().round(2).alias("pnl"),
                       pl.col("pnl_usd").filter(pl.col("pnl_usd") > 0).len().alias("win"),
                   ])
                   .to_dicts()
            )

            for row in agg:
                side = row["filter_side"] # Giá trị này phải là 'long' hoặc 'short'
                if side in self.stats:
                    self.stats[side]["total"] = row["total"]
                    self.stats[side]["pnl"] = float(row["pnl"])
                    self.stats[side]["win"] = int(row["win"])
        except Exception as e:
            print(f"Lỗi LongShortWidget: {e}")

        self.update()

    def mousePressEvent(self, event):
        y = event.position().y()       
        
        clicked_side = None
        
        # Vùng Long (Từ trên cùng đến khoảng giữa)
        if 0 <= y <= 75:
            clicked_side = "long"
            
        # Vùng Short (Từ khoảng giữa xuống dưới)
        elif 85 <= y <= 150:
            clicked_side = "short"
            
        # Nếu click vào vùng trống ở giữa hoặc ngoài phạm vi -> Không làm gì (hoặc Bỏ chọn)
        if clicked_side is None:
            return

        # Logic Toggle: Click lại cái đang chọn thì bỏ chọn
        if self.selected_side == clicked_side:
            self.selected_side = None # Gán về None
        else:
            self.selected_side = clicked_side
            
        # Gửi signal (None hoặc "long"/"short")
        self.side_clicked.emit(self.selected_side)
        self.update()

    def paintEvent(self, event):
        if not self.stats or (self.stats['long']['total'] == 0 and self.stats['short']['total'] == 0):
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor(CARD_BG))
            painter.setPen(QColor(TEXT_SUB))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No Data Available")
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(CARD_BG))
        w, h = self.width(), self.height()
        margin = 16
        bar_height = 40
        
        # Vẽ LONG
        self.draw_bar(painter, margin, 30, w-2*margin, bar_height, "LONG", self.stats["long"], QColor("#4CAF50"), is_selected=(self.selected_side=="long"))
        
        # Vẽ SHORT
        self.draw_bar(painter, margin, 30 + bar_height + 20, w-2*margin, bar_height, "SHORT", self.stats["short"], QColor("#FF5252"), is_selected=(self.selected_side=="short"))

    def draw_bar(self, painter, x, y, w, h, title, data, color, is_selected=False):
        # --- Vẽ khung highlight ---
        if is_selected:
            painter.setPen(QPen(QColor(ACCENT_COLOR), 1))
            c_highlight = QColor(ACCENT_COLOR)
            c_highlight.setAlpha(30)
            painter.setBrush(c_highlight)
            # Vẽ khung ôm sát nội dung
            painter.drawRoundedRect(QRectF(x - 5, y - 25, w + 10, 45), 6, 6)

        painter.setPen(QColor(TEXT_MAIN))
        painter.setFont(FONT_LABEL)
        total = data["total"]
        winrate = (data["win"] / total * 100) if total > 0 else 0.0
        pnl = data["pnl"]
        
        # Hiệu ứng mờ (Dim) nếu side kia đang được chọn
        if self.selected_side is not None and not is_selected:
            painter.setOpacity(0.3)
        else:
            painter.setOpacity(1.0)

        text = f"{title}: {total} lệnh | Win: {winrate:.1f}% | PnL: {pnl:+.2f}$"
        painter.drawText(int(x), int(y - 5), text)
        
        bg_rect = QRectF(x, y, w, 10)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#333"))
        painter.drawRoundedRect(bg_rect, 5, 5)
        
        if total > 0:
            win_w = w * (winrate / 100)
            if win_w < 5 and winrate > 0: win_w = 5
            win_rect = QRectF(x, y, win_w, 10)
            painter.setBrush(color)
            painter.drawRoundedRect(win_rect, 5, 5)
            
        painter.setOpacity(1.0)

# =================================================================================
# HÀM XỬ LÝ LOGIC LỌC (CHẠY TRÊN NHÂN CPU RIÊNG - LUỒNG 2 & 3)
# =================================================================================
def execute_filtering_task(df_main: pl.DataFrame, filters: dict, initial_capital: float):
    try:
        if df_main is None or df_main.is_empty():
            return [], [{'balance': initial_capital}], []

        # Khởi tạo biểu thức lọc
        expr = pl.lit(True)
        
        # Sửa lỗi so sánh: filters.get("key") phải so sánh trực tiếp với giá trị
        if filters.get("date"):
            expr &= (pl.col("filter_date") == filters["date"])
        
        if filters.get("side"):
            # Đảm bảo filters["side"] truyền xuống là 'long' hoặc 'short' (lowercase)
            expr &= (pl.col("filter_side") == filters["side"])
            
        if filters.get("weekday") is not None:
            expr &= (pl.col("filter_weekday") == filters["weekday"])
            
        if filters.get("hour") is not None:
            expr &= (pl.col("filter_hour") == filters["hour"])

        # Thực hiện lọc
        df_step1 = df_main.filter(expr)
        
        df_final = df_step1
        if filters.get("symbol"):
            df_final = df_final.filter(pl.col("symbol") == filters["symbol"])

        # Convert sang dict để gửi về Main UI
        final_trades = df_final.to_dicts()
        trades_for_coin_list = df_step1.to_dicts()

        # Tính Equity Curve
        if not df_final.is_empty():
            # Sắp xếp theo thời gian để cum_sum chính xác
            equity_df = (
                df_final.sort("time_close")
                .with_columns([
                    (pl.col("pnl_usd").cum_sum() + initial_capital).alias("balance")
                ])
            )
            balances = [initial_capital] + equity_df["balance"].to_list()
            new_equity = [{'balance': b} for b in balances]
        else:
            new_equity = [{'balance': initial_capital}]

        return final_trades, new_equity, trades_for_coin_list
    except Exception as e:
        print(f"Lỗi logic lọc: {e}")
        return [], [{'balance': initial_capital}], []

# =================================================================================
# THREAD QUẢN LÝ (ĐIỀU PHỐI GIỮA GIAO DIỆN VÀ TIẾN TRÌNH CON)
# =================================================================================
class ProcessWorkerThread(QThread):
    # Trả về kết quả: (Lệnh đã lọc, Vốn, Lệnh cho danh sách coin)
    filter_finished = pyqtSignal(list, list, list)

    def __init__(self, df_main, filters, initial_capital, executor_pool):
        super().__init__()
        self.df_main = df_main
        self.filters = filters
        self.initial_capital = initial_capital
        self.executor = executor_pool

    def run(self):
        # Gửi công việc vào Pool 2 luồng cố định
        future = self.executor.submit(
            execute_filtering_task, 
            self.df_main, 
            self.filters, 
            self.initial_capital
        )
        try:
            result = future.result()
            self.filter_finished.emit(*result)
        except Exception as e:
            print(f"Lỗi thực thi Thread: {e}")
            self.filter_finished.emit([], [], [])

# =================================================================================
# MAIN WINDOW - DASHBOARD
# =================================================================================
class DraggableDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Backtest Dashboard")
        self.resize(1600, 900)
        
        # Thiết lập màu sắc và giao diện
        bg = BG_COLOR if 'BG_COLOR' in globals() else "#0e0e0e"
        self.setStyleSheet(f"background-color: {bg};")
        self.setDockNestingEnabled(True)

        # --- QUẢN LÝ DỮ LIỆU ---
        self.all_trades_raw = [] 
        self.all_trades_df = pl.DataFrame() 
        self.initial_capital = 10000.0 
        self.is_started = False
        self.has_finished_once = False
        self.is_ui_paused = False
        self.latest_data_cache = {} 
        self.is_filtering = False

        self.worker = None

        self.active_filters = {
            "date": None, "symbol": None, "side": None, "weekday": None, "hour": None
        }

        # --- QUẢN LÝ LUỒNG CPU (Sử dụng luồng riêng để lọc) ---
        from concurrent.futures import ThreadPoolExecutor
        self.executor_pool = ThreadPoolExecutor(max_workers=1) 
        self.current_worker = None 

        # Khởi tạo các thành phần
        self._init_ui_elements()
        self._init_widgets()
        self._init_layout()

        # Timer cho animation trạng thái Funny Quant
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.update_status_animation)
        self.anim_timer.setInterval(100)

        # Tự động bắt đầu sau khi giao diện ổn định
        #QTimer.singleShot(500, self.start_backtest_process)

    # =========================================================================
    # HÀM KHỞI TẠO GIAO DIỆN (FIXED)
    # =========================================================================

    def _init_ui_elements(self):
        """Khởi tạo Toolbar và các nút điều khiển"""
        c_bg = CARD_BG if 'CARD_BG' in globals() else "#141414"
        b_color = BORDER_COLOR if 'BORDER_COLOR' in globals() else "#2a2a2a"
        acc_color = ACCENT_COLOR if 'ACCENT_COLOR' in globals() else "#C8AA6E"
        t_sub = TEXT_SUB if 'TEXT_SUB' in globals() else "#999999"

        toolbar = QToolBar("Main Toolbar")
        toolbar.setStyleSheet(f"background: {c_bg}; border-bottom: 1px solid {b_color}; spacing: 10px; padding: 5px;")
        self.addToolBar(toolbar)
        
        # --- NÚT 1: CHẠY BACKTEST (Logic cũ) ---
        self.btn_control = QPushButton("▶ Bắt đầu Backtest")
        self.btn_control.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_control.setStyleSheet(f"background-color: {acc_color}; color: #000; font-weight: bold; padding: 6px 15px; border-radius: 4px;")
        self.btn_control.clicked.connect(self.on_btn_control_clicked)
        toolbar.addWidget(self.btn_control)

        # --- NÚT 2: LOAD CSV (Chức năng mới) ---
        self.btn_load_csv = QPushButton("📂 Mở File CSV")
        self.btn_load_csv.setCursor(Qt.CursorShape.PointingHandCursor)
        # Style màu xanh hoặc xám để phân biệt với nút Run
        self.btn_load_csv.setStyleSheet("background-color: #2962FF; color: #FFF; font-weight: bold; padding: 6px 15px; border-radius: 4px;")
        self.btn_load_csv.clicked.connect(self.on_btn_load_csv_clicked)
        toolbar.addWidget(self.btn_load_csv)

        self.lbl_status = QLabel("  Sẵn sàng.")
        self.lbl_status.setStyleSheet(f"color: {t_sub}; font-weight: bold; margin-left: 10px;")
        toolbar.addWidget(self.lbl_status)
        self.setCentralWidget(QLabel("")); self.centralWidget().setVisible(False)

    def _init_widgets(self):
        """Khởi tạo tất cả các Widget biểu đồ và bảng"""
        self.widget_pnl = DailyPnLBarChart()
        self.widget_cal = CalendarWidget()
        self.widget_stats = BacktestSummaryWidget()
        self.widget_coins = CoinResultWidget()
        self.widget_dist_w = self.create_dist_widget() # Đã fix lỗi missing attribute
        self.widget_asset = TotalAssetChart()
        self.widget_history = TradeHistoryWidget()
        self.widget_Scatter = TradeScatterWidget()
        self.widget_ls = LongShortWidget()

        # Kết nối các tín hiệu lọc từ Widget
        self.widget_cal.date_selected.connect(self.handle_date_filter)
        self.widget_pnl.date_clicked.connect(self.handle_date_filter)
        self.widget_coins.coin_selected_signal.connect(self.handle_coin_filter)
        self.widget_ls.side_clicked.connect(self.handle_side_filter)
        self.day_dist.bar_clicked.connect(self.handle_dist_filter)
        self.hour_dist.bar_clicked.connect(self.handle_dist_filter)

    def create_dist_widget(self):
        """Hàm bọc cho hai biểu đồ phân phối lệnh"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        self.day_dist = DistributionChart("day")
        self.hour_dist = DistributionChart("hour")
        layout.addWidget(self.day_dist)
        layout.addWidget(self.hour_dist)
        return container

    def _init_layout(self):
        """Sắp xếp các DockWidget trên màn hình chính"""
        self.dock_pnl = DraggableCard("Lãi Lỗ Hằng Ngày", self.widget_pnl)
        self.dock_cal = DraggableCard("Lịch Giao Dịch", self.widget_cal)
        self.dock_stats = DraggableCard("Chỉ Số Hiệu Suất", self.widget_stats)
        self.dock_coins = DraggableCard("Kết Quả Theo Coin", self.widget_coins)
        self.dock_dist = DraggableCard("Phân Phối Lệnh", self.widget_dist_w)
        self.dock_asset = DraggableCard("Tổng Tài Sản", self.widget_asset)
        self.dock_history = DraggableCard("Chi Tiết Lệnh", self.widget_history)
        self.dock_Scatter = DraggableCard("Phân tích giữ lệnh", self.widget_Scatter)
        self.dock_ls = DraggableCard("Long vs Short", self.widget_ls)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_stats)
        self.splitDockWidget(self.dock_stats, self.dock_coins, Qt.Orientation.Vertical)
        self.splitDockWidget(self.dock_coins, self.dock_ls, Qt.Orientation.Vertical)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_pnl)
        self.splitDockWidget(self.dock_pnl, self.dock_dist, Qt.Orientation.Horizontal)
        self.splitDockWidget(self.dock_dist, self.dock_asset, Qt.Orientation.Vertical)
        self.splitDockWidget(self.dock_dist, self.dock_Scatter, Qt.Orientation.Vertical)
        self.splitDockWidget(self.dock_pnl, self.dock_history, Qt.Orientation.Vertical)
        self.splitDockWidget(self.dock_pnl, self.dock_cal, Qt.Orientation.Horizontal)
        
        self.resizeDocks([self.dock_pnl, self.dock_Scatter, self.dock_stats], [1050, 350, 300], Qt.Orientation.Horizontal)
        self.resizeDocks([self.dock_pnl, self.dock_history], [250, 450], Qt.Orientation.Vertical)
        self.resizeDocks([self.dock_Scatter, self.dock_dist], [300, 400], Qt.Orientation.Vertical)
        self.resizeDocks([self.dock_stats, self.dock_coins, self.dock_ls], [250, 400, 150], Qt.Orientation.Vertical)

    # =========================================================================
    # LUỒNG XỬ LÝ DỮ LIỆU ĐA LUỒNG (FIX LAG & CRASH)
    # =========================================================================
    def process_new_data(self, data):
        trades = data.get('trades', [])
        self.initial_capital = float(data.get("initial_capital", 10000.0))
        if not trades: return

        df = pl.DataFrame(trades)

        for col in ["time_close", "time_open"]:
            if col in df.columns and df[col].dtype == pl.Utf8:
                df = df.with_columns(pl.col(col).str.strptime(pl.Datetime, strict=False))

        self.all_trades_df = df.with_columns([
            pl.col("time_close").dt.date().alias("filter_date"),
            pl.col("time_close").dt.weekday().alias("filter_weekday"),
            pl.col("time_close").dt.hour().alias("filter_hour"),
            
            pl.when(pl.col("side").str.to_lowercase().str.strip_chars() == "buy")
              .then(pl.lit("long"))
              .when(pl.col("side").str.to_lowercase().str.strip_chars() == "sell")
              .then(pl.lit("short"))
              .otherwise(pl.col("side").str.to_lowercase())
              .alias("filter_side"),

            pl.col("symbol").str.to_uppercase().str.strip_chars()
        ])

        self.apply_filters()

    def handle_date_filter(self, d):
        self.active_filters["date"] = None if self.active_filters.get("date") == d else d
        self.apply_filters()

    def apply_filters(self):
        if self.all_trades_df.is_empty() or self.is_filtering:
            return

        self.is_filtering = True
        self.current_worker = ProcessWorkerThread(
            self.all_trades_df, 
            self.active_filters, 
            self.initial_capital,
            self.executor_pool
        )
        self.current_worker.filter_finished.connect(self.on_filtering_finished)
        self.current_worker.start()

    def on_filtering_finished(self, filtered_trades, equity_curve, coin_list_trades):
        self.update_ui_filtered(filtered_trades, equity_curve, coin_list_trades)
        self.is_filtering = False
        self.lbl_status.setText(f"✅ Đã lọc: {len(filtered_trades)} lệnh")

    def update_ui_filtered(self, trades, equity, coin_list_trades):
        # 1. Tái tạo DataFrame từ list kết quả
        df_trades = pl.DataFrame(trades)
        df_coin_list = pl.DataFrame(coin_list_trades)
        
        # 2. định dạng Datetime và Số cho các cột quan trọng
        if not df_trades.is_empty():
            cols_to_fix = []
            # Xử lý time_close
            if "time_close" in df_trades.columns and df_trades["time_close"].dtype == pl.Utf8:
                cols_to_fix.append(pl.col("time_close").str.strptime(pl.Datetime, strict=False))
            
            # Xử lý time_open (Cần thiết cho Scatter Plot tính duration)
            if "time_open" in df_trades.columns and df_trades["time_open"].dtype == pl.Utf8:
                cols_to_fix.append(pl.col("time_open").str.strptime(pl.Datetime, strict=False))
                
            # Xử lý PnL
            if "pnl_usd" in df_trades.columns:
                cols_to_fix.append(pl.col("pnl_usd").cast(pl.Float64))

            if cols_to_fix:
                df_trades = df_trades.with_columns(cols_to_fix)

        packet = {'trades': trades, 'equity_curve': equity}
        self.widget_stats.update_data(packet)
        self.widget_asset.update_data(equity)

        wd_val = self.active_filters["weekday"]
        wd_idx = (wd_val - 1) if wd_val is not None else None

        # 5. Cập nhật các widget đồ họa (Dùng DataFrame đã chuẩn hóa)
        widgets_to_update = [
            (self.widget_pnl, 'update_data', df_trades),
            (self.widget_ls, 'update_data', df_trades, self.active_filters["side"]),
            (self.widget_Scatter, 'update_data', df_trades), 
            (self.widget_coins, 'update_data', df_coin_list, self.active_filters["symbol"]),
            # Truyền wd_idx đã xử lý để highlight đúng cột
            (self.day_dist, 'update_data', df_trades, wd_idx),
            (self.hour_dist, 'update_data', df_trades, self.active_filters["hour"]),
        ]

        for widget, method, *args in widgets_to_update:
            try:
                # Gọi hàm update của từng widget
                if hasattr(widget, method):
                    getattr(widget, method)(*args)
            except Exception as e:
                print(f"Lỗi render tại {widget.__class__.__name__}: {e}")

        # 6. Lịch sử lệnh (Giảm xuống 100 để không treo máy)
        recent_trades = trades[-100:] if len(trades) > 100 else trades
        self.widget_history.update_data(recent_trades)
        
        # 7. Calendar
        self.widget_cal.set_trades(trades, self.active_filters["date"])

    # =========================================================================
    # EVENT HANDLERS
    # =========================================================================
    def on_btn_control_clicked(self):
        if getattr(self, 'is_view_mode', False):
            self.is_view_mode = False
            self.is_started = False
        
        # Logic Bắt đầu/Tạm dừng cũ
        if not self.is_started:
            self.start_backtest_process()
            self.btn_control.setText("⏸ Tạm dừng")
        else:
            # Logic tạm dừng cũ...
            pass

    def start_backtest_process(self):
        if self.is_started: 
            return # Nếu đang chạy rồi thì thôi

        # --- BƯỚC 1: XÓA DỮ LIỆU CŨ ---
        self.reset_dashboard_data()

        # --- BƯỚC 2: THIẾT LẬP UI ---
        self.lbl_status.setText("🚀 Đang khởi động Backtest...")
        self.is_started = True
        self.btn_control.setText("⏸ Tạm dừng")
        
        # --- BƯỚC 3: KHỞI TẠO WORKER ---
        # Nếu có worker cũ thì xóa đi cho sạch
        if self.worker is not None:
            if self.worker.isRunning():
                self.worker.terminate()
                self.worker.wait() # Đợi nó dừng hẳn
            self.worker = None

        # Tạo worker mới
        self.worker = BacktestWorker() # csv_path=None (Mặc định chạy live)
        
        # Kết nối tín hiệu
        self.worker.progress_signal.connect(self.on_live_update)
        self.worker.finished_signal.connect(self.on_process_finished)
        if hasattr(self.worker, 'error_signal'):
             self.worker.error_signal.connect(self.on_worker_error) 
        
        # BẮT ĐẦU CHẠY
        self.worker.start()
        
        if hasattr(self, 'anim_timer'):
            self.anim_timer.start()

    def on_live_update(self, data):
        self.latest_data_cache = data 
        if not self.is_ui_paused: self.process_new_data(data)

    def on_process_finished(self, result):
        self.is_started = False
        self.btn_control.setText("✔️ Xong")
        self.btn_control.setEnabled(False)
        if result: self.process_new_data(result)

    def update_status_animation(self):
        if not self.is_ui_paused: self.lbl_status.setText(funny_quant_runner())

    def safe_update_widget(self, widget, method, *args):
        if hasattr(widget, method): getattr(widget, method)(*args)

    def handle_coin_filter(self, c):
        self.active_filters["symbol"] = None if self.active_filters.get("symbol") == c else c
        self.apply_filters()

    def handle_dist_filter(self, i, t):
        if t == "day":
            val = (i + 1) if i != -1 else None
            self.active_filters["weekday"] = val 
        else:
            val = i if i != -1 else None
            self.active_filters["hour"] = val
            
        self.apply_filters()

    def handle_side_filter(self, s):
        norm_s = s.lower() if s else None
        self.active_filters["side"] = None if self.active_filters.get("side") == norm_s else norm_s
        self.apply_filters()

    # =========================================================================
    # XỬ LÝ FILE CSV (NEW FUNCTION)
    # =========================================================================
    def on_btn_load_csv_clicked(self):
        if self.worker is not None:
             self.worker = None

        self.is_started = False
        if hasattr(self, 'anim_timer'): self.anim_timer.stop()
        self.btn_control.setText("▶ Bắt đầu Backtest")
        
        # Mở file
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file CSV", "", "CSV Files (*.csv)")

        if file_path:
            # --- XÓA DỮ LIỆU CŨ TRƯỚC KHI LOAD MỚI ---
            self.reset_dashboard_data() 
            
            self.load_csv_data(file_path)
        else:
            self.lbl_status.setText("Đã hủy chọn file.")

    def load_csv_data(self, file_path):
        try:
            self.lbl_status.setText(f"⏳ Đang đọc file: {file_path}...")

            df = pl.read_csv(file_path)

            required_columns = ["symbol", "side", "time_close", "pnl_usd"]
            if not all(col in df.columns for col in required_columns):
                return

            trades_list = df.to_dicts()

            data_packet = {
                'trades': trades_list,
                'initial_capital': 10000.0, 
                'equity_curve': [] 
            }

            self.process_new_data(data_packet)

            self.lbl_status.setText(f"📂 Chế độ xem file: {len(trades_list)} lệnh")

            self.btn_control.setText("▶ Chạy Backtest Mới")
            self.btn_control.setEnabled(True) 

            self.latest_data_cache = {} 
            self.is_started = False

        except Exception as e:
            print(f"Lỗi: {e}")

    def on_worker_error(self, err_msg):
        self.is_started = False
        self.anim_timer.stop()
        self.btn_control.setText("▶ Bắt đầu Backtest")
        self.lbl_status.setText("❌ Đã xảy ra lỗi!")

        QMessageBox.critical(self, "Lỗi Backtest", err_msg)

    def reset_dashboard_data(self):
        self.all_trades_df = pl.DataFrame()
        self.latest_data_cache = {}
        self.active_filters = {"date": None, "symbol": None, "side": None, "weekday": None, "hour": None}

        empty_df = pl.DataFrame()
        empty_list = []

        self.safe_update_widget(self.widget_pnl, 'update_data', empty_df)
        self.safe_update_widget(self.widget_asset, 'update_data', empty_list) 
        self.safe_update_widget(self.widget_stats, 'update_data', {'trades': [], 'equity_curve': []})
        self.safe_update_widget(self.widget_history, 'update_data', empty_list)
        self.safe_update_widget(self.widget_coins, 'update_data', empty_df, None)
        self.safe_update_widget(self.widget_ls, 'update_data', empty_df, None)
        self.safe_update_widget(self.widget_Scatter, 'update_data', empty_df)

        self.widget_cal.set_trades([], None)

        self.safe_update_widget(self.day_dist, 'update_data', empty_df, None)
        self.safe_update_widget(self.hour_dist, 'update_data', empty_df, None)
        
        self.lbl_status.setText("🧹 Đã xóa dữ liệu cũ.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 9))
    window = DraggableDashboard()
    window.show()
    sys.exit(app.exec())