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
# 입력 영역
# ----------------------
st.subheader("🔧 입력값")

col1, col2 = st.columns(2)

with col1:
    base_days = st.number_input(
        "기본 건설 일수 (Days)",
        min_value=0,
        value=0
    )
    base_hours = st.number_input(
        "기본 건설 시간 (Hours)",
        min_value=0,
        max_value=23,
        value=0
    )

with col2:
    base_minutes = st.number_input(
        "기본 건설 분 (Minutes)",
        min_value=0,
        max_value=59,
        value=0
    )
    base_seconds = st.number_input(
        "기본 건설 초 (Seconds)",
        min_value=0,
        max_value=59,
        value=0
    )

st.divider()

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

    # 기본 시간 → 초 변환
    base_seconds_total = (
        base_days * 86400 +
        base_hours * 3600 +
        base_minutes * 60 +
        base_seconds
    )

    if base_seconds_total <= 0:
        st.error("기본 건설 시간은 0보다 커야 합니다.")
    else:
        # 가속 계산
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

        st.caption("※ 완료 예정 시각은 계산 버튼을 누른 시점을 기준으로 합니다.")

# ----------------------
# 설명 영역 (안전한 문자열 방식)
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
