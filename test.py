import json

# The JSON data (you can also load this from a file)
json_data = '''
{
  "quiz123": {
    "title": "Mixed Topics Quiz",
    "questions": [
      {
        "id": 1,
        "question": "What is the capital of Japan?",
        "options": ["Beijing", "Seoul", "Tokyo", "Bangkok"],
        "correctAnswer": "Tokyo"
      },
      {
        "id": 2,
        "question": "Which planet is known as the 'Blue Planet'?",
        "options": ["Mars", "Venus", "Earth", "Neptune"],
        "correctAnswer": "Earth"
      },
      {
        "id": 3,
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
        "correctAnswer": "William Shakespeare"
      },
      {
        "id": 4,
        "question": "What is the chemical symbol for gold?",
        "options": ["Ag", "Au", "Fe", "Cu"],
        "correctAnswer": "Au"
      },
      {
        "id": 5,
        "question": "Which country is home to the kangaroo?",
        "options": ["New Zealand", "South Africa", "Australia", "Brazil"],
        "correctAnswer": "Australia"
      }
    ]
  }
}
'''

#Extract first key from JSON data


# Parse the JSON data
quiz_data = json.loads(json_data)

# Get the first key from the JSON object
first_key = next(iter(quiz_data))
print(f"The first key is: {first_key}")

# Load all questions from quiz_data into a list
questions = quiz_data['quiz123']['questions']

print(questions)