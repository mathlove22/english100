import streamlit as st
import random

# 1. 영어 문장 데이터와 한글 번역
sentences = [
    {"number": 1, "english": "I like pizza.", "korean": "나는 피자를 좋아해."},
    {"number": 2, "english": "She has a blue bag.", "korean": "그녀는 파란 가방을 가지고 있어."},
    {"number": 3, "english": "They are my friends.", "korean": "그들은 내 친구들이야."},
    {"number": 4, "english": "Can you help me?", "korean": "나를 도와줄 수 있니?"},
    {"number": 5, "english": "He goes to school every day.", "korean": "그는 매일 학교에 가."},
    {"number": 6, "english": "I am reading a book.", "korean": "나는 책을 읽고 있어."},
    {"number": 7, "english": "The sun is shining.", "korean": "태양이 빛나고 있어."},
    {"number": 8, "english": "We live in a big house.", "korean": "우리는 큰 집에 살아."},
    {"number": 9, "english": "It is a beautiful day.", "korean": "오늘은 아름다운 날이야."},
    {"number": 10, "english": "What is your name?", "korean": "너의 이름은 뭐니?"},
    {"number": 11, "english": "This is my favorite color.", "korean": "이것이 내가 가장 좋아하는 색이야."},
    {"number": 12, "english": "I can run fast.", "korean": "나는 빨리 달릴 수 있어."},
    {"number": 13, "english": "She is my sister.", "korean": "그녀는 내 여동생이야."},
    {"number": 14, "english": "He plays the piano.", "korean": "그는 피아노를 연주해."},
    {"number": 15, "english": "The cat is under the table.", "korean": "고양이가 테이블 아래에 있어."},
    {"number": 16, "english": "I like to play soccer.", "korean": "나는 축구하는 것을 좋아해."},
    {"number": 17, "english": "She has a pet dog.", "korean": "그녀는 애완견을 가지고 있어."},
    {"number": 18, "english": "My brother is tall.", "korean": "내 남동생은 키가 커."},
    {"number": 19, "english": "What time is it?", "korean": "몇 시야?"},
    {"number": 20, "english": "The sky is blue.", "korean": "하늘이 파랗다."},
    {"number": 21, "english": "Do you want some juice?", "korean": "주스 좀 마실래?"},
    {"number": 22, "english": "I have two pencils.", "korean": "나는 연필 두 자루를 가지고 있어."},
    {"number": 23, "english": "He is a good student.", "korean": "그는 좋은 학생이야."},
    {"number": 24, "english": "Where is the library?", "korean": "도서관이 어디에 있니?"},
    {"number": 25, "english": "Can I sit here?", "korean": "여기 앉아도 돼?"},
    {"number": 26, "english": "She is watching TV.", "korean": "그녀는 TV를 보고 있어."},
    {"number": 27, "english": "We are eating lunch.", "korean": "우리는 점심을 먹고 있어."},
    {"number": 28, "english": "It is raining outside.", "korean": "밖에 비가 오고 있어."},
    {"number": 29, "english": "I need a new book.", "korean": "나는 새 책이 필요해."},
    {"number": 30, "english": "She is riding a bike.", "korean": "그녀는 자전거를 타고 있어."},
    {"number": 31, "english": "What is your favorite food?", "korean": "네가 가장 좋아하는 음식은 뭐야?"},
    {"number": 32, "english": "I can swim very well.", "korean": "나는 수영을 아주 잘해."},
    {"number": 33, "english": "They are playing in the park.", "korean": "그들은 공원에서 놀고 있어."},
    {"number": 34, "english": "The dog is barking loudly.", "korean": "개가 크게 짖고 있어."},
    {"number": 35, "english": "I want to go home.", "korean": "나는 집에 가고 싶어."},
    {"number": 36, "english": "He is drawing a picture.", "korean": "그는 그림을 그리고 있어."},
    {"number": 37, "english": "The flowers are pretty.", "korean": "꽃들이 예뻐."},
    {"number": 38, "english": "I like to read stories.", "korean": "나는 이야기를 읽는 것을 좋아해."},
    {"number": 39, "english": "She is wearing a red dress.", "korean": "그녀는 빨간 드레스를 입고 있어."},
    {"number": 40, "english": "He likes to play video games.", "korean": "그는 비디오 게임을 하는 것을 좋아해."},
    {"number": 41, "english": "I have a big family.", "korean": "나는 대가족이야."},
    {"number": 42, "english": "The bird is flying in the sky.", "korean": "새가 하늘을 날고 있어."},
    {"number": 43, "english": "What do you want to eat?", "korean": "뭐 먹고 싶어?"},
    {"number": 44, "english": "She is good at math.", "korean": "그녀는 수학을 잘해."},
    {"number": 45, "english": "He is my best friend.", "korean": "그는 내 가장 친한 친구야."},
    {"number": 46, "english": "The cake is delicious.", "korean": "케이크가 맛있어."},
    {"number": 47, "english": "I can see the stars.", "korean": "나는 별들을 볼 수 있어."},
    {"number": 48, "english": "We are going to the beach.", "korean": "우리는 해변에 가고 있어."},
    {"number": 49, "english": "The baby is sleeping.", "korean": "아기가 자고 있어."},
    {"number": 50, "english": "Do you like ice cream?", "korean": "너는 아이스크림을 좋아하니?"},
    {"number": 51, "english": "She is playing the guitar.", "korean": "그녀는 기타를 치고 있어."},
    {"number": 52, "english": "The bus is coming soon.", "korean": "버스가 곧 올 거야."},
    {"number": 53, "english": "I have a lot of homework.", "korean": "나는 숙제가 많아."},
    {"number": 54, "english": "They are talking to each other.", "korean": "그들은 서로 이야기하고 있어."},
    {"number": 55, "english": "The phone is ringing.", "korean": "전화가 울리고 있어."},
    {"number": 56, "english": "I am going to the store.", "korean": "나는 상점에 가고 있어."},
    {"number": 57, "english": "The movie is starting now.", "korean": "영화가 지금 시작하고 있어."},
    {"number": 58, "english": "She is dancing in the room.", "korean": "그녀는 방에서 춤추고 있어."},
    {"number": 59, "english": "He is building a sandcastle.", "korean": "그는 모래성을 만들고 있어."},
    {"number": 60, "english": "The fish is swimming in the water.", "korean": "물고기가 물속에서 수영하고 있어."},
    {"number": 61, "english": "I can hear the birds singing.", "korean": "나는 새들이 노래하는 소리를 들을 수 있어."},
    {"number": 62, "english": "They are waiting for the train.", "korean": "그들은 기차를 기다리고 있어."},
    {"number": 63, "english": "My mom is cooking dinner.", "korean": "엄마가 저녁을 요리하고 계셔."},
    {"number": 64, "english": "The car is very fast.", "korean": "그 차는 매우 빨라."},
    {"number": 65, "english": "I need to study English.", "korean": "나는 영어를 공부해야 해."},
    {"number": 66, "english": "The trees are green.", "korean": "나무들이 초록색이야."},
    {"number": 67, "english": "He is reading a comic book.", "korean": "그는 만화책을 읽고 있어."},
    {"number": 68, "english": "I love my family.", "korean": "나는 내 가족을 사랑해."},
    {"number": 69, "english": "She is learning how to swim.", "korean": "그녀는 수영하는 법을 배우고 있어."},
    {"number": 70, "english": "They are cleaning the room.", "korean": "그들은 방을 청소하고 있어."},
    {"number": 71, "english": "The sun is setting.", "korean": "태양이 지고 있어."},
    {"number": 72, "english": "The water is cold.", "korean": "물이 차가워."},
    {"number": 73, "english": "I am happy today.", "korean": "나는 오늘 행복해."},
    {"number": 74, "english": "She is opening the door.", "korean": "그녀는 문을 열고 있어."},
    {"number": 75, "english": "He is eating a sandwich.", "korean": "그는 샌드위치를 먹고 있어."},
    {"number": 76, "english": "I have a small toy.", "korean": "나는 작은 장난감을 가지고 있어."},
    {"number": 77, "english": "The teacher is very kind.", "korean": "선생님은 매우 친절하셔."},
    {"number": 78, "english": "The computer is new.", "korean": "컴퓨터가 새 거야."},
    {"number": 79, "english": "I am writing a letter.", "korean": "나는 편지를 쓰고 있어."},
    {"number": 80, "english": "She is going to bed.", "korean": "그녀는 자러 가고 있어."},
    {"number": 81, "english": "He is brushing his teeth.", "korean": "그는 이를 닦고 있어."},
    {"number": 82, "english": "The dog is very cute.", "korean": "그 개는 매우 귀여워."},
    {"number": 83, "english": "We are playing a game.", "korean": "우리는 게임을 하고 있어."},
    {"number": 84, "english": "She is reading a storybook.", "korean": "그녀는 동화책을 읽고 있어."},
    {"number": 85, "english": "I am listening to music.", "korean": "나는 음악을 듣고 있어."},
    {"number": 86, "english": "The chair is broken.", "korean": "의자가 고장났어."},
    {"number": 87, "english": "I can see a rainbow.", "korean": "나는 무지개를 볼 수 있어."},
    {"number": 88, "english": "He is doing his homework.", "korean": "그는 숙제를 하고 있어."},
    {"number": 89, "english": "The clock is ticking.", "korean": "시계가 똑딱거리고 있어."},
    {"number": 90, "english": "She is eating an apple.", "korean": "그녀는 사과를 먹고 있어."},
    {"number": 91, "english": "I am packing my bag.", "korean": "나는 가방을 싸고 있어."},
    {"number": 92, "english": "They are watching a movie.", "korean": "그들은 영화를 보고 있어."},
    {"number": 93, "english": "The tree is very tall.", "korean": "그 나무는 매우 커."},
    {"number": 94, "english": "He is fixing the bike.", "korean": "그는 자전거를 고치고 있어."},
    {"number": 95, "english": "I want to drink water.", "korean": "나는 물을 마시고 싶어."},
    {"number": 96, "english": "The room is clean now.", "korean": "방이 이제 깨끗해."},
    {"number": 97, "english": "She is writing in her notebook.", "korean": "그녀는 노트북에 글을 쓰고 있어."},
    {"number": 98, "english": "He is helping his friend.", "korean": "그는 친구를 돕고 있어."},
    {"number": 99, "english": "The balloon is flying away.", "korean": "풍선이 날아가고 있어."},
    {"number": 100, "english": "I can jump high.", "korean": "나는 높이 뛸 수 있어."},
]

