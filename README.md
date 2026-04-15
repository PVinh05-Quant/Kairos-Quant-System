<div align="center">
 
<img width="224" height="224" alt="image" src="https://github.com/user-attachments/assets/5a1b5bcf-e6bb-4d92-a4a7-0c55697ba30e" />

# KAIROS QUANT SYSTEM
### **End-to-End Data Analytics System for Strategy Optimization in Financial Markets**

[![Python](https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Market](https://img.shields.io/badge/Market-Crypto-orange?style=for-the-badge)](https://www.binance.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](https://opensource.org/licenses/MIT)

`Python` • `Pandas` • `Polars` • `Scikit-Learn` • `ETL Pipeline` • `Backtesting` • `Quant Analysis`

<div align="left">
 
-----

### 🚀 Điểm nổi bật của dự án (Project Highlights)

  * **Xây dựng hệ thống phân tích dữ liệu:** Giao dịch từ nhiều nguồn (**Binance, OKX, Bybit**) nhằm hỗ trợ ra quyết định dựa trên dữ liệu.
  * **Thiết kế pipeline ETL tự động:** Thu thập, xử lý và chuẩn hóa dữ liệu đa khung thời gian (**1m–1d**).
  * **Phân tích dữ liệu lịch sử quy mô lớn:** Xử lý hàng triệu dòng dữ liệu để xác định các pattern thị trường (**trend, breakout, mean-reversion**).
  * **Phát triển hệ thống backtesting:** Đánh giá hiệu suất và so sánh các chiến lược giao dịch một cách khách quan.
  * **Ứng dụng Machine Learning:** Phân loại trạng thái thị trường và hỗ trợ cải thiện chất lượng tín hiệu.
  * **Trực quan hóa dữ liệu:** Hiển thị hiệu suất thông qua dashboard phục vụ phân tích và ra quyết định chuyên sâu.

-----

### 📊 Minh họa Backtesting

![$RV424Z6](https://github.com/user-attachments/assets/4883c4f4-e1ca-4e34-b806-220ae38faccc)

-----

## 📊 Kết quả đạt được (Key Results)

- Xử lý dữ liệu lịch sử quy mô lớn (hàng triệu dòng) trên nhiều năm  
- Tăng tốc backtesting bằng phương pháp vector hóa, nhanh hơn đáng kể so với xử lý tuần tự (loop)  
- Hỗ trợ phân tích đa khung thời gian (từ 1 phút đến 1 ngày)  
- Tự động hóa toàn bộ quy trình từ thu thập, xử lý đến phân tích dữ liệu  

## 📖 Mục lục tổng quan (Table of Contents)

1. [Tầm nhìn & Triết lý hệ thống (Vision & Philosophy)](#1)
2. [Giới thiệu chung (Overview)](#2)
3. [Tính năng cốt lõi & Công nghệ đột phá](#3)
4. [Kiến trúc hệ thống (System Architecture)](#4)
5. [Logic Chiến lược giao dịch (Core Engine & Voting System)](#5)
6. [Hệ thống Trí tuệ Nhân tạo & Machine Learning (AI/ML)](#6)
7. [Hệ thống Backtest & Trực quan hóa (PyQt6 Dashboard)](#7)
8. [Quản trị rủi ro & Quản lý vốn (Risk Management)](#8)
9. [Cấu trúc thư mục (Directory Tree)](#9)
10. [Yêu cầu & Hướng dẫn cài đặt (Setup Instructions)](#10)
11. [Hướng dẫn sử dụng & Cấu hình (Configuration & Usage)](#11)
12. [Lộ trình phát triển tương lai (Roadmap)](#12)
13. [Cảnh báo rủi ro (Disclaimer)](#13)

-----

<a name="1"></a>

## 1. TẦM NHÌN & TRIẾT LÝ HỆ THỐNG (VISION & PHILOSOPHY)

**KAIROS QUANT SYSTEM** không chỉ là một trading bot — mà là một **Hệ sinh thái giao dịch định lượng (Quantitative Trading Ecosystem)** được thiết kế để vận hành theo nguyên tắc **data-driven, xác suất và tự động hóa hoàn toàn**.

Tầm nhìn của hệ thống là xây dựng một **a systematic, data-driven decision engine designed to minimize emotional bias**, nơi mọi hành động đều được dẫn dắt bởi dữ liệu, mô hình thống kê và logic định lượng.

**Triết lý cốt lõi:**
**“Tư duy chiến lược của con người – tốc độ và kỷ luật tuyệt đối của máy móc.”**

### Kiến trúc vận hành

* **System Architect – Bộ não chiến lược:** thiết kế kiến trúc tổng thể của hệ thống: từ logic giao dịch, pipeline dữ liệu (ETL), mô hình quản trị rủi ro, đến cơ chế chấm điểm và tối ưu hóa chiến lược. Mọi quyết định đều được chuẩn hóa thành thuật toán có thể kiểm chứng bằng dữ liệu lịch sử.
* **AI & Automation – Bộ máy thực thi:** AI và Automation được sử dụng để tăng tốc quá trình phát triển, tối ưu hóa mã nguồn và áp dụng Machine Learning vào việc phân loại tín hiệu thị trường, nhận diện mẫu hành vi giá và cải thiện hiệu suất chiến lược theo thời gian thực.

### Mục tiêu hệ thống

* Loại bỏ hoàn toàn yếu tố cảm xúc của con người (FOMO, Panic Sell).
* Chuẩn hóa quyết định giao dịch dựa trên xác suất thống kê.
* Tự động hóa quy trình phân tích → ra quyết định → thực thi.
* Tối ưu hóa hiệu suất thông qua backtest và học từ dữ liệu lịch sử.
* Xây dựng hệ thống có khả năng mở rộng thành nền tảng Quant hoàn chỉnh.

**KAIROS QUANT SYSTEM được tạo ra để biến giao dịch từ “nghệ thuật cảm tính” thành “khoa học định lượng”** — nơi kỷ luật, dữ liệu và thuật toán thay thế hoàn toàn trực giác.

-----

<a name="2"></a>

## 2. GIỚI THIỆU CHUNG (OVERVIEW)

**KAIROS** là một **End-to-End Algorithmic Trading System** được thiết kế chuyên sâu cho thị trường tiền điện tử, bao phủ toàn bộ vòng đời của một giao dịch — từ thu thập dữ liệu, xử lý, ra quyết định đến backtest và trực quan hóa.

Hệ thống được xây dựng theo kiến trúc **pipeline định lượng hoàn chỉnh**, đảm bảo tốc độ xử lý cao, khả năng mở rộng và tính nhất quán trong ra quyết định.

### Các thành phần chính của hệ thống

* **ETL Pipeline – Thu thập & chuẩn hóa dữ liệu:** Tự động thu thập dữ liệu đa khung thời gian (Multi-Timeframe) từ 1m đến 1d thông qua API của các sàn giao dịch lớn. Dữ liệu được chuẩn hóa và lưu trữ theo cấu trúc time-series để phục vụ phân tích định lượng và backtesting.
* **High-Performance Processing – Xử lý hiệu năng cao:** Ứng dụng kỹ thuật **vectorization** kết hợp với các thư viện như **Pandas / Polars** để xử lý hàng triệu dòng dữ liệu thị trường trong thời gian ngắn. Pipeline được tối ưu để giảm latency và tăng tốc độ tính toán indicator, signal và feature engineering.
* **Intelligent Decision Engine – Bộ máy ra quyết định thông minh:** Kết hợp các phương pháp phân tích kỹ thuật truyền thống với mô hình Machine Learning nhằm dự báo trạng thái thị trường. Hệ thống đồng thời tích hợp các tín hiệu vi mô như order book, cấu trúc thanh khoản và biến động ngắn hạn để nâng cao chất lượng quyết định giao dịch.
* **Visual Backtesting Platform – Nền tảng kiểm thử trực quan:** Một ứng dụng Desktop phát triển bằng PyQt6, hoạt động như một nền tảng Quant chuyên nghiệp, cho phép người dùng tương tác trực tiếp với dữ liệu lịch sử, kiểm thử chiến lược, phân tích hiệu suất và tối ưu hóa tham số trong môi trường trực quan.

**KAIROS hướng tới việc chuẩn hóa toàn bộ quy trình giao dịch thành một hệ thống định lượng khép kín** — nơi dữ liệu, thuật toán và hiệu suất được kiểm soát chặt chẽ từ đầu vào đến đầu ra.

### 🚀 4 Chế độ hoạt động chính (The 4-Mode Execution Framework):

1. **Live Trading (Realtime):** Giao dịch tiền thật trực tiếp trên hệ thống máy chủ của sàn với độ trễ tối thiểu (Low-latency Execution).
2. **Paper Trading (Demo):** Giao dịch giả lập với dữ liệu thị trường thật theo thời gian thực (Forward Testing), giúp đánh giá thuật toán an toàn tuyệt đối trước khi nạp tiền thật.
3. **Bar-to-Bar Backtest (Event-driven):** Mô phỏng nghiêm ngặt dòng thời gian thực (Candle-by-Candle) nhằm loại bỏ hoàn toàn lỗi nhìn trước tương lai (Look-ahead bias). Hỗ trợ linh hoạt hai chế độ tùy theo quy mô phần cứng:
   * **Đơn luồng (Single-threading):** Chạy kiểm thử chuyên sâu cho 1 cặp tiền cụ thể.
   * **Đa luồng (Multi-threading):** Kiểm thử song song cùng lúc hàng chục cặp tiền để tối ưu hóa thời gian chờ.
4. **Vectorized Backtest (Kiểm thử ma trận):** Ứng dụng kỹ thuật xử lý mảng trên Pandas/Polars. Cho phép quét qua khối lượng dữ liệu lịch sử khổng lồ (hàng triệu nến) chỉ trong vài phút, phục vụ chuyên biệt cho quá trình R&D và dò tìm siêu tham số (Hyperparameters) cực nhanh.

-----

<a name="3"></a>

## 3. TÍNH NĂNG CỐT LÕI & CÔNG NGHỆ ĐỘT PHÁ

### 🚀 Core Trading & Execution

* **Multi-Exchange Integration:** Tích hợp liền mạch với Binance, OKX, Bybit thông qua chuẩn `ccxt`, giúp dễ dàng mở rộng sang các sàn khác mà không cần viết lại logic.
* **Dynamic Position Sizing:** Tự động tính toán khối lượng lệnh (Lot size) dựa trên % rủi ro cho phép trên tổng vốn (Risk per trade) và đòn bẩy linh hoạt.

### ⚡ Xử lý dữ liệu High-Performance (Dual-Engine)

* **Quy trình Kiểm định kép (Dual-Backtesting):** Ứng dụng Vectorized Backtest để tìm kiếm ý tưởng giao dịch nhanh chóng, sau đó dùng Bar-to-Bar Backtest để thẩm định lại độ chính xác, kiểm soát trượt giá (Slippage) và độ trễ.
* **Tối ưu hóa với Pandas/Polars (Vectorization):** Thay vì dùng vòng lặp `for` chậm chạp để duyệt qua từng cây nến, KAIROS tính toán các bộ chỉ báo phức tạp (TA Indicators như RSI, MACD, ATR, Bollinger Bands...) bằng các phép toán ma trận (Matrix operations) trên toàn bộ mảng dữ liệu. Điều này giúp tăng tốc độ xử lý và Backtest lên **gấp hàng trăm lần** so với truyền thống.

### 📡 Hệ thống Monitor & Thông báo

* **Logging System đa cấp độ:** Ghi nhận mọi hoạt động (Info, Warning, Error, Trade Execution) vào file `.log` để dễ dàng traceback lỗi hệ thống.
* **Telegram/Email Webhooks:** Bắn thông báo ngay lập tức về điện thoại khi có lệnh Mở/Đóng, Cắt lỗ/Chốt lời hoặc khi hệ thống phát hiện rủi ro bất thường.

-----

<a name="4"></a>

## 4. KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE)

Hệ thống được thiết kế theo chuẩn Modular Architecture, phân tách rõ ràng trách nhiệm của từng khối (Separation of Concerns).

```mermaid
graph TD
    A[Thu thập Dữ liệu - CCXT API] -->|Dữ liệu thô OHLCV & Sổ lệnh| B(Bộ Xử lý Dữ liệu ETL)
    B -->|Dữ liệu Sạch Vector hóa| C{Bộ lọc Thị trường AI/ML}
    C -->|Trạng thái: Đi ngang/Có xu hướng| D[Hệ thống Chấm điểm Đa chiến lược]
    D -->|Tín hiệu + Điểm bỏ phiếu| E{Quản trị Rủi ro & Tính Toán Đi Vốn}
    E -->|Tín hiệu Hợp lệ| F[Động cơ Thực thi Lệnh]
    E -->|Tín hiệu Bị từ chối| B
    F -->|Mở/Đóng Lệnh| G[Máy chủ Sàn Giao dịch]
    F -->|Thông tin Giao dịch| H[Quản lý Vị thế - Cắt lỗ/Chốt lời]
    H --> G
    
    I[Động cơ Backtest Vector hóa] -->|Dữ liệu Lịch sử| D
    I -->|Nhật ký Giao dịch| J[Bảng điều khiển PyQt6 Chuyên nghiệp]
````

1.  **Lớp Dữ liệu (`/lay_du_lieu`):** Đóng vai trò là hệ thống ETL (Extract-Transform-Load), chịu trách nhiệm kết nối trực tiếp với API các sàn giao dịch để kéo dữ liệu nến (OHLCV) và thông tin tài khoản. Lớp này thực hiện gộp nến (Resampling) đa khung thời gian, xử lý các lỗ hổng dữ liệu (Fill NA), định dạng lại chuỗi thời gian (Time-series) và chuẩn bị dữ liệu đầu vào sạch cho các bộ lọc phía sau.

2.  **Lớp Chiến lược (`/chien_luoc`):** Bộ não logic chứa các công thức toán học và hệ thống chỉ báo kỹ thuật (TA indicators) như EMA, RSI, Bollinger Bands để xác định cấu trúc giá. Lớp này kết hợp các mô hình chiến lược vĩ mô, chỉ số tham lam và sợ hãi (Fear & Greed Index) cùng phân tích tâm lý thị trường để đưa ra quyết định giao dịch chính xác thay vì chỉ dựa vào công thức kỹ thuật thuần túy.

3.  **Lớp Trí tuệ Nhân tạo (`/ml` - AI/ML Core Engine):** Đóng vai trò là trung tâm tri giác của hệ thống, được thiết kế theo cấu trúc mở (Extensible Framework) để làm nền tảng sẵn sàng cấy ghép đa dạng các mô hình Machine Learning trong tương lai (như mô hình dự báo giá, phát hiện dòng tiền Whale, hay NLP phân tích tin tức).
    Trọng tâm hiện tại là mô hình Deep Learning sử dụng kiến trúc mạng Neural đa tầng (**TradingMLP**) kết hợp các khối **ResBlock** tiên tiến nhằm phân tích độ nhiễu và phân loại thị trường vào các trạng thái (Noise, Trend, Breakout...). Điểm sáng giá nhất của lớp này là cơ chế **tự tiến hóa (Self-learning)**: hệ thống liên tục ôn tập và tái huấn luyện (Fine-tuning) trọng số dựa trên kinh nghiệm từ nhật ký thực chiến `trading_memory.csv`, giúp AI tự động thích nghi khi cấu trúc thị trường thay đổi.
    *(Các công cụ xử lý dữ liệu như lọc nhiễu, cân bằng nhãn chỉ đóng vai trò là các tiện ích phụ trợ ẩn bên dưới để cung cấp dữ liệu sạch cho Core AI).*

4.  **Lớp Thực thi (`/thuc_thi_lenh`):** Công cụ thực thi lệnh (Execution Engine) đảm bảo an toàn cho tài sản thông qua việc quản lý bảo mật API Keys, xử lý Nonce và tuân thủ giới hạn tần suất gọi lệnh (Rate-limits) của sàn. Lớp này chịu trách nhiệm tính toán Position Sizing, quản lý rủi ro danh mục và thực hiện các lệnh đóng/mở vị thế một cách tối ưu.

5.  **Lớp Giám sát & Giao diện Trực quan (`/hien_thi` - Telemetry & Command Center):** Đóng vai trò là "Trung tâm chỉ huy" của toàn bộ hệ sinh thái, biến hàng triệu điểm dữ liệu khô khan và luồng log phức tạp thành các báo cáo trực quan theo thời gian thực (Real-time). Lớp này không chỉ đơn thuần để "nhìn ngắm" biểu đồ, mà là một hệ thống phân tích hiệu suất (Performance Analytics) chuyên sâu phục vụ cho việc ra quyết định của Kiến trúc sư.

      * **CLI Dashboard (Real-time Telemetry):** Cung cấp bảng điều khiển siêu tốc ngay trên Terminal thông qua thư viện `Rich`. Điểm nhấn cốt lõi là màn hình giám sát **Live Feed** – nơi trực quan hóa cuộc "đối đầu" giữa **Dự đoán của AI** (Neural Network) và **Nhận định của Chuyên gia** (Technical Teacher). Hệ thống hiển thị rõ ràng độ tin cậy (Confidence Score), tỷ lệ Win/Loss và trạng thái thị trường theo từng nhịp đập (Tick-by-tick) mà không gây ngốn tài nguyên máy tính.
      * **Phân tích Đồ họa Chuyên sâu (Visual Analytics):** Tích hợp các giao diện đồ họa bậc cao (PyQt6 / Streamlit) để mổ xẻ kết quả sau những đợt Vectorized Backtest cường độ cao và backtest bar-to-bar đơn thuần. Thuật toán sẽ trực quan hóa đường cong vốn (Equity Curve), biểu đồ sụt giảm tài sản (Underwater/Drawdown Chart), phân bố lợi nhuận và thống kê chi tiết lịch sử lệnh (Trade breakdown).
      * **Kiểm soát Đa môi trường (Multi-environment Monitoring):** Cung cấp góc nhìn toàn cảnh về "sức khỏe danh mục" (Portfolio Health) một cách minh bạch và liên tục xuyên suốt 3 môi trường vận hành: Kiểm thử quá khứ (Backtest), Giao dịch giả lập (Paper Trading / Demo) và Thực chiến trên sàn (Live Trading).

-----

<a name="5"></a>

## 5\. LOGIC CHIẾN LƯỢC GIAO DỊCH (CORE ENGINE & VOTING SYSTEM)

**KAIROS QUANT SYSTEM** từ chối việc đi tìm một "chén thánh" (Holy Grail) trong giao dịch hay phụ thuộc vào bất kỳ một chỉ báo đơn lẻ nào. Điểm tạo nên sự khác biệt của hệ thống là **Cơ chế Bỏ phiếu Chiến lược Tổ hợp (Ensemble Strategy Voting System)**.

Hệ thống được thiết kế theo kiến trúc mở (Plug-and-Play), cho phép đánh giá thị trường qua nhiều góc nhìn độc lập và có thể dễ dàng mở rộng thêm các module mới trong tương lai:

**Các Module Đánh Giá Cốt Lõi (Có thể mở rộng thêm):**

1.  **Trend Following (Thuận xu hướng):** Đo lường sức mạnh xu hướng vĩ mô (H1, H4) thông qua Cấu trúc giá (Market Structure), giao cắt EMA và định hướng của mây Ichimoku.
2.  **Volatility & Breakout (Biến động & Phá vỡ):** Phân tích sự co thắt của dải Bollinger (Squeeze) kết hợp với hồ sơ khối lượng (Volume Profile / Volume Spike) để săn tìm các nhịp bùng nổ thanh khoản.
3.  **Mean Reversion (Đảo chiều trung bình):** Sử dụng VWAP và các chỉ báo Động lượng (RSI, Stochastic) kết hợp với tín hiệu Phân kỳ (Divergence) để bắt các điểm cạn kiệt lực mua/bán (Exhaustion points).
4.  **Multi-Timeframe Alignment (Đồng pha đa khung):** Đóng vai trò màng lọc nhiễu. Tín hiệu ở khung vi mô (M1, M5) chỉ được cấp phép hoạt động nếu đồng thuận với sóng chủ ở khung vĩ mô (H1, H4).
5.  **AI/ML Confidence (Xác suất Học máy):** Trọng tài thứ 5 đến từ mô hình Deep Learning (TradingMLP), trả về tỷ lệ phần trăm tự tự tin (Confidence Score) dựa trên việc đối chiếu hoàn cảnh hiện tại với dữ liệu lịch sử trong `trading_memory.csv`.
6.  **Macro & Sentiment (Vĩ mô & Tâm lý - *Mở rộng*):** Tích hợp điểm số từ dữ liệu On-chain, Orderbook Imbalance (Mất cân bằng sổ lệnh) và chỉ số Tham lam/Sợ hãi (Fear & Greed Index).

**Quy trình chấm điểm và Trọng số động (Dynamic Scoring Engine):**
Mỗi module chiến lược độc lập sẽ trả về một điểm tín hiệu `Score` dao động từ `-100` (Bán cực mạnh) đến `+100` (Mua cực mạnh).

Hệ thống không cộng dồn một cách máy móc, mà sử dụng công thức **Trọng số động (Dynamic Weighting)**:

> `Total Score = (W1*Trend) + (W2*Breakout) + (W3*Reversion) + (W4*MultiTF) + (W5*AI) + ... + (Wn*New_Module)`

  * **Sự thích nghi của Trọng số (W):** Các biến `W` không cố định. Chúng được AI tự động điều chỉnh dựa trên *Trạng thái thị trường*. Ví dụ: Nếu AI nhận diện thị trường đang ở pha "Đi ngang" (Ranging), trọng số của `W3` (Mean Reversion) sẽ được khuếch đại, trong khi `W1` (Trend) bị hạ thấp để tránh tín hiệu nhiễu (Fakeout).
  * **Quyết định Thực thi (Execution Logic):** \* Nếu `Total Score` vượt qua `Ngưỡng xác nhận (Threshold)`, hệ thống mới tiến hành mở lệnh Long hoặc Short.
      * **Dynamic Sizing:** `Total Score` càng lớn (thể hiện sự đồng thuận tuyệt đối của tất cả các góc nhìn), khối lượng vốn bơm vào lệnh (Position Size) sẽ càng được tăng cường một cách linh hoạt để tối đa hóa lợi nhuận.

-----

<a name="6"></a>

## 6\. HỆ THỐNG TRÍ TUỆ NHÂN TẠO & MACHINE LEARNING (AI/ML)

Để phá vỡ giới hạn của các chiến lược tĩnh, KAIROS tích hợp một Module ML độc lập (`/ml/trang_thai_thi_truong_ml`). Không chỉ dừng lại ở một bộ lọc đơn giản, đây là một **Kiến trúc Trí tuệ nhân tạo mở rộng (Extensible AI Framework)**, đóng vai trò như một màng lọc rủi ro tối thượng và có thể cấy ghép thêm vô số mô hình dự báo trong tương lai:

  * **Động cơ Phân loại Trạng thái Đa chiều (Multi-dimensional Market State Classification):** Thay vì chỉ chia thị trường thành 2 thái cực (Trending/Ranging), KAIROS sử dụng mạng Deep Learning đa tầng (**TradingMLP** với **ResBlock** trên nền tảng `PyTorch`) để phân rã cấu trúc thị trường thành 6 trạng thái vi mô: *Noise (Nhiễu), Trend following, Mean reversion, Squeeze (Tích lũy nén), Breakout, và Scalping*.
    *(Kiến trúc dạng Plug-and-play cho phép dễ dàng cắm thêm các mô hình như Random Forest, SVM hay LSTM để tăng độ tin cậy).*

  * **Hệ thống Điều hướng Chiến lược Động (Dynamic Strategy Routing):**
    AI đóng vai trò là "Người điều phối giao thông". Khi mô hình dự báo thị trường đang rơi vào pha "Noise" (Nhiễu loạn hỗn mang) hoặc "Squeeze" (Tích lũy), hệ thống sẽ tự động vô hiệu hóa (kill-switch) các module Trend Following và Breakout để triệt tiêu hoàn toàn rủi ro tín hiệu giả (False Breakout). Đồng thời, nó đánh thức và cấp vốn cho chiến lược Mean Reversion hoặc Scalping để khai thác các biên độ dao động hẹp.

  * **Cơ chế Thầy - Trò & Tự tiến hóa (Trading Teacher & Self-Evolution Loop):**
    Hệ thống không bao giờ dậm chân tại chỗ. KAIROS vận hành một vòng lặp phản hồi (Feedback Loop) liên tục:

      * Thuật toán giám sát mọi lệnh thắng/thua (PnL) và đối chiếu với nhãn dữ liệu từ "Hệ thống chuyên gia" (Trading Teacher).
      * Từ những sai lầm (Losses) trong quá khứ, AI tự động "ôn bài" (thông qua hàm `tu_dong_hoc_tu_log`) để tinh chỉnh lại trọng số mạng Neural (Weights Fine-tuning) lưu trong `trading_memory.csv`.

  * **Sẵn sàng Mở rộng (Future-Proof Extensibility):**
    Lớp ML hiện tại chỉ là nền móng. Cấu trúc tách biệt này cho phép KAIROS dễ dàng mở rộng thêm các Module AI khác trong tương lai mà không làm vỡ logic cốt lõi, chẳng hạn như:

      * **NLP Sentiment Analysis:** Xử lý ngôn ngữ tự nhiên để đọc tin tức từ X (Twitter) hoặc báo cáo kinh tế vĩ mô.
      * **On-chain Clustering:** Nhóm các cụm hành vi ví cá mập (Whale wallets).
      * **Orderbook Computer Vision:** Dùng AI thị giác máy tính để phân tích bản đồ nhiệt (Heatmap) của sổ lệnh.

-----

<a name="7"></a>

## 7\. HỆ THỐNG BACKTEST & TRỰC QUAN HÓA (PYQT6 DASHBOARD)

KAIROS sở hữu một phần mềm Desktop chuyên dụng được xây dựng bằng **PyQt6**, biến dữ liệu khô khan thành các Insight có giá trị.

  * **Interactive UI (Giao diện tương tác):** Thiết kế dạng Dockable Widgets (kéo thả linh hoạt các cửa sổ) giúp người dùng tùy biến không gian làm việc.
  * **Siêu tốc độ với Polars:** Lọc hàng triệu dòng kết quả giao dịch (theo Ngày, Giờ, Coin, Long/Short) chỉ trong tích tắc.
  * **Daily PnL & Intraday Equity Curve:** Biểu đồ hiển thị lợi nhuận từng ngày. Click vào một ngày cụ thể để phân tích chi tiết từng lệnh được đánh trong ngày hôm đó.
  * **Heatmap & Time Distribution:** Biểu đồ nhiệt phân tích hành vi giá. Trả lời câu hỏi: *"Hệ thống kiếm được nhiều tiền nhất vào thứ mấy trong tuần? Khung giờ nào có tỷ lệ Win cao nhất?"*
  * **Trade Scatter Plot:** Biểu đồ phân tán (Scatter) đo lường mối tương quan giữa Thời gian giữ lệnh (Hold Duration) và Lợi nhuận (PnL). Giúp phát hiện lỗi "gồng lỗ quá lâu" hoặc "chốt lời quá sớm".
    
<img width="1920" height="1080" alt="Ảnh chụp màn hình (520)" src="https://github.com/user-attachments/assets/e01c8ea9-eb98-4673-b681-41fdb774d801" />

-----

<a name="8"></a>

## 8\. QUẢN TRỊ RỦI RO & QUẢN LÝ VỐN (RISK MANAGEMENT)

Được thiết kế với tư duy của dân Tài chính định lượng, rủi ro là yếu tố được đặt lên hàng đầu:

  * **Bảo vệ tài khoản (Account Drawdown Limit):** Nếu hệ thống thua lỗ liên tục chạm ngưỡng Max Drawdown (VD: âm 15% tổng tài khoản), bot sẽ tự động ngắt kết nối (Kill-switch) để bảo toàn vốn.
  * **Stoploss động theo Volatility (ATR-based SL):** Stoploss không đặt cố định theo % tĩnh, mà co giãn theo biến động thị trường (Average True Range). Thị trường giật mạnh, SL nới rộng; thị trường êm, SL thắt chặt.
  * **Trailing Stop & Break-even:** Tự động dời Stoploss về điểm hòa vốn (Entry) khi giá đã chạy được một mức lợi nhuận nhất định. Tự động cuốn chiếu lợi nhuận (Trailing) để ăn trọn con sóng.

-----

<a name="9"></a>

## 9\. CẤU TRÚC THƯ MỤC (DIRECTORY TREE)

Cấu trúc được quy hoạch chặt chẽ, dễ dàng bảo trì và mở rộng:

```text
KAIROS_QUANT_SYSTEM_v2.0/
├── main.py                     # Entry point: Menu điều hướng chính của toàn hệ thống
├── REALME.MD                   # Tổng quan hệ thống và hướng dẫn vận hành
├── requirements.txt            # Danh sách thư viện phụ thuộc (PyTorch, Polars, CCXT, Rich...)
│
├── config/                     # QUẢN LÝ CẤU HÌNH
│   ├── cau_hinh_giao_ao.json   # Setup thông số cho môi trường Backtest/Demo
│   ├── cau_hinh_giao_dich.yaml # Setup vốn, đòn bẩy, cặp coin, quản trị rủi ro
│   ├── tai_khoan_api.json      # Nơi lưu trữ API Key, Secret Key (đã mã hóa)
│   └── thong_tin_san.yaml      # Thông số kỹ thuật sàn (Min lot, Tick size, Leverage)
│
├── ml/                             # KHỐI MACHINE LEARNING (AI Core)
│   ├── main.py                     # Luồng điều phối ML: Huấn luyện, chạy Dashboard, Auto-Learning
│   ├── tool/                       # Module công cụ hổ trợ
│   │   ├── data_filter.py          # Xử lý nhiễu và cân bằng dữ liệu log (trading_memory.csv)
│   │   └── trading_teacher.py      # Hệ thống chuyên gia: Tính toán kỹ thuật (RSI, VWAP, EMA) gán nhãn
│   └── trang_thai_thi_truong_ml/   # Module phân loại trạng thái thị trường chuyên sâu
│       ├── ml_model.py             # Kiến trúc mạng Neural (TradingMLP, ResBlock, BatchNorm)
│       ├── ml_predict.py           # Logic dự đoán Realtime & Đánh giá hiệu quả (PnL/Reward)
│       ├── tao_feature.py          # Trích xuất đặc trưng (Features) đa khung bằng Polars
│       ├── ml_compare.py           # So sánh hiệu suất giữa các phiên bản Model AI
│       ├── ml_deploy.py            # Triển khai và đóng gói mô hình sẵn sàng thực chiến
│       └── du_lieu_ml/             # Kho lưu trữ dữ liệu và trọng số vật lý
│           ├── model_pytorch.pth   # File trọng số mạng Neural đã huấn luyện thành công
│           ├── model_info.json     # Cấu hình kiến trúc Input/Output của mô hình
│           ├── scaler_params.json  # Tham số chuẩn hóa dữ liệu đầu vào (Mean/Std)
│           └── trading_memory.csv  # Nhật ký kinh nghiệm dùng làm tập dữ liệu học máy
│
├── lay_du_lieu/                    # KHỐI ETL & API (Data Acquisition)
│   ├── lay_ohlcv.py                # Kéo nến lịch sử đa khung thời gian
│   ├── lay_marketsnapshot.py       # Lấy dữ liệu Realtime (Orderbook, Ticker, Liquidation)
│   └── lay_thong_tin_tai_khoan.py  # Lấy thông tin tài khoản
│
├── chien_luoc/                 # KHỐI CORE LOGIC (Strategy)
│   ├── logic_vectorized/       # Thuật toán ma trận dùng cho Backtest quy mô lớn
│   └── logic_bar_to_bar/       # Thuật toán chạy Live (xử lý dữ liệu từng Tick/Nến)
│
├── thuc_thi_lenh/              # KHỐI EXECUTION ENGINE
│   ├── bo_may_thuc_thi.py      # Xử lý vòng đời lệnh (Khởi tạo -> Quản lý -> Kết thúc)
│   ├── quan_ly_danh_muc.py     # Tính toán Position Sizing, Margin & Drawdown
│   ├── ket_noi_san/            # Wrapper đa sàn (Binance, Bybit, OKX) qua CCXT
│   └── [mo_lenh.py, dong_lenh.py, theo_doi_lenh.py...] # Các logic xử lý lệnh chi tiết
│
├── chuc_nang/                  # CÁC CHẾ ĐỘ VẬN HÀNH (Operation Modes)
│   ├── backtest_donluong.py    # Engine chạy Backtest kiểm thử chiến thuật
│   ├── backtest_daluong.py     # Engine chạy Backtest kiểm thử chiến thuật song song nhiều luồng
│   ├── vectorized_backtest.py  # Backtest siêu tốc bằng phương pháp Vector hóa
│   ├── chay_demo.py            # Kích hoạt Paper Trading (Giao dịch ảo Realtime)
│   └── chay_realtime.py        # Kích hoạt Live Trading (Giao dịch thật trên sàn)
│
├── hien_thi/                   # KHỐI GIAO DIỆN & MONITORING
│   ├── dashboard_realtime.py   # Bảng điều khiển giám sát lệnh và thị trường Live
│   ├── dashboard_backtest.py   # Trực quan hóa kết quả phân tích lịch sử
│   ├── dashboard_vectorized.py # Trực quan hóa điểm vào lệnh và thoát lệnh của chiến lược trên biểu đồ nến    
│   └── dashboard_demo.py       # Giám sát hiệu quả giao dịch thử nghiệm
│
├── du_lieu/                    # KHO LƯU TRỮ DỮ LIỆU HỆ THỐNG
│   ├── lich_su_gia/            # CSV/Parquet chứa nến lịch sử kết quả backtest
│   ├── du_lieu_vectorized/     # CSV/Parquet chứa nến lịch sử đã làm sạch
│   ├── thong_tin_lenh/         # Trạng thái JSON các lệnh đang mở/lịch sử lệnh
│   └── nhat_ky_hoat_dong.log   # Logs chi tiết lỗi và hoạt động hệ thống
│
├── thong_bao/                  # HỆ THỐNG ALERTS
│   ├── gui_telegram.py         # Gửi tín hiệu, báo cáo PnL và cảnh báo qua Telegram
│   └── gui_email.py            # Báo cáo tổng kết định kỳ qua Email
│
└── utils/                      # TIỆN ÍCH HỖ TRỢ (Helpers)
    ├── thoi_gian.py            # Xử lý Timestamp, Timezone, đồng bộ giờ sàn
    ├── doc_cau_hinh.py         # Parser chuyên dụng cho YAML/JSON
    ├── ham_tien_ich.py         # Các hàm toán học, định dạng dữ liệu bổ trợ
    ├── save_datafile.py        # Logic lưu trữ và quản lý format file console/log
    └── chuyen_doi_don_vi.py    # Chuyển đổi khối lượng, đòn bẩy và đơn vị tiền tệ
```

-----

<a name="10"></a>

## 10\. YÊU CẦU & HƯỚNG DẪN CÀI ĐẶT (SETUP INSTRUCTIONS)

*(Phần này dành cho các thông tin cập nhật về môi trường hệ thống và thư viện cài đặt)*

<a name="11"></a>

## 11\. HƯỚNG DẪN SỬ DỤNG & CẤU HÌNH (CONFIGURATION & USAGE)

### 11.1 Cấu hình hệ thống (YAML & JSON)

Bạn cần thiết lập file `config/cau_hinh_giao_dich.yaml` trước khi chạy:

```yaml
san_giao_dich_chinh: "okx" # Hỗ trợ: binance, bybit, okx
cap_giao_dich:
  - "BTC/USDT"
  - "ETH/USDT"
  - "SOL/USDT"

von_moi_lenh_usdt: 100
don_bay: 7 # là số trung vị của khoảng đòn bẩy từ 5 đến 9
max_lenh_cho_phep: 20
cat_lo_percent: 0.1   # Cắt lỗ 10%
chot_loi_percent: 0.15  # Chốt lời 15%    # Bật Stoploss động theo ATR
```

Tiếp theo, điền API Key vào `config/tai_khoan_api.json`. **Lưu ý: Chỉ cấp quyền Đọc (Read) và Giao dịch (Trade/Futures). Tuyệt đối KHÔNG cấp quyền Rút tiền (Withdraw).**

### 11.2 Khởi chạy KAIROS

*(Tiến hành gọi lệnh khởi chạy từ file `main.py` ở thư mục gốc để vào màn hình điều hướng của hệ thống).*

-----

<a name="12"></a>

## 12\. LỘ TRÌNH PHÁT TRIỂN TƯƠNG LAI (ROADMAP)

### Lộ trình nâng cấp Hệ thống (Roadmap v2.0 & v3.0)

Với vai trò là người thiết kế hệ thống (Kiến trúc sư), định hướng phát triển KAIROS trong tương lai không chỉ dừng lại ở việc phân tích giá, mà sẽ vươn lên thành một cỗ máy tự tư duy toàn diện. Lộ trình nâng cấp bao gồm:

  * **Tích hợp Nguồn dữ liệu Ngoại vi (Alternative Data):** Thay vì chỉ nhìn vào biểu đồ nến, KAIROS sẽ biết "lắng nghe" thị trường. Hệ thống sẽ quét mạng xã hội để đo lường tâm lý đám đông, phân tích Chỉ số Tham lam & Sợ hãi, và theo dõi dòng tiền thật của "cá mập" trên chuỗi khối (On-chain data). Những thông tin này sẽ được dùng làm điểm cộng/trừ trong cơ chế Bỏ phiếu chiến lược để chốt lệnh chính xác hơn.
  * **Học tăng cường - Cho AI tự thực chiến (Reinforcement Learning):** Nâng cấp module "Thầy giáo" hiện tại thành một cỗ máy AI có khả năng tự động "cày" hàng triệu kịch bản thị trường (giống như cách AI học chơi cờ). Nó sẽ tự chơi, tự thua và tự rút kinh nghiệm để mò ra những **bộ thông số cài đặt hoàn hảo nhất** (Hyperparameters) – những con số tối ưu đến mức bộ não con người không thể tự nghĩ ra được.
  * **Tự động Phân bổ và Bảo vệ Vốn (Portfolio Optimization):** Thay vì chia tiền bằng tay hay dồn hết vào một giỏ, thuật toán sẽ tự động phân bổ vốn thông minh. Nó sẽ chọn ra các đồng coin có hướng đi "trái ngược nhau" (độ tương quan thấp). Nhờ vậy, nếu một đồng coin bị sập, lợi nhuận từ đồng coin khác sẽ gánh lại. Điều này tạo ra một lá chắn an toàn (Hedging) tuyệt đối cho tổng tài khoản của bạn.
  * **Mở rộng sang thị trường Phái sinh Quyền chọn (Options):** Không chỉ đánh Lên/Xuống (Long/Short) thông thường, hệ thống sẽ tiến hóa để kiếm tiền từ mọi ngóc ngách của thị trường. Bot sẽ ăn lợi nhuận từ **chênh lệch biên độ giật của giá** và thu tiền từ việc **thời gian của hợp đồng bị hao mòn từng ngày**. (Ngay cả khi giá đi ngang, tài khoản vẫn tự động sinh lời).
  * **Tối ưu hóa Tốc độ "Thần tốc" (Hybrid Low-level Programming):** Để tăng tính cạnh tranh, KAIROS sẽ không chỉ dùng Python. Hệ thống sẽ kết hợp thêm các ngôn ngữ bậc thấp có tốc độ xử lý nhanh như **C++** hoặc **Rust**. Python sẽ đóng vai trò là "người chỉ huy" thông minh, trong khi C++/Rust là các "vận động viên" thực hiện những việc tính toán nặng nhọc nhất. Điều này giúp giảm độ trễ (Latency) khi đặt lệnh xuống mức tối thiểu và giúp việc chạy giả lập (Backtest) hàng triệu nến dữ liệu diễn ra nhanh hơn.

-----

<a name="13"></a>

## 13\. CẢNH BÁO RỦI RO (DISCLAIMER)

⚠️ **QUAN TRỌNG:**

1.  Thị trường Cryptocurrency rủi ro cực kỳ cao. Bot KAIROS phân tích dựa trên Xác suất thống kê (Statistical Probability) dựa trên dữ liệu quá khứ, **KHÔNG có khả năng dự đoán tương lai chính xác 100%**. Lợi nhuận trong quá khứ không đảm bảo cho tương lai.
2.  **System Bug:** Mặc dù đã được kiểm thử (Unit test/Integration test), phần mềm vẫn có thể tồn tại lỗi không lường trước (Bug), hoặc rủi ro về độ trễ mạng lưới, lỗi từ API của Sàn giao dịch.
3.  Người dùng hoàn toàn chịu trách nhiệm cho các quyết định cấu hình vốn, đòn bẩy và API Keys của mình. Tác giả không chịu trách nhiệm cho bất kỳ tổn thất tài chính nào phát sinh trong quá trình sử dụng hệ thống.

-----

📌 **LƯU Ý QUAN TRỌNG VỀ MÃ NGUỒN (SOURCE CODE NOTICE):**
Mã nguồn được chia sẻ tại kho lưu trữ này chỉ là phiên bản nền tảng sơ khai nhất (v1.0). Nhằm bảo vệ quyền sở hữu trí tuệ và lợi thế giao dịch (Alpha), rất nhiều công năng lõi, thuật toán nâng cao và cơ chế thực chiến đã được cắt giảm. Các phiên bản nâng cấp mới nhất và hoàn thiện nhất của hệ thống KAIROS sẽ **không được công khai (Closed-source)**. Phiên bản mã nguồn mở này chủ yếu đóng vai trò là một Proof-of-Concept (Bản minh họa) về kiến trúc và tư duy xây dựng hệ thống Quant Trading.

-----

### 👨‍💻 THÔNG TIN TÁC GIẢ (AUTHOR & ARCHITECT)

  * **System Architect & Logic Designer:** P Vinh (Quant Developer) AI-assisted development workflow
  * **Role:** Quant Developer / Quant Researcher
  * **Contact:** ppvinh1513@gmail.com
  * **Development Methodology:** Human Logic + AI Assisted Coding (Prompt Engineering).

*“Romain Rolland: "There is only one heroism in the world: to see the world as it is, and to love it."”*

```
```
