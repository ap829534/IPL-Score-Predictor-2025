import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Load the better performing model
model = joblib.load("ipl_gb_model.pkl")

# Streamlit Page Config
st.set_page_config(
    page_title="IPL Score Predictor",
    page_icon="🏏",
    layout="centered",
)

# Custom style
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #fceabb, #f8b500);
        font-family: 'Segoe UI', sans-serif;
    }
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🏏 IPL Score Predictor 2025</div>', unsafe_allow_html=True)

with st.expander("📄 Description"):
    st.markdown("Predict the final score of an IPL first innings using machine learning!")

# Team options
teams = ['Chennai Super Kings', 'Mumbai Indians', 'Royal Challengers Bangalore',
         'Kolkata Knight Riders', 'Rajasthan Royals', 'Delhi Capitals',
         'Punjab Kings', 'Sunrisers Hyderabad', 'Lucknow Super Giants', 'Gujarat Titans']

# Inputs
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox(" Select the Batting Team", teams)
with col2:
    bowling_team = st.selectbox(" Select the Bowling Team", teams)

overs = st.slider(" Overs Completed", 5.0, 20.0, step=0.1)
wickets = st.slider(" Wickets Lost", 0, 10)
runs = st.number_input(" Current Score", 0, 300)
last_5_runs = st.number_input(" Runs in Last 5 Overs", 0, 100)

# Prediction function
def predict_score():
    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'over': [overs],
        'cumulative_runs': [runs],
        'cumulative_wickets': [wickets],
        'rolling_runs': [last_5_runs]
    })
    return int(model.predict(input_df)[0])

# Predict
if st.button("Predict Score"):
    if batting_team != bowling_team:
        prediction = predict_score()
        st.success(f" Predicted Final Score: *{prediction} Runs*")

        # Simulated Score Progression Graph
        current_rr = runs / overs if overs > 0 else 0
        projected_scores = [int(current_rr * o) for o in range(int(overs)+1, 21)]

        full_overs = list(range(int(overs)+1, 21))

        plt.figure(figsize=(10, 4))
        plt.plot(full_overs, projected_scores, marker='o', color='green')
        plt.axhline(y=prediction, color='red', linestyle='--', label='Predicted Final Score')
        plt.title(" Projected Score Progression")
        plt.xlabel("Over")
        plt.ylabel("Score")
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

    else:
        st.error("Bowling and Batting teams must be different.")