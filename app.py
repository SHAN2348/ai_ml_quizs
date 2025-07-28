import streamlit as st
import pandas as pd
from db import create_table, store_response, fetch_all_responses

# Set up the page
st.set_page_config(page_title="AI & ML Quiz", layout="centered")
st.title("🧠 AI & Machine Learning Quiz")

# Initialize DB
create_table()

# Quiz questions
quiz_data = [
    ("What is the difference between AI and Machine Learning?", [
        "AI is a type of ML",
        "ML is a subset of AI",
        "They are the same",
        "AI uses ML for hardware"
    ], "ML is a subset of AI"),
    ("What is supervised learning?", [
        "Learning without labeled data",
        "Learning by rewards",
        "Learning from unlabeled data",
        "Learning from labeled data"
    ], "Learning from labeled data"),
    ("Which of the following is a classification problem?", [
        "Predicting stock prices",
        "Predicting temperature",
        "Detecting spam emails",
        "Calculating loan interest"
    ], "Detecting spam emails"),
    ("What is overfitting?", [
        "The model performs well on test data",
        "The model performs well on training data but poorly on new data",
        "The model is too simple",
        "The model has high bias"
    ], "The model performs well on training data but poorly on new data"),
    ("What is the purpose of splitting data into training and testing sets?", [
        "To make the model run faster",
        "To prevent bias",
        "To evaluate generalization performance",
        "To reduce memory usage"
    ], "To evaluate generalization performance"),
    ("Which metric tells you how many relevant items are selected?", [
        "Recall",
        "Precision",
        "Accuracy",
        "F1 Score"
    ], "Precision"),
    ("What does a confusion matrix show?", [
        "Model structure",
        "Training time",
        "True and false predictions",
        "Correlation between features"
    ], "True and false predictions"),
    ("What is cross-validation used for?", [
        "Optimizing memory",
        "Avoiding model training",
        "Improving accuracy by resampling",
        "Feature scaling"
    ], "Improving accuracy by resampling"),
    ("Which of the following is NOT a classification algorithm?", [
        "Logistic Regression",
        "Decision Tree",
        "Linear Regression",
        "Support Vector Machine"
    ], "Linear Regression"),
    ("What is gradient descent used for?", [
        "Increasing accuracy",
        "Normalizing data",
        "Optimizing the loss function",
        "Data augmentation"
    ], "Optimizing the loss function")
]

# Get user input
username = st.text_input("Enter your name to begin the quiz:")

if username.strip():
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    if not st.session_state.submitted:
        st.markdown("### Please answer the following questions:")
        user_answers = []

        for i, (question, options, _) in enumerate(quiz_data, 1):
            answer = st.radio(f"**{i}. {question}**", options, key=f"q{i}")
            user_answers.append(answer)

        if st.button("Submit Quiz"):
            score = 0
            results = []

            for i, (_, _, correct_answer) in enumerate(quiz_data):
                user_answer = user_answers[i]
                is_correct = user_answer == correct_answer
                results.append((i + 1, user_answer, correct_answer, is_correct))
                if is_correct:
                    score += 1

            st.success(f"🎉 {username}, your score: {score} / {len(quiz_data)}")
            store_response(username, score, user_answers)

            st.subheader("📋 Answer Review:")
            for q_num, user_a, correct_a, is_right in results:
                if is_right:
                    st.markdown(f"**{q_num}. Correct ✅** – Your answer: *{user_a}*")
                else:
                    st.markdown(f"**{q_num}. Incorrect ❌** – Your answer: *{user_a}*, Correct answer: *{correct_a}*")

            st.session_state.submitted = True

    else:
        if st.button("Try Again"):
            st.session_state.submitted = False
            st.rerun()

# Leaderboard
st.sidebar.title("🏆 Leaderboard")
if st.sidebar.button("View Leaderboard"):
    responses = fetch_all_responses()

    if responses:
        sorted_responses = sorted(responses, key=lambda x: x[2], reverse=True)
        st.sidebar.markdown("### Top Scores:")
        for i, row in enumerate(sorted_responses[:10], 1):
            st.sidebar.markdown(f"**{i}. {row[1]}** – {row[2]}/10")

        # CSV Export
        df = pd.DataFrame(responses, columns=["ID", "Username", "Score", "Answers", "Submitted At"])
        csv = df.to_csv(index=False).encode("utf-8")

        st.sidebar.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="quiz_scores.csv",
            mime="text/csv"
        )
    else:
        st.sidebar.info("No submissions yet.")

# Developer Contact Section
st.markdown("---")
st.subheader("👨‍💻 Developer Contact")
st.markdown("""
**Name:** Shan Shareef 
**Email:** `SSdev@example.com`  
**GitHub:** [github.com/SHAN2348](https://github.com/SHAN2348)  
**Location:** India
""")
