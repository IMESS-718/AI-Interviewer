# =========================================================
# AI JOB RECOMMENDER
# =========================================================

import re


# =========================================================
# JOB DATABASE
# =========================================================

JOB_DATABASE = {

    "Python Developer": {

        "skills": [
            "python",
            "django",
            "flask",
            "fastapi",
            "sql",
            "api",
            "git"
        ],

        "description":
            "Develops software applications and backend systems using Python."
    },


    "Web Developer": {

        "skills": [
            "html",
            "css",
            "javascript",
            "python",
            "flask",
            "django",
            "sql",
            "api"
        ],

        "description":
            "Builds and maintains websites and web applications."
    },


    "Cybersecurity Analyst": {

        "skills": [
            "cybersecurity",
            "security",
            "networking",
            "firewall",
            "encryption",
            "authentication",
            "vpn",
            "linux",
            "siem"
        ],

        "description":
            "Monitors systems and networks to identify and respond to security threats."
    },


    "SOC Analyst": {

        "skills": [
            "soc",
            "cybersecurity",
            "security",
            "siem",
            "firewall",
            "networking",
            "linux",
            "incident response"
        ],

        "description":
            "Monitors security events and investigates potential cyber attacks."
    },


    "Network Engineer": {

        "skills": [
            "networking",
            "cisco",
            "router",
            "switch",
            "tcp",
            "ip",
            "dns",
            "dhcp",
            "vpn"
        ],

        "description":
            "Designs, configures and maintains computer networks."
    },


    "Network Security Engineer": {

        "skills": [
            "networking",
            "cybersecurity",
            "firewall",
            "vpn",
            "ids",
            "ips",
            "cisco",
            "linux",
            "security"
        ],

        "description":
            "Protects networks using security technologies and monitoring systems."
    },


    "Data Analyst": {

        "skills": [
            "python",
            "sql",
            "excel",
            "pandas",
            "numpy",
            "statistics",
            "data analysis",
            "power bi"
        ],

        "description":
            "Analyzes data and creates insights to support business decisions."
    },


    "Machine Learning Engineer": {

        "skills": [
            "python",
            "machine learning",
            "tensorflow",
            "pytorch",
            "scikit-learn",
            "numpy",
            "pandas",
            "statistics"
        ],

        "description":
            "Builds and deploys machine learning models and intelligent applications."
    },


    "Cloud Engineer": {

        "skills": [
            "cloud",
            "aws",
            "azure",
            "gcp",
            "linux",
            "docker",
            "networking",
            "python"
        ],

        "description":
            "Designs and manages cloud infrastructure and cloud-based services."
    },


    "DevOps Engineer": {

        "skills": [
            "devops",
            "docker",
            "kubernetes",
            "linux",
            "git",
            "jenkins",
            "aws",
            "azure",
            "ci/cd"
        ],

        "description":
            "Automates software development, deployment and infrastructure processes."
    }

}


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_text(text):

    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9+#./ -]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# EXTRACT SKILLS
# =========================================================

def extract_skills(text):

    text = normalize_text(text)

    found_skills = []

    all_skills = set()

    for job in JOB_DATABASE.values():

        for skill in job["skills"]:

            all_skills.add(
                normalize_text(skill)
            )


    for skill in all_skills:

        if skill and skill in text:

            found_skills.append(skill)


    return list(set(found_skills))


# =========================================================
# EXPERIENCE SCORE
# =========================================================

def experience_score(experience):

    text = normalize_text(
        experience
    )


    # Fresher

    if (
        "fresher" in text
        or
        "0 year" in text
        or
        "0 years" in text
        or
        "student" in text
    ):

        return 40


    # Extract number of years

    numbers = re.findall(
        r"\d+(?:\.\d+)?",
        text
    )


    if numbers:

        try:

            years = float(
                numbers[0]
            )


            if years >= 5:

                return 100

            elif years >= 3:

                return 90

            elif years >= 2:

                return 80

            elif years >= 1:

                return 70

            else:

                return 50

        except:

            pass


    return 50


# =========================================================
# RECOMMEND JOBS
# =========================================================

def recommend_jobs(
    resume_text,
    experience="",
    candidate_skills="",
    current_role=""
):

    resume_text = normalize_text(
        resume_text
    )

    candidate_skills = normalize_text(
        candidate_skills
    )

    current_role = normalize_text(
        current_role
    )


    # Combine resume and candidate skills

    combined_text = (
        resume_text
        + " "
        + candidate_skills
    )


    # Extract skills

    candidate_skill_list = extract_skills(
        combined_text
    )


    # Experience score

    exp_score = experience_score(
        experience
    )


    recommendations = []


    # =====================================================
    # CALCULATE EACH JOB MATCH
    # =====================================================

    for job_name, job_data in JOB_DATABASE.items():

        job_skills = [

            normalize_text(skill)

            for skill in job_data["skills"]

        ]


        # Find matching skills

        matched_skills = [

            skill

            for skill in job_skills

            if skill in combined_text

        ]


        # Skill match percentage

        if job_skills:

            skill_match = (

                len(matched_skills)
                /
                len(job_skills)

            ) * 100

        else:

            skill_match = 0


        # =================================================
        # EXPERIENCE COMPONENT
        # =================================================

        experience_component = exp_score


        # =================================================
        # FINAL SCORE
        # =================================================

        score = (

            skill_match * 0.75
            +
            experience_component * 0.25

        )


        # =================================================
        # CURRENT ROLE BONUS
        # =================================================

        if current_role:

            role_words = set(
                current_role.split()
            )

            job_words = set(
                normalize_text(
                    job_name
                ).split()
            )


            if role_words.intersection(
                job_words
            ):

                score += 5


        # Limit score

        score = min(
            round(score),
            100
        )


        recommendations.append({

            "job":
                job_name,

            "match":
                score,

            "description":
                job_data["description"],

            "skills":
                matched_skills

        })


    # =====================================================
    # SORT BY BEST MATCH
    # =====================================================

    recommendations.sort(

        key=lambda x:
        x["match"],

        reverse=True

    )


    # =====================================================
    # RETURN TOP 5
    # =====================================================

    return recommendations[:5]


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    sample_resume = """
    Python developer with knowledge of Python,
    Flask, SQL, networking, cybersecurity,
    Linux and Docker.
    """

    results = recommend_jobs(

        sample_resume,

        experience="Fresher",

        candidate_skills=
            "Python, Networking, Cybersecurity",

        current_role=
            "Cybersecurity Analyst"

    )


    print("\nAI JOB RECOMMENDATIONS")
    print("======================")

    for result in results:

        print(
            result["job"],
            "-",
            result["match"],
            "%"
        )