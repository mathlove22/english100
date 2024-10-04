import streamlit as st
import random
import pandas as pd
import time
import json

# JSON 파일에서 문장 데이터를 불러오는 함수
def load_sentences_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()  # 파일에서 읽어온 데이터를 공백 제거
            if content:  # 내용이 있을 경우
                sentences = json.loads(content)
            else:
                st.error(f"{file_path} 파일이 비어 있습니다.")
                sentences = []
        return sentences
    except FileNotFoundError:
        st.error(f"{file_path} 파일을 찾을 수 없습니다.")
        return []
    except json.JSONDecodeError:
        st.error(f"{file_path} 파일의 JSON 형식이 잘못되었습니다.")
        return []

# JSON 파일에 기록을 저장하는 함수
def save_results_to_json(filename, results):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []  # 파일이 없거나 JSON 형식이 잘못된 경우 빈 리스트로 초기화
    
    data.append(results)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

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

# 문장에서 랜덤으로 단어를 빈칸으로 만드는 함수
def create_blank_sentence(sentence):
    words = sentence.split()
    random_index = random.randint(0, len(words) - 1)
    correct_answer = words[random_index]
    words[random_index] = "□" * len(correct_answer)
    blank_sentence = " ".join(words)
    return blank_sentence, correct_answer

# 새로운 문제 로드
def load_new_question(sentences):
    if not sentences:
        st.error("선택한 범위에 해당하는 문장이 없습니다. 범위를 다시 선택하세요.")
        return
    sentence = random.choice(sentences)
    blank_sentence, correct_answer = create_blank_sentence(sentence["english"])
    st.session_state.current_sentence = sentence
    st.session_state.blank_sentence = blank_sentence
    st.session_state.correct_answer = correct_answer
    st.session_state.input_key += 1

# 메인 함수
def main():
    st.title("영어 학습: 빈칸 채우기")
    
    # 문장 데이터를 불러오기
    sentences = load_sentences_from_json('sentence03.json')
    
    # 세션 상태 초기화
    initialize_session_state()

    # 닉네임 입력
    nickname = st.text_input("닉네임 입력", key="nickname")
    
    # 문장 범위 선택
    sentence_range = st.slider("문장 범위를 선택하세요", 1, 100, (1, 10))
    filtered_sentences = [s for s in sentences if sentence_range[0] <= s["number"] <= sentence_range[1]]
    
    # 목표 설정
    goal_num_questions = st.number_input("맞추고 싶은 문제 수", min_value=1, value=10)
    goal_score = st.number_input("목표 점수", min_value=1, value=70)

    # 타이머 시작
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()
    
    # 새로운 문제를 로드
    if st.session_state.current_sentence is None or st.button("다음 문제"):
        load_new_question(filtered_sentences)

    # 문제와 번역 표시
    st.write(f"번역: {st.session_state.current_sentence['korean']}")
    st.write(f"문장: {st.session_state.blank_sentence}")
    
    # 사용자 입력
    user_input = st.text_input("정답 입력", key=f"user_input_{st.session_state.input_key}")
    
    # 제출 버튼
    if st.button("제출"):
        st.session_state.total_attempts += 1
        if user_input.strip().lower() == st.session_state.correct_answer.strip().lower():
            st.session_state.correct_attempts += 1
            st.success("정답입니다!")
        else:
            st.error(f"오답입니다. 정답은 '{st.session_state.correct_answer}'입니다.")
    
    # 점수 표시
    st.write(f"점수: {st.session_state.correct_attempts}/{st.session_state.total_attempts}")
    
    # 퍼센트 점수 표시
    if st.session_state.total_attempts > 0:
        score_percentage = (st.session_state.correct_attempts / st.session_state.total_attempts) * 100
        st.write(f"퍼센트 점수: {score_percentage:.2f}점")
    
    # 목표 달성 여부 확인
    if st.session_state.correct_attempts >= goal_num_questions and score_percentage >= goal_score:
        st.success("목표 달성!")
        st.session_state.time_spent = time.time() - st.session_state.start_time
        st.write(f"걸린 시간: {st.session_state.time_spent:.2f}초")
        
        # 결과를 JSON 파일에 저장
        result = {
            "nickname": nickname,
            "score": f"{st.session_state.correct_attempts}/{st.session_state.total_attempts}",
            "percentage": score_percentage,
            "time_spent": st.session_state.time_spent
        }
        save_results_to_json("results.json", result)
        
        st.stop()

if __name__ == "__main__":
    main()
