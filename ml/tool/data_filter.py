import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, 'du_lieu_ml', 'trading_memory.csv')
OUTPUT_FILE = os.path.join(BASE_DIR, 'du_lieu_ml', 'trading_memory_balanced.csv')

def tao_log_can_bang():
    print(f"📂 Đang đọc dữ liệu từ: {INPUT_FILE}...")
    
    if not os.path.exists(INPUT_FILE):
        print("❌ Không tìm thấy file log gốc.")
        return

    try:
        df = pd.read_csv(INPUT_FILE)

        df['correct'] = pd.to_numeric(df['correct'], errors='coerce')

        df_clean = df.dropna(subset=['correct']).copy()
        df_clean['correct'] = df_clean['correct'].astype(int)

        if df_clean.empty:
            print("⚠️ File log không có dữ liệu 'correct' hợp lệ nào.")
            return

        count_series = df_clean['correct'].value_counts()
        print("\n📊 Phân bố dữ liệu GỐC:")
        print(count_series.sort_index())

        if len(count_series) < 2:
            print("⚠️ Chỉ có 1 loại nhãn duy nhất. Không cần cân bằng.")
            df_clean.to_csv(OUTPUT_FILE, index=False)
            return

        min_samples = count_series.min()
        print(f"\n✂️ Sẽ cắt gọt dữ liệu về mức thấp nhất: {min_samples} dòng/loại")

        balanced_dfs = []
        for label in count_series.index:
            df_subset = df_clean[df_clean['correct'] == label]
            
            df_sampled = df_subset.sample(n=min_samples, random_state=42)
            balanced_dfs.append(df_sampled)

        df_final = pd.concat(balanced_dfs)
        df_final = df_final.sample(frac=1, random_state=42).reset_index(drop=True)

        df_final.to_csv(OUTPUT_FILE, index=False)

        print("-" * 50)
        print(f"✅ ĐÃ TẠO FILE LOG CÂN BẰNG: {OUTPUT_FILE}")
        print(f"📊 Tổng số dòng: {len(df_final)}")
        print(f"🔍 Phân bố MỚI (Đều tăm tắp):")
        print(df_final['correct'].value_counts().sort_index())
        print("-" * 50)
        
        print("💡 Gợi ý: Hãy đổi tên file này thành 'trading_memory.csv' nếu muốn AI học ngay lập tức.")

    except Exception as e:
        print(f"❌ Lỗi xử lý: {e}")

tao_log_can_bang()