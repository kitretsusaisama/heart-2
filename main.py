import streamlit as st
import pandas as pd
import pickle


model_path = 'model.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

st.set_page_config(
        page_title="Heart Disease Prediction Model", layout='wide',
)

st.title('Heartfelt Predictions :heartpulse:')
st.caption('Dealing with Matters of the Heart with Data Science. See https://www.kaggle.com/datasets/kamilpytlak/personal-key-indicators-of-heart-disease/ for original dataset')
st.markdown("""
    Cardiovascular diseases (CVDs) are the leading cause of death globally, taking an estimated 17.9 million lives each year. CVDs are a group of disorders of the heart and blood vessels and include coronary heart disease, cerebrovascular disease, rheumatic heart disease and other conditions. More than four out of five CVD deaths are due to heart attacks and strokes, and one third of these deaths occur prematurely in people under 70 years of age
    (*https://www.who.int/health-topics/cardiovascular-diseases#tab=tab_1*)        
    
    As we age, we get more susceptible to disease. It's never too early to make the necessary lifestyle changes to avoid cardiovascular disease!
""")
st.sidebar.header('Input your Information')


height = st.sidebar.number_input('Enter your height in centimeters: ', step=1, min_value=1)
weight = st.sidebar.number_input('Enter your weight in kilograms: ', step=1, min_value=1)
age = st.sidebar.number_input('Enter your age: ', step=1, min_value=18)
gender = st.sidebar.radio('Gender: ', ['M', 'F'])

general_health = st.sidebar.selectbox('Would you say your general health is: ', ['Excellent', 'Very good', 'Good', 'Fair', 'Poor'])

smoker = st.sidebar.radio('Have you smoked at least 100 cigarettes in your entire life? [Note: 5 packs = 100 cigarettes]', ['Yes','No'])
alcohol = st.sidebar.radio('Are you a heavy drinker? (adult men having more than 14 drinks per week and adult women having more than 7 drinks per week)', ['Yes','No'])
physical_activity = st.sidebar.radio('Have you done any physical activity in the past 30 days aside from your regular job?', ['Yes','No'])

stroke = st.sidebar.radio('Have you ever had a stroke?', ['Yes','No'])
diff_walking = st.sidebar.radio('Do you have serious difficulty walking or climbing stairs?', ['Yes','No'])
skin_cancer = st.sidebar.radio('Have you ever had skin cancer?', ['Yes','No'])
kidney_disease = st.sidebar.radio('Not including kidney stones, bladder infection or incontinence, were you ever told you had kidney disease?', ['Yes','No'])
diabetic = st.sidebar.radio('Have you ever had diabetes?', ['Yes', 'Yes, during pregnancy', 'No', 'No, but borderline'])
asthma = st.sidebar.radio('Have you ever had asthma?', ['Yes','No'])

sleep_time = st.sidebar.slider('On average, how many hours of sleep do you get in a 24-hour period?', min_value=0, max_value=24, step=1)
physical_health = st.sidebar.slider('Thinking about your physical health, which includes physical illness and injury, for how many days during the past 30 days was your physical health not good? (0-30 days)', min_value=0, max_value=30, step=1)
mental_health = st.sidebar.slider('Thinking about your mental health, for how many days during the past 30 days was your mental health not good? (0-30 days)', min_value=0, max_value=30, step=1)



bmi = weight/(height/100)**2


if age <= 24:
    age = '18-24'
elif age <= 29:
    age = '25-29'
elif age <= 34:
    age = '30-34'
elif age <= 39:
    age = '35-39'
elif age <= 44:
    age = '40-44'
elif age <= 49:
    age = '45-49'
elif age <= 54:
    age = '50-54'
elif age <= 59:
    age = '55-59'
elif age <= 64:
    age = '60-64'
elif age <= 69:
    age = '65-69'
elif age <= 74:
    age = '70-74'
elif age <= 79:
    age = '75-79'
else:
    age = '80 or older'

user_dict = {'BMI': bmi, 'Smoking': smoker, 'AlcoholDrinking': alcohol, 'Stroke': stroke , 'PhysicalHealth': physical_health,
    'MentalHealth': mental_health, 'DiffWalking': diff_walking, 'AgeCategory': age, 'PhysicalActivity': physical_activity,
    'GenHealth': general_health, 'SleepTime': sleep_time, 'Asthma': asthma, 'KidneyDisease': kidney_disease, 'SkinCancer': skin_cancer}

if gender == 'M':
    user_dict['Sex_Male'] = 1
    user_dict['Sex_Female'] = 0
else:
    user_dict['Sex_Male'] = 0
    user_dict['Sex_Female'] = 1

if diabetic == 'Yes':
    user_dict['Diabetic_Yes'] = 1
    user_dict['Diabetic_No_borderline_diabetes'] = 0
    user_dict['Diabetic_No'] = 0
    user_dict['Diabetic_Yes_during_pregnancy'] = 0
elif diabetic == 'No':
    user_dict['Diabetic_Yes'] = 0
    user_dict['Diabetic_No_borderline_diabetes'] = 0
    user_dict['Diabetic_No'] = 1
    user_dict['Diabetic_Yes_during_pregnancy'] = 0
elif diabetic == 'No, but borderline':
    user_dict['Diabetic_Yes'] = 0
    user_dict['Diabetic_No_borderline_diabetes'] = 1
    user_dict['Diabetic_No'] = 0
    user_dict['Diabetic_Yes_during_pregnancy'] = 0
else:
    user_dict['Diabetic_Yes'] = 0
    user_dict['Diabetic_No_borderline_diabetes'] = 0
    user_dict['Diabetic_No'] = 0
    user_dict['Diabetic_Yes_during_pregnancy'] = 1

user_df = pd.DataFrame(user_dict, index=[0]).replace({'Yes': 1, 'No': 0})
user_df = user_df.replace({'18-24': 0, '25-29': 1, '30-34': 2, '35-39': 3, '40-44': 4, '45-49': 5, '50-54': 6, '55-59': 7, '60-64': 8, '65-69': 9, '70-74': 10, '75-79': 11, '80 or older':12})
user_df = user_df.replace({'Poor': 0, 'Fair': 1, 'Good': 2, 'Very good': 3, 'Excellent': 4})

def run_model(df):
    entry = df.iloc[0].values.reshape(1, -1)
    return model.predict(entry)

if st.sidebar.button('Submit!'):
    if run_model(user_df)[0] == 0:
        prediction = "No heart disease! :sparkling_heart:"
        message = "Our model has predicted that you're safe from heart problems! Make sure to maintain a healthy lifestyle."
    else:
        prediction = "Potential heart disease! :broken_heart:"
        message = "Oh no, our model believes that you're at risk of heart problems! Being physically active :woman-lifting-weights:, avoiding smoking and alcohol consumption :no_entry:, getting adequate sleep :zzz:, and a healthy diet :herb: are all things that we can control to improve our overall health"

    st.header("Assessment: ")
    st.write(prediction)
    st.write(message)
    st.caption("Please note that this is not a medical diagnosis, please consult an actual doctor if you think you are unwell.")



