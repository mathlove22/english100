import streamlit as st
import random
import json

# 1. JSON 파일에서 문장 데이터를 불러오는 함수
def load_sentences_from_json(file_path):
    with open(file_path, 'r') as f:
        sentences = json.load(f)
    return sentences

sentences = load_sentences_from_json('sentence03.json')

# 2. 문장에서 랜덤으로 단어를 빈칸으로 만드는 함수
def create_blank_sentence(sentence):
    words = sentence.split()
    random_index = random.randint(0, len(words) - 1)
    correct_answer = words[random_index]
    blank_length = len(correct_answer)
    words[random_index] = "□" * blank_length
    blank_sentence = " ".join(words)
    return blank_sentence, correct_answer

# 3. 세션 상태 초기화
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

# 4. 새로운 문제를 로드하는 함수
def load_new_question():
    sentence = random.choice(sentences)
    blank_sentence, correct_answer = create_blank_sentence(sentence["english"])
    st.session_state.current_sentence = sentence
    st.session_state.blank_sentence = blank_sentence
    st.session_state.correct_answer = correct_answer
    st.session_state.input_key += 1  # 입력 필드의 키를 변경

# 5. 웹앱 인터페이스 만들기
def main():
    initialize_session_state()

    st.title("영어 학습: 빈칸 채우기")
    st.write("문장의 빈칸을 채워보세요.")

    # 새로운 문제를 처음 로드하거나 사용자가 '다음 문제' 버튼을 클릭하면 새로운 문제 생성
    if st.session_state.current_sentence is None or st.button("다음 문제"):
        load_new_question()

    # 한글 번역 제공
    st.write(f"번역: {st.session_state.current_sentence['korean']}")

    # 빈칸이 있는 문장 표시
    st.write(f"문장: {st.session_state.blank_sentence}")

    # 사용자 입력 받기 (동적 키 사용)
    user_input = st.text_input("정답 입력", key=f"user_input_{st.session_state.input_key}")

    # 제출 버튼
    if st.button("제출"):
        st.session_state.total_attempts += 1
        if user_input.strip().lower() == st.session_state.correct_answer.strip().lower():
            st.session_state.correct_attempts += 1
            st.success("정답입니다!")
        else:
            st.error(f"오답입니다. 정답은 '{st.session_state.correct_answer}' 입니다.")

    # 점수 표시
    st.write(f"점수: {st.session_state.correct_attempts}/{st.session_state.total_attempts}")

    # 퍼센트 점수 표시
    if st.session_state.total_attempts > 0:
        score_percentage = (st.session_state.correct_attempts / st.session_state.total_attempts) * 100
        st.write(f"퍼센트 점수: {score_percentage:.2f}점")

if __name__ == "__main__":
    main()
