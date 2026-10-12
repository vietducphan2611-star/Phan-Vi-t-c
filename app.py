
# 6. Tao Web App quan ly diem sinh vien bang Streamlit

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cau hinh trang web
st.set_page_config(
    page_title="Quan ly diem sinh vien",
    page_icon="🎓",
    layout="wide"
)

# Tiêu đề
st.title("📚 QUẢN LÝ ĐIỂM SINH VIÊN")

# Tao du lieu 10 sinh vien
data = {
    "Ho_ten": [
        "Phạm Gia Huy",
        "Nguyễn Khánh Linh",
        "Trần Minh Quân",
        "Lê Thảo Nguyên",
        "Võ Thanh Tùng",
        "Bùi Phương Thảo",
        "Trần Thị Thanh An",
        "Lê Thị Ngọc Nhi",
        "Hàng Võ Khánh Ngân",
        "Nông Nguyễn Ái Nhi"
    ],
    "Chuyen_can": [4,6,8,5,8,7,9,9,9,9],
    "Giua_ky":    [5,9,5,6,6,8,7,10,7,10],
    "Cuoi_ky":    [5,7,7,5,8,7,9,10,9,9]
}

df = pd.DataFrame(data)

# Tinh diem tong ket
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"]
    + 0.3 * df["Giua_ky"]
    + 0.5 * df["Cuoi_ky"]
)

# Xep loai sinh vien
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# Tieu de Web App
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.write("Bảng điểm và thống kê kết quả học tập của 10 sinh viên.")

# Hien thi bang diem
st.subheader("1. Bảng điểm sinh viên")

bang_diem = df.rename(columns={
    "Ho_va_ten": "Họ tên",
    "Chuyen_can": "Chuyên cần",
    "Giua_ky": "Giữa kỳ",
    "Cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
})

st.dataframe(
    bang_diem.style.format({"Tổng kết": "{:.2f}"}),
    use_container_width=True,
    hide_index=True
)

# Thong ke ket qua hoc tap
st.subheader("2. Thống kê kết quả")

diem_tb = df["Tong_ket"].mean()
idx_max = df["Tong_ket"].idxmax()
idx_min = df["Tong_ket"].idxmin()
so_sinh_vien_dat = (df["Tong_ket"] >= 5).sum()

cot1, cot2, cot3, cot4 = st.columns(4)

cot1.metric("Điểm trung bình", f"{diem_tb:.2f}")
cot2.metric(
    "Điểm cao nhất",
    f"{df.loc[idx_max, 'Tong_ket']:.2f}",
    df.loc[idx_max, "Ho_va_ten"]
)
cot3.metric(
    "Điểm thấp nhất",
    f"{df.loc[idx_min, 'Tong_ket']:.2f}",
    df.loc[idx_min, "Ho_va_ten"]
)
cot4.metric("Số sinh viên đạt", f"{so_sinh_vien_dat}/10")

# Chon sinh vien bang Selectbox
st.subheader("3. Tra cứu thông tin sinh viên")

ten_chon = st.selectbox(
    "Chọn sinh viên:",
    df["Ho_va_ten"]
)

sv = df[df["Ho_va_ten"] == ten_chon].iloc[0]

st.write(f"**Họ và tên:** {sv['Ho_va_ten']}")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Chuyên cần", f"{sv['Chuyen_can']:.1f}")
c2.metric("Giữa kỳ", f"{sv['Giua_ky']:.1f}")
c3.metric("Cuối kỳ", f"{sv['Cuoi_ky']:.1f}")
c4.metric("Tổng kết", f"{sv['Tong_ket']:.2f}")
c5.metric("Xếp loại", sv["Xep_loai"])

# Ve bieu do cot
st.subheader("4. Biểu đồ điểm tổng kết")

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(df["Ho_va_ten"], df["Tong_ket"])

ax.set_title("BIỂU ĐỒ ĐIỂM TỔNG KẾT CỦA 10 SINH VIÊN")
ax.set_xlabel("Họ và tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.tick_params(axis="x", labelrotation=45)

for i, diem in enumerate(df["Tong_ket"]):
    ax.text(i, diem + 0.1, f"{diem:.1f}", ha="center")

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Thong tin nguoi tao ung dung
st.divider()
st.caption("Người tạo ứng dụng: [Phan Việt Đức] | MSSV: [052208010383]")
