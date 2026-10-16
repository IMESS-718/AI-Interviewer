from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# QUESTION BANK
# =========================================================

QUESTION_BANK = {

    "cybersecurity": [

        {
            "question": "What is a firewall and why is it used?",

            "keywords": [
                "firewall",
                "network",
                "security",
                "traffic",
                "incoming",
                "outgoing",
                "rules",
                "allow",
                "block",
                "unauthorized",
                "access",
                "protection"
            ]
        },

        {
            "question": "Explain the difference between TCP and UDP.",

            "keywords": [
                "tcp",
                "udp",
                "connection",
                "connectionless",
                "reliable",
                "reliability",
                "protocol",
                "faster",
                "transmission",
                "data"
            ]
        },

        {
            "question": "What is phishing and how can users prevent it?",

            "keywords": [
                "phishing",
                "email",
                "attack",
                "fake",
                "link",
                "credentials",
                "password",
                "information",
                "security",
                "user",
                "verify"
            ]
        },

        {
            "question": "What is encryption?",

            "keywords": [
                "encryption",
                "data",
                "security",
                "plaintext",
                "ciphertext",
                "key",
                "encrypt",
                "decrypt",
                "protection"
            ]
        },

        {
            "question": "What is a vulnerability assessment?",

            "keywords": [
                "vulnerability",
                "assessment",
                "security",
                "weakness",
                "system",
                "network",
                "scanning",
                "risk",
                "identify",
                "attack"
            ]
        }
    ],


    # =====================================================
    # SOFTWARE QUESTIONS
    # =====================================================

    "software": [

        {
            "question": "What is object-oriented programming?",

            "keywords": [
                "object",
                "class",
                "inheritance",
                "polymorphism",
                "encapsulation",
                "abstraction",
                "programming",
                "method",
                "data"
            ]
        },

        {
            "question": "What is the difference between a list and tuple in Python?",

            "keywords": [
                "list",
                "tuple",
                "python",
                "mutable",
                "immutable",
                "change",
                "elements",
                "collection"
            ]
        },

        {
            "question": "What is an API?",

            "keywords": [
                "api",
                "application",
                "programming",
                "interface",
                "communication",
                "software",
                "request",
                "response",
                "server",
                "client"
            ]
        },

        {
            "question": "What is exception handling?",

            "keywords": [
                "exception",
                "error",
                "handling",
                "try",
                "except",
                "program",
                "runtime",
                "error",
                "execution"
            ]
        },

        {
            "question": "How do you debug a program?",

            "keywords": [
                "debug",
                "error",
                "program",
                "testing",
                "breakpoint",
                "logs",
                "code",
                "identify",
                "fix",
                "problem"
            ]
        }
    ],


    # =====================================================
    # DATA SCIENCE QUESTIONS
    # =====================================================

    "data science": [

        {
            "question": "What is machine learning?",

            "keywords": [
                "machine",
                "learning",
                "data",
                "model",
                "algorithm",
                "training",
                "prediction",
                "learn",
                "patterns"
            ]
        },

        {
            "question": "Explain supervised and unsupervised learning.",

            "keywords": [
                "supervised",
                "unsupervised",
                "learning",
                "labeled",
                "unlabeled",
                "data",
                "training",
                "classification",
                "clustering"
            ]
        },

        {
            "question": "What is overfitting?",

            "keywords": [
                "overfitting",
                "model",
                "training",
                "data",
                "generalization",
                "accuracy",
                "test",
                "unseen"
            ]
        },

        {
            "question": "What is a confusion matrix?",

            "keywords": [
                "confusion",
                "matrix",
                "classification",
                "true",
                "false",
                "positive",
                "negative",
                "prediction"
            ]
        },

        {
            "question": "Why is data preprocessing important?",

            "keywords": [
                "data",
                "preprocessing",
                "cleaning",
                "missing",
                "values",
                "scaling",
                "features",
                "quality",
                "model"
            ]
        }
    ]
}


# =========================================================
# QUESTION GENERATOR
# =========================================================

