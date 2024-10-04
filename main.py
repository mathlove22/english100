import streamlit as st
import random
import json
import time

# JSON 파일에서 문장 데이터를 불러오는 함수
def load_sentences_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sentences = json.load(f)
        return sentences
    except FileNotFoundError:
        st.error(f"{file_path} 파일을 찾을 수 없습니다.")
        return []

# JSON 파일에 기록을 저장하는 함수
def save_results_to_json(filename, results):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    
    data.append(results)
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# 세션 상태 초기화 함수
def initialize_session_state():
    if "current_sentence" not in st.session_state:
        st.session_state.current_sentence = None
    if "blank_sentence" not in st.session_state:
        st.session_state.blank_sentence = None
    if "correct_answer" not in st.session_state:
        st.session_state.correct_answer = None
    if "total_attempts" not in st.session_state:
        st.session_state.total_attempts = 0
    if "correct_attempts" not in st.session_state:
        st.session_state.correct_attempts = 0
    if "input_key" not in st.session_state:
        st.session_state.input_key = 0
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "time_spent" not in st.session_state:
        st.session_state.time_spent = 0
    if "screen" not in st.session_state:
        st.session_state.screen = "initial"  # Start on the initial screen
    if "nickname" not in st.session_state:
        st.session_state.nickname = ""  # Initialize nickname
    if "sentence_range" not in st.session_state:
        st.session_state.sentence_range = (1, 10)  # 기본 문장 범위 초기화

# 문장에서 랜덤으로 단어를 빈칸으로 만드는 함수
def create_blank_sentence(sentence):
    words = sentence.split()
    random_index = random.randint(0, len(words) - 1)
    correct_answer = words[random_index]
    words[random_index] = "□" * len(correct_answer)
    blank_sentence = " ".join(words)
    return blank_sentence, correct_answer

# 새로운 문제 로드
def load_new_question(filtered_sentences):
    sentence = random.choice(filtered_sentences)
    blank_sentence, correct_answer = create_blank_sentence(sentence["english"])
    st.session_state.current_sentence = sentence
    st.session_state.blank_sentence = blank_sentence
    st.session_state.correct_answer = correct_answer
    st.session_state.input_key += 1

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
        goal_num_questions = st.number_input("풀고 싶은 문제 수", min_value=1, value=10)
        goal_score = st.number_input("목표 정답 수", min_value=1, value=7)
        
        if st.button("시작하기"):
            # 유효성 검사 추가
            if not nickname.strip():
                st.error("닉네임을 입력하세요.")
            elif goal_score > goal_num_questions:
                st.error("목표 정답 수는 문제 수를 초과할 수 없습니다.")
            else:
                # 모든 정보가 입력되면 다음 화면으로 넘어감
                st.session_state.screen = "question"
                st.session_state.nickname = nickname
                st.session_state.sentence_range = sentence_range  # 범위 저장
                st.session_state.goal_num_questions = goal_num_questions
                st.session_state.goal_score = goal_score
                st.session_state.start_time = time.time()  # Start timer when the game begins
                st.rerun()  # 화면을 즉시 다시 로드

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

            # 목표 달성 여부 확인
            if st.session_state.total_attempts >= st.session_state.goal_num_questions:
                st.session_state.time_spent = time.time() - st.session_state.start_time
                st.session_state.screen = "result"
                st.rerun()  # 결과 화면으로 즉시 전환

        # 점수 표시
        st.write(f"점수: {st.session_state.correct_attempts}/{st.session_state.total_attempts}")
        st.write(f"목표: {st.session_state.goal_num_questions}문제 중 {st.session_state.goal_score}개 정답")

    elif st.session_state.screen == "result":  # 여기가 수정된 부분
        # 결과 화면
        st.balloons()  # 축하 효과
        st.title("🎉 퀴즈 결과 🎉")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("닉네임", st.session_state.nickname)
            st.metric("총 문제 수", st.session_state.goal_num_questions)
            st.metric("목표 정답 수", st.session_state.goal_score)
        
        with col2:
            correct_ratio = st.session_state.correct_attempts / st.session_state.total_attempts
            percentage_score = correct_ratio * 100
            st.metric("정답률", f"{percentage_score:.1f}%")
            st.metric("걸린 시간", f"{st.session_state.time_spent:.1f}초")
            goal_achieved = st.session_state.correct_attempts >= st.session_state.goal_score
            st.metric("목표 달성", "성공 🏆" if goal_achieved else "실패 😢")

        st.progress(correct_ratio)
        
        st.write("---")
        st.subheader("상세 결과")
        st.write(f"문장 범위: {st.session_state.sentence_range[0]} ~ {st.session_state.sentence_range[1]}")
        st.write(f"맞춘 문제 수: {st.session_state.correct_attempts} / {st.session_state.total_attempts}")
        
        # 백분위 점수 계산 (간단한 방식으로 구현)
        percentile = min(100, max(0, int((percentage_score - 50) * 2)))
        st.write(f"백분위 점수: {percentile}%")
        st.info(f"당신의 점수는 상위 {100-percentile}%에 해당합니다.")
        
        # 결과를 JSON 파일에 저장
        result = {
            "nickname": st.session_state.nickname,
            "score": f"{st.session_state.correct_attempts}/{st.session_state.total_attempts}",
            "goal_achieved": goal_achieved,
            "percentage": percentage_score,
            "percentile": percentile,
            "time_spent": st.session_state.time_spent,
            "sentence_range": st.session_state.sentence_range,
            "num_questions": st.session_state.goal_num_questions,
            "goal_score": st.session_state.goal_score
        }
        save_results_to_json("results.json", result)
        
        if st.button("다시 시작", key="restart_button"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()
