# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

|             |                                                                                        |
| ----------- | -------------------------------------------------------------------------------------- |
| Họ và tên   | Nguyễn Đình Phúc                                                                       |
| MSSV        | 2A202602953                                                                            |
| Lớp / Khóa  | A20-k4                                                                                 |
| Repo GitHub | https://github.com/rin1652/K4-L3-DAY21-NguyenDinhPhuc-2A202602953-CI-CD-for-AI-Systems |
| Ngày nộp    | 7/10/2026                                                                              |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
| -------- | ------------ | ------------- | --------- | -------- | -------- |
| 1        | 100          | 0.1           | 3         | 0.7109   | 0.8780   |
| 2        | 50           | 0.05          | 2         | 0.6051   | 0.8460   |
| 3        | 200          | 0.1           | 5         | 0.7149   | 0.8740   |

**Bộ siêu tham số đã chọn:** `n_estimators=200`, `learning_rate=0.1`, `max_depth=5`.
**Lý do:** Cho F1-score cao nhất (0.7149). F1 cân bằng giữa Precision và Recall, phản ánh tốt hơn Accuracy. Tăng `n_estimators` và `max_depth` giúp mô hình học các đặc trưng phức tạp.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Tỷ lệ lớp dương (thu nhập > 50K) chỉ 24,8%. Một mô hình dự đoán toàn 0 sẽ đạt Accuracy 75,2% nhưng vô dụng. F1-score đo lường độ chính xác trên lớp thiểu số, tránh bị nhiễu bởi sự mất cân bằng dữ liệu.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Giải quyết |
| -------- | ---------- |
| Lỗi 403 Forbidden S3 | Cập nhật file `income-api.service` và truyền biến `AWS_ACCESS_KEY` vào môi trường. |
| Crash do khác bản sklearn | Chạy `pip3 install scikit-learn==1.4.2` trên EC2 để đồng bộ. |
| GitHub Actions mất credentials | Xóa secret cũ, điền lại đúng 2 biến môi trường lấy từ `~/.aws/credentials`. |

---

## 4. So Sánh Bước 2 và Bước 3

| Bước | f1_score | accuracy |
| --- | -------- | -------- |
| 2   | 0.7149   | 0.8740   |
| 3   | 0.7354   | 0.8820   |

**Nhận xét:** F1-score tăng khi thêm dữ liệu mới. Điều này chứng minh CI/CD tự động train và deploy khi dữ liệu cập nhật hoạt động tốt.

---

## 5. Phần Bonus Đã Thực Hiện

- [x] Bonus 1: Tracking MLflow từ xa với DagsHub: Kết nối repo lên DagsHub, thêm env variables vào GitHub Secrets và sửa cicd.yml.
- [x] Bonus 2: Quét ngưỡng xác suất: Thêm vòng lặp tìm `threshold` từ 0.1 đến 0.9 thay vì 0.5 để tối ưu F1.
- [x] Bonus 3: Báo cáo Precision / Recall: Tự động lưu `classification_report.json` và `confusion_matrix.txt` thành MLflow artifact.
- [x] Bonus 4: Hoàn trả về phiên bản trước (Rollback): Tải report cũ từ S3, so sánh F1 ở bước Quality Gate và chặn deploy nếu F1 mới < F1 cũ.
- [x] Bonus 5: Cảnh báo Data Drift: Tính tỷ lệ lớp dương tập train và cảnh báo nếu lệch quá 5% so với 24.8%.
