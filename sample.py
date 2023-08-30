import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import openai
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI

def predict_strengths(path, model_path):
    # Load the data
    data = pd.read_csv(path + 'recruiting_raw.csv', encoding='ms949')

    # Prompt the user to enter a person's name
    person_name = st.text_input("이름을 입력하세요: ")

    if person_name:
        # Find the row corresponding to the person's name
        person_row = data[data['name'].str.contains(person_name, na=False)]

        if not person_row.empty:
            # Extract the person's values
            selected_person_values = person_row.iloc[:, 6:].values.flatten().tolist()[:43]

            # Load the strength models
            strength_1_model = joblib.load(model_path + 'strength_1_model.pkl')
            strength_2_model = joblib.load(model_path + 'strength_2_model.pkl')
            strength_3_model = joblib.load(model_path + 'strength_3_model.pkl')
            strength_4_model = joblib.load(model_path + 'strength_4_model.pkl')

            # Define strength dictionaries
            strength_1 = {1: "책임", 2: "집중", 3: "체계", 4: "심사숙고", 5: "공정성", 6: "신념", 7: "정리", 8: "성취"}
            strength_2 = {1: "커뮤니케이션", 2: "승부", 3: "주도력", 4: "행동", 5: "사교성", 6: "자기확신", 7: "존재감", 8: "최상화"}
            strength_3 = {1: "절친", 2: "개발", 3: "연결성", 4: "적용", 5: "화합", 6: "개별화", 7: "포용", 8: "공감"}
            strength_4 = {1: "분석", 2: "회고", 3: "미래지향", 4: "발상", 5: "수집", 6: "지적사고", 7: "배움", 8: "전략"}

            # Make predictions
            pred_strength_1 = strength_1_model.predict([selected_person_values])[0]
            pred_strength_2 = strength_2_model.predict([selected_person_values])[0]
            pred_strength_3 = strength_3_model.predict([selected_person_values])[0]
            pred_strength_4 = strength_4_model.predict([selected_person_values])[0]

            # Retrieve strength descriptions
            desc_strength_1 = strength_1[pred_strength_1]
            desc_strength_2 = strength_2[pred_strength_2]
            desc_strength_3 = strength_3[pred_strength_3]
            desc_strength_4 = strength_4[pred_strength_4]

            # Output the result
            result = f"{person_name}의 강점은 {desc_strength_1}, {desc_strength_2}, {desc_strength_3}, {desc_strength_4}입니다."
        else:
            result = "해당 이름의 정보를 찾을 수 없습니다."
    else:
        result = "이름을 입력하세요."

    return result


def ask_question(question):
    openai.api_key = ""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    )
    answer = response['choices'][0]['message']['content']
    return answer

path = "C:/Users/endlo/Desktop/etc/Lpoint/"
model_path = "C:/Users/endlo/Desktop/etc/Lpoint/model/"
api_key = ""

## ML 예측 결과 ##
st.title("AI 강점 예측 시스템")
result =predict_strengths(path, model_path)
st.write(result)

## Pandasai output ##
llm = OpenAI(api_key)
pandas_ai = PandasAI(llm, conversational=False)

data = pd.read_csv(path+'recruiting_raw.csv', encoding='ms949')
data_prep = pandas_ai.run(
data,
"성별,나이별로 사람수가 얼마나 되는지 보여줘"
)
st.dataframe(data_prep)

# Plot histogram by gender and age using different colors for each bar
fig, ax = plt.subplots()
data_prep.plot(kind='bar', ax=ax)

# Add title and labels to the plot
ax.set_title("Histogram of People by Gender and Age")
ax.set_xlabel("Gender(1:Man, 2:Woman),AGE")
ax.set_ylabel("Frequency")

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show the plot
st.pyplot(fig)

## ML 예측 결과 chatGPT 질문 결과 ##
text = '이 4가지 강점 조합 전부를 가진 사람에게 가장 추천할만한 직업은 무엇일지를 표로 만들어줘'
question = result + " " + text
answer = ask_question(question)
st.write(answer)
