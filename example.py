import pandas as pd
import random
import streamlit as st

# 원본 데이터프레임 생성
pose = pd.read_csv('pose.csv', encoding='ms949')
practice = pd.read_csv('practice.csv', encoding='ms949')
dictation = pd.read_csv('dictation_3.csv', encoding='ms949')

# 랜덤한 결과 출력하는 함수
def show_random_results():

    # 가슴, 팔운동 중에서 랜덤 질문 1개 선택
    random_practice_1 = random.sample(practice[practice['gubun'].isin(['가슴_팔'])]['name'].tolist(), 1)

    # 등, 어깨운동 중에서 랜덤 질문 1개 선택
    random_practice_2 = random.sample(practice[practice['gubun'].isin(['등_어깨'])]['name'].tolist(), 1)

    # 하체 운동 중에서 랜덤 질문 1개 선택
    random_practice_3 = random.sample(practice[practice['gubun'].isin(['하체'])]['name'].tolist(), 1)

    # 복근 운동 중에서 랜덤 질문 1개 선택
    random_practice_4 = random.sample(practice[practice['gubun'].isin(['복근'])]['name'].tolist(), 1)

    random_pose = random.sample(pose['pose'].tolist(), 1)

    # 규정 중에서 랜덤 질문 2개 선택
    #random_dictation_1 = random.sample(dictation[dictation['gubun'].isin(['규정'])]['question'].tolist(), 2)

    # 지도방법 중에서 랜덤 질문 2개 선택
    #random_dictation_2 = random.sample(dictation[dictation['gubun'].isin(['지도방법'])]['question'].tolist(), 2)

    
    # 협회최신규정, 종목소개 중에서 랜덤 질문 1개 선택
    random_dictation_1 = random.sample(dictation[dictation['gubun_1'].isin(['협회최신규정', '종목소개'])]['question'].tolist(), 1)

    # 스포츠 인권, 생활체육 개요 중에서 랜덤 질문 1개 선택
    random_dictation_2 = random.sample(dictation[dictation['gubun_1'].isin(['스포츠 인권', '생활체육 개요'])]['question'].tolist(), 1)

    # 웨이트트레이닝, 규정포즈 중에서 랜덤 질문 1개 선택
    random_dictation_3 = random.sample(dictation[dictation['gubun_1'].isin(['웨이트트레이닝', '규정포즈'])]['question'].tolist(), 1)

    # 과학적 지도방법, 응급처치 중에서 랜덤 질문 1개 선택
    random_dictation_4 = random.sample(dictation[dictation['gubun_1'].isin(['과학적 지도방법', '응급처치'])]['question'].tolist(), 1)

    # 새로운 데이터프레임 생성
    selected_practice = practice[practice['name'].isin(random_practice_1 + random_practice_2 + random_practice_3 + random_practice_4)]
    selected_pose = pose[pose['pose'].isin(random_pose)]
    #selected_dictation = dictation[dictation['question'].isin(random_dictation_1 + random_dictation_2)]
    selected_dictation = dictation[dictation['question'].isin(random_dictation_1 + random_dictation_2 + random_dictation_3 + random_dictation_4)]

    # 결과 출력
    st.write("1. 실기 자세 문제:")
    practice_results = [f"{i+1}. {name}" for i, name in enumerate(selected_practice['name'])]
    st.write("\n".join(practice_results))

    st.write("2. 실기 포즈 문제:")
    st.write(selected_pose.pose.unique()[0])

    st.write("3. 구술 문제:")
    dictation_results = [f"{i+1}. {question}" for i, question in enumerate(selected_dictation['question'])]
    st.write("\n".join(dictation_results))

    st.write("\n 실기 포즈 이름:\n")
    pose_name = [f"{i+1}. {name}" for i, name in enumerate(selected_pose['name'])]
    st.write("\n".join(pose_name))

    st.write("\n 구술 문제 정답:\n")
    dictation_answer = [f"{i+1}. {answer}" for i, answer in enumerate(selected_dictation['answer'])]
    st.write("\n".join(dictation_answer))


# Streamlit 애플리케이션 구성
st.title("생체사 2급 실기/구슬 모의 평가")
start_button = st.button("시작")

# Start 버튼이 클릭되면 결과 출력
if start_button:
    show_random_results()
