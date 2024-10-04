import streamlit as st
import random
import json
import time

# ... (이전 함수들은 그대로 유지) ...

# 메인 함수
def main():
    st.title("영어 학습: 빈칸 채우기")
    
    # 세션 상태 초기화
    initialize_session_state()

    # 화면에 따라 다르게 처리
    if st.session_state.screen == "initial":
        # 초기 화면
        st.write("이름, 문장 범위, 문제 수, 목표 점수를 입력하세요.")
        nickname = st.text_input("닉네임 입력", key="nickname_input")
        
        # 문장 범위 선택
        sentence_range = st.slider("문장 범위를 선택하세요", 1, 100, (1, 10))
        goal_num_questions = st.number_input("맞추고 싶은 문제 수", min_value=1, value=10)
        goal_score = st.number_input("목표 점수", min_value=1, value=70)
        
        if st.button("시작하기"):
            # 유효성 검사 추가
            if not nickname.strip():
                st.error("닉네임을 입력하세요.")
            else:
                # 모든 정보가 입력되면 다음 화면으로 넘어감
                st.session_state.screen = "question"
                st.session_state.nickname = nickname
                st.session_state.sentence_range = sentence_range  # 범위 저장
                st.session_state.goal_num_questions = goal_num_questions
                st.session_state.goal_score = goal_score
                st.session_state.start_time = time.time()  # Start timer when the game begins
                st.experimental_rerun()  # 화면을 즉시 다시 로드

    elif st.session_state.screen == "question":
        # 문장 데이터를 불러오기
        sentences = load_sentences_from_json('sentence03.json')
        
        # 선택한 범위에 따라 문장 필터링
        filtered_sentences = [s for s in sentences if st.session_state.sentence_range[0] <= s["number"] <= st.session_state.sentence_range[1]]
        
        # 새로운 문제를 로드
        if st.session_state.current_sentence is None or st.button("다음 문제"):
            if len(filtered_sentences) > 0:
                load_new_question(filtered_sentences)
            else:
                st.error("선택한 범위에 문장이 없습니다.")

        # 문제와 번역 표시
        st.write(f"번역: {st.session_state.current_sentence['korean']}")
        st.write(f"문장: {st.session_state.blank_sentence}")

        # 사용자 입력
        user_input = st.text_input("정답 입력", key=f"user_input_{st.session_state.input_key}")

        # 제출 버튼 (입력이 있을 때만 활성화)
        if st.button("제출", disabled=not user_input.strip()):
            st.session_state.total_attempts += 1
            if user_input.strip().lower() == st.session_state.correct_answer.strip().lower():
                st.session_state.correct_attempts += 1
                st.success("정답입니다!")
            else:
                st.error(f"오답입니다. 정답은 '{st.session_state.correct_answer}'입니다.")

        # 점수 표시
        st.write(f"점수: {st.session_state.correct_attempts}/{st.session_state.total_attempts}")

        # 목표 달성 여부 확인
        if st.session_state.total_attempts >= st.session_state.goal_num_questions:
            if st.session_state.correct_attempts >= st.session_state.goal_score:
                st.session_state.time_spent = time.time() - st.session_state.start_time
                st.session_state.screen = "result"
                st.experimental_rerun()  # 결과 화면으로 즉시 전환

    elif st.session_state.screen == "result":
        # ... (결과 화면 코드는 그대로 유지) ...

if __name__ == "__main__":
    main()
