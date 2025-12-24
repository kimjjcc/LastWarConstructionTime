import streamlit as st
from datetime import datetime, timedelta
import re

# ----------------------
# 유틸 함수
# ----------------------
def to_million(value: int) -> str:
    m = value / 1_000_000
    if m.is_integer():
        return f"{int(m)}M"
    return f"{m:.1f}M"

def add_space_between_text_and_number(text: str) -> str:
    """
    과학센터11 -> 과학센터 11
    병영27 -> 병영 27
    """
    return re.sub(r"([가-힣A-Za-z]+)(\d+)", r"\1 \2", text)

# ----------------------
# 페이지 설정
# ----------------------
st.set_page_config(
    page_title="Last War 건설 시간 계산기",
    page_icon="lastwarg.png",
    layout="centered"
)

col_icon, col_title = st.columns([1, 6])

with col_icon:
    st.image("lastwarg.png", width=64)

with col_title:
    st.markdown("## Last War 건설 시간 계산기")

st.caption("건물 업그레이드 시 예상 완료 시간과 필요 자원을 확인할 수 있습니다.")
st.divider()

# ----------------------
# 데이터
# ----------------------
BUILD_DATA_TABLE = {
    "본부(Headquarters)": {
        "10 → 11": {
            "time": (0, 7, 4, 0),
            "resource": (1_900_000, 1_900_000, 600_000),
            "require": ("과학센터10", "베리어10"),
        },
        "11 → 12": {
            "time": (0, 9, 6, 0),
            "resource": (3_200_000, 3_200_000, 1_000_000),
            "require": ("과학센터11", "병영11"),
        },
        "12 → 13": {
            "time": (0, 12, 5, 0),
            "resource": (3_500_000, 3_500_000, 1_100_000),
            "require": ("과학센터12", "탱크센터12"),
        },
        "13 → 14": {
            "time": (0, 16, 2, 0),
            "resource": (4_900_000, 4_900_000, 1_600_000),
            "require": ("과학센터13", "연병장13"),
        },
        "14 → 15": {
            "time": (0, 22, 7, 0),
            "resource": (6_800_000, 6_800_000, 2_200_000),
            "require": ("과학센터14", "베리어14"),
        },
    }
}

# ----------------------
# 업그레이드 선택
# ----------------------
st.subheader("🛠️ 업그레이드 선택")

col1, col2 = st.columns(2)

with col1:
    building_type = st.selectbox("건물 선택", BUILD_DATA_TABLE.keys())

with col2:
    building_step = st.selectbox(
        "레벨 구간",
        list(BUILD_DATA_TABLE[building_type].keys())[::-1]
    )

data = BUILD_DATA_TABLE[building_type][building_step]

base_days, base_hours, base_minutes, base_seconds = data["time"]
iron, food, gold = data["resource"]
req1, req2 = data["require"]

# ----------------------
# 기본 건설 시간 (크게 표시)
# ----------------------
st.markdown(
    f"""
    <div style="font-size:22px; font-weight:700; margin-top:10px;">
        ⏱️ 기본 건설 시간<br>
        <span style="font-size:28px;">
            {base_days}D {base_hours:02}:{base_minutes:02}:{base_seconds:02}
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ----------------------
# 자원 표시 (아이콘 이미지 사용)
# ----------------------
st.subheader("📦 필요 자원")

col_r1, col_r2, col_r3 = st.columns(3)

with col_r1:
    st.image("iron.png", width=48)
    st.markdown(f"**철**  \n{to_million(iron)}")

with col_r2:
    st.image("food.png", width=48)
    st.markdown(f"**식량**  \n{to_million(food)}")

with col_r3:
    st.image("gold.png", width=48)
    st.markdown(f"**골드**  \n{to_million(gold)}")

# ----------------------
# 요구 조건 (띄어쓰기 적용)
# ----------------------
st.subheader("📌 요구 조건")

req1 = add_space_between_text_and_number(req1)
req2 = add_space_between_text_and_number(req2)

st.markdown(
    f"""
    - {req1}  
    - {req2}
    """
)

st.divider()

# ----------------------
# 가속 입력
# ----------------------
st.subheader("⚡ 건설 가속")

col3, col4 = st.columns(2)

with col3:
    my_speed = st.number_input(
        "나의 건설 속도 (%)",
        min_value=0.0,
        max_value=500.0,
        value=0.0,
        step=0.1
    )

with col4:
    mayor_speed = st.selectbox(
        "건설 장관 가속 (%)",
        options=[0.0, 25.0, 50.0],
        index=2
    )

# ----------------------
# 계산
# ----------------------
if st.button("🚀 계산하기", use_container_width=True):

    base_seconds_total = (
        base_days * 86400 +
        base_hours * 3600 +
        base_minutes * 60 +
        base_seconds
    )

    total_speed = (my_speed + mayor_speed) / 100.0
    final_seconds = base_seconds_total / (1 + total_speed)

    duration = timedelta(seconds=int(final_seconds))
    finish_time = datetime.now() + duration

    days = duration.days
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    st.success("✅ 계산 완료")

    st.metric(
        "⏱️ 최종 건설 시간",
        f"{days}D {hours:02}:{minutes:02}:{seconds:02}"
    )

    st.metric(
        "📅 완료 예정 시각",
        finish_time.strftime("%Y-%m-%d %H:%M:%S")
    )

# ----------------------
# 공식
# ----------------------
st.divider()
st.subheader("📘 계산 공식")

st.markdown(
    "**최종 건설 시간 = 기본 건설 시간 ÷ (1 + 총 건설 가속 %)**\n\n"
    "- 총 건설 가속 % = 나의 건설 속도 + 건설 장관 가속\n"
    "- 자원 표기는 M 단위 기준"
)
