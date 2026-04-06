import sys
import os
import time
import polars as pl
import pyqtgraph as pg
from datetime import datetime, timedelta
from pyqtgraph import QtCore, QtGui
from functools import partial
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QTableWidget, QTableWidgetItem, QHeaderView, 
    QComboBox, QFrame, QSplitter, QAbstractItemView, QStatusBar,
    QPushButton, QSizePolicy, QDockWidget, QToolBar, QGridLayout, QScrollArea, QStackedWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QRectF, QPointF
from PyQt6.QtGui import QColor, QFont, QPicture, QPainter, QPen, QBrush, QLinearGradient

# --- PROJECT PATH SETUP ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from utils.log import logger
from chuc_nang.chay_demo import chay_demo
import thuc_thi_lenh.quan_ly_lenh as quan_ly_lenh
from thuc_thi_lenh.quan_ly_lenh import ui_signals, get_all_data

# =================================================================================
# 1. THEME CONFIGURATION
# =================================================================================
BG_COLOR = "#0e0e0e"
CARD_BG = "#141414"
BORDER_COLOR = "#2a2a2a"
TEXT_MAIN = "#E0E0E0"
TEXT_SUB = "#999999"
ACCENT_COLOR = "#C8AA6E"
COLOR_WIN = "#4CAF50" # Green
COLOR_LOSS = "#E53935" # Red

# =================================================================================
# 2. DRAGGABLE CARD
# =================================================================================
class DraggableCard(QDockWidget):
    def __init__(self, title, widget, parent=None):
        super().__init__(title, parent)
        self.setWidget(widget)
        # FIX: Combine features manually for PyQt6
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | 
                         QDockWidget.DockWidgetFeature.DockWidgetFloatable |
                         QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.setTitleBarWidget(None) 
        self.setStyleSheet(f"QDockWidget {{ border: 1px solid {BORDER_COLOR}; color: {TEXT_MAIN}; }} QDockWidget::title {{ background: {CARD_BG}; padding: 6px; font-weight: bold; font-size: 11px; color: {ACCENT_COLOR}; }}")

