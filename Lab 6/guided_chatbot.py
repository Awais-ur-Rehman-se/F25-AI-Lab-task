
from sklearn.feature_extraction.text import TfidfVectorizer

FAQ = [
    {"question": "How do I reset my password?",
     "answer": "Use the recovery link on the login page.",
     "source": "it_help.txt"},

    {"question": "Where do I submit my assignment?",
     "answer": "Use the assignment upload page in the learning portal.",
     "source": "assessment.txt"},

    {"question": "Can illness justify a late submission?",
     "answer": "Request an extension with medical evidence before the deadline.",
     "source": "handbook.txt"},

    {"question": "How can I contact my teacher?",
     "answer": "Contact your teacher through the learning portal.",
     "source": "teacher_help.txt"},

    {"question": "Where can I check my grades?",
     "answer": "Check your grades in the learning portal.",
     "source": "grades_help.txt"}
]

texts = [item["question"] + " " + item["answer"] for item in FAQ]

vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(texts)


def chatbot(query):

    if not query.strip():
        return "Please enter a question."

    for item in FAQ:
        if query.strip().lower() == item["question"].lower():
            return item["answer"] + " [source: " + item["source"] + "]"

    query_vector = vectorizer.transform([query])

    if query_vector.nnz == 0:
        return "No matching FAQ. Please contact the help desk."

    scores = (query_vector @ matrix.T).toarray()[0]

    ranked = sorted(range(len(FAQ)), key=lambda i: (-scores[i], i))

    result = "Possible matches; choose or rephrase your question:\n"

    for i in ranked[:3]:
        result += FAQ[i]["question"] + " (similarity " + str(round(scores[i], 3)) + ")\n"

    return result


tests = [
    "How do I reset my password?",
    "password recovery",
    ""
]

for question in tests:
    print("You:", repr(question))
    print("Bot:", chatbot(question))
    print("------------------------------")


print("FAQ Assistant - Type exit to stop")

while True:
    query = input("You: ")

    if query.strip().lower() == "exit":
        break

    print("Bot:", chatbot(query))
