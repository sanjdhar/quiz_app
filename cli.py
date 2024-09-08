import time
import random

class Question:
    def __init__(self, question, options, correct_answer):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer

class QuizApp:
    def __init__(self):
        self.questions = []
        self.users = {}

    def add_question(self, question, options, correct_answer):
        self.questions.append(Question(question, options, correct_answer))

    def register_user(self, username):
        if username not in self.users:
            self.users[username] = 0

    def run_quiz(self):
        for question in self.questions:
            print("\n" + question.question)
            for i, option in enumerate(question.options):
                print(f"{i + 1}. {option}")

            start_time = time.time()
            for username in self.users:
                answer = input(f"{username}, enter your answer (1-{len(question.options)}): ")
                end_time = time.time()
                response_time = end_time - start_time

                if answer == str(question.correct_answer):
                    score = max(10 - int(response_time), 1)  # Minimum score of 1 point
                    self.users[username] += score
                    print(f"Correct! You earned {score} points.")
                else:
                    print("Incorrect.")

    def show_results(self):
        print("\nFinal Scores:")
        for username, score in sorted(self.users.items(), key=lambda x: x[1], reverse=True):
            print(f"{username}: {score} points")

# Example usage
if __name__ == "__main__":
    quiz = QuizApp()

    # Admin creates questions
    quiz.add_question("What is the capital of France?", ["London", "Berlin", "Paris", "Madrid"], 3)
    quiz.add_question("Which planet is known as the Red Planet?", ["Mars", "Venus", "Jupiter", "Saturn"], 1)

    # Register users
    quiz.register_user("Alice")
    quiz.register_user("Bob")

    # Run the quiz
    quiz.run_quiz()

    # Show results
    quiz.show_results()