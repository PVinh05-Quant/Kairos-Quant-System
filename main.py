import sys
import os
import time
import shutil
import subprocess

# Thêm thư mục hiện tại vào sys.path để import các module con
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

CONTENT_WIDTH = 62

def get_indent():
    """Tính toán khoảng trắng để căn giữa nội dung"""
    try:
        terminal_width = shutil.get_terminal_size().columns
        padding = max(0, (terminal_width - CONTENT_WIDTH) // 2)
        return " " * padding
    except:
        return ""

def dung_man_hinh():
    """Dừng màn hình để người dùng đọc thông báo"""
    indent = get_indent()
    print("\n")
    try:
        input(indent + Fore.WHITE + Style.DIM + "👉 Nhấn phím Enter để đóng cửa sổ...")
    except:
        pass

# --- XỬ LÝ IMPORT THƯ VIỆN NGOÀI (COLORAMA) ---
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    # Fallback nếu chưa cài colorama
    class ColorFallback:
        def __getattr__(self, name): return ""
    init = lambda **kwargs: None
    Fore = Back = Style = ColorFallback()

# --- XỬ LÝ IMPORT MODULE NỘI BỘ ---
try:
    from utils.log import logger
    from chuc_nang.chay_demo import chay_demo
except ImportError as e:
    print(f"❌ Lỗi Import Module: {e}")
    print("👉 Hãy đảm bảo cấu trúc thư mục đúng: KAIROS QUANT SYSTEM v1.0/")
    input("👉 Nhấn Enter để thoát...")
    sys.exit(1)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    indent = get_indent()
    
    print("\n" * 2) 
    
    print(indent + Fore.CYAN + Style.BRIGHT + "╔" + "═"*60 + "╗")
    print(indent + Fore.CYAN + Style.BRIGHT + "║" + " "*60 + "║")

    # --- TÊN DỰ ÁN MỚI ---
    title_text = "⚡  KAIROS QUANT SYSTEM v1.0  ⚡"
    
    print(indent + Fore.CYAN + Style.BRIGHT + "║" + Fore.YELLOW + Style.BRIGHT + "{:^58}".format(title_text) + Fore.CYAN + Style.BRIGHT + "║")
    
    print(indent + Fore.CYAN + Style.BRIGHT + "║" + " "*60 + "║")
    print(indent + Fore.CYAN + Style.BRIGHT + "╚" + "═"*60 + "╝")
    
    print(indent + Fore.BLUE + Style.DIM + " Dev by: Mop | " + time.strftime("%Y-%m-%d %H:%M"))
    print("\n")

def hien_thi_menu():
    indent = get_indent()
    
    print(indent + Fore.WHITE + " CHỌN CHẾ ĐỘ GIAO DỊCH:")
    print(indent + Fore.WHITE + " " + "─"*30)
    
    print(indent + Fore.GREEN + Style.BRIGHT +  " [1] 🎮  PAPER TRADING   " + Fore.RESET + Style.DIM + "  (Chạy Demo - An toàn)")
    print(indent + Fore.YELLOW + Style.BRIGHT + " [2] 📊  BACKTEST        " + Fore.RESET + Style.DIM + "  (Giao diện phân tích)") 
    print(indent + Fore.WHITE + " " + "─"*30)
    print(indent + Fore.MAGENTA + Style.BRIGHT +" [3] ❌  EXIT")
    print("\n")

def main():
    while True:
        print_banner()
        hien_thi_menu()
        
        indent = get_indent()
        try:
            choice = input(indent + Fore.CYAN + Style.BRIGHT + "👉 Nhập lựa chọn (1-4): " + Style.RESET_ALL).strip()
        except KeyboardInterrupt:
            break

        print("\n" + indent + Fore.WHITE + "─"*60)


        if choice == '1':
            print(indent + Back.YELLOW + Fore.BLACK + " 📊 ĐANG KHỞI ĐỘNG DASHBOARD... " + Style.RESET_ALL)
            print(indent + Fore.YELLOW + " ⏳ Vui lòng đợi cửa sổ phân tích hiện lên...")
            time.sleep(1)

            dashboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hien_thi', 'dashboard_demo.py')

            if os.path.exists(dashboard_path):
                try:
                    # Chạy Dashboard bằng subprocess để tách biệt process
                    subprocess.run([sys.executable, dashboard_path], check=True)
                except KeyboardInterrupt:
                    pass
                except Exception as e:
                    print(indent + Fore.RED + f"❌ Lỗi khi mở Dashboard: {e}")
                    print(indent + Fore.RED + "   Hãy đảm bảo bạn đã cài thư viện: pip install PyQt6 pandas matplotlib")
            else:
                print(indent + Fore.RED + "❌ Không tìm thấy file 'hien_thi/dashboard_demo.py'!")
                print(indent + Fore.RED + f"   Đường dẫn: {dashboard_path}")

        elif choice == '2':
            print(indent + Back.YELLOW + Fore.BLACK + " 📊 ĐANG KHỞI ĐỘNG DASHBOARD... " + Style.RESET_ALL)
            print(indent + Fore.YELLOW + " ⏳ Vui lòng đợi cửa sổ phân tích hiện lên...")
            time.sleep(1)

            # Đường dẫn tương đối đến file Dashboard
            dashboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hien_thi', 'dashboard_backtest.py')
            
            if os.path.exists(dashboard_path):
                try:
                    # Chạy Dashboard bằng subprocess để tách biệt process
                    subprocess.run([sys.executable, dashboard_path], check=True)
                except KeyboardInterrupt:
                    pass
                except Exception as e:
                    print(indent + Fore.RED + f"❌ Lỗi khi mở Dashboard: {e}")
                    print(indent + Fore.RED + "   Hãy đảm bảo bạn đã cài thư viện: pip install PyQt6 pandas matplotlib")
            else:
                print(indent + Fore.RED + "❌ Không tìm thấy file 'hien_thi/dashboard_backtest.py'!")
                print(indent + Fore.RED + f"   Đường dẫn: {dashboard_path}")
            

        elif choice == '3':
            print(indent + Fore.CYAN + "👋 Hẹn gặp lại! Chúc bạn trade thắng lớn!")
            break 
        
        else:
            print(indent + Fore.RED + "❌ Lựa chọn không hợp lệ! Vui lòng thử lại.")
            time.sleep(1.5)
            continue

        print("\n" + indent + Fore.WHITE + "─"*60)
        input(indent + Fore.WHITE + Style.DIM + "👉 Nhấn Enter để quay lại menu chính...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Đã xảy ra lỗi không mong muốn: {e}")
    except KeyboardInterrupt:
        pass
    
    dung_man_hinh()