import streamlit as st
from datetime import datetime, timedelta

# ----------------------
# 유틸 함수
# ----------------------
def to_million(value: int) -> str:
    """
    숫자를 M 단위 문자열로 변환
    예: 1_900_000 -> 1.9M
        110_000_000 -> 110M
    """
    m = value / 1_000_000
    if m.is_integer():
        return f"{int(m)}M"
    return f"{m:.1f}M"

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
# 데이터 테이블
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
        "15 → 16": {
            "time": (1, 3, 0, 0),
            "resource": (12_000_000, 12_000_000, 3_900_000),
            "require": ("과학센터15", "연맹센터15"),
        },
        "16 → 17": {
            "time": (1, 8, 0, 0),
            "resource": (16_000_000, 16_000_000, 5_100_000),
            "require": ("과학센터16", "탱크센터16"),
        },
        "17 → 18": {
            "time": (2, 6, 0, 0),
            "resource": (28_000_000, 28_000_000, 8_900_000),
            "require": ("과학센터17", "병원17"),
        },
        "18 → 19": {
            "time": (3, 6, 0, 0),
            "resource": (33_000_000, 33_000_000, 11_000_000),
            "require": ("과학센터18", "베리어18"),
        },
        "19 → 20": {
            "time": (5, 1, 0, 0),
            "resource": (60_000_000, 60_000_000, 19_000_000),
            "require": ("과학센터19", "병영19"),
        },
        "20 → 21": {
            "time": (6, 6, 0, 0),
            "resource": (84_000_000, 84_000_000, 27_000_000),
            "require": ("과학센터20", "탱크센터20"),
        },
        "21 → 22": {
            "time": (8, 6, 0, 0),
            "resource": (110_000_000, 110_000_000, 35_000_000),
            "require": ("과학센터21", "연병장21"),
        },
        "22 → 23": {
            "time": (11, 1, 0, 0),
            "resource": (140_000_000, 140_000_000, 44_000_000),
            "require": ("과학센터22", "베리어22"),
        },
        "23 → 24": {
            "time": (15, 6, 0, 0),
            "resource": (170_000_000, 170_000_000, 54_000_000),
            "require": ("과학센터23", "연맹센터23"),
        },
        "24 → 25": {
            "time": (21, 9, 0, 0),
            "resource": (290_000_000, 290_000_000, 93_000_000),
            "require": ("과학센터24", "탱크센터24"),
        },
        "25 → 26": {
            "time": (30, 6, 0, 0),
            "resource": (400_000_000, 400_000_000, 130_000_000),
            "require": ("과학센터25", "병원25"),
        },
        "26 → 27": {
            "time": (42, 9, 0, 0),
            "resource": (530_000_000, 530_000_000, 170_000_000),
            "require": ("과학센터26", "베리어26"),
        },
        "27 → 28": {
            "time": (60, 2, 54, 20),
            "resource": (740_000_000, 740_000_000, 240_000_000),
            "require": ("과학센터27", "병영27"),
        },
        "28 → 29": {
            "time": (78, 3, 46, 37),
            "resource": (1_000_000_000, 1_000_000_000, 330_000_000),
            "require": ("과학센터28", "탱크센터28"),
        },
        "29 → 30": {
            "time": (101, 14, 30, 37),
            "resource": (1_400_000_000, 1_400_000_000, 460_000_000),
            "require": ("과학센터29", "연병장29"),
        },
    }
}

# ----------------------
# 입력 영역
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
# 기본 정보 표시
# ----------------------
st.caption(
    f"⏱️ 기본 건설 시간: "
    f"{base_days}D {base_hours:02}:{base_minutes:02}:{base_seconds:02}"
)

col_r1, col_r2, col_r3 = st.columns(3)
col_r1.metric("⛏️ 철", to_million(iron))
col_r2.metric("🌾 식량", to_million(food))
col_r3.metric("🪙 골드", to_million(gold))

st.markdown(
    f"**📌 요구 조건**  \n"
    f"- {req1}  \n"
    f"- {req2}"
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
        "⏱️ 최종 건설 시간",
        f"{days}D {hours:02}:{minutes:02}:{seconds:02}"
    )

    st.metric(
        "📅 완료 예정 시각",
        finish_time.strftime("%Y-%m-%d %H:%M:%S")
    )

# ----------------------
# 설명
# ----------------------
st.divider()
st.subheader("📘 계산 공식")

st.markdown(
    "**최종 건설 시간 = 기본 건설 시간 ÷ (1 + 총 건설 가속 %)**\n\n"
    "- 총 건설 가속 % = 나의 건설 속도 + 건설 장관 가속\n"
    "- 자원은 항상 M 단위로 표기됨"
)
