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

**Lý do:** Em chọn bộ siêu tham số thứ 3 vì nó cho kết quả F1-score cao nhất (0.7149) so với hai lần chạy còn lại. Lần chạy có Accuracy cao nhất (0.8780 ở lần 1) không trùng với lần có F1 cao nhất, điều này cho thấy Accuracy không phản ánh đúng hoàn toàn khả năng nhận diện lớp dương (những người có thu nhập cao) của mô hình. Trong khi đó, F1-score cân bằng tốt hơn giữa Precision và Recall. Nhìn chung, việc tăng `n_estimators` lên 200 và giữ `learning_rate` ở 0.1 giúp mô hình học được nhiều đặc trưng phức tạp hơn mà không bị quá khớp (overfitting).

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Trong bài toán dự đoán thu nhập, tỷ lệ người có thu nhập > 50K (lớp dương) chỉ chiếm khoảng 24,8% tổng số mẫu dữ liệu, tạo ra sự mất cân bằng dữ liệu nghiêm trọng. 
Nếu dùng một mô hình vô tri luôn dự đoán "thu nhập thấp" (0) cho mọi trường hợp, Accuracy vẫn sẽ đạt tới khoảng 75,2%. Con số này gây hiểu nhầm rất lớn vì mô hình trông có vẻ hoạt động tốt nhưng thực chất là vô dụng. 
Do đó, ta phải dùng F1-score (harmonic mean của Precision và Recall) đối với lớp dương để đánh giá chính xác khả năng nhận diện nhóm thiểu số quan trọng. Việc không dùng average="weighted" hay "macro" đảm bảo rằng ta chỉ tập trung đo lường độ chính xác trên nhóm lớp dương thay vì bị pha loãng bởi nhóm lớp âm áp đảo.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
| -------- | ----------- | --------------- |
| Lỗi 403 Forbidden tải mô hình ở EC2 | File cấu hình `systemd` trên máy ảo chưa được cấp quyền `AWS_ACCESS_KEY` để gọi S3 | Cập nhật cấu hình môi trường trong `/etc/systemd/system/income-api.service` và truyền biến bí mật vào. |
| EC2 restart service failed (bị crash) | Thư viện `scikit-learn` trên EC2 cài mặc định (1.5.x) không tương thích với mô hình đã train (1.4.2) | Cài đặt lại thư viện trên máy chủ bằng lệnh `pip3 install scikit-learn==1.4.2` cho trùng với bản gốc. |
| Lỗi GitHub Actions `Unable to locate credentials` | Biến `AWS_ACCESS_KEY_ID` rỗng do cấu hình sai GitHub Secrets ban đầu | Xóa thiết lập cũ, cập nhật lại đúng 2 biến Secrets từ cấu hình mặc định của ~/.aws/credentials. |

---

## 4. So Sánh Bước 2 và Bước 3

|                              | f1_score | accuracy |
| ---------------------------- | -------- | -------- |
| Bước 2 (chỉ `train_batch1`)  | 0.7149   | 0.8740   |
| Bước 3 (thêm `train_batch2`) | 0.7354   | 0.8820   |

**Nhận xét:** F1-score tăng nhẹ (khoảng 0.02) khi bổ sung thêm dữ liệu mới. Do 2 tập dữ liệu được tách ra từ cùng 1 nguồn nên có chung phân phối, mô hình đã học được đa số các đặc trưng từ ban đầu. Dù hiệu năng không đột phá mạnh, bước này chứng minh được vòng lặp CI/CD đã hoạt động trơn tru: tự động train lại và triển khai khi có dữ liệu mới.
