
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "quiz_secret_key_123"

# Quiz Questions
questions = [
    {
        "question": "Who developed Python?",
        "options": ["James Gosling", "Guido van Rossum", "Dennis Ritchie", "Bjarne Stroustrup"],
        "answer": "Guido van Rossum"
    },
    {
        "question": "Which keyword is used to define a function?",
        "options": ["function", "def", "fun", "define"],
        "answer": "def"
    },
    {
        "question": "Which data type stores multiple values?",
        "options": ["int", "float", "list", "bool"],
        "answer": "list"
    },
    {
        "question": "Which symbol is used for comments in Python?",
        "options": ["//", "#", "/*", "--"],
        "answer": "#"
    },
    {
        "question": "Which function displays output?",
        "options": ["input()", "print()", "show()", "display()"],
        "answer": "print()"
    },
    {
        "question": "Which loop is used to iterate over a sequence?",
        "options": ["if", "while", "for", "switch"],
        "answer": "for"
    },
    {
        "question": "Which operator is used for exponentiation?",
        "options": ["*", "**", "//", "%"],
        "answer": "**"
    },
    {
        "question": "Which keyword is used for a condition?",
        "options": ["if", "for", "def", "import"],
        "answer": "if"
    },
    {
        "question": "Which function takes input from the user?",
        "options": ["print()", "input()", "scan()", "get()"],
        "answer": "input()"
    },
    {
        "question": "What is the extension of a Python file?",
        "options": [".java", ".cpp", ".py", ".html"],
        "answer": ".py"
    }
]


@app.route("/", methods=["GET", "POST"])
def home():

    if "current" not in session:
        session["current"] = 0
        session["score"] = 0
        session["answered"] = False

    current = session["current"]

    if request.method == "POST":

        action = request.form.get("action")

        if action == "submit" and not session["answered"]:

            selected = request.form.get("option")

            if not selected:
                return render_template(
                    "index.html",
                    questions=questions,
                    current=current,
                    answered=False,
                    error="Please select an option!"
                )

            correct = questions[current]["answer"]

            if selected == correct:
                session["score"] += 1
                session["feedback"] = "Correct Answer!"
            else:
                session["feedback"] = (
                    "Wrong Answer! Correct Answer: " + correct
                )

            session["answered"] = True

        elif action == "next" and session["answered"]:

            session["current"] += 1
            session["answered"] = False
            session.pop("feedback", None)

            return redirect(url_for("home"))

        elif action == "restart":

            session.clear()
            return redirect(url_for("home"))

        current = session["current"]

    if current >= len(questions):
        return render_template(
            "index.html",
            result=True,
            score=session["score"]
        )

    return render_template(
        "index.html",
        questions=questions,
        current=current,
        answered=session["answered"],
        feedback=session.get("feedback"),
        error=None
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
