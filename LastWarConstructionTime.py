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

st.caption("원하는 건물과 건설 가속률을 입력하면 예상 완료 시간과 필요 자원을 확인할 수 있습니다.")
st.divider()

# ----------------------
# 기본 데이터 테이블
# ----------------------
# 단위
# time: (days, hours, minutes, seconds)
# resource: (iron, food, gold)
# ----------------------
BUILD_DATA_TABLE = {
    "본부(Headquarters)": {
        "10 → 11": {
            "time": (0, 7, 4, 0),
            "resource": (0, 0, 0),   # TODO: 철, 식량, 골드
        },
        "11 → 12": {
            "time": (0, 9, 6, 0),
            "resource": (0, 0, 0),
        },
        "12 → 13": {
            "time": (0, 12, 5, 0),
            "resource": (0, 0, 0),
        },
        "13 → 14": {
            "time": (0, 16, 2, 0),
            "resource": (0, 0, 0),
        },
        "14 → 15": {
            "time": (0, 22, 7, 0),
            "resource": (0, 0, 0),
        },
        "15 → 16": {
            "time": (1, 3, 0, 0),
            "resource": (0, 0, 0),
        },
        "16 → 17": {
            "time": (1, 8, 0, 0),
            "resource": (0, 0, 0),
        },
        "17 → 18": {
            "time": (2, 6, 0, 0),
            "resource": (0, 0, 0),
        },
        "18 → 19": {
            "time": (3, 6, 0, 0),
            "resource": (0, 0, 0),
        },
        "19 → 20": {
            "time": (5, 1, 0, 0),
            "resource": (0, 0, 0),
        },
        "20 → 21": {
            "time": (6, 6, 0, 0),
            "resource": (0, 0, 0),
        },
        "21 → 22": {
            "time": (8, 6, 0, 0),
            "resource": (0, 0, 0),
        },
        "22 → 23": {
            "time": (11, 1, 0, 0),
            "resource": (0, 0, 0),
        },
        "23 → 24": {
            "time": (15, 6, 0, 0),
            "resource": (0, 0, 0),
        },
        "24 → 25": {
            "time": (21, 9, 0, 0),
            "resource": (0, 0, 0),
        },
        "25 → 26": {
            "time": (30, 6, 0, 0),
            "resource": (0, 0, 0),
        },
        "26 → 27": {
            "time": (42, 9, 0, 0),
            "resource": (0, 0, 0),
        },
        "27 → 28": {
            "time": (60, 2, 54, 20),
            "resource": (0, 0, 0),
        },
        "28 → 29": {
            "time": (78, 3, 46, 37),
            "resource": (0, 0, 0),
        },
        "29 → 30": {
            "time": (101, 14, 30, 37),
            "resource": (0, 0, 0),
        },
    }
}

# ----------------------
# 입력 영역
# ----------------------
st.subheader("🛠️ 기본 정보 선택")

col1, col2 = st.columns(2)

with col1:
    building_type = st.selectbox(
        "건물 선택",
        BUILD_DATA_TABLE.keys()
    )

with col2:
    building_step = st.selectbox(
        "레벨 구간",
        list(BUILD_DATA_TABLE[building_type].keys())[::-1]
    )

selected_data = BUILD_DATA_TABLE[building_type][building_step]

# 시간
base_days, base_hours, base_minutes, base_seconds = selected_data["time"]

# 자원
iron, food, gold = selected_data["resource"]

# ----------------------
# 기본 정보 표시
# ----------------------
st.caption(
    f"⏱️ 기본 건설 시간: "
    f"{base_days}D {base_hours:02}:{base_minutes:02}:{base_seconds:02}"
)

# 🔽 자원 표시 위치 (시간 바로 아래)
col_r1, col_r2, col_r3 = st.columns(3)

col_r1.metric("⛏️ 철", f"{iron:,}")
col_r2.metric("🌾 식량", f"{food:,}")
col_r3.metric("🪙 골드", f"{gold:,}")

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
        "⏱️ 최종 건설 시간",
        f"{days}D {hours:02}:{minutes:02}:{seconds:02}"
    )

    st.metric(
        "📅 완료 예정 시각",
        finish_time.strftime("%Y-%m-%d %H:%M:%S")
    )

# ----------------------
# 설명 영역
# ----------------------
st.divider()
st.subheader("📘 계산 공식 설명")

st.markdown(
    "**최종 건설 시간 계산식**\n\n"
    "```\n"
    "최종 건설 시간 = 기본 건설 시간 ÷ (1 + 총 건설 가속 %)\n"
    "```\n\n"
    "- 총 건설 가속 % = 나의 건설 속도 + 건설 장관 가속\n"
    "- 모든 가속은 단순 합산 방식\n"
    "- 건설은 시작 시점 기준으로 계산됨"
)

st.info(
    "⚠️ 자원 소모량은 가속 여부와 무관하며, "
    "게임 내 실제 수치와 차이가 있을 수 있습니다."
)
