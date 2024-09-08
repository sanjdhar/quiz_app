import streamlit as st
import time
import random
from google.cloud import storage
from google.cloud import datastore
import json

# Instantiate a Google Cloud Storage client and specify required bucket and file
storage_client = storage.Client()
bucket = storage_client.get_bucket('sd-bucket-2024')
blob = bucket.blob('quiz_questions.json')
dict_result = json.loads(blob.download_as_string(client=None))

# Get the output file name from first key from the JSON object
out_file_name = next(iter(dict_result))

quiz_questions = dict_result['quiz123']['questions']



def main():
    st.title("Quiz App")

    # Initialize session state
    if 'nickname' not in st.session_state:
        st.session_state.nickname = ""
    if 'nickname_entered' not in st.session_state:
        st.session_state.nickname_entered = False
    if 'started' not in st.session_state:
        st.session_state.started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'question_times' not in st.session_state:
        st.session_state.question_times = []
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'randomized_options' not in st.session_state:
        st.session_state.randomized_options = []

    if not st.session_state.nickname_entered:
        st.subheader("Welcome to the Quiz!")
        nickname = st.text_input("Enter your nickname or first name:")
        if st.button("Enter"):
            if nickname.strip():  # Ensure the nickname is not empty
                st.session_state.nickname = nickname
                st.session_state.nickname_entered = True
                st.rerun()
            else:
                st.warning("Please enter a valid nickname.")
    elif not st.session_state.started:
        st.subheader(f"Welcome, {st.session_state.nickname}!")
        if st.button("Start Quiz"):
            st.session_state.started = True
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.user_answers = []
            st.session_state.question_times = []
            st.session_state.start_time = time.time()
            st.session_state.randomized_options = [randomize_options(q) for q in quiz_questions]
            st.rerun()
    else:
        display_quiz()

def randomize_options(question):
    options = question["options"].copy()
    random.shuffle(options)
    return options

def display_quiz():
    if st.session_state.current_question < len(quiz_questions):
        question = quiz_questions[st.session_state.current_question]
        randomized_options = st.session_state.randomized_options[st.session_state.current_question]
        
        st.subheader(f"Question {st.session_state.current_question + 1}")
        st.write(question["question"])
     
        # Use radio buttons for single-choice questions with no default selection
        user_answer = st.radio(
            "Select your answer:",
            randomized_options,
            key=f"q{st.session_state.current_question}",
            index=None  # This ensures no option is pre-selected
        )
        
        # Only allow proceeding if an answer is selected
        if user_answer:
            if st.button("Next"):
                end_time = time.time()
                question_time = end_time - st.session_state.start_time
                st.session_state.question_times.append(question_time)
                
                st.session_state.user_answers.append(user_answer)
                if user_answer == question["correctAnswer"]:
                    st.session_state.score += 1
                st.session_state.current_question += 1
                st.session_state.start_time = time.time()  # Reset start time for next question
                st.rerun()
        else:
            st.warning("Please select an answer before proceeding.")
    else:
        display_results()

def display_results():
    st.subheader(f"Quiz Completed, {st.session_state.nickname}!")
    percentage_score = (st.session_state.score / len(quiz_questions)) * 100
    st.write(f"Your score: {st.session_state.score} out of {len(quiz_questions)} ({percentage_score:.2f}%)")

    st.subheader("Time Summary:")
    total_time = sum(st.session_state.question_times)
    st.write(f"Total time taken: {total_time:.2f} seconds")
    
    for i, (question, user_answer, question_time) in enumerate(zip(quiz_questions, st.session_state.user_answers, st.session_state.question_times)):
        st.write(f"Question {i + 1}:")
        st.write(f"Time taken: {question_time:.2f} seconds")
        st.write(f"Your answer: {user_answer}")
        st.write(f"Correct answer: {question['correctAnswer']}")
        st.write("---")
    
    if st.button("Restart Quiz"):
        st.session_state.nickname_entered = False
        st.session_state.started = False
        st.session_state.randomized_options = []
        st.rerun()

if __name__ == "__main__":
    main()