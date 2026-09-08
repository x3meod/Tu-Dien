# Ứng dụng Từ Điển Anh - Việt / Việt - Anh

## 1. Giới thiệu

Đây là ứng dụng từ điển desktop được viết bằng **Python**, sử dụng **Tkinter** để xây dựng giao diện và **SQLite3** để lưu trữ dữ liệu.

Ứng dụng hiện tập trung vào các chức năng cốt lõi:

- Tra từ Anh → Việt và Việt → Anh.
- Đổi chiều dịch.
- Lưu và xem lịch sử tra cứu.
- Thêm từ mới vào cơ sở dữ liệu.
- Quản lý và xóa từ vựng.
- Thêm từ vào danh sách **Từ cần học**.
- Kiểm tra trùng trước khi thêm từ cần học.
- Học từ ngẫu nhiên.
- Chế độ học từ: hiện từ trước, có nút **Hiện nghĩa** và **Từ tiếp theo**.
- Import dữ liệu từ file JSONL vào database SQLite.

---

## 2. Công nghệ sử dụng

- **Python 3**
- **Tkinter**: tạo giao diện đồ họa.
- **SQLite3**: lưu dữ liệu cục bộ.
- **JSON**: đọc dữ liệu từ file JSONL.
- **Regular Expression (`re`)**: xử lý phần phiên âm trong dữ liệu Anh - Việt.

---

## 3. Cấu trúc project

```text
tudien/
├── tu_dien.py       # Chương trình chính
├── import_db.py     # Import dữ liệu JSONL vào SQLite
├── tudien.db        # Cơ sở dữ liệu SQLite
└── README.md        # Tài liệu mô tả project
```

---

## 4. Cơ sở dữ liệu

Chương trình sử dụng **một database duy nhất**:

```text
tudien.db
```

Trong code, các bảng chính được định nghĩa gồm:

### `tu_vung`

Lưu dữ liệu từ điển.

| Cột | Ý nghĩa |
|---|---|
| `id` | ID tự tăng |
| `tu_goc` | Từ gốc |
| `nghia` | Nghĩa của từ |
| `ngon_ngu_nguon` | Ngôn ngữ nguồn (`en` hoặc `vi`) |
| `ngon_ngu_dich` | Ngôn ngữ đích (`vi` hoặc `en`) |

### `lich_su`

Lưu lịch sử tra cứu.

| Cột | Ý nghĩa |
|---|---|
| `id` | ID tự tăng |
| `tu_da_tra` | Từ/cụm từ đã tra |
| `ket_qua` | Kết quả tra |
| `thoi_gian` | Thời gian tra cứu |

### `tu_can_hoc`

Lưu những từ người dùng muốn học.

| Cột | Ý nghĩa |
|---|---|
| `id` | ID tự tăng |
| `tu_goc` | Từ cần học |
| `nghia` | Nghĩa |
| `muc_do` | Mức độ ghi nhớ, mặc định là `0` |
| `ngay_them` | Ngày thêm vào danh sách |

> Lưu ý: cột `muc_do` đã được tạo trong database nhưng phiên bản code hiện tại chưa sử dụng nó để chấm điểm hoặc điều chỉnh độ ưu tiên học.

---

## 5. Các chức năng cốt lõi

## 5.1. Tra từ / Dịch

Người dùng nhập từ vào ô văn bản và bấm **Tra từ / Dịch**.

Chương trình tìm dữ liệu trong bảng `tu_vung` bằng:

- So sánh từ không phân biệt chữ hoa/chữ thường.
- Kiểm tra đúng ngôn ngữ nguồn.
- Kiểm tra đúng ngôn ngữ đích.

Ví dụ:

```text
Input:
hello

Output:
xin chào
```

Nếu không tìm thấy từ, chương trình hiển thị thông báo không tìm thấy nghĩa.

Mỗi lần tra, dữ liệu cũng được ghi vào bảng `lich_su`.

---

## 5.2. Đổi chiều dịch

Nút:

```text
🔄 Đổi chiều dịch
```

cho phép chuyển:

```text
Anh → Việt
```

sang:

```text
Việt → Anh
```

và ngược lại.

Ngoài việc đổi ngôn ngữ nguồn/đích, chương trình còn đổi nội dung giữa hai ô nhập và kết quả.

---

## 5.3. Thêm từ mới

Trong menu **Tùy chọn → Thêm từ mới**, người dùng có thể nhập:

- Từ gốc.
- Nghĩa dịch.
- Ngôn ngữ nguồn.
- Ngôn ngữ đích.

Sau khi lưu, dữ liệu được thêm vào bảng:

```text
tu_vung
```

Chương trình có kiểm tra dữ liệu đầu vào để đảm bảo các trường bắt buộc không bị bỏ trống.

---

## 5.4. Quản lý / Xóa từ

Chức năng này hiển thị danh sách từ trong bảng `tu_vung` bằng `Treeview`.

Có hỗ trợ tìm kiếm gần đúng theo phần đầu của từ:

```sql
WHERE tu_goc LIKE ?
```

Người dùng có thể:

- Xem danh sách từ.
- Tìm kiếm từ.
- Chọn một từ.
- Xóa từ đã chọn.

---

## 5.5. Lịch sử tra cứu

Mỗi lần thực hiện tra từ, chương trình lưu:

```text
tu_da_tra
ket_qua
thoi_gian
```

vào bảng:

```text
lich_su
```

Người dùng có thể mở:

```text
File → Xem lịch sử
```

để xem các lần tra gần đây.

---

## 5.6. Thêm vào "Từ cần học"

