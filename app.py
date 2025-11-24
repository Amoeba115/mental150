import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BYU Connection Compass",
    page_icon="🧭",
    layout="centered"
)

# Custom CSS to make the app look less "data sciency" and more like a mental health resource
st.markdown("""
<style>
    /* General Font and Background */
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Helvetica', sans-serif;
    }
    
    /* Headers */
    h1 {
        color: #002E5D; /* BYU Navy */
        font-weight: 700;
        text-align: center;
        padding-bottom: 20px;
    }
    h2, h3 {
        color: #002E5D;
    }
    
    /* Question Card Styling */
    .stRadio > label {
        font-weight: bold;
        font-size: 1.1rem;
        color: #333;
    }
    div.row-widget.stRadio > div {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Button Styling */
    .stButton > button {
        background-color: #0062B8; /* BYU Royal */
        color: white;
        border-radius: 50px;
        padding: 10px 24px;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #002E5D;
        color: white;
    }

    /* Resource Box Styling */
    .resource-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #0062B8;
        margin-bottom: 10px;
    }
    .resource-title {
        font-weight: bold;
        color: #002E5D;
        font-size: 1.1rem;
    }
    .resource-link {
        color: #0062B8;
        text-decoration: none;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. STATE MANAGEMENT
# -----------------------------------------------------------------------------
# Initialize session state variables to track progress and answers
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# Helper function to move to next step
def next_step():
    st.session_state.step += 1

def restart():
    st.session_state.step = 0
    st.session_state.answers = {}

# -----------------------------------------------------------------------------
# 3. QUESTIONNAIRE DATA
# -----------------------------------------------------------------------------
# Defined strictly based on the design we created
questions = {
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
            "I have friends, but I feel like I have to hide who I really am to fit in."
        ],
        "keys": ["A", "B", "C", "D", "E"]
    },
    "q3": {
        "text": "When you think about trying to make new friends, what is your immediate gut reaction?",
        "options": [
            "It's pointless; nobody understands me anyway.",
            "I don't even know where to start looking.",
            "I want to, but I'm terrified I'll say the wrong thing or be judged.",
            "I just don't have the energy or time; school/work is drowning me.",
            "I miss the person/group I used to have; no one else compares."
        ],
        "keys": ["A", "B", "C", "D", "E"]
    },
    "q4": {
        "text": "How long have you felt this way?",
        "options": [
            "It’s been a constant feeling for years, even before college.",
            "It started when I came to BYU/college.",
            "It’s very recent (last few weeks/months) due to a specific event.",
            "It comes and goes in waves."
        ],
        "keys": ["A", "B", "C", "D"]
    },
    "q5": {
        "text": "How is this loneliness affecting your daily life?",
        "options": [
            "I’m functioning okay, just feeling sad or empty when I’m alone.",
            "It’s hard to get out of bed; I feel heavy, hopeless, or numb.",
            "My heart races, I feel shaky, or I panic when I have to talk to people.",
            "I’m exhausted, not sleeping well, and physically drained."
        ],
        "keys": ["A", "B", "C", "D"]
    },
    "q6": {
        "text": "When you are alone, what do you usually do?",
        "options": [
            "Scroll social media and see everyone else having fun.",
            "Sleep or stare at the ceiling.",
            "Focus intensely on schoolwork to distract myself.",
            "Ruminate (think over and over) about what is 'wrong' with me."
        ],
        "keys": ["A", "B", "C", "D"]
    },
    "q7": {
        "text": "If you could wave a magic wand and fix one thing right now, what would it be?",
        "options": [
            "To have just one person who really 'gets' me.",
            "To have a big group of friends to hang out with on weekends.",
            "To stop feeling so afraid of social interaction.",
            "To stop feeling this deep sadness/numbness."
        ],
        "keys": ["A", "B", "C", "D"]
    }
}

# -----------------------------------------------------------------------------
# 4. LOGIC ENGINE
# -----------------------------------------------------------------------------
def determine_archetype(answers):
    """
    Analyzes the answers dictionary and returns the specific Group ID, Title, and Message.
    Hierarchy: Safety > Clinical > Situational > Anxiety > Identity > Burnout > Isolation > Emotional > Comparison
    """
    
    # 1. CRISIS CASE (Safety First)
    if answers.get('q1') == 'C':
        return 1
        
    # 2. CHRONIC / CLINICAL STRUGGLE
    # Long term duration OR Severe depressive symptoms
    if answers.get('q4') == 'A' or answers.get('q5') == 'B':
        return 8
        
    # 3. SITUATIONAL / RECENTLY HEARTBROKEN
    # Loss of specific person OR Recent acute onset OR Missing specific group
    if answers.get('q2') == 'C' or answers.get('q4') == 'C' or answers.get('q3') == 'E':
        return 5

    # 4. SOCIALLY ANXIOUS
    # Nervous to go OR Terrified of judgment OR Panic symptoms
    if answers.get('q2') == 'D' or answers.get('q3') == 'C' or answers.get('q5') == 'C':
        return 4
        
    # 5. IDENTITY ISOLATED
    # Hiding who they are
    if answers.get('q2') == 'E':
        return 6
        
    # 6. BURNOUT
    # No energy/time
    if answers.get('q3') == 'D':
        return 7
        
    # 7. FRESHMAN / ISOLATION
    # Physically alone OR Started when came to college
    if answers.get('q2') == 'B' or answers.get('q4') == 'B':
        return 3
        
    # 8. EMOTIONAL LONELINESS (Lonely in a crowd)
    # People around but not connected OR Wants one person who 'gets' them
    if answers.get('q2') == 'A' or answers.get('q7') == 'A':
        return 2

    # 9. COMPARISON TRAP
    # Scrolling social media
    if answers.get('q6') == 'A':
        return 9
        
    # 10. GENERAL / CATCH-ALL
    return 10

# -----------------------------------------------------------------------------
# 5. UI RENDERING
# -----------------------------------------------------------------------------

# --- STEP 0: WELCOME SCREEN ---
if st.session_state.step == 0:
    st.title("Connection Compass")
    st.markdown("""
    College can be crowded, but it can also feel incredibly quiet. 
    
    You are not alone in feeling this way. In fact, research shows that over half of students currently feel disconnected.
    
    This short, anonymous check-in will help you identify **why** you might be feeling this way and point you toward the specific resources that match your situation.
    """)
    if st.button("Start Check-in"):
        next_step()
        st.rerun()

# --- STEP 1: SAFETY TRIAGE ---
elif st.session_state.step == 1:
    st.subheader("Safety Check")
    q = questions['q1']
    response = st.radio(q['text'], q['options'], index=None)
    
    if st.button("Next"):
        if response:
            # Map the text answer back to the Key (A, B, C)
            st.session_state.answers['q1'] = q['keys'][q['options'].index(response)]
            
            # Immediate Crisis Redirect
            if st.session_state.answers['q1'] == 'C':
                st.session_state.step = 99 # Jump to crisis page
            else:
                next_step()
            st.rerun()
        else:
            st.error("Please select an option to continue.")

# --- STEP 2: ROOT CAUSE (Questions 2-4) ---
elif st.session_state.step == 2:
    st.progress(33)
    st.subheader("Understanding Your Situation")
    
    # Question 2
    q2 = questions['q2']
    a2 = st.radio(q2['text'], q2['options'], index=None, key="rad_q2")
    
    # Question 3
    q3 = questions['q3']
    a3 = st.radio(q3['text'], q3['options'], index=None, key="rad_q3")
    
    # Question 4
    q4 = questions['q4']
    a4 = st.radio(q4['text'], q4['options'], index=None, key="rad_q4")

    if st.button("Next"):
        if a2 and a3 and a4:
            st.session_state.answers['q2'] = q2['keys'][q2['options'].index(a2)]
            st.session_state.answers['q3'] = q3['keys'][q3['options'].index(a3)]
            st.session_state.answers['q4'] = q4['keys'][q4['options'].index(a4)]
            next_step()
            st.rerun()
        else:
            st.error("Please answer all questions to continue.")

# --- STEP 3: SYMPTOMS (Questions 5-7) ---
elif st.session_state.step == 3:
    st.progress(66)
    st.subheader("How It Affects You")
    
    # Question 5
    q5 = questions['q5']
    a5 = st.radio(q5['text'], q5['options'], index=None, key="rad_q5")
    
    # Question 6
    q6 = questions['q6']
    a6 = st.radio(q6['text'], q6['options'], index=None, key="rad_q6")
    
    # Question 7
    q7 = questions['q7']
    a7 = st.radio(q7['text'], q7['options'], index=None, key="rad_q7")

    if st.button("See My Results"):
        if a5 and a6 and a7:
            st.session_state.answers['q5'] = q5['keys'][q5['options'].index(a5)]
            st.session_state.answers['q6'] = q6['keys'][q6['options'].index(a6)]
            st.session_state.answers['q7'] = q7['keys'][q7['options'].index(a7)]
            next_step()
            st.rerun()
        else:
            st.error("Please answer all questions to continue.")

# --- STEP 99: IMMEDIATE CRISIS SCREEN ---
elif st.session_state.step == 99:
    st.error("⚠️ IMMEDIATE SUPPORT NEEDED")
    st.markdown("""
    ### You are not alone, and there is help available right now.
    Based on your answer, we want to make sure you speak to a human immediately.
    
    **Please use one of these resources right now:**
    
    * **Crisis Text Line:** Text **HOME** to **741741** (Free, 24/7)
    * **BYU CAPS Crisis Service:** Call **801.422.3035** (During business hours)
    * **University Police:** Call **801.422.2222** (If you are in immediate danger)
    
    You do not have to carry this heavy burden by yourself.
    """)
    if st.button("Restart"):
        restart()
        st.rerun()

# --- STEP 4: RESULTS & RESOURCES ---
elif st.session_state.step == 4:
    st.progress(100)
    
    # Determine the archetype
    group_id = determine_archetype(st.session_state.answers)
    
    # Content Dictionary for Results
    results_content = {
        1: { # Covered by Step 99, but here for fallback
            "title": "Crisis Support",
            "msg": "Please reach out for immediate help.",
            "resources": [] 
        },
        2: {
            "title": "Emotional Loneliness (Lonely in a Crowd)",
            "msg": "You are surrounded by people, yet you feel invisible. This is 'Emotional Loneliness.' It’s painful to be seen but not known. Your loneliness isn't about needing *more* people, but needing *deeper* connection.",
            "resources": [
                {"name": "End Social Isolation (Deepening Connections)", "url": "https://www.endsocialisolation.org/support/"},
                {"name": "BYU CAPS Group Therapy", "url": "https://caps.byu.edu/"},
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
                {"name": "BYU CAPS (Anxiety Services)", "url": "https://caps.byu.edu/"},
                {"name": "CDC: Coping with Stress", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html"},
                {"name": "Crisis Text Line (Text HOME to 741741)", "url": "https://www.crisistextline.org/topics/loneliness/"}
            ]
        },
        5: {
            "title": "Situational Grief & Loss",
            "msg": "You are grieving a connection. Whether it's a breakup or a passing, this is a specific kind of loneliness that takes time to heal. Be gentle with yourself.",
            "resources": [
                {"name": "BYU CAPS (Grief Support)", "url": "https://caps.byu.edu/"},
                {"name": "Crisis Text Line (For late nights)", "url": "https://www.crisistextline.org/topics/loneliness/"},
                {"name": "End Social Isolation", "url": "https://www.endsocialisolation.org/support/"}
            ]
        },
        6: {
            "title": "Identity & Belonging",
            "msg": "It is exhausting to wear a mask. You deserve a space where you can be fully yourself without fear of judgment. Finding your specific community is key.",
            "resources": [
                {"name": "BYU CAPS (Safe Space)", "url": "https://caps.byu.edu/"},
                {"name": "USGA at BYU (Unofficial)", "url": "https://www.usgabyu.com/"},
                {"name": "End Social Isolation", "url": "https://www.endsocialisolation.org/support/"}
            ]
        },
        7: {
            "title": "Burnout & Overwhelm",
            "msg": "You are prioritizing survival over connection, but connection is part of survival. You need to schedule 'people time' just like you schedule class.",
            "resources": [
                {"name": "BYU CAPS (Stress Management)", "url": "https://caps.byu.edu/"},
                {"name": "EduMed Balance Resources", "url": "https://www.edumed.org/resources/student-loneliness-help-and-support/"},
                {"name": "CDC: Time Management & Health", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html"}
            ]
        },
        8: {
            "title": "Chronic Struggle",
            "msg": "This loneliness feels like a heavy blanket you can't shake. It might be linked to your brain chemistry (Depression), and that means it is treatable and not your fault.",
            "resources": [
                {"name": "BYU CAPS (Make an Appointment)", "url": "https://caps.byu.edu/"},
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
                {"name": "BYU CAPS", "url": "https://caps.byu.edu/"}
            ]
        },
        10: {
            "title": "General Loneliness",
            "msg": "Loneliness is complex and unique to everyone. While we couldn't pin down your exact 'type,' these resources are the best place to start.",
            "resources": [
                {"name": "End Social Isolation (Main Library)", "url": "https://www.endsocialisolation.org/support/"},
                {"name": "CDC Loneliness Page", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html"},
                {"name": "BYU CAPS", "url": "https://caps.byu.edu/"}
            ]
        }
    }
    
    result = results_content[group_id]
    
    st.header(result['title'])
    st.info(result['msg'])
    
    st.subheader("Recommended Resources for You")
    
    for res in result['resources']:
        st.markdown(f"""
        <div class="resource-box">
            <div class="resource-title">{res['name']}</div>
            <a href="{res['url']}" target="_blank" class="resource-link">Visit Website -></a>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    if st.button("Start Over"):
        restart()
        st.rerun()
