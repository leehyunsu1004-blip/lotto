import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(
    page_title="로또 번호 생성기",
    page_icon="🎱",
    layout="centered"
)

# 커스텀 스타일 (로또 공 및 레이아웃 디자인)
st.markdown("""
<style>
    .lotto-row {
        display: flex;
        align-items: center;
        gap: 12px;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 12px;
    }
    .set-label {
        font-weight: 700;
        font-size: 16px;
        color: #475569;
        min-width: 55px;
    }
    .balls-container {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    .lotto-ball {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 16px;
        color: white;
        box-shadow: inset -2px -2px 5px rgba(0, 0, 0, 0.3), 1px 2px 4px rgba(0, 0, 0, 0.15);
    }
    /* 실제 동행복권 공 색상 규격 */
    .ball-yellow { background-color: #f59e0b; } /* 1 ~ 10 */
    .ball-blue   { background-color: #3b82f6; } /* 11 ~ 20 */
    .ball-red    { background-color: #ef4444; } /* 21 ~ 30 */
    .ball-gray   { background-color: #6b7280; } /* 31 ~ 40 */
    .ball-green  { background-color: #10b981; } /* 41 ~ 45 */
</style>
""", unsafe_allow_html=True)


# 1~45 범위에 따른 로또 공 색상 클래스 매핑 함수
def get_ball_class(num: int) -> str:
    if num <= 10:
        return "ball-yellow"
    elif num <= 20:
        return "ball-blue"
    elif num <= 30:
        return "ball-red"
    elif num <= 40:
        return "ball-gray"
    else:
        return "ball-green"


# 세션 상태 초기화 (누적 게임 리스트 저장)
if "lotto_history" not in st.session_state:
    st.session_state.lotto_history = []

# 제목 및 안내
st.title("🎱 로또 6/45 번호 생성기")
st.write("버튼을 누르면 1~45 사이의 중복 없는 6개 번호가 생성되며, 최대 5세트까지 저장됩니다.")

# 버튼 영역 (생성 및 초기화)
col1, col2 = st.columns([3, 1])

with col1:
    is_max = len(st.session_state.lotto_history) >= 5
    if st.button("🎲 로또번호 생성", use_container_width=True, disabled=is_max, type="primary"):
        # 1~45 중 중복 없이 6개 추출 후 오름차순 정렬
        new_set = sorted(random.sample(range(1, 46), 6))
        st.session_state.lotto_history.append(new_set)
        st.rerun()

with col2:
    if st.button("🔄 초기화", use_container_width=True):
        st.session_state.lotto_history = []
        st.rerun()

# 5세트 도달 시 알림
if is_max:
    st.info("최대 5게임이 모두 생성되었습니다. 다시 시작하려면 '초기화'를 눌러주세요.")

st.markdown("---")

# 번호 세트 출력 영역
labels = ["A", "B", "C", "D", "E"]

if not st.session_state.lotto_history:
    st.caption("아직 생성된 로또 번호가 없습니다. [로또번호 생성] 버튼을 눌러보세요.")
else:
    for idx, numbers in enumerate(st.session_state.lotto_history):
        label_text = f"{labels[idx]} 세트"

        # 공 HTML 태그 조립
        balls_html = "".join([
            f'<div class="lotto-ball {get_ball_class(num)}">{num}</div>'
            for num in numbers
        ])

        row_html = f"""
        <div class="lotto-row">
            <span class="set-label">{label_text}</span>
            <div class="balls-container">
                {balls_html}
            </div>
        </div>
        """
        st.markdown(row_html, unsafe_allow_html=True)

