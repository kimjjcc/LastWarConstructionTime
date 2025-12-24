from datetime import datetime, timedelta

def calculate_build_time(
    base_days: int,
    base_hours: int,
    base_minutes: int,
    base_seconds: int,
    my_speed_percent: float,
    mayor_percent: float
):
    # 1. 기본 건설 시간을 초로 변환
    base_seconds_total = (
        base_days * 86400 +
        base_hours * 3600 +
        base_minutes * 60 +
        base_seconds
    )

    # 2. 총 건설 가속 계산
    total_speed = (my_speed_percent + mayor_percent) / 100
    final_seconds = base_seconds_total / (1 + total_speed)

    # 3. timedelta 변환
    final_duration = timedelta(seconds=int(final_seconds))

    # 4. 완료 예정 시각
    finish_time = datetime.now() + final_duration

    return final_duration, finish_time


if __name__ == "__main__":
    # 🔹 예시 입력
    base_days = 101
    base_hours = 14
    base_minutes = 30
    base_seconds = 0

    my_speed = 82.5      # 나의 건설 속도 %
    mayor_speed = 50.0   # 건설 장관 %

    duration, finish = calculate_build_time(
        base_days,
        base_hours,
        base_minutes,
        base_seconds,
        my_speed,
        mayor_speed
    )

    # 🔹 결과 출력
    days = duration.days
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    print(f"[최종 건설 시간] {days}D {hours:02}:{minutes:02}:{seconds:02}")
    print(f"[완료 예정 시각] {finish.strftime('%Y-%m-%d %H:%M:%S')}")
