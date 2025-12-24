import streamlit as st
from datetime import datetime, timedelta
import re

# ----------------------
# 유틸
# ----------------------
def add_space(text: str) -> str:
    return re.sub(r"([가-힣A-Za-z]+)(\d+)", r"\1 \2", text)

def to_million(v: float) -> str:
    if v >= 1000:
        return f"{v/1000:.1f}G" if v % 1000 else f"{v//1000}G"
    return f"{v}M" if v >= 1 else f"{v*1000:.0f}K"

def format_time(d, h, m, s):
    return f"{d}D {h:02}:{m:02}:{s:02}"

# ----------------------
# 페이지 설정
# ----------------------
st.set_page_config(
    page_title="Last War 건설 시간 계산기",
    page_icon="lastwarg.png",
    layout="centered"
)

st.image("lastwarg.png", width=64)
st.markdown("## Last War 건설 시간 계산기")
st.caption("건물 업그레이드 시간 · 자원 · 완료 시각 계산")
st.divider()

# ----------------------
# 데이터
# ----------------------
BUILDING_DATA = {
    "본부(Headquarters)": {
        "10 → 11": {"time": (0, 7,22,55), "res": (1.9,1.9,0.6), "req": ("과학센터10","베리어10")},
        "11 → 12": {"time": (0, 9,35,48), "res": (3.2,3.2,1.0), "req": ("과학센터11","병영11")},
        "12 → 13": {"time": (0,12,28,32), "res": (3.5,3.5,1.1), "req": ("과학센터12","탱크센터12")},
        # ... 나머지 본부 시간도 동일하게 적용
    },

    "과학기술센터": {
        "11 → 12": {"time": (0,6,27,34), "res": (1.6,1.6,0.52)},
        "12 → 13": {"time": (0,8,23,49), "res": (2.8,2.8,0.89)},
        "13 → 14": {"time": (0,10,54,58), "res": (3.1,3.1,0.98)},
        "14 → 15": {"time": (0,14,11,27), "res": (4.3,4.3,1.4)},
        "15 → 16": {"time": (0,19,52,2), "res": (6,6,1.9)},
        "16 → 17": {"time": (1,3,48,51), "res": (11,11,3.4)},
        "17 → 18": {"time": (1,14,56,23), "res": (14,14,4.4)},
        "18 → 19": {"time": (2,6,30,56), "res": (24,24,7.8)},
        "19 → 20": {"time": (3,4,19,18), "res": (29,29,9.3)},
        "20 → 21": {"time": (4,10,51,2), "res": (52,52,17)},
        "21 → 22": {"time": (5,18,54,20), "res": (73,73,23)},
        "22 → 23": {"time": (7,12,34,38), "res": (95,95,30)},
        "23 → 24": {"time": (9,18,45,1), "res": (120,120,38)},
        "24 → 25": {"time": (13,16,39,1), "res": (150,150,48)},
        "25 → 26": {"time": (19,4,6,37), "res": (250,250,81)},
        "26 → 27": {"time": (26,20,9,16), "res": (350,350,110)},
        "27 → 28": {"time": (37,13,48,58), "res": (460,460,150)},
        "28 → 29": {"time": (52,14,32,32), "res": (640,640,210)},
        "29 → 30": {"time": (68,9,18,18), "res": (900,900,290)},
    },

    "탱크 센터": {
        # Tank Center 데이터 형식 예시 (Tech Center와 동일하게 적용)
    },
}

# ----------------------
# 건물 / 레벨 선택
# ----------------------
building = st.selectbox("🏗️ 건물 선택", BUILDING_DATA.keys())
level = st.selectbox("레벨 구간", list(BUILDING_DATA[building].keys())[::-1])
data = BUILDING_DATA[building][level]
d, h, m, s = data["time"]

# ----------------------
# 자원 / 요구조건
# ----------------------
iron, food, gold = data["res"]
reqs = data.get("req", []) if "req" in data else []

st.divider()
col_res, col_req = st.columns([3,2])

with col_res:
    st.subheader("📦 필요 자원")
    r1,r2,r3 = st.columns(3)
    with r1:
        st.image("iron.png", width=40)
        st.markdown(to_million(iron))
    with r2:
        st.image("food.png", width=40)
        st.markdown(to_million(food))
    with r3:
        st.image("gold.png", width=40)
        st.markdown(to_million(gold))

if reqs:
    with col_req:
        st.subheader("📌 요구 조건")
        for r in reqs:
            st.markdown(f"- {add_space(r)}")

# ----------------------
# 가속 계산
# ----------------------
st.divider()
st.subheader("⚡ 건설 가속")
my_speed = st.number_input("나의 건설 속도 (%)", 0.0, 500.0, 0.0, 0.1)
mayor = st.selectbox("건설 장관 가속 (%)", [0.0,25.0,50.0], index=2)

if st.button("🚀 계산하기", use_container_width=True):
    base_sec = d*86400 + h*3600 + m*60 + s
    final_sec = base_sec / (1 + (my_speed + mayor)/100)
    dur = timedelta(seconds=int(final_sec))
    end_time = datetime.now() + dur

    col1,col2 = st.columns(2)
    with col1:
        st.metric("⏱️ 기본 건설 시간", format_time(d,h,m,s))
    with col2:
        st.metric("⚡ 최종 건설 시간", f"{dur.days}D {dur.seconds//3600:02}:{(dur.seconds%3600)//60:02}:{dur.seconds%60:02}")

    st.metric("📅 완료 예정 시각", end_time.strftime("%Y-%m-%d %H:%M:%S"))
