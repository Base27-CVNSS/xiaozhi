# Hướng dẫn đóng góp

Cảm ơn bạn muốn phát triển XiaoZhi ESP32 bản tiếng Việt.

## Trước khi bắt đầu

1. Tìm issue hoặc pull request tương tự.
2. Xác định thay đổi thuộc lõi, bo mạch, audio, protocol, UI, tài liệu hay bản dịch.
3. Đọc cách triển khai gần nhất trong cùng thư mục.
4. Với bo mạch mới, đọc `docs/custom-board.md`.

## Quy tắc mã nguồn

- Tuân thủ Google C++ Style và `.clang-format`.
- Chỉ format file C/C++ đã sửa.
- Không đưa hành vi riêng bo mạch vào lõi.
- Không thay pin của bo mạch cũ để hỗ trợ phần cứng khác.
- Mỗi build chỉ có một `DECLARE_BOARD(...)`.
- Dùng `Application::SetDeviceState()` để đổi trạng thái.
- Callback ngoài main task dùng `Application::Schedule()` hoặc event bit.
- Không chặn main/audio task và không tạo hàng đợi không giới hạn.
- Khi đổi hợp đồng `Protocol`, kiểm tra WebSocket lẫn MQTT + UDP.
- Không commit token, khóa API, Wi-Fi, chứng chỉ riêng, file build hoặc mã dịch ngược.

## Bản dịch tiếng Việt

- Ưu tiên câu ngắn, tự nhiên và đọc tốt trên màn hình nhỏ.
- Giữ nguyên placeholder `%s`, `%d` và thứ tự tham số.
- Dùng thuật ngữ nhất quán: “bo mạch”, “mô-đun”, “kết nối”, “cập nhật”, “đánh thức”, “khử vọng”.
- Nếu sửa câu thoại, kiểm tra cả văn bản hiển thị và file âm thanh tương ứng.

## Kiểm thử

```bash
python3 -m unittest discover -s scripts/tests -v
python scripts/build.py --list-boards
python scripts/build.py --list-languages
```

Nếu có ESP-IDF:

```bash
python scripts/build.py <bo-mach> --name <bien-the> --language vi-VN
```

Trong pull request, nêu rõ phần đã kiểm thử trên thiết bị thật và phần chỉ kiểm tra tĩnh/biên dịch.

## Nội dung pull request

- Vấn đề cần giải quyết.
- Kiến trúc hoặc lớp sở hữu thay đổi.
- Tệp đã sửa.
- Ảnh/video/log nếu thay đổi UI hoặc phần cứng.
- Kết quả kiểm thử.
- Ảnh hưởng tương thích OTA/NVS/protocol.
- Nguồn và giấy phép của mọi tài nguyên mới.

Thay đổi lớn nên được chia thành các commit độc lập: lõi, tài nguyên tiếng Việt và tài liệu.