Sau khi tra một từ, người dùng có thể bấm:

```text
📚 Thêm vào từ cần học
```

Chương trình lấy:

- Nội dung trong ô nhập.
- Nội dung trong ô kết quả.

Sau đó kiểm tra xem từ đó đã tồn tại trong bảng `tu_can_hoc` hay chưa.

Nếu đã tồn tại, chương trình thông báo:

```text
Từ đã có trong danh sách từ cần học.
```

Nếu chưa có, chương trình thêm dữ liệu vào:

```text
tu_can_hoc
```

---

## 5.7. Danh sách "Từ cần học"

Trong:

```text
Tùy chọn → Từ cần học
```

chương trình hiển thị danh sách từ cần học bằng `Treeview`.

Các cột đang hiển thị:

```text
ID | Từ | Nghĩa | Mức độ
```

Danh sách được đọc trực tiếp từ bảng:

```text
tu_can_hoc
```

---

## 5.8. Học từ ngẫu nhiên

Trong cửa sổ **Từ cần học**, có nút:

```text
🎲 Học từ ngẫu nhiên
```

Chương trình sử dụng SQLite:

```sql
SELECT id, tu_goc, nghia
FROM tu_can_hoc
ORDER BY RANDOM()
LIMIT 1
```

để chọn ngẫu nhiên một từ trong danh sách.

Cửa sổ học từ sẽ hiển thị:

```text
🎲 TỪ VỰNG

abandon

???
```

Người dùng có thể:

```text
👀 Hiện nghĩa
```

để xem đáp án hoặc:

```text
🎲 Từ tiếp theo
```

để chuyển sang một từ ngẫu nhiên khác.

Đây là phần biến ứng dụng từ một từ điển đơn thuần thành một công cụ hỗ trợ học từ vựng.

---

# 6. Import dữ liệu từ JSONL

File:

```text
import_db.py
```

được sử dụng để đưa dữ liệu từ các file JSONL vào:

```text
tudien.db
```

Script hiện hỗ trợ:

```text
Anh → Việt
Việt → Anh
```

Các file đầu vào được sử dụng trong script:

```text
anhviet109K.dict.jsonl
vietanh.dict.jsonl
```

Quy trình import:

```text
JSONL
  ↓
Đọc từng dòng
  ↓
Phân tích JSON
  ↓
Lấy từ
  ↓
Lấy các gloss/ nghĩa
  ↓
Làm sạch dữ liệu
  ↓
INSERT vào tu_vung
  ↓
tudien.db
```

Đối với dữ liệu Anh - Việt, script có xử lý phần phiên âm ở cuối từ bằng Regular Expression trước khi lưu.

---

## 7. Luồng hoạt động tổng thể

```text
                    ỨNG DỤNG TỪ ĐIỂN
                           |
            +--------------+--------------+
            |                             |
        Tra từ / Dịch                 Tùy chọn
            |                             |
            |              +--------------+--------------+
            |              |              |              |
            |          Thêm từ mới    Quản lý từ    Từ cần học
            |                                             |
            |                                             |
            +-------> Lưu lịch sử                    Random / Học
                           |
                       lich_su


                  TẤT CẢ LƯU TRONG
                      tudien.db
```

---

## 8. Database một file, nhiều bảng

Thiết kế hiện tại sử dụng một database:

```text
tudien.db
```

và phân chia dữ liệu theo bảng:

```text
tudien.db
├── tu_vung
├── lich_su
└── tu_can_hoc
```

Cách tổ chức này giúp dữ liệu từ điển, lịch sử và danh sách học tập được quản lý trong cùng một file SQLite nhưng vẫn tách biệt theo từng loại dữ liệu.

---

## 9. Điểm nổi bật của project

### Lưu trữ cục bộ

Ứng dụng sử dụng SQLite nên dữ liệu được lưu trực tiếp trên máy trong:

```text
tudien.db
```

Không cần một hệ quản trị cơ sở dữ liệu riêng.

### Giao diện đơn giản

Sử dụng Tkinter nên project có thể chạy trên môi trường Python có Tkinter mà không cần framework GUI lớn.

### Kết hợp từ điển và học từ

Ngoài chức năng tra cứu, project đã có nền tảng cho việc học:

```text
Tra từ
→ Thêm vào từ cần học
→ Random từ
→ Hiện nghĩa
→ Học từ tiếp theo
```

### Có thể mở rộng

Code hiện tại có thể tiếp tục phát triển thêm các chức năng như:

- Từ yêu thích.
- Theo dõi tiến độ học dựa trên `muc_do`.
- Thống kê số từ đã học.
- Hình ảnh cho từ.
- Quiz trắc nghiệm.
- Chế độ online/offline.

Các chức năng trên **chưa phải chức năng hoàn chỉnh trong phiên bản code hiện tại**.

---

## 10. Cách chạy

### Chạy ứng dụng

```bash
python tu_dien.py
```

### Import dữ liệu

Đặt các file JSONL cùng thư mục với `import_db.py`, sau đó chạy:

```bash
python import_db.py
```

Script sẽ ghi dữ liệu vào:

```text
tudien.db
```

---

## 11. Phiên bản hiện tại

Phiên bản hiện tại tập trung vào 3 nhóm chức năng chính:

```text
1. Từ điển
   - Tra từ
   - Đổi chiều dịch
   - Thêm / xóa từ

2. Lịch sử
   - Lưu lịch sử tra
   - Xem lịch sử

3. Học từ
   - Thêm từ cần học
   - Xem danh sách
   - Random từ
   - Hiện nghĩa
   - Từ tiếp theo
```

