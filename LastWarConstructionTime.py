import streamlit as st
from datetime import datetime, timedelta
import re

# ----------------------
# 유틸
# ----------------------
def add_space(text: str) -> str:
    return re.sub(r"([가-힣A-Za-z]+)(\d+)", r"\1 \2", text)

def to_million(v: float) -> str:
    return f"{int(v)}M" if v.is_integer() else f"{v:.1f}M"

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
        "10 → 11": {"time": (0, 7, 4, 0), "res": (1.9, 1.9, 0.6), "req": ("과학센터10", "베리어10")},
        "11 → 12": {"time": (0, 9, 6, 0), "res": (3.2, 3.2, 1.0), "req": ("과학센터11", "병영11")},
        "12 → 13": {"time": (0,12, 5, 0), "res": (3.5, 3.5, 1.1), "req": ("과학센터12", "탱크센터12")},
        "13 → 14": {"time": (0,16, 2, 0), "res": (4.9, 4.9, 1.6), "req": ("과학센터13", "연병장13")},
        "14 → 15": {"time": (0,22, 7, 0), "res": (6.8, 6.8, 2.2), "req": ("과학센터14", "베리어14")},
        "15 → 16": {"time": (1, 7,48, 0), "res": (12, 12, 3.9),  "req": ("과학센터15", "연맹센터15")},
        "16 → 17": {"time": (1,19,12, 0), "res": (16, 16, 5.1),  "req": ("과학센터16", "탱크센터16")},
        "17 → 18": {"time": (2,14,24, 0), "res": (28, 28, 8.9),  "req": ("과학센터17", "병원17")},
        "18 → 19": {"time": (3,14,24, 0), "res": (33, 33, 11),   "req": ("과학센터18", "베리어18")},
        "19 → 20": {"time": (5, 2,24, 0), "res": (60, 60, 19),   "req": ("과학센터19", "병영19")},
        "20 → 21": {"time": (6,14,24, 0), "res": (84, 84, 27),   "req": ("과학센터20", "탱크센터20")},
        "21 → 22": {"time": (8,14,24, 0), "res": (110,110,35),   "req": ("과학센터21", "연병장21")},
        "22 → 23": {"time": (11, 2,24,0), "res": (140,140,44),   "req": ("과학센터22", "베리어22")},
        "23 → 24": {"time": (15,14,24,0), "res": (170,170,54),   "req": ("과학센터23", "연맹센터23")},
        "24 → 25": {"time": (21,21,36,0), "res": (290,290,93),   "req": ("과학센터24", "탱크센터24")},
        "25 → 26": {"time": (30,14,24,0), "res": (400,400,130),  "req": ("과학센터25", "병원25")},
        "26 → 27": {"time": (42,21,36,0), "res": (530,530,170),  "req": ("과학센터26", "베리어26")},
        "27 → 28": {"time": (60, 2,24,0), "res": (740,740,240),  "req": ("과학센터27", "병영27")},
        "28 → 29": {"time": (78, 2,24,0), "res": (1000,1000,330),"req": ("과학센터28", "탱크센터28")},
        "29 → 30": {"time": (101,14,24,0),"res": (1400,1400,460),"req": ("과학센터29", "연병장29")},
    },

    "과학기술센터": {},
    "병영": {},
    "병원": {},
    "탱크 센터": {},
    "연병장": {},
    "연맹 센터": {},
    "베리어": {},
}

# ----------------------
# 건물 / 레벨 선택
# ----------------------
col_sel1, col_sel2 = st.columns([3, 2])

with col_sel1:
    building = st.selectbox("🏗️ 건물 선택", BUILDING_DATA.keys())

levels = BUILDING_DATA[building]
if not levels:
    with col_sel2:
        st.selectbox("레벨 구간", [])
    st.info("⚠️ 이 건물의 상세 데이터는 아직 준비 중입니다.")
    st.stop()

with col_sel2:
    level = st.selectbox("레벨 구간", list(levels.keys())[::-1])

data = levels[level]
d, h, m, s = data["time"]

# ----------------------
# 본부 전용 정보
# ----------------------
if building.startswith("본부"):
    iron, food, gold = data["res"]
    req1, req2 = map(add_space, data["req"])

    st.divider()

    col_res, col_req = st.columns([3, 2])

    with col_res:
        st.subheader("📦 필요 자원")

        # ⬇⬇⬇ 여기 비율을 직접 줄이면 자원 간 간격이 더 좁아짐 ⬇⬇⬇
        # 예: [0.8, 0.8, 0.8] / [0.6, 0.6, 0.6] 등
        r1, r2, r3 = st.columns([0.7, 0.7, 0.7])

        with r1:
            st.image("iron.png", width=40)
            st.markdown(to_million(iron))
        with r2:
            st.image("food.png", width=40)
            st.markdown(to_million(food))
        with r3:
            st.image("gold.png", width=40)
            st.markdown(to_million(gold))

    with col_req:
        st.subheader("📌 요구 조건")
        st.markdown(f"- {req1}\n- {req2}")

# ----------------------
# 가속 계산
# ----------------------
st.divider()
st.subheader("⚡ 건설 가속")

my_speed = st.number_input("나의 건설 속도 (%)", 0.0, 500.0, 0.0, 0.1)
mayor = st.selectbox("건설 장관 가속 (%)", [0.0, 25.0, 50.0], index=2)

if st.button("🚀 계산하기", use_container_width=True):
    base_sec = d*86400 + h*3600 + m*60 + s
    final_sec = base_sec / (1 + (my_speed + mayor) / 100)

    dur = timedelta(seconds=int(final_sec))
    end_time = datetime.now() + dur

    st.success("계산 완료")

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        st.metric(
            "⏱️ 기본 건설 시간",
            format_time(d, h, m, s)
        )

    with col_t2:
        st.metric(
            "⚡ 최종 건설 시간",
            f"{dur.days}D {dur.seconds//3600:02}:{(dur.seconds%3600)//60:02}"
        )

    st.metric(
        "📅 완료 예정 시각",
        end_time.strftime("%Y-%m-%d %H:%M:%S")
    )



