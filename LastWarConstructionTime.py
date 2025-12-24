import streamlit as st
from datetime import datetime, timedelta

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

st.caption("원하는 건물과 건설 가속률을 입력하면 예상 완료 시간을 계산합니다.")
st.divider()

# ----------------------
# 기본 건설 시간 테이블
# 단위: (days, hours, minutes, seconds)
# ----------------------
BUILD_TIME_TABLE = {
    "본부(Headquarters)": {
        "10 → 11": (0, 7, 4, 0),
        "11 → 12": (0, 9, 6, 0),
        "12 → 13": (0, 12, 5, 0),
        "13 → 14": (0, 16, 2, 0),
        "14 → 15": (0, 22, 7, 0),
        "15 → 16": (1, 3, 0, 0),
        "16 → 17": (1, 8, 0, 0),
        "17 → 18": (2, 6, 0, 0),
        "18 → 19": (3, 6, 0, 0),
        "19 → 20": (5, 1, 0, 0),
        "20 → 21": (6, 6, 0, 0),
        "21 → 22": (8, 6, 0, 0),
        "22 → 23": (11, 1, 0, 0),
        "23 → 24": (15, 6, 0, 0),
        "24 → 25": (21, 9, 0, 0),
        "25 → 26": (30, 6, 0, 0),
        "26 → 27": (42, 9, 0, 0),
        "27 → 28": (60, 2, 54, 20),
        "28 → 29": (78, 3, 46, 37),
        "29 → 30": (101, 14, 30, 37),
    }
}

# ----------------------
# 입력 영역
# ----------------------
st.subheader("🛠️ 기본 건설 시간 선택")

col1, col2 = st.columns(2)

with col1:
    building_type = st.selectbox(
        "건물 선택",
        BUILD_TIME_TABLE.keys()
    )

with col2:
    building_step = st.selectbox(
        "레벨 구간",
        list(BUILD_TIME_TABLE[building_type].keys())[::-1]  # 높은 레벨이 위로
    )

base_days, base_hours, base_minutes, base_seconds = \
    BUILD_TIME_TABLE[building_type][building_step]

st.caption(
    f"선택된 기본 건설 시간: "
    f"{base_days}D {base_hours:02}:{base_minutes:02}:{base_seconds:02}"
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
# 계산 버튼
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
        label="⏱️ 최종 건설 시간",
        value=f"{days}D {hours:02}:{minutes:02}:{seconds:02}"
    )

    st.metric(
        label="📅 완료 예정 시각",
        value=finish_time.strftime("%Y-%m-%d %H:%M:%S")
    )

# ----------------------
# 설명 영역
# ----------------------
st.divider()
st.subheader("📘 계산 공식")

st.markdown(
    """
