import streamlit as st
import time

# Sample quiz questions
quiz_questions = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct_answer": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Mars", "Venus", "Jupiter", "Saturn"],
        "correct_answer": "Mars"
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["African Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
        "correct_answer": "Blue Whale"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
        "correct_answer": "Leonardo da Vinci"
    },
    {
        "question": "What is the chemical symbol for gold?",
        "options": ["Au", "Ag", "Fe", "Cu"],
        "correct_answer": "Au"
    }
]

def main():
    st.title("Quiz App")

    # Initialize session state
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

    if not st.session_state.started:
        if st.button("Start Quiz"):
            st.session_state.started = True
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.user_answers = []
            st.session_state.question_times = []
            st.session_state.start_time = time.time()
            st.rerun()
    else:
        display_quiz()

def display_quiz():
    if st.session_state.current_question < len(quiz_questions):
        question = quiz_questions[st.session_state.current_question]
        st.subheader(f"Question {st.session_state.current_question + 1}")
        st.write(question["question"])
        
        # Use radio buttons for single-choice questions with no default selection
        user_answer = st.radio(
            "Select your answer:",
            question["options"],
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
                if user_answer == question["correct_answer"]:
                    st.session_state.score += 1
                st.session_state.current_question += 1
                st.session_state.start_time = time.time()  # Reset start time for next question
                st.rerun()
        else:
            st.warning("Please select an answer before proceeding.")
    else:
        display_results()

def display_results():
    st.subheader("Quiz Completed!")
    st.write(f"Your score: {st.session_state.score} out of {len(quiz_questions)}")
    
    st.subheader("Time Summary:")
    total_time = sum(st.session_state.question_times)
    st.write(f"Total time taken: {total_time:.2f} seconds")
    
    for i, (question, user_answer, question_time) in enumerate(zip(quiz_questions, st.session_state.user_answers, st.session_state.question_times)):
        st.write(f"Question {i + 1}:")
        st.write(f"Time taken: {question_time:.2f} seconds")
        st.write(f"Your answer: {user_answer}")
        st.write(f"Correct answer: {question['correct_answer']}")
        st.write("---")
    
    if st.button("Restart Quiz"):
        st.session_state.started = False
        st.rerun()

if __name__ == "__main__":
    main()