def get_questions(role, skills, difficulty):

    role = role.lower()
    skills = skills.lower()

    text = role + " " + skills

    # Cybersecurity
    if (
        "cyber" in text
        or "security" in text
        or "network security" in text
    ):

        category = "cybersecurity"

    # Data Science / AI / ML
    elif (
        "data" in text
        or "machine learning" in text
        or "data science" in text
        or "artificial intelligence" in text
        or "ai" in text
    ):

        category = "data science"

    # Software
    else:

        category = "software"


    return QUESTION_BANK[category]


# =========================================================
# AI ANSWER EVALUATION
# =========================================================

def evaluate_answer(answer, question_data):

    answer = answer.lower().strip()

    keywords = question_data["keywords"]


    # =====================================================
    # 1. KEYWORD ANALYSIS
    # =====================================================

    matched_keywords = []

    for keyword in keywords:

        if keyword.lower() in answer:

            matched_keywords.append(keyword)


    if len(keywords) > 0:

        keyword_score = (
            len(matched_keywords) / len(keywords)
        ) * 100

    else:

        keyword_score = 0


    keyword_score = round(keyword_score)


    # =====================================================
    # 2. NLP SIMILARITY
    # =====================================================

    expected_text = " ".join(keywords)


    try:

        vectorizer = TfidfVectorizer()

        vectors = vectorizer.fit_transform(
            [answer, expected_text]
        )

        similarity = cosine_similarity(
            vectors[0],
            vectors[1]
        )[0][0]

        similarity_score = round(
            similarity * 100
        )

    except:

        similarity_score = 0


    # =====================================================
    # 3. ANSWER COMPLETENESS
    # =====================================================

    word_count = len(answer.split())


    if word_count >= 50:

        completeness = 100

    elif word_count >= 40:

        completeness = 95

    elif word_count >= 30:

        completeness = 90

    elif word_count >= 20:

        completeness = 80

    elif word_count >= 15:

        completeness = 70

    elif word_count >= 8:

        completeness = 50

    elif word_count >= 3:

        completeness = 30

    else:

        completeness = 10


    # =====================================================
    # 4. TECHNICAL KNOWLEDGE
    # =====================================================

    technical = keyword_score


    # Give a small bonus for multiple relevant concepts

    if len(matched_keywords) >= 8:

        technical = min(100, technical + 5)

    elif len(matched_keywords) >= 5:

        technical = min(100, technical + 3)


    # =====================================================
    # 5. RELEVANCE
    # =====================================================

    # Combine keyword matching and NLP similarity

    relevance = round(

        keyword_score * 0.70

        +

        similarity_score * 0.30

    )


    # =====================================================
    # 6. FINAL SCORE
    # =====================================================

    overall = round(

        relevance * 0.40

        +

        technical * 0.40

        +

        completeness * 0.20

    )


    # Keep score between 0 and 100

    overall = max(0, min(100, overall))


    # =====================================================
    # 7. AI FEEDBACK
    # =====================================================

    if overall >= 85:

        feedback = (

            "Excellent answer! You clearly understood "
            "the question and included important "
            "technical concepts. Your answer is relevant, "
            "complete, and well explained."
        )

    elif overall >= 70:

        feedback = (

            "Very good answer. You demonstrated a good "
            "understanding of the topic. Adding a few "
            "more technical details or examples would "
            "make your answer stronger."
        )

    elif overall >= 55:

        feedback = (

            "Good attempt. Your answer contains some "
            "relevant concepts, but you should explain "
            "the topic in more technical detail."
        )

    elif overall >= 40:

        feedback = (

            "Partially correct answer. Try to include "
            "the important technical concepts and "
            "provide a practical example."
        )

    else:

        feedback = (

            "The answer needs improvement. Review the "
            "topic and try to explain the key concepts "
            "clearly and accurately."
        )


    # =====================================================
    # 8. RETURN RESULT
    # =====================================================

    return {

        "relevance": relevance,

        "technical": technical,

        "completeness": completeness,

        "overall": overall,

        "feedback": feedback,

        "matched_keywords": matched_keywords

    }