# =================================================================================
# 3. HEATMAP WIDGET
# =================================================================================
class MarketHeatmap(QWidget):
    # Signal: Sends (symbol, timeframe) when clicked
    cell_clicked = pyqtSignal(str, str) 

    def __init__(self):
        super().__init__()
        self.layout = QGridLayout(self)
        self.layout.setSpacing(4) 
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        # Mapping: Display Name (Header) -> System Code
        # Ensure these codes match exactly what your Chart Widget expects
        self.tf_map = {
            "1m": "1m", 
            "5m": "5m", 
            "15m": "15m", 
            "30m": "30m", 
            "1h": "1h", 
            "4h": "4h", 
            "1d": "1d"
        }
        # List of headers in desired order
        self.display_headers = ["1m", "5m", "15m", "30m", "1h", "4h", "1d"]
        
        self.init_header()

    def init_header(self):
        # Top-left corner cell
        lbl_sym = QLabel("SYMBOL")
        lbl_sym.setStyleSheet(f"color: {ACCENT_COLOR}; font-weight: bold; font-size: 12px;")
        lbl_sym.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(lbl_sym, 0, 0)

        # Timeframe Headers
        for col, header in enumerate(self.display_headers):
            lbl = QLabel(header)
            lbl.setStyleSheet(f"color: {TEXT_SUB}; font-weight: bold; font-size: 11px;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(lbl, 0, col + 1)

    def on_btn_click(self, symbol, tf):
        """Intermediate function to handle clicks accurately"""
        # Debug print to verify what is being sent
        # print(f"Heatmap Clicked: {symbol} - {tf}") 
        self.cell_clicked.emit(symbol, tf)

    def update_data(self, data):
        # 1. FILTER: Only get OPEN POSITIONS
        raw_positions = data.get('lenh_dang_chay', {})
        
        if not raw_positions or not isinstance(raw_positions, dict):
            self.clear_content()
            return

        open_positions = raw_positions
        symbols = sorted(list(open_positions.keys()))
        
        if not symbols: 
            self.clear_content()
            return

        # Clear old data (keep header row 0)
        self.clear_content()

        # 2. Draw Table
        for row_idx, sym in enumerate(symbols):
            actual_row = row_idx + 1 
            
            # --- Column 0: Symbol Name ---
            btn_sym = QPushButton(sym)
            btn_sym.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_sym.setFlat(True)
            btn_sym.setStyleSheet(f"color: {TEXT_MAIN}; font-weight: bold; text-align: left; padding-left: 5px; border: none;")
            
            # Click symbol -> Default to 1m
            btn_sym.clicked.connect(partial(self.on_btn_click, sym, "1m"))
            self.layout.addWidget(btn_sym, actual_row, 0)

            # --- Get Position Info ---
            order_info = open_positions.get(sym)
            position_side = 'buy'
            if isinstance(order_info, dict):
                position_side = order_info.get('side', 'buy')
            
            # --- Timeframe Columns (Colored Buttons) ---
            import random 
            for col_idx, header in enumerate(self.display_headers):
                tf_code = self.tf_map[header] # Get code: "30m" from header "30m"
                
                # Logic for color (Mock logic, replace with real data if available)
                is_bullish = True
                if header in ["4h", "1d"]: is_bullish = (position_side == 'buy')
                else: 
                    # Random logic for demo
                    if position_side == 'buy': is_bullish = random.random() > 0.2
                    else: is_bullish = random.random() < 0.2

                color = COLOR_WIN if is_bullish else COLOR_LOSS
                
                # Create Button
                btn_tf = QPushButton()
                btn_tf.setFixedSize(35, 25) 
                btn_tf.setCursor(Qt.CursorShape.PointingHandCursor)
                btn_tf.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color}; 
                        border: 1px solid #222; 
                        border-radius: 3px;
                    }}
                    QPushButton:hover {{ border: 1px solid white; }}
                """)
                
                # --- CRITICAL FIX: Use partial to freeze arguments ---
                # This ensures the button is tied to the specific 'sym' and 'tf_code' of this iteration
                btn_tf.clicked.connect(partial(self.on_btn_click, sym, tf_code))
                
                self.layout.addWidget(btn_tf, actual_row, col_idx + 1)

        # Push layout to top
        self.layout.setRowStretch(len(symbols) + 1, 1)

    def clear_content(self):
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            if item.widget():
                idx = self.layout.getItemPosition(self.layout.indexOf(item.widget()))
                if idx[0] > 0: item.widget().setParent(None)

# =================================================================================
# 4. CHART WIDGET
# =================================================================================
class BieuDoGiaoDich(QWidget):
    back_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        # ===== LAYOUT =====
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # ===== HUD (Thông số trên đầu) =====
        self.lbl_info = QLabel("SẴN SÀNG")
        self.lbl_info.setFixedHeight(30)
        self.lbl_info.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_MAIN};
                font-family: 'Segoe UI';
                font-size: 13px;
                font-weight: bold;
                padding-left: 10px;
                background-color: {BG_COLOR};
                border-bottom: 1px solid #333;
            }}
        """)
        self.layout.addWidget(self.lbl_info)

        # ===== PLOT =====
        self.plot = pg.PlotWidget()
        self.plot.setBackground(BG_COLOR)
        
        # Grid
        self.plot.showGrid(x=False, y=True, alpha=0.2) 
        self.plot.getPlotItem().hideButtons()

        # Trục Y
        self.plot.getAxis('left').setPen(None)
        self.plot.getAxis('left').setTextPen(TEXT_SUB)
        self.plot.getAxis('left').setStyle(tickTextOffset=8)
        
        # Trục X: Ẩn
        self.plot.showAxis('bottom', False)

        # Tắt AutoRange
        self.plot.enableAutoRange(axis='y', enable=False)
        self.plot.enableAutoRange(axis='x', enable=True)
        
        # QUAN TRỌNG: Tắt clip để text không bị cắt
        self.plot.setClipToView(False)

        # Đường giá chính
        self.price_line = self.plot.plot(
            pen=pg.mkPen("#2962FF", width=2.5) 
        )

        self.layout.addWidget(self.plot)

        # ===== SIGNAL =====
        self.plot.scene().sigMouseClicked.connect(self.on_chart_clicked)

        # ===== STATE =====
        self.current_symbol = ""
        self.current_tf = "1m"
        self.current_data = {}

    # ================== UTILS ==================
    def format_price(self, v):
        if v is None: return ""
        try:
            return f"{float(v):.8f}".rstrip('0').rstrip('.')
        except:
            return str(v)

    # ================== EVENTS ==================
    def on_chart_clicked(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.back_clicked.emit()

    # ================== DATA ==================
    def switch_context(self, symbol, timeframe):
        self.current_symbol = symbol
        self.current_tf = timeframe
        self.re_render()

    def update_data(self, data):
        self.current_data = data
        if not self.current_symbol:
            syms = list(data.get('lenh_dang_chay', {}).keys())
            if syms:
                self.current_symbol = syms[0]
        self.re_render()

    # ================== RENDER ==================
    def re_render(self):
        try:
            sym = self.current_symbol
            tf = self.current_tf
            key_df = f"df_{tf}"

            if not sym or sym not in self.current_data.get('data_lenh_dang_chay', {}):
                return

            # Lấy dữ liệu
            df = self.current_data['data_lenh_dang_chay'][sym].get(key_df)
            if df is None: return
            if hasattr(df, 'is_empty') and df.is_empty(): return
            if not hasattr(df, 'select'): df = pl.from_pandas(df)

            closes = df['close'].cast(pl.Float64).to_list()
            x = list(range(len(closes)))
            current_price = closes[-1]

            # 1. Vẽ đường giá
            self.price_line.setData(x, closes)

            # 2. Cập nhật HUD
            self.lbl_info.setText(f"""
                <html>
                <span style='color:{ACCENT_COLOR}; font-size:14px'>{sym}</span>
                <span style='color:#555'> | </span>
                <span style='color:{TEXT_SUB}'>{tf}</span>
                <span style='color:#555'> | </span>
                <span style='color:#2962FF; font-size:14px'>${self.format_price(current_price)}</span>
                </html>
            """)

            # 3. Xóa line cũ
            for item in list(self.plot.items()):
                if item is not self.price_line and not isinstance(
                    item, (pg.AxisItem, pg.ViewBox, pg.GridItem)
                ):
                    self.plot.removeItem(item)

            # 4. Vẽ Lệnh & Tính Range
            order = self.current_data.get('lenh_dang_chay', {}).get(sym)
            view_values = [min(closes), max(closes)]

            if order:
                # --- ENTRY (Màu Trắng Sáng) ---
                if order.get('entry_price'):
                    entry = order['entry_price']
                    view_values.append(entry)
                    line_entry = pg.InfiniteLine(
                        pos=entry, angle=0,
                        pen=pg.mkPen('#E0E0E0', width=1.5, style=Qt.PenStyle.DashLine)
                    )
                    # position=0.1: Đẩy vào trong 10% để tránh bị che bởi trục Y
                    line_entry.label = pg.InfLineLabel(
                        line_entry, text=f"{self.format_price(entry)}", 
                        position=0.1, color='#E0E0E0', movable=True, anchor=(0, 1)
                    )
                    self.plot.addItem(line_entry)

                # --- TP (Xanh) ---
                if order.get('tp_price'):
                    tp = order['tp_price']
                    view_values.append(tp)
                    line_tp = pg.InfiniteLine(
                        pos=tp, angle=0,
                        pen=pg.mkPen(COLOR_WIN, width=1.5, style=Qt.PenStyle.DashLine)
                    )
                    line_tp.label = pg.InfLineLabel(
                        line_tp, text=f"{self.format_price(tp)}", 
                        position=0.95, color=COLOR_WIN, movable=True, anchor=(1, 1) 
                    )
                    self.plot.addItem(line_tp)

                # --- SL (Đỏ) ---
                if order.get('sl_price'):
                    sl = order['sl_price']
                    view_values.append(sl)
                    line_sl = pg.InfiniteLine(
                        pos=sl, angle=0,
                        pen=pg.mkPen(COLOR_LOSS, width=1.5, style=Qt.PenStyle.DashLine)
                    )
                    line_sl.label = pg.InfLineLabel(
                        line_sl, text=f"{self.format_price(sl)}", 
                        position=0.95, color=COLOR_LOSS, movable=True, anchor=(1, 0)
                    )
                    self.plot.addItem(line_sl)

            # 5. TỰ ĐỘNG ZOOM (Tính toán Padding thủ công để chắc chắn)
            if view_values:
                min_y = min(view_values)
                max_y = max(view_values)
                
                diff = max_y - min_y
                if diff == 0: diff = 1
                
                # Tăng padding lên 15% để chừa chỗ cho chữ
                pad = diff * 0.15
                
                # Set Range thủ công, đảm bảo không bao giờ cắt mất chữ
                self.plot.setYRange(min_y - pad, max_y + pad, padding=0)

        except Exception as e:
            print(f"Chart Render Error: {e}")


# =================================================================================
# 5. MARKET VIEW CONTAINER
# =================================================================================
class MarketViewContainer(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self); self.layout.setContentsMargins(0,0,0,0)
        self.stack = QStackedWidget()
        
        self.heatmap_view = QWidget()
        h_layout = QVBoxLayout(self.heatmap_view); h_layout.setContentsMargins(0,0,0,0)
        self.heatmap = MarketHeatmap()
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setWidget(self.heatmap)
        scroll.setStyleSheet("background: transparent; border: none;")
        h_layout.addWidget(scroll)
        
        self.chart_view = BieuDoGiaoDich()
        
        self.stack.addWidget(self.heatmap_view)
        self.stack.addWidget(self.chart_view)
        self.layout.addWidget(self.stack)
        
        self.heatmap.cell_clicked.connect(self.go_to_chart)
        self.chart_view.back_clicked.connect(self.go_to_heatmap)

    def go_to_chart(self, symbol, timeframe):
        self.chart_view.switch_context(symbol, timeframe)
        self.stack.setCurrentIndex(1) 

    def go_to_heatmap(self):
        self.stack.setCurrentIndex(0) 

    def update_data(self, data):
        self.heatmap.update_data(data)
        self.chart_view.update_data(data)

# =================================================================================
# 6. SUMMARY, POSITIONS, HISTORY
# =================================================================================
class SummaryBox(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self); self.main_layout.setContentsMargins(10, 10, 10, 10); self.main_layout.setSpacing(15)
        self.lbl_equity_title = QLabel("VỐN SỞ HỮU (EQUITY)"); self.lbl_equity_title.setStyleSheet(f"color: {TEXT_SUB}; font-size: 10px; font-weight: bold;")
        self.val_equity = QLabel("$0.00"); self.val_equity.setStyleSheet(f"color: {ACCENT_COLOR}; font-size: 24px; font-weight: bold;")
        self.main_layout.addWidget(self.lbl_equity_title); self.main_layout.addWidget(self.val_equity)
        grid_frame = QFrame(); grid_frame.setStyleSheet(f"background: {BG_COLOR}; border-radius: 4px;")
        self.grid_layout = QVBoxLayout(grid_frame) 
        self.lbl_pnl = self._row("PnL Ròng", "$0.00", TEXT_MAIN)
        self.lbl_winrate = self._row("Tỷ lệ thắng", "0%", TEXT_MAIN)
        self.lbl_total = self._row("Tổng lệnh", "0", TEXT_MAIN)
        self.main_layout.addWidget(grid_frame); self.main_layout.addStretch()

    def _row(self, title, val, color):
        w = QWidget(); l = QHBoxLayout(w); l.setContentsMargins(0,2,0,2)
        t = QLabel(title); t.setStyleSheet(f"color: {TEXT_SUB}; font-size: 11px;")
        v = QLabel(val); v.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 12px;")
        l.addWidget(t); l.addStretch(); l.addWidget(v)
        self.grid_layout.addWidget(w); return v

    def update_data(self, data):
        hist = data.get('lich_su', []); 
        if not hist: return
        df = pl.DataFrame(hist)
        sum_pnl = df.select(pl.col("pnl").sum()).item()
        total = df.height
        wins = df.filter(pl.col("pnl") > 0).height
        win_rate = (wins/total*100) if total > 0 else 0
        self.val_equity.setText(f"${sum_pnl:,.2f}"); self.val_equity.setStyleSheet(f"color: {COLOR_WIN if sum_pnl >=0 else COLOR_LOSS}; font-size: 24px; font-weight: bold;")
        self.lbl_pnl.setText(f"{sum_pnl:+.2f}$"); self.lbl_winrate.setText(f"{win_rate:.1f}%"); self.lbl_total.setText(str(total))

class TableBase(QTableWidget):
    def __init__(self, headers):
        super().__init__(0, len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.setShowGrid(False); self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers); self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setStyleSheet(f"QTableWidget {{ background-color: {CARD_BG}; color: {TEXT_MAIN}; border: none; outline: 0; }} QHeaderView::section {{ background-color: {BG_COLOR}; color: {TEXT_SUB}; border: none; padding: 5px; font-weight: bold; }} QTableWidget::item {{ padding: 5px; border-bottom: 1px solid {BORDER_COLOR}; }} QTableWidget::item:selected {{ background-color: #333; }}")
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.last_row_clicked = -1; self.cellClicked.connect(self.handle_row_click)
    def handle_row_click(self, row, col):
        if row == self.last_row_clicked and self.selectionModel().hasSelection(): self.clearSelection(); self.last_row_clicked = -1
        else: self.last_row_clicked = row

class PositionsTable(TableBase):
    def __init__(self): super().__init__(["Mã", "Chiều", "Giá Vào", "Size", "Thời Gian"])
    def refresh(self, data):
        pos = data.get('lenh_dang_chay', {}); self.setRowCount(len(pos))
        for i, (sym, info) in enumerate(pos.items()):
            self.setItem(i, 0, QTableWidgetItem(str(sym)))
            item_side = QTableWidgetItem(info['side'].upper()); item_side.setForeground(QColor(COLOR_WIN) if info['side'] == 'buy' else QColor(COLOR_LOSS)); self.setItem(i, 1, item_side)
            self.setItem(i, 2, QTableWidgetItem(f"{info['entry_price']}")); self.setItem(i, 3, QTableWidgetItem(f"{info['amount']}")); self.setItem(i, 4, QTableWidgetItem(str(info['time'])))
            for j in range(5): self.item(i, j).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

from datetime import datetime, timedelta

class HistoryTable(TableBase):
    def __init__(self):
        # Đổi tên cột 3 thành "Thời Lượng"
        super().__init__(["Mã", "PnL ($)", "Thời Lượng", "Lý Do"])

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        self.verticalHeader().setDefaultSectionSize(26)
        self.setAlternatingRowColors(True)

    def refresh(self, data):
        hist = data.get("lich_su", [])
        if not hist:
            self.setRowCount(0)
            return

        # Lấy 30 dòng mới nhất
        recent_data = hist[-30:][::-1]
        self.setRowCount(len(recent_data))

        for i, row in enumerate(recent_data):

            # ─── 1. SYMBOL ───────────────────────────
            item_symbol = QTableWidgetItem(str(row.get("symbol", "")))
            item_symbol.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(i, 0, item_symbol)

            # ─── 2. PNL ──────────────────────────────
            pnl = float(row.get("pnl", 0.0))
            # Thêm khoảng trắng để số không dính lề
            pnl_text = f"{pnl:+.2f} " 

            item_pnl = QTableWidgetItem(pnl_text)
            item_pnl.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            if pnl > 0:
                item_pnl.setForeground(QColor(COLOR_WIN))
                # item_pnl.setBackground(QColor(0, 80, 0)) # Bỏ background nếu muốn giao diện sạch hơn
            elif pnl < 0:
                item_pnl.setForeground(QColor(COLOR_LOSS))
                # item_pnl.setBackground(QColor(80, 0, 0))

            item_pnl.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            self.setItem(i, 1, item_pnl)

            # ─── 3. THỜI LƯỢNG (DURATION) ─────────────
            duration_str = "--"
            try:
                day = str(row.get('day', ''))
                # Cắt bỏ phần giây lẻ (.123) nếu có để tránh lỗi format
                t_open = str(row.get('open_time', '')).split('.')[0]
                t_close = str(row.get('close_time', '')).split('.')[0]
                
                fmt = "%Y-%m-%d %H:%M:%S"
                # Ghép ngày và giờ
                start_dt = datetime.strptime(f"{day} {t_open}", fmt)
                end_dt = datetime.strptime(f"{day} {t_close}", fmt)
                
                # --- XỬ LÝ QUA ĐÊM (Overnight) ---
                # Nếu giờ đóng < giờ mở, nghĩa là đã qua ngày hôm sau -> Cộng 1 ngày
                if end_dt < start_dt:
                    end_dt += timedelta(days=1)
                
                # Tính khoảng cách giây
                secs = int((end_dt - start_dt).total_seconds())
                h = secs // 3600
                m = (secs % 3600) // 60
                s = secs % 60
                
                # Format hiển thị (1h30p, 15p, 45s)
                if h > 0:
                    duration_str = f"{h}h{m}p"
                elif m > 0:
                    duration_str = f"{m}p"
                else:
                    duration_str = f"{s}s"
                    
            except Exception:
                # Fallback nếu dữ liệu lỗi
                duration_str = str(row.get('close_time', ''))

            item_duration = QTableWidgetItem(duration_str)
            item_duration.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(i, 2, item_duration)

            # ─── 4. LÝ DO (REASON) ────────────────────
            reason = str(row.get("reason", ""))
            item_reason = QTableWidgetItem(reason)
            item_reason.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.setItem(i, 3, item_reason)

                    
# =================================================================================
# 7. MAIN WINDOW & THREAD
# =================================================================================
class TradingBridge(QThread):
    data_signal = pyqtSignal(dict)
    def run(self):
        try:
            ui_signals.data_changed.connect(self.data_signal.emit)
            chay_demo()
            self.data_signal.emit(get_all_data())
            self.exec()
        except Exception as e: logger.error(f"Bridge Error: {e}")

class MainDashboard_demo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("demo")
        self.resize(750, 500); self.setStyleSheet(f"background-color: {BG_COLOR};")
        self.setDockNestingEnabled(True) 

        self.market_view = MarketViewContainer()
        self.pos_table = PositionsTable()
        self.summary_widget = SummaryBox()
        self.hist_table = HistoryTable()

        self.dock_market = DraggableCard("THỊ TRƯỜNG", self.market_view)
        self.dock_pos = DraggableCard("VỊ THẾ ĐANG MỞ", self.pos_table)
        self.dock_stats = DraggableCard("TỔNG QUAN TÀI KHOẢN", self.summary_widget)
        self.dock_hist = DraggableCard("LỊCH SỬ GIAO DỊCH", self.hist_table)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_market)
        self.splitDockWidget(self.dock_market, self.dock_pos, Qt.Orientation.Vertical)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_stats)
        self.splitDockWidget(self.dock_stats, self.dock_hist, Qt.Orientation.Vertical)

        self.resizeDocks([self.dock_market, self.dock_pos], [316, 384], Qt.Orientation.Vertical)
        self.resizeDocks([self.dock_stats, self.dock_hist], [250, 450], Qt.Orientation.Vertical)
        self.resizeDocks([self.dock_market, self.dock_stats], [400, 350], Qt.Orientation.Horizontal)

        self.setStatusBar(QStatusBar()); self.statusBar().setStyleSheet(f"color: {TEXT_SUB}; background: {CARD_BG}; border-top: 1px solid {BORDER_COLOR};")
        self.worker = TradingBridge()
        self.worker.data_signal.connect(self.sync_all)
        self.worker.start()

    def sync_all(self, data):
        self.market_view.update_data(data)
        self.pos_table.refresh(data)
        self.summary_widget.update_data(data)
        self.hist_table.refresh(data)
        p_count = len(data.get('lenh_dang_chay', {}))
        self.statusBar().showMessage(f"🟢 Running Realtime | Lệnh mở: {p_count} | Update: {time.strftime('%H:%M:%S')}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 9))
    win = MainDashboard_demo()
    win.show()
    sys.exit(app.exec())