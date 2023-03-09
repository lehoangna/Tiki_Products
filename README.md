[Python + MongoDB] Crawl products in Tiki
Introduction
Bài toán: Lấy toàn bộ sản phẩm trên các danh mục của trang tiki.vn để sử dụng cho nhiều mục đích.

Yêu cầu :

Dữ liệu được crawl về sẽ lưu trong MongoDB
Đánh index để hỗ trợ tìm kiếm thông tin trên trường “short_description” được nhanh chóng. Ví dụ: Query từ “hộp sữa” MongoDB sẽ trả về nhanh các document có từ hộp sữa
Tải toàn bộ ảnh ở “base_url” của mỗi sản phẩm về lưu trong ổ cứng (mỗi sản phẩm có từ 3-5 ảnh)
Tạo các biểu đồ cho mỗi danh mục sản phẩm, biểu đồ dạng line, thể hiện độ tương quan giữa giá, rating và số lượng
Liệt kê toàn bộ các categories của sản phẩm (từ category cha đến category con), và thống kê mỗi category có bao nhiêu sản phầm
