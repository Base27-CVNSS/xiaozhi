# Quy trình đồng bộ với upstream

Kho tiếng Việt phải nhận được bản sửa lỗi, phần cứng mới và cập nhật bảo mật từ [`78/xiaozhi-esp32`](https://github.com/78/xiaozhi-esp32) mà không làm mất tùy chỉnh địa phương.

## 1. Nguyên tắc

- Giữ remote `origin` cho `Base27-CVNSS/xiaozhi`.
- Giữ remote `upstream` cho `78/xiaozhi-esp32`.
- Tùy chỉnh tiếng Việt nằm trong các commit nhỏ, dễ đọc.
- Không dịch hàng loạt định danh, tên lớp hoặc comment lõi.
- Không sửa file sinh tự động, thư mục build hoặc dependency được quản lý.
- Mỗi lần đồng bộ phải chạy kiểm thử host và ít nhất một build đại diện nếu có ESP-IDF.

## 2. Thiết lập remote

```bash
git remote -v
git remote add upstream https://github.com/78/xiaozhi-esp32.git
git fetch --prune upstream
```

Nếu `upstream` đã tồn tại:

```bash
git remote set-url upstream https://github.com/78/xiaozhi-esp32.git
```

## 3. Đồng bộ định kỳ

Tạo nhánh riêng:

```bash
git fetch --prune upstream
git switch main
git pull --ff-only origin main
git switch -c maintenance/sync-upstream-YYYY-MM-DD
git merge --no-ff upstream/main
```

Giải quyết xung đột theo thứ tự:

1. mã lõi và giao thức ưu tiên hành vi upstream;
2. `README.md` giữ tài liệu tiếng Việt nhưng cập nhật số liệu/tính năng mới;
3. `README_EN.md` ưu tiên bản tiếng Anh upstream;
4. `main/Kconfig.projbuild` giữ `LANGUAGE_VI_VN` làm mặc định;
5. `main/assets/locales/vi-VN/language.json` giữ thuật ngữ Việt Nam, đồng thời bổ sung đủ khóa mới.

## 4. Kiểm tra ngôn ngữ

```bash
python scripts/build.py --list-languages
```

So sánh khóa `vi-VN` với `en-US`. Không được:

- xóa placeholder `%s`, `%d`;
- đổi số lượng hoặc kiểu placeholder;
- chèn newline không cần thiết vào màn hình nhỏ;
- dùng chuỗi quá dài mà không kiểm tra OLED/LCD.

## 5. Kiểm thử

```bash
python3 -m unittest discover -s scripts/tests -v
python scripts/build.py --list-boards
```

Nếu môi trường ESP-IDF 6.0.2 sẵn sàng, build biến thể đại diện:

```bash
python scripts/build.py bread-compact-wifi \
  --name bread-compact-wifi \
  --language vi-VN
```

Thay đổi protocol phải kiểm tra cả WebSocket và MQTT + UDP. Thay đổi audio phải kiểm tra thu, phát, wake/VAD, AEC, ngắt lời và kết nối lại.

## 6. Ghi nhận snapshot

Trong nội dung pull request, ghi:

- SHA upstream trước và sau;
- danh sách xung đột;
- thay đổi riêng của nhánh Việt Nam được giữ;
- kiểm thử đã chạy;
- phần chưa thể kiểm thử trên phần cứng.

Không gắn thẻ phát hành nếu chưa xác định được bo mạch, target chip, partition và nguồn OTA của artifact.
