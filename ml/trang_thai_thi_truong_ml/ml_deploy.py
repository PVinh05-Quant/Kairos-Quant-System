import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'trang_thai_thi_truong_ml', 'du_lieu_ml')

OLD_PATH = os.path.join(DATA_DIR, 'model_new.pth')
NEW_PATH = os.path.join(DATA_DIR, 'model_pytorch.pth')

if os.path.exists(OLD_PATH):
    if os.path.exists(NEW_PATH):
        os.rename(NEW_PATH, NEW_PATH + ".bak")

    os.rename(OLD_PATH, NEW_PATH)
    print(f"✅ Đã Deploy thành công! 'model_new.pth' -> 'model_pytorch.pth'")
else:
    print("❌ Không tìm thấy model_new.pth để deploy")