from flask import Flask, render_template, request, session

from ai.engine import get_questions, evaluate_answer


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)

app.secret_key = "ai_interviewer_secret_key"


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# CANDIDATE PROFILE
# =========================================================

@app.route("/profile")
def profile():

    return render_template("profile.html")


# =========================================================
# START INTERVIEW
# =========================================================

@app.route("/start-interview", methods=["POST"])
def start_interview():

    # Candidate information

    session["name"] = request.form["name"]

    session["education"] = request.form["education"]

    session["skills"] = request.form["skills"]

    session["experience"] = request.form["experience"]

    session["role"] = request.form["role"]

    session["difficulty"] = request.form["difficulty"]


    # Generate questions

    questions = get_questions(

        session["role"],

        session["skills"],

        session["difficulty"]

    )


    # Store questions

    session["questions"] = questions


    # Start from first question

    session["question_number"] = 0


    # Empty result list

    session["results"] = []


    # First question

    question_data = questions[0]

    question = question_data["question"]


    return render_template(

        "interview.html",

        question=question,

        question_number=1,

        total_questions=len(questions),

        role=session["role"]

    )


# =========================================================
# SUBMIT ANSWER
# =========================================================

@app.route("/answer", methods=["POST"])
def answer():

    # Candidate answer

    answer_text = request.form["answer"]


    # Current question

    q = session["question_number"]


    # Get question data

    question_data = session["questions"][q]


    question = question_data["question"]


    # =====================================================
    # AI EVALUATION
    # =====================================================

    evaluation = evaluate_answer(

        answer_text,

        question_data

    )


    # =====================================================
    # STORE RESULT
    # =====================================================

    results = session["results"]


    results.append({

        "question": question,

        "answer": answer_text,

        "relevance": evaluation["relevance"],

        "technical": evaluation["technical"],

        "completeness": evaluation["completeness"],

        "score": evaluation["overall"],

        "feedback": evaluation["feedback"],

        "matched_keywords": evaluation["matched_keywords"]

    })


    session["results"] = results


    # Move to next question

    q += 1

    session["question_number"] = q


    # =====================================================
    # INTERVIEW FINISHED
    # =====================================================

    if q >= len(session["questions"]):

        scores = [

            item["score"]

            for item in results

        ]


        if scores:

            overall = round(

                sum(scores) / len(scores)

            )

        else:

            overall = 0


        return render_template(

            "result.html",

            name=session["name"],

            role=session["role"],

            score=overall,

            results=results

        )


    # =====================================================
    # NEXT QUESTION
    # =====================================================

    next_question_data = session["questions"][q]


    next_question = next_question_data["question"]


    return render_template(

        "interview.html",

        question=next_question,

        question_number=q + 1,

        total_questions=len(session["questions"]),

        role=session["role"]

    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)