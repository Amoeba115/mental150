BYU Mental Health & Connection Help🧠

An interactive digital assessment designed to help students identify the root causes of their loneliness and connect with targeted resources.

Project Overview

"BYU Mental Health & Connection Help" is a Python-based web application built with Streamlit. It addresses the "loneliness epidemic" on college campuses, specifically tailored to the unique social environment at Brigham Young University (BYU).

Instead of a one-size-fits-all approach, this tool functions as a diagnostic wizard. It uses a branching questionnaire to sort users into 10 specific archetypes (e.g., "Socially Anxious," "Situational Grief," "Emotional Loneliness") and provides immediate, curated resources for their specific situation. It also includes free-response options to ensure users feel heard, even if their situation is unique.

Research Basis

The logic and questionnaire design are grounded in recent research regarding social isolation and student mental health, including:

Holt-Lunstad, J. (BYU) - Research on social connection as a medical health factor.

Research Square - Studies on the "Loneliness Epidemic" post-COVID-19.

US Surgeon General - 2023 Advisory on the Healing Effects of Social Connection.

EduMed & CDC - Frameworks for identifying symptoms of isolation.

Features

Dark Mode Aesthetic: Designed with a calming, private "dark mode" interface to reduce screen fatigue and create a safe environment.

Triaging Logic: Immediate detection of safety/crisis responses to redirect users to emergency services.

Branching Questionnaire: A "Hierarchy of Needs" algorithm that prioritizes clinical or safety issues over general social advice.

"Other" Option Support: Users can type in their own feelings if standard options don't fit, ensuring they feel validated rather than boxed in.

10 Unique Outcomes: Users are matched to specific profiles rather than generic advice.

Anonymous: No data is stored or tracked; the session resets completely upon reload.

How to Run Locally

If you want to run this code on your own machine:

Clone the repository

git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name


Install Requirements
Ensure you have Python installed, then run:

pip install -r requirements.txt


Launch the App

streamlit run app.py


The application will open automatically in your default web browser (usually at http://localhost:8501).

Deployment (Streamlit Cloud)

This app is optimized for Streamlit Cloud, which allows for free hosting directly from GitHub.

Push this code to a GitHub repository.

Go to share.streamlit.io.

Connect your GitHub account.

Select your repository and the main file (app.py).

Click Deploy.

Files in this Repository

app.py: The main application logic, CSS styling, and questionnaire data.

requirements.txt: List of Python dependencies required to build the app.

README.md: Project documentation.
