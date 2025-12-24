import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="Last War 건설 시간 계산기",
    page_icon="lastwarg.png",
    layout="wide"
)

# ===============================
# 이미지 로드 (Base64)
# ===============================
def load_image_b64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()

IRON_B64 = load_image_b64("iron.png")
FOOD_B64 = load_image_b64("food.png")
GOLD_B64 = load_image_b64("gold.png")

# ===============================
# 기본 건설 시간 (시간 단위)
# ===============================
BASE_BUILD_TIME = {
    10: 7.4,
    11: 9.6,
    12: 12.5,
    13: 16.2,
    14: 22.7,
    15: 31.2,
    16: 43.2,
    17: 62.4,
    18: 86.4,
    19: 122.4,
    20: 158.4,
    21: 206.4,
    22: 266.4,
    23: 374.4,
    24: 525.6,
    25: 734.4,
    26: 1029.6,
    27: 1442.4,
    28: 2016.0,
    29: 2438.4,
}

# ===============================
# 본부 자원 + 요구조건
# (M 단위)
# ===============================
HQ_DATA = {
    10: (1.9, 1.9, 0.6, "과학센터 10", "베리어 10"),
    11: (3.2, 3.2, 1.0, "과학센터 11", "병영 11"),
    12: (3.5, 3.5, 1.1, "과학센터 12", "탱크센터 12"),
    13: (4.9, 4.9, 1.6, "과학센터 13", "연병장 13"),
    14: (6.8, 6.8, 2.2, "과학센터 14", "베리어 14"),
    15: (12, 12, 3.9, "과학센터 15", "연맹센터 15"),
    16: (16, 16, 5.1, "과학센터 16", "탱크센터 16"),
    17: (28, 28, 8.9, "과학센터 17", "병원 17"),
    18: (33, 33, 11, "과학센터 18", "베리어 18"),
    19: (60, 60, 19, "과학센터 19", "병영 19"),
    20: (84, 84, 27, "과학센터 20", "탱크센터 20"),
    21: (110, 110, 35, "과학센터 21", "연병장 21"),
    22: (140, 140, 44, "과학센터 22", "베리어 22"),
    23: (170, 170, 54, "과학센터 23", "연맹센터 23"),
    24: (290, 290, 93, "과학센터 24", "탱크센터 24"),
    25: (400, 400, 130, "과학센터 25", "병원 25"),
    26: (530, 530, 170, "과학센터 26", "베리어 26"),
    27: (740, 740, 240, "과학센터 27", "병영 27"),
    28: (1000, 1000, 330, "과학센터 28", "탱크센터 28"),
    29: (1400, 1400, 460, "과학센터 29", "연병장 29"),
}

# ===============================
# CSS (자원 간격 조절 가능)
# ===============================
st.markdown("""
<style>
.resource-row {
    display: flex;
    gap: 6px;   /* ← 🔥 여기 숫자를 직접 줄이세요 (예: 6 → 4 → 2) */
    align-items: center;
}
.resource-item {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 16px;
}
.require-box {
    margin-left: 20px;
    font-size: 15px;
}
.time-box {
    font-size: 26px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# UI
# ===============================
st.title("🏗️ Last War 건설 시간 계산기")

left, right = st.columns([1, 2])

with left:
    building = st.selectbox("건물 선택", ["본부"])
    level = st.selectbox("레벨 구간 선택", list(range(10, 30)))
    speed = st.number_input("총 건설 가속 (%)", min_value=0.0, value=0.0)

# ===============================
# 계산
# ===============================
base_time = BASE_BUILD_TIME[level]
final_time = base_time / (1 + speed / 100)

iron, food, gold, req1, req2 = HQ_DATA[level]

# ===============================
# 결과 표시
# ===============================
st.subheader("📊 결과")

st.markdown(f"""
<div class="time-box">
기본 건설 시간: {base_time:.1f} h<br>
최종 건설 시간: {final_time:.1f} h
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="resource-row">
    <div class="resource-item">
        <img src="data:image/png;base64,{IRON_B64}" width="24">
        <span>{iron}M</span>
    </div>
    <div class="resource-item">
        <img src="data:image/png;base64,{FOOD_B64}" width="24">
        <span>{food}M</span>
    </div>
    <div class="resource-item">
        <img src="data:image/png;base64,{GOLD_B64}" width="24">
        <span>{gold}M</span>
    </div>

    <div class="require-box">
        요구조건: {req1}, {req2}
    </div>
</div>
""", unsafe_allow_html=True)
