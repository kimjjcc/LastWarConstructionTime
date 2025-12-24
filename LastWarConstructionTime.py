import streamlit as st
from datetime import datetime, timedelta

# ----------------------
# 페이지 설정
# ----------------------
st.set_page_config(
    page_title="Last War 건설 시간 계산기",
    page_icon="🏗️",
    layout="centered"
)

st.title("🏗️ Last War 건설 시간 계산기")
st.caption("기본 건설 시간 ÷ (1 + 총 건설 가속 %)")

st.divider()

# ----------------------
# 기본 건설 시간 테이블 (⚠️ 네가 채울 부분)
# 단위: (days, hours, minutes, seconds)
# ----------------------
BUILD_TIME_TABLE = {
    "본부": {
        10: (0, 0, 0, 0),
        11: (0, 0, 0, 0),
        # ...
        30: (101, 6, 0, 0),
    },
    "과학 기술 센터": {
        10: (0, 0, 0, 0),
        30: (0, 0, 0, 0),
    },
    "탱크 센터": {
        10: (0, 0, 0, 0),
        30: (0, 0, 0, 0),
    },
    "병영": {
        10: (0, 0, 0, 0),
        30: (0, 0, 0, 0),
    },
    "연병장": {
        10: (0, 0, 0, 0),
        30: (0, 0, 0, 0),
    },
    "연맹 센터": {
        10: (0, 0, 0, 0),
        30: (0, 0, 0, 0),
    },
    "병원": {
        10: (0, 0, 0, 0),
        30: (0, 0, 0, 0),
    },
    "베리어": {
        10: (0, 0, 0, 0),
        30: (0, 0, 0, 0),
    },
}

# ----------------------
# 입력 영역
# ----------------------
st.subheader("🛠️ 기본 건설 시간 입력")

col1, col2 = st.columns(2)

with col1:
    building_type = st.selectbox(
        "건물 선택",
        list(BUILD_TIME_TABLE.keys())
    )

with col2:
    building_level = st.selectbox(
        "건물 레벨",
        list(range(10, 31))
    )

# 선택된 기본 시간 불러오기
base_days, base_hours, base_minutes, base_seconds = \
    BUILD_TIME_TABLE.get(building_type, {}).get(
        building_level, (0, 0, 0, 0)
    )

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
        value=80.0,
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

    if base_seconds_total <= 0:
        st.error("⚠️ 선택한 건물/레벨의 기본 건설 시간이 설정되어 있지 않습니다.")
    else:
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
st.subheader("📘 계산 공식 설명")

st.markdown(
    "**최종 건설 시간 계산식**\n\n"
    "```\n"
    "최종 건설 시간 = 기본 건설 시간 ÷ (1 + 총 건설 가속 %)\n"
    "```\n\n"
    "- 총 건설 가속 % = 나의 건설 속도 + 건설 장관\n"
    "- 모든 가속은 단순 합산 방식\n"
    "- 건설 시작 시점에 활성화된 가속만 적용됨"
)

st.info(
    "⚠️ 게임 내 UI에 표시되는 가속 수치와 실제 적용 가속은 다를 수 있습니다.\n"
    "건설은 시작 시점 기준으로 계산됩니다."
)




