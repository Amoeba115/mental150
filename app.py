import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BYU Mental Health & Connection Help",
    page_icon="🧠",
    layout="centered"
)

# Custom CSS - DEEP NAVY / DARK MODE AESTHETIC
st.markdown("""
<style>
    /* General Font and Background */
    .stApp {
        background-color: #0b101d; /* Deep Midnight Navy */
        color: #c9d1d9; /* Soft grey-white for readability */
        font-family: 'Helvetica', sans-serif;
    }
    
    /* Headers */
    h1 {
        color: #ffffff;
        font-weight: 700;
        text-align: center;
        padding-bottom: 20px;
    }
    h2, h3 {
        color: #58a6ff; /* Soft Blue for headers (Github dark mode style) */
    }
    
    /* Text Styling */
    p, li, .stMarkdown {
        color: #c9d1d9;
        font-size: 1.05rem;
    }
    
    /* Question Card Styling */
    .stRadio > label {
        font-weight: bold;
        font-size: 1.1rem;
        color: #ffffff;
        padding-bottom: 10px;
        display: block;
    }
    div.row-widget.stRadio > div {
        background-color: #161b22; /* Dark Navy-Grey */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.6);
        border: 1px solid #30363d;
    }
    
    /* Radio Button Text Color */
    .stRadio div[role='radiogroup'] > label {
        color: #c9d1d9 !important;
    }
    
    /* Text Input Styling for 'Other' */
    .stTextInput > div > div > input {
        border-radius: 5px;
        background-color: #0d1117;
        color: white;
        border: 1px solid #30363d;
    }
    
    /* Button Styling */
    .stButton > button {
        background-color: #002E5D; /* Darker BYU Navy */
        color: white;
        border-radius: 50px;
        padding: 10px 24px;
        font-weight: bold;
        border: 1px solid #1f6feb;
        width: 100%;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: #001f3f; /* Even darker on hover */
        border-color: #58a6ff;
        color: white;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #002E5D; /* BYU Navy */
    }

    /* Resource Box Styling */
    .resource-box {
        background-color: #161b22;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #002E5D; /* BYU Navy Border */
        margin-bottom: 15px;
        border: 1px solid #30363d;
    }
    .resource-title {
        font-weight: bold;
        color: #58a6ff;
        font-size: 1.1rem;
        margin-bottom: 5px;
    }
    .resource-desc {
        color: #c9d1d9;
        font-size: 0.9rem;
        margin-bottom: 8px;
        font-style: italic;
    }
    .resource-link {
        color: #58a6ff;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 5px;
    }
    .resource-link:hover {
        color: #ffffff;
        text-decoration: underline;
    }
    
    /* Crisis/Info Box Styling */
    .info-box {
        background-color: #161b22;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #30363d;
        color: #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. STATE MANAGEMENT
# -----------------------------------------------------------------------------
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

def next_step():
    st.session_state.step += 1

def restart():
    st.session_state.step = 0
    st.session_state.answers = {}

# -----------------------------------------------------------------------------
# 3. QUESTIONNAIRE DATA
# -----------------------------------------------------------------------------
questions = {
    # Q1 kept strict for safety triage - NO 'Other' option here
    "q1": {
        "text": "Right now, in this exact moment, how safe do you feel?",
        "options": [
            "I’m okay, just struggling with feelings.",
            "I’m feeling overwhelmed, but I’m safe.",
            "I feel unsafe or am having thoughts of hurting myself or others."
        ],
        "keys": ["A", "B", "C"]
    },
    "q2": {
        "text": "Which of these best describes your current social environment?",
        "options": [
            "I have people around me (roommates, classmates), but I don’t feel connected to any of them.",
            "I am physically alone most of the time; I don't really have a circle of friends here yet.",
            "I have friends, but I’ve recently lost a specific person (breakup, falling out, passing away).",
            "I have opportunities to socialize, but I get too nervous or anxious to go.",
            "I have friends, but I feel like I have to hide who I really am to fit in.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "E", "OTHER"]
    },
    "q3": {
        "text": "When you think about trying to make new friends, what is your immediate gut reaction?",
        "options": [
            "It's pointless; nobody understands me anyway.",
            "I don't even know where to start looking.",
            "I want to, but I'm terrified I'll say the wrong thing or be judged.",
            "I just don't have the energy or time; school/work is drowning me.",
            "I miss the person/group I used to have; no one else compares.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "E", "OTHER"]
    },
    "q4": {
        "text": "How long have you felt this way?",
        "options": [
            "It’s been a constant feeling for years, even before college.",
            "It started when I came to BYU/college.",
            "It’s very recent (last few weeks/months) due to a specific event.",
            "It comes and goes in waves.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "OTHER"]
    },
    "q5": {
        "text": "How is this loneliness affecting your daily life?",
        "options": [
            "I’m functioning okay, just feeling sad or empty when I’m alone.",
            "It’s hard to get out of bed; I feel heavy, hopeless, or numb.",
            "My heart races, I feel shaky, or I panic when I have to talk to people.",
            "I’m exhausted, not sleeping well, and physically drained.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "OTHER"]
    },
    "q6": {
        "text": "When you are alone, what do you usually do?",
        "options": [
            "Scroll social media and see everyone else having fun.",
            "Sleep or stare at the ceiling.",
            "Focus intensely on schoolwork to distract myself.",
            "Ruminate (think over and over) about what is 'wrong' with me.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "OTHER"]
    },
    "q7": {
        "text": "If you could wave a magic wand and fix one thing right now, what would it be?",
        "options": [
            "To have just one person who really 'gets' me.",
            "To have a big group of friends to hang out with on weekends.",
            "To stop feeling so afraid of social interaction.",
            "To stop feeling this deep sadness/numbness.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "OTHER"]
    }
}

# -----------------------------------------------------------------------------
# 4. LOGIC ENGINE
# -----------------------------------------------------------------------------
def determine_archetype(answers):
    """
    Analyzes answers. If 'OTHER' is used too frequently, or if no specific pattern is matched,
    it defaults to Group 10 (General).
    """
    
    # 1. CRISIS CASE (Safety First) - Explicit check, cannot be 'Other'
    if answers.get('q1') == 'C':
        return 1
    
    # Check for too many "Other" answers (e.g., 3 or more)
    other_count = list(answers.values()).count('OTHER')
    if other_count >= 3:
        return 10
        
    # 2. CHRONIC / CLINICAL STRUGGLE
    if answers.get('q4') == 'A' or answers.get('q5') == 'B':
        return 8
        
    # 3. SITUATIONAL / RECENTLY HEARTBROKEN
    if answers.get('q2') == 'C' or answers.get('q4') == 'C' or answers.get('q3') == 'E':
        return 5

    # 4. SOCIALLY ANXIOUS
    if answers.get('q2') == 'D' or answers.get('q3') == 'C' or answers.get('q5') == 'C':
        return 4
        
    # 5. IDENTITY ISOLATED
    if answers.get('q2') == 'E':
        return 6
        
    # 6. BURNOUT
    if answers.get('q3') == 'D':
        return 7
        
    # 7. FRESHMAN / ISOLATION
    if answers.get('q2') == 'B' or answers.get('q4') == 'B':
        return 3
        
    # 8. EMOTIONAL LONELINESS
    if answers.get('q2') == 'A' or answers.get('q7') == 'A':
        return 2

    # 9. COMPARISON TRAP
    if answers.get('q6') == 'A':
        return 9
        
    # 10. GENERAL / CATCH-ALL
    return 10

# Helper to render question with conditional "Other" text box
def render_question(key_id):
    q = questions[key_id]
    response = st.radio(q['text'], q['options'], index=None, key=f"rad_{key_id}")
    
    # If they selected the last option (which we know is "Other" for Q2-Q7)
    if response and "Other" in response:
        st.text_input("Please explain (optional):", key=f"text_{key_id}", placeholder="Type your answer here...")
        
    return response

# -----------------------------------------------------------------------------
# 5. UI RENDERING
# -----------------------------------------------------------------------------

# --- STEP 0: WELCOME SCREEN ---
if st.session_state.step == 0:
    st.title("BYU Mental Health & Connection Help")
    st.markdown("""
    College can be crowded, but it can also feel incredibly quiet. 
    
    You are not alone in feeling this way. In fact, research shows that over half of students currently feel disconnected.
    
    This short, anonymous assessment will help you identify **why** you might be feeling this way and point you toward the specific resources that match your situation.
    """)
    if st.button("Start Assessment"):
        next_step()
        st.rerun()

# --- STEP 1: SAFETY TRIAGE ---
elif st.session_state.step == 1:
    st.subheader("Safety Check")
    q = questions['q1']
    response = st.radio(q['text'], q['options'], index=None)
    
    if st.button("Next"):
        if response:
            st.session_state.answers['q1'] = q['keys'][q['options'].index(response)]
            if st.session_state.answers['q1'] == 'C':
                st.session_state.step = 99
            else:
                next_step()
            st.rerun()
        else:
            st.error("Please select an option to continue.")

# --- STEP 2: ROOT CAUSE (Questions 2-4) ---
elif st.session_state.step == 2:
    st.progress(33)
    st.subheader("Understanding Your Situation")
    
    a2 = render_question('q2')
    a3 = render_question('q3')
    a4 = render_question('q4')

    if st.button("Next"):
        if a2 and a3 and a4:
            # Map answers. If "Other" is in the string, map to 'OTHER' key
            st.session_state.answers['q2'] = 'OTHER' if "Other" in a2 else questions['q2']['keys'][questions['q2']['options'].index(a2)]
            st.session_state.answers['q3'] = 'OTHER' if "Other" in a3 else questions['q3']['keys'][questions['q3']['options'].index(a3)]
            st.session_state.answers['q4'] = 'OTHER' if "Other" in a4 else questions['q4']['keys'][questions['q4']['options'].index(a4)]
            next_step()
            st.rerun()
        else:
            st.error("Please answer all questions to continue.")

# --- STEP 3: SYMPTOMS (Questions 5-7) ---
elif st.session_state.step == 3:
    st.progress(66)
    st.subheader("How It Affects You")
    
    a5 = render_question('q5')
    a6 = render_question('q6')
    a7 = render_question('q7')

    if st.button("See My Results"):
        if a5 and a6 and a7:
            st.session_state.answers['q5'] = 'OTHER' if "Other" in a5 else questions['q5']['keys'][questions['q5']['options'].index(a5)]
            st.session_state.answers['q6'] = 'OTHER' if "Other" in a6 else questions['q6']['keys'][questions['q6']['options'].index(a6)]
            st.session_state.answers['q7'] = 'OTHER' if "Other" in a7 else questions['q7']['keys'][questions['q7']['options'].index(a7)]
            next_step()
            st.rerun()
        else:
            st.error("Please answer all questions to continue.")

# --- STEP 99: IMMEDIATE CRISIS SCREEN ---
elif st.session_state.step == 99:
    # REPLACED ST.ERROR WITH A CALMER LAYOUT
    st.markdown("""
    <div class="info-box">
        <h2 style="color: #58a6ff; margin-top:0;">Support Resources</h2>
        <p style="font-size: 1.1rem;">
            It sounds like you are carrying a really heavy burden right now. 
            We want to make sure you have someone to talk to who can help you navigate this safely.
        </p>
        <p><strong>Please consider using one of these resources:</strong></p>
        <ul>
            <li><strong>Crisis Text Line:</strong> Text <strong>HOME</strong> to <strong>741741</strong> (Free, 24/7)</li>
            <li><strong>BYU CAPS (Counseling & Psychological Services):</strong> Call <strong>801.422.3035</strong>. Free crisis support for students.</li>
            <li><strong>University Police:</strong> Call <strong>801.422.2222</strong> (If you are in immediate danger)</li>
        </ul>
        <p>You do not have to do this alone.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("") # Spacer
    if st.button("Restart"):
        restart()
        st.rerun()

# --- STEP 4: RESULTS & RESOURCES ---
elif st.session_state.step == 4:
    st.progress(100)
    
    group_id = determine_archetype(st.session_state.answers)
    
    results_content = {
        1: { "title": "Crisis Support", "msg": "Please reach out for immediate help.", "resources": [] },
        2: {
            "title": "Emotional Loneliness (Lonely in a Crowd)",
            "msg": "You are surrounded by people, yet you feel invisible. This is 'Emotional Loneliness.' It’s painful to be seen but not known. Your loneliness isn't about needing *more* people, but needing *deeper* connection.",
            "resources": [
                {"name": "End Social Isolation (Deepening Connections)", "url": "https://www.endsocialisolation.org/support/"},
                {"name": "BYU CAPS (Group Therapy)", "url": "https://caps.byu.edu/", "desc": "Counseling & Psychological Services: Free, confidential group sessions to connect with others."},
                {"name": "CDC: How Right Now", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html"}
            ]
        },
        3: {
            "title": "Transitional Isolation (Fish Out of Water)",
            "msg": "You are in a transition gap. You left your old support system and haven't built the new one yet. This is normal for students, but it requires action to fix.",
            "resources": [
                {"name": "BYU Clubs & Associations", "url": "https://clubs.byu.edu/"},
                {"name": "End Social Isolation: Breaking the Ice", "url": "https://www.endsocialisolation.org/support/"},
                {"name": "CDC: Finding Connection", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html"}
            ]
        },
        4: {
            "title": "Social Anxiety & Avoidance",
            "msg": "Your brain is perceiving social situations as a threat. The goal isn't to stop being lonely instantly, but to lower the anxiety so you can connect without panic.",
            "resources": [
                {"name": "BYU CAPS (Anxiety Services)", "url": "https://caps.byu.edu/", "desc": "Counseling & Psychological Services: Free, confidential support from licensed professionals."},
                {"name": "CDC: Coping with Stress", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html"},
                {"name": "Crisis Text Line (Text HOME to 741741)", "url": "https://www.crisistextline.org/topics/loneliness/"}
            ]
        },
        5: {
            "title": "Situational Grief & Loss",
            "msg": "You are grieving a connection. Whether it's a breakup or a passing, this is a specific kind of loneliness that takes time to heal. Be gentle with yourself.",
            "resources": [
                {"name": "BYU CAPS (Grief Support)", "url": "https://caps.byu.edu/", "desc": "Counseling & Psychological Services: Free, confidential counseling for navigating loss."},
                {"name": "Crisis Text Line (For late nights)", "url": "https://www.crisistextline.org/topics/loneliness/"},
                {"name": "End Social Isolation", "url": "https://www.endsocialisolation.org/support/"}
            ]
        },
        6: {
            "title": "Identity & Belonging",
            "msg": "It is exhausting to wear a mask. You deserve a space where you can be fully yourself without fear of judgment. Finding your specific community is key.",
            "resources": [
                {"name": "BYU CAPS (Safe Space)", "url": "https://caps.byu.edu/", "desc": "Counseling & Psychological Services: A free, safe, and confidential place to talk with a professional."},
                {"name": "USGA at BYU (Unofficial)", "url": "https://www.usgabyu.com/"},
                {"name": "End Social Isolation", "url": "https://www.endsocialisolation.org/support/"}
            ]
        },
        7: {
            "title": "Burnout & Overwhelm",
            "msg": "You are prioritizing survival over connection, but connection is part of survival. You need to schedule 'people time' just like you schedule class.",
            "resources": [
                {"name": "BYU CAPS (Stress Management)", "url": "https://caps.byu.edu/", "desc": "Counseling & Psychological Services: Free professional support for managing academic stress."},
                {"name": "EduMed Balance Resources", "url": "https://www.edumed.org/resources/student-loneliness-help-and-support/"},
                {"name": "CDC: Time Management & Health", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html"}
            ]
        },
        8: {
            "title": "Chronic Struggle",
            "msg": "This loneliness feels like a heavy blanket you can't shake. It might be linked to your brain chemistry (Depression), and that means it is treatable and not your fault.",
            "resources": [
                {"name": "BYU CAPS (Make an Appointment)", "url": "https://caps.byu.edu/", "desc": "Counseling & Psychological Services: Free, confidential therapy for full-time students."},
                {"name": "CDC: Understanding Mental Health", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html"},
                {"name": "Crisis Text Line", "url": "https://www.crisistextline.org/topics/loneliness/"}
            ]
        },
        9: {
            "title": "The Comparison Trap",
            "msg": "You are comparing your 'behind-the-scenes' with everyone else's 'highlight reel.' BYU culture makes this hard, but remember: looking happy isn't the same as being connected.",
            "resources": [
                {"name": "End Social Isolation (Social Media Limits)", "url": "https://www.endsocialisolation.org/support/"},
                {"name": "CDC: Building Self-Worth", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html"},
                {"name": "BYU CAPS", "url": "https://caps.byu.edu/", "desc": "Counseling & Psychological Services: Free support to help rebuild self-esteem."}
            ]
        },
        10: {
            "title": "General Loneliness",
            "msg": "Your answers indicate a unique situation or perhaps a mix of factors. Loneliness is complex, but these resources are the best place to start building your bridge back to connection.",
            "resources": [
                {"name": "End Social Isolation (Main Library)", "url": "https://www.endsocialisolation.org/support/"},
                {"name": "CDC Loneliness Page", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html"},
                {"name": "BYU CAPS", "url": "https://caps.byu.edu/", "desc": "Counseling & Psychological Services: Free, confidential support for any student."}
            ]
        }
    }
    
    result = results_content[group_id]
    
    st.header(result['title'])
    st.info(result['msg'])
    
    st.subheader("Recommended Resources for You")
    
    for res in result['resources']:
        # Check for description field and render it if present
        desc_html = f'<div class="resource-desc">{res["desc"]}</div>' if "desc" in res else ""
        
        st.markdown(f"""
        <div class="resource-box">
            <div class="resource-title">{res['name']}</div>
            {desc_html}
            <a href="{res['url']}" target="_blank" class="resource-link">Visit Website -></a>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    if st.button("Start Over"):
        restart()
        st.rerun()import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BYU Mental Health & Connection Help",
    page_icon="🧠",
    layout="centered"
)

# Custom CSS - DEEP NAVY / DARK MODE AESTHETIC
st.markdown("""
<style>
    /* General Font and Background */
    .stApp {
        background-color: #0b101d; /* Deep Midnight Navy */
        color: #c9d1d9; /* Soft grey-white for readability */
        font-family: 'Helvetica', sans-serif;
    }
    
    /* Headers */
    h1 {
        color: #ffffff;
        font-weight: 700;
        text-align: center;
        padding-bottom: 20px;
    }
    h2, h3 {
        color: #58a6ff; /* Soft Blue for headers (Github dark mode style) */
    }
    
    /* Text Styling */
    p, li, .stMarkdown {
        color: #c9d1d9;
        font-size: 1.05rem;
    }
    
    /* Question Card Styling */
    .stRadio > label {
        font-weight: bold;
        font-size: 1.1rem;
        color: #ffffff;
        padding-bottom: 10px;
        display: block;
    }
    div.row-widget.stRadio > div {
        background-color: #161b22; /* Dark Navy-Grey */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.6);
        border: 1px solid #30363d;
    }
    
    /* Radio Button Text Color */
    .stRadio div[role='radiogroup'] > label {
        color: #c9d1d9 !important;
    }
    
    /* Text Input Styling for 'Other' */
    .stTextInput > div > div > input {
        border-radius: 5px;
        background-color: #0d1117;
        color: white;
        border: 1px solid #30363d;
    }
    
    /* Button Styling */
    .stButton > button {
        background-color: #002E5D; /* Darker BYU Navy */
        color: white;
        border-radius: 50px;
        padding: 10px 24px;
        font-weight: bold;
        border: 1px solid #1f6feb;
        width: 100%;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: #001f3f; /* Even darker on hover */
        border-color: #58a6ff;
        color: white;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #002E5D; /* BYU Navy */
    }

    /* Resource Box Styling */
    .resource-box {
        background-color: #161b22;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #002E5D; /* BYU Navy Border */
        margin-bottom: 15px;
        border: 1px solid #30363d;
    }
    .resource-title {
        font-weight: bold;
        color: #58a6ff;
        font-size: 1.1rem;
        margin-bottom: 5px;
    }
    .resource-desc {
        color: #c9d1d9;
        font-size: 0.9rem;
        margin-bottom: 8px;
        font-style: italic;
    }
    .resource-link {
        color: #58a6ff;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 5px;
    }
    .resource-link:hover {
        color: #ffffff;
        text-decoration: underline;
    }
    
    /* Crisis/Info Box Styling */
    .info-box {
        background-color: #161b22;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #30363d;
        color: #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. STATE MANAGEMENT
# -----------------------------------------------------------------------------
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

def next_step():
    st.session_state.step += 1

def restart():
    st.session_state.step = 0
    st.session_state.answers = {}

# -----------------------------------------------------------------------------
# 3. QUESTIONNAIRE DATA
# -----------------------------------------------------------------------------
questions = {
    # Q1 kept strict for safety triage - NO 'Other' option here
    "q1": {
        "text": "Right now, in this exact moment, how safe do you feel?",
        "options": [
            "I’m okay, just struggling with feelings.",
            "I’m feeling overwhelmed, but I’m safe.",
            "I feel unsafe or am having thoughts of hurting myself or others."
        ],
        "keys": ["A", "B", "C"]
    },
    "q2": {
        "text": "Which of these best describes your current social environment?",
        "options": [
            "I have people around me (roommates, classmates), but I don’t feel connected to any of them.",
            "I am physically alone most of the time; I don't really have a circle of friends here yet.",
            "I have friends, but I’ve recently lost a specific person (breakup, falling out, passing away).",
            "I have opportunities to socialize, but I get too nervous or anxious to go.",
            "I have friends, but I feel like I have to hide who I really am to fit in.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "E", "OTHER"]
    },
    "q3": {
        "text": "When you think about trying to make new friends, what is your immediate gut reaction?",
        "options": [
            "It's pointless; nobody understands me anyway.",
            "I don't even know where to start looking.",
            "I want to, but I'm terrified I'll say the wrong thing or be judged.",
            "I just don't have the energy or time; school/work is drowning me.",
            "I miss the person/group I used to have; no one else compares.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "E", "OTHER"]
    },
    "q4": {
        "text": "How long have you felt this way?",
        "options": [
            "It’s been a constant feeling for years, even before college.",
            "It started when I came to BYU/college.",
            "It’s very recent (last few weeks/months) due to a specific event.",
            "It comes and goes in waves.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "OTHER"]
    },
    "q5": {
        "text": "How is this loneliness affecting your daily life?",
        "options": [
            "I’m functioning okay, just feeling sad or empty when I’m alone.",
            "It’s hard to get out of bed; I feel heavy, hopeless, or numb.",
            "My heart races, I feel shaky, or I panic when I have to talk to people.",
            "I’m exhausted, not sleeping well, and physically drained.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "OTHER"]
    },
    "q6": {
        "text": "When you are alone, what do you usually do?",
        "options": [
            "Scroll social media and see everyone else having fun.",
            "Sleep or stare at the ceiling.",
            "Focus intensely on schoolwork to distract myself.",
            "Ruminate (think over and over) about what is 'wrong' with me.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "OTHER"]
    },
    "q7": {
        "text": "If you could wave a magic wand and fix one thing right now, what would it be?",
        "options": [
            "To have just one person who really 'gets' me.",
            "To have a big group of friends to hang out with on weekends.",
            "To stop feeling so afraid of social interaction.",
            "To stop feeling this deep sadness/numbness.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "OTHER"]
    }
}

# -----------------------------------------------------------------------------
# 4. LOGIC ENGINE
# -----------------------------------------------------------------------------
def determine_archetype(answers):
    """
    Analyzes answers. If 'OTHER' is used too frequently, or if no specific pattern is matched,
    it defaults to Group 10 (General).
    """
    
    # 1. CRISIS CASE (Safety First) - Explicit check, cannot be 'Other'
    if answers.get('q1') == 'C':
        return 1
    
    # Check for too many "Other" answers (e.g., 3 or more)
    other_count = list(answers.values()).count('OTHER')
    if other_count >= 3:
        return 10
        
    # 2. CHRONIC / CLINICAL STRUGGLE
    if answers.get('q4') == 'A' or answers.get('q5') == 'B':
        return 8
        
    # 3. SITUATIONAL / RECENTLY HEARTBROKEN
    if answers.get('q2') == 'C' or answers.get('q4') == 'C' or answers.get('q3') == 'E':
        return 5

    # 4. SOCIALLY ANXIOUS
    if answers.get('q2') == 'D' or answers.get('q3') == 'C' or answers.get('q5') == 'C':
        return 4
        
    # 5. IDENTITY ISOLATED
    if answers.get('q2') == 'E':
        return 6
        
    # 6. BURNOUT
    if answers.get('q3') == 'D':
        return 7
        
    # 7. FRESHMAN / ISOLATION
    if answers.get('q2') == 'B' or answers.get('q4') == 'B':
        return 3
        
    # 8. EMOTIONAL LONELINESS
    if answers.get('q2') == 'A' or answers.get('q7') == 'A':
        return 2

    # 9. COMPARISON TRAP
    if answers.get('q6') == 'A':
        return 9
        
    # 10. GENERAL / CATCH-ALL
    return 10

# Helper to render question with conditional "Other" text box
def render_question(key_id):
    q = questions[key_id]
    response = st.radio(q['text'], q['options'], index=None, key=f"rad_{key_id}")
    
    # If they selected the last option (which we know is "Other" for Q2-Q7)
    if response and "Other" in response:
        st.text_input("Please explain (optional):", key=f"text_{key_id}", placeholder="Type your answer here...")
        
    return response

# -----------------------------------------------------------------------------
# 5. UI RENDERING
# -----------------------------------------------------------------------------

# --- STEP 0: WELCOME SCREEN ---
if st.session_state.step == 0:
    st.title("BYU Mental Health & Connection Help")
    st.markdown("""
    College can be crowded, but it can also feel incredibly quiet. 
    
    You are not alone in feeling this way. In fact, research shows that over half of students currently feel disconnected.
    
    This short, anonymous assessment will help you identify **why** you might be feeling this way and point you toward the specific resources that match your situation.
    """)
    if st.button("Start Assessment"):
        next_step()
        st.rerun()

# --- STEP 1: SAFETY TRIAGE ---
elif st.session_state.step == 1:
    st.subheader("Safety Check")
    q = questions['q1']
    response = st.radio(q['text'], q['options'], index=None)
    
    if st.button("Next"):
        if response:
            st.session_state.answers['q1'] = q['keys'][q['options'].index(response)]
            if st.session_state.answers['q1'] == 'C':
                st.session_state.step = 99
            else:
                next_step()
            st.rerun()
        else:
            st.error("Please select an option to continue.")

# --- STEP 2: ROOT CAUSE (Questions 2-4) ---
elif st.session_state.step == 2:
    st.progress(33)
    st.subheader("Understanding Your Situation")
    
    a2 = render_question('q2')
    a3 = render_question('q3')
    a4 = render_question('q4')

    if st.button("Next"):
        if a2 and a3 and a4:
            # Map answers. If "Other" is in the string, map to 'OTHER' key
            st.session_state.answers['q2'] = 'OTHER' if "Other" in a2 else questions['q2']['keys'][questions['q2']['options'].index(a2)]
            st.session_state.answers['q3'] = 'OTHER' if "Other" in a3 else questions['q3']['keys'][questions['q3']['options'].index(a3)]
            st.session_state.answers['q4'] = 'OTHER' if "Other" in a4 else questions['q4']['keys'][questions['q4']['options'].index(a4)]
            next_step()
            st.rerun()
        else:
            st.error("Please answer all questions to continue.")

# --- STEP 3: SYMPTOMS (Questions 5-7) ---
elif st.session_state.step == 3:
    st.progress(66)
    st.subheader("How It Affects You")
    
    a5 = render_question('q5')
    a6 = render_question('q6')
    a7 = render_question('q7')

    if st.button("See My Results"):
        if a5 and a6 and a7:
            st.session_state.answers['q5'] = 'OTHER' if "Other" in a5 else questions['q5']['keys'][questions['q5']['options'].index(a5)]
            st.session_state.answers['q6'] = 'OTHER' if "Other" in a6 else questions['q6']['keys'][questions['q6']['options'].index(a6)]
            st.session_state.answers['q7'] = 'OTHER' if "Other" in a7 else questions['q7']['keys'][questions['q7']['options'].index(a7)]
            next_step()
            st.rerun()
        else:
            st.error("Please answer all questions to continue.")

# --- STEP 99: IMMEDIATE CRISIS SCREEN ---
elif st.session_state.step == 99:
    # REPLACED ST.ERROR WITH A CALMER LAYOUT
    st.markdown("""
    <div class="info-box">
        <h2 style="color: #58a6ff; margin-top:0;">Support Resources</h2>
        <p style="font-size: 1.1rem;">
            It sounds like you are carrying a really heavy burden right now. 
            We want to make sure you have someone to talk to who can help you navigate this safely.
        </p>
        <p><strong>Please consider using one of these resources:</strong></p>
        <ul>
            <li><strong>Crisis Text Line:</strong> Text <strong>HOME</strong> to <strong>741741</strong> (Free, 24/7)</li>
            <li><strong>BYU CAPS (Counseling & Psychological Services):</strong> Call <strong>801.422.3035</strong>. Free crisis support for students.</li>
            <li><strong>University Police:</strong> Call <strong>801.422.2222</strong> (If you are in immediate danger)</li>
        </ul>
        <p>You do not have to do this alone.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("") # Spacer
    if st.button("Restart"):
        restart()
        st.rerun()

# --- STEP 4: RESULTS & RESOURCES ---
elif st.session_state.step == 4:
    st.progress(100)
    
    group_id = determine_archetype(st.session_state.answers)
    
    results_content = {
        1: { "title": "Crisis Support", "msg": "Please reach out for immediate help.", "resources": [] },
        2: {
            "title": "Emotional Loneliness (Lonely in a Crowd)",
            "msg": "You are surrounded by people, yet you feel invisible. This is 'Emotional Loneliness.' It’s painful to be seen but not known. Your loneliness isn't about needing *more* people, but needing *deeper* connection.",
            "resources": [
                {"name": "End Social Isolation (Deepening Connections)", "url": "https://www.endsocialisolation.org/support/"},
                {"name": "BYU CAPS (Group Therapy)", "url": "https://caps.byu.edu/", "desc": "Counseling & Psychological Services: Free, confidential group sessions to connect with others."},
                {"name": "CDC: How Right Now", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html"}
            ]
        },
        3: {
            "title": "Transitional Isolation (Fish Out of Water)",
            "msg": "You are in a transition gap. You left your old support system and haven't built the new one yet. This is normal for students, but it requires action to fix.",
            "resources": [
                {"name": "BYU Clubs & Associations", "url": "https://clubs.byu.edu/"},
                {"name": "End Social Isolation: Breaking the Ice", "url": "https://www.endsocialisolation.org/support/"},
                {"name": "CDC: Finding Connection", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html"}
            ]
        },
        4: {
            "title": "Social Anxiety & Avoidance",
            "msg": "Your brain is perceiving social situations as a threat. The goal isn't to stop being lonely instantly, but to lower the anxiety so you can connect without panic.",
            "resources": [
                {"name": "BYU CAPS (Anxiety Services)", "url": "https://caps.byu.edu/", "desc": "Counseling & Psychological Services: Free, confidential support from licensed professionals."},
                {"name": "CDC: Coping with Stress", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html"},
                {"name": "Crisis Text Line (Text HOME to 741741)", "url": "https://www.crisistextline.org/topics/loneliness/"}
            ]
        },
        5: {
            "title": "Situational Grief & Loss",
            "msg": "You are grieving a connection. Whether it's a breakup or a passing, this is a specific kind of loneliness that takes time to heal. Be gentle with yourself.",
            "resources": [
                {"name": "BYU CAPS (Grief Support)", "url": "https://caps.byu.edu/", "desc": "Counseling & Psychological Services: Free, confidential counseling for navigating loss."},
                {"name": "Crisis Text Line (For late nights)", "url": "https://www.crisistextline.org/topics/loneliness/"},
                {"name": "End Social Isolation", "url": "https://www.endsocialisolation.org/support/"}
            ]
        },
        6: {
            "title": "Identity & Belonging",
            "msg": "It is exhausting to wear a mask. You deserve a space where you can be fully yourself without fear of judgment. Finding your specific community is key.",
            "resources": [
                {"name": "BYU CAPS (Safe Space)", "url": "https://caps.byu.edu/", "desc": "Counseling & Psychological Services: A free, safe, and confidential place to talk with a professional."},
                {"name": "USGA at BYU (Unofficial)", "url": "https://www.usgabyu.com/"},
                {"name": "End Social Isolation", "url": "https://www.endsocialisolation.org/support/"}
            ]
        },
        7: {
            "title": "Burnout & Overwhelm",
            "msg": "You are prioritizing survival over connection, but connection is part of survival. You need to schedule 'people time' just like you schedule class.",
            "resources": [
                {"name": "BYU CAPS (Stress Management)", "url": "https://caps.byu.edu/", "desc": "Counseling & Psychological Services: Free professional support for managing academic stress."},
                {"name": "EduMed Balance Resources", "url": "https://www.edumed.org/resources/student-loneliness-help-and-support/"},
                {"name": "CDC: Time Management & Health", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html"}
            ]
        },
        8: {
            "title": "Chronic Struggle",
            "msg": "This loneliness feels like a heavy blanket you can't shake. It might be linked to your brain chemistry (Depression), and that means it is treatable and not your fault.",
            "resources": [
                {"name": "BYU CAPS (Make an Appointment)", "url": "https://caps.byu.edu/", "desc": "Counseling & Psychological Services: Free, confidential therapy for full-time students."},
                {"name": "CDC: Understanding Mental Health", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html"},
                {"name": "Crisis Text Line", "url": "https://www.crisistextline.org/topics/loneliness/"}
            ]
        },
        9: {
            "title": "The Comparison Trap",
            "msg": "You are comparing your 'behind-the-scenes' with everyone else's 'highlight reel.' BYU culture makes this hard, but remember: looking happy isn't the same as being connected.",
            "resources": [
                {"name": "End Social Isolation (Social Media Limits)", "url": "https://www.endsocialisolation.org/support/"},
                {"name": "CDC: Building Self-Worth", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html"},
                {"name": "BYU CAPS", "url": "https://caps.byu.edu/", "desc": "Counseling & Psychological Services: Free support to help rebuild self-esteem."}
            ]
        },
        10: {
            "title": "General Loneliness",
            "msg": "Your answers indicate a unique situation or perhaps a mix of factors. Loneliness is complex, but these resources are the best place to start building your bridge back to connection.",
            "resources": [
                {"name": "End Social Isolation (Main Library)", "url": "https://www.endsocialisolation.org/support/"},
                {"name": "CDC Loneliness Page", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html"},
                {"name": "BYU CAPS", "url": "https://caps.byu.edu/", "desc": "Counseling & Psychological Services: Free, confidential support for any student."}
            ]
        }
    }
    
    result = results_content[group_id]
    
    st.header(result['title'])
    st.info(result['msg'])
    
    st.subheader("Recommended Resources for You")
    
    for res in result['resources']:
        # Check for description field and render it if present
        desc_html = f'<div class="resource-desc">{res["desc"]}</div>' if "desc" in res else ""
        
        st.markdown(f"""
        <div class="resource-box">
            <div class="resource-title">{res['name']}</div>
            {desc_html}
            <a href="{res['url']}" target="_blank" class="resource-link">Visit Website -></a>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    if st.button("Start Over"):
        restart()
        st.rerun()