# 2. 문장에서 랜덤으로 단어를 빈칸으로 만드는 함수
def create_blank_sentence(sentence):
    words = sentence.split()
    random_index = random.randint(0, len(words) - 1)
    correct_answer = words[random_index]
    words[random_index] = "_____"
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
    if "new_question" not in st.session_state:
        st.session_state.new_question = False
    if "input_key" not in st.session_state:
        st.session_state.input_key = 0

# 4. 새로운 문제를 로드하는 함수
def load_new_question():
    sentence = random.choice(sentences)
    blank_sentence, correct_answer = create_blank_sentence(sentence["english"])
    st.session_state.current_sentence = sentence
    st.session_state.blank_sentence = blank_sentence
    st.session_state.correct_answer = correct_answer
    st.session_state.new_question = True
    st.session_state.input_key += 1  # 입력 필드의 키를 변경

# 5. 웹앱 인터페이스 만들기
def main():
    initialize_session_state()

    st.title("영어 학습: 빈칸 채우기")
    st.write("문장의 빈칸을 채워보세요.")

    # 새로운 문제를 처음 로드하거나 사용자가 '다음 문제' 버튼을 클릭하면 새로운 문제 생성
    if st.session_state.current_sentence is None or st.session_state.new_question:
        load_new_question()
        st.session_state.new_question = False

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

    # '다음 문제' 버튼
    if st.button("다음 문제"):
        load_new_question()
        st.experimental_rerun()

if __name__ == "__main__":
    main()