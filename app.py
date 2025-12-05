import streamlit as st
import streamlit.components.v1 as components
import time

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Student Connection & Mental Health Guide",
    page_icon="🐞",
    layout="centered"
)

# -----------------------------------------------------------------------------
# 2. SCROLL ANCHOR & LOGIC
# -----------------------------------------------------------------------------
# This invisible div is the "target" we will scroll to
st.markdown('<div id="top_of_page"></div>', unsafe_allow_html=True)

# Initialize scroll state if not present
if 'scroll_to_top' not in st.session_state:
    st.session_state.scroll_to_top = False

# JavaScript to force scroll to anchor
if st.session_state.scroll_to_top:
    js = """
    <script>
        // We use a slight delay to ensure the new content is rendered
        setTimeout(function() {
            try {
                // Find the anchor element in the parent document (the main app)
                var anchor = window.parent.document.getElementById("top_of_page");
                if (anchor) {
                    // This method is more robust on mobile than window.scrollTo
                    anchor.scrollIntoView({behavior: "instant", block: "start"});
                }
            } catch(e) {
                console.log("Scroll error:", e);
            }
        }, 100);
    </script>
    """
    components.html(js, height=0, width=0)
    st.session_state.scroll_to_top = False

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
        padding-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        color: #58a6ff;
        font-weight: bold;
        margin-bottom: 20px;
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

    /* Disclaimer Footer */
    .disclaimer {
        font-size: 0.8rem;
        color: #6e7681;
        text-align: center;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #30363d;
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
    st.session_state.scroll_to_top = True # Trigger scroll on next reload

def restart():
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.scroll_to_top = True # Trigger scroll on next reload

# -----------------------------------------------------------------------------
# 3. QUESTIONNAIRE DATA
# -----------------------------------------------------------------------------
questions = {
    # Q0: Initial Question
    "q0": {
        "text": "Before we begin, who are you looking for resources for today?",
        "options": [
            "For myself.",
            "I want to learn how to support a friend or classmate."
        ],
        "keys": ["SELF", "OTHER_PERSON"]
    },
    # Q1: Safety Check
    "q1": {
        "text": "How are you feeling about your safety right now?",
        "options": [
            "I’m managing okay, just working through some difficult emotions.",
            "I feel overwhelmed, but I am safe.",
            "I don't feel safe, or I'm having thoughts about hurting myself or others."
        ],
        "keys": ["A", "B", "C"]
    },
    "q2": {
        "text": "Which statement resonates most with your current social experience?",
        "options": [
            "I’m around people often (roommates, classmates), but I don't feel a deep connection with them.",
            "I spend a lot of time alone and haven't found my group yet.",
            "I had a close connection, but that has recently changed (due to a breakup, loss, or drift).",
            "I want to socialize, but nervousness often holds me back.",
            "I have friends, but I feel I can't be my full, authentic self around them.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "E", "OTHER"]
    },
    "q3": {
        "text": "When you think about reaching out to make new friends, what comes to mind?",
        "options": [
            "I worry that I won't be fully understood.",
            "I’m not quite sure where to begin.",
            "I want to, but I feel anxious about saying the wrong thing.",
            "I honestly feel too drained or busy to try right now.",
            "I find myself missing a specific connection I used to have.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "E", "OTHER"]
    },
    "q4": {
        "text": "How long have you been navigating these feelings?",
        "options": [
            "This has been a familiar feeling for a long time.",
            "It mostly started during this phase of my life (college/BYU).",
            "It is very recent and linked to a specific event.",
            "It tends to come and go.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "OTHER"]
    },
    "q5": {
        "text": "How is this affecting your day-to-day well-being?",
        "options": [
            "I'm managing my daily tasks, but I feel a bit empty when I'm alone.",
            "I find it difficult to find motivation, and things feel heavier than usual.",
            "I feel physically anxious (racing heart, shakiness) in social situations.",
            "I feel physically exhausted or drained.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "OTHER"]
    },
    "q6": {
        "text": "When you are by yourself, where does your focus tend to go?",
        "options": [
            "I often check social media and compare my life to others.",
            "I tend to sleep or zone out to escape.",
            "I distract myself with work or study.",
            "I find myself replaying thoughts about what I could do differently.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "OTHER"]
    },
    "q7": {
        "text": "If you could change one aspect of your situation today, what would it be?",
        "options": [
            "To find someone who truly understands me.",
            "To have a community to do things with.",
            "To feel more confident and calm when talking to people.",
            "To lift this feeling of heaviness or sadness.",
            "Other (please explain)"
        ],
        "keys": ["A", "B", "C", "D", "OTHER"]
    }
}

# -----------------------------------------------------------------------------
# 4. LOGIC ENGINE (ROBUST MULTI-RESULT)
# -----------------------------------------------------------------------------
def determine_matches(answers):
    """
    Analyzes answers and collects ALL matching categories (Robust/Multi-result).
    Returns a list of group IDs.
    """
    matches = []

    # 1. CRISIS CASE (Safety First) - Exclusive
    if answers.get('q1') == 'C':
        return [1]
    
    # 2. Check for "Other" overload - Exclusive if nothing else works
    other_count = list(answers.values()).count('OTHER')
    if other_count >= 3:
        return [10]
        
    # --- NON-EXCLUSIVE CHECKS (Collect all matches) ---
    
    # Chronic / Clinical Struggle
    if answers.get('q4') == 'A' or answers.get('q5') == 'B':
        matches.append(8)
        
    # Situational / Grief
    if answers.get('q2') == 'C' or answers.get('q4') == 'C' or answers.get('q3') == 'E':
        matches.append(5)

    # Social Anxiety
    if answers.get('q2') == 'D' or answers.get('q3') == 'C' or answers.get('q5') == 'C':
        matches.append(4)
        
    # Identity Isolated
    if answers.get('q2') == 'E':
        matches.append(6)
        
    # Burnout
    if answers.get('q3') == 'D':
        matches.append(7)
        
    # Freshman / Isolation
    if answers.get('q2') == 'B' or answers.get('q4') == 'B':
        matches.append(3)
        
    # Emotional Loneliness
    if answers.get('q2') == 'A' or answers.get('q7') == 'A':
        matches.append(2)

    # Comparison Trap
    if answers.get('q6') == 'A':
        matches.append(9)
        
    # Fallback: If no specific triggers found, use General
    if not matches:
        matches.append(10)
        
    # Limit to top 3 matches to avoid overwhelming the user
    return list(set(matches))[:3]

# Helper to render question with conditional "Other" text box
def render_question(key_id):
    q = questions[key_id]
    response = st.radio(q['text'], q['options'], index=None, key=f"rad_{key_id}")
    
    if response and "Other" in response:
        st.text_input("Please explain (optional):", key=f"text_{key_id}", placeholder="Type your answer here...", max_chars=100)
        
    return response

# -----------------------------------------------------------------------------
# 5. UI RENDERING
# -----------------------------------------------------------------------------

# --- STEP 0: WELCOME SCREEN ---
if st.session_state.step == 0:
    st.title("Student Connection & Mental Health Guide")
    st.markdown('<div class="subtitle">Designed for BYU Students</div>', unsafe_allow_html=True)
    
    st.markdown("""
    College can be crowded, but it can also feel incredibly quiet. 
    
    You are not alone in feeling this way. In fact, research shows that over half of students currently feel disconnected.
    
    This short, anonymous assessment will help you identify **why** you might be feeling this way and point you toward the specific resources that match your situation.
    """)
    if st.button("Start Assessment"):
        next_step()
        st.rerun()

    # Footer Disclaimer
    st.markdown("""
    <div class="disclaimer">
        Disclaimer: This tool is a student-created project and is not officially affiliated with Brigham Young University. 
        It is designed for educational and resource-finding purposes only and does not constitute professional medical advice or diagnosis.
    </div>
    """, unsafe_allow_html=True)

# --- STEP 1: PURPOSE (SELF OR OTHER) ---
elif st.session_state.step == 1:
    st.subheader("Welcome")
    q = questions['q0']
    response = st.radio(q['text'], q['options'], index=None)
    
    if st.button("Next"):
        if response:
            key = q['keys'][q['options'].index(response)]
            st.session_state.answers['q0'] = key
            
            if key == "OTHER_PERSON":
                st.session_state.step = 88 # Jump to 'Helper' page
            else:
                next_step()
            st.rerun()
        else:
            st.error("Please select an option to continue.")

# --- STEP 2: SAFETY TRIAGE ---
elif st.session_state.step == 2:
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

# --- STEP 3: ROOT CAUSE (Questions 2-4) ---
elif st.session_state.step == 3:
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

# --- STEP 4: SYMPTOMS (Questions 5-7) ---
elif st.session_state.step == 4:
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

# --- STEP 88: HELPER RESOURCE PAGE ---
elif st.session_state.step == 88:
    st.header("Supporting a Friend")
    st.markdown("""
    It takes courage and kindness to look out for others. Research shows that social support is one of the most critical factors in mental health.
    
    **Here are a few ways you can support someone who might be struggling:**
    
    * **Listen without solving:** Often, people just need to be heard. You don't need to fix their problem; just validating their feelings ("That sounds really hard") is powerful.
    * **Invite them along:** Keep inviting them to low-pressure activities (getting lunch, studying), even if they say no often.
    * **Know your limits:** You are a friend, not a therapist. If you are worried about their safety, it is okay to ask for professional help.
    """)
    
    # Practical Tools
    st.subheader("Resources to Share or Use")
    
    helper_resources = [
        {"name": "BYU CAPS (Referring a Student)", "url": "https://caps.byu.edu/", "desc": "Free counseling and psychology services for students. They can guide you on how to set boundaries and effectively support a friend in crisis."},
        {"name": "Seize the Awkward", "url": "https://seizetheawkward.org/", "desc": "A guide to starting conversations about mental health. It provides practical icebreakers to help you move past the awkwardness and offer real support."},
        {"name": "End Social Isolation: How to Help", "url": "https://www.endsocialisolation.org/support/", "desc": "An educational hub on the signs of loneliness. It helps you recognize subtle distress signals in friends so you can reach out sooner."}
    ]
    
    for res in helper_resources:
        st.markdown(f"""
        <div class="resource-box">
            <div class="resource-title">{res['name']}</div>
            <div class="resource-desc">{res['desc']}</div>
            <a href="{res['url']}" target="_blank" class="resource-link">Visit Website -></a>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    
    # Research Logic Sources
    st.subheader("Deep Dive: The Science of Connection")
    st.markdown("If you want to understand the research behind why connection is a vital health factor, these are the sources that informed this project:")

    research_resources = [
        {"name": "Surgeon General's Advisory on Loneliness", "url": "https://www.hhs.gov/about/news/2023/05/03/new-surgeon-general-advisory-raises-alarm-about-devastating-impact-epidemic-loneliness-isolation-united-states.html", "desc": "The 2023 advisory declaring loneliness a public health epidemic and detailing its physical health consequences."},
        {"name": "BYU Research: Social Connection as a Vital Sign", "url": "https://news.byu.edu/intellect/byu-researchers-show-social-connection-is-still-underappreciated-as-a-medically-relevant-health-factor", "desc": "Research from BYU's Julianne Holt-Lunstad showing that social connection is as critical to physical health as exercise or diet."},
        {"name": "Research Square: Student Loneliness", "url": "https://www.researchsquare.com/article/rs-93878/v2", "desc": "Studies analyzing the specific impact of the pandemic and transition periods on university student loneliness."}
    ]

    for res in research_resources:
        st.markdown(f"""
        <div class="resource-box">
            <div class="resource-title">{res['name']}</div>
            <div class="resource-desc">{res['desc']}</div>
            <a href="{res['url']}" target="_blank" class="resource-link">Read Article -></a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("Start Over"):
        restart()
        st.rerun()

# --- STEP 99: IMMEDIATE CRISIS SCREEN ---
elif st.session_state.step == 99:
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
            <li>
                <strong>BYU CAPS (Counseling & Psychological Services):</strong> 
                <br>Call <strong>801.422.3035</strong>.
                <br><em>Free counseling and psychology services for students.</em>
                <br><a href="https://caps.byu.edu/" target="_blank" style="color:#58a6ff;">Visit Website</a>
                <br><strong>Walk-in Hours:</strong> 8:00 AM - 5:00 PM, Mon-Fri (1500 WSC)
            </li>
            <li><strong>University Police:</strong> Call <strong>801.422.2222</strong> (If you are in immediate danger)</li>
        </ul>
        <p>You do not have to do this alone.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("") # Spacer
    if st.button("Restart"):
        restart()
        st.rerun()

# --- STEP 5: RESULTS & RESOURCES ---
elif st.session_state.step == 5:
    st.progress(100)
    
    # Run the robust, multi-result logic
    matches = determine_matches(st.session_state.answers)
    
    st.header("Your Personalized Resources")
    st.markdown("Based on your answers, we have identified a few specific areas where support might be helpful.")
    st.write("")
    
    # Full Content Dictionary (Keys match the Group IDs)
    results_content = {
        1: { 
            "topic": "crisis support",
            "resources": [] 
        },
        2: {
            "topic": "feelings of loneliness despite being around others",
            "resources": [
                {"name": "CDC: Ways to Improve Social Connectedness", "url": "https://www.cdc.gov/social-connectedness/improving/", "desc": "Practical, science-backed strategies specifically for improving the quality of your social connections, rather than just increasing the quantity."},
                {"name": "BYU CAPS (Group Therapy)", "url": "https://caps.byu.edu/", "desc": "Free counseling and psychology services for students. Group therapy provides a safe environment to practice connecting with others who also feel isolated."},
                {"name": "Psychology Today: Loneliness Basics", "url": "https://www.psychologytoday.com/us/basics/loneliness", "desc": "A clear guide to understanding why we feel lonely and how to distinguish between solitude and isolation."}
            ]
        },
        3: {
            "topic": "adjusting to a new environment",
            "resources": [
                {"name": "The Jed Foundation: Transitioning to College", "url": "https://jedfoundation.org/resource/transitioning-to-college/", "desc": "A guide specifically for the college transition. It validates the awkwardness of the freshman experience and offers tips for finding your footing."},
                {"name": "BYU Clubs & Associations", "url": "https://clubs.byu.edu/", "desc": "The central directory for student organizations. Finding a group based on shared interests is the fastest way to build a new support system in a new environment."},
                {"name": "End Social Isolation: Breaking the Ice", "url": "https://www.endsocialisolation.org/support/", "desc": "Guides on breaking the ice and starting conversations. These tips help overcome the initial friction of meeting new people during life transitions."}
            ]
        },
        4: {
            "topic": "social anxiety and nervousness",
            "resources": [
                {"name": "ADAA: Understanding Social Anxiety", "url": "https://adaa.org/understanding-anxiety/social-anxiety-disorder", "desc": "The Anxiety & Depression Association of America provides clinical-grade information to help you understand social anxiety disorder."},
                {"name": "BYU CAPS (Anxiety Services)", "url": "https://caps.byu.edu/", "desc": "Free counseling and psychology services for students. Licensed professionals can teach you biofeedback and cognitive strategies to manage physiological anxiety symptoms."},
                {"name": "Crisis Text Line (Text HOME to 741741)", "url": "https://www.crisistextline.org/topics/loneliness/", "desc": "Immediate, anonymous support via text. It provides a non-judgmental space to de-escalate panic attacks or intense anxiety in the moment."}
            ]
        },
        5: {
            "topic": "recent loss or heartbreak",
            "resources": [
                {"name": "APA: Coping with Loss", "url": "https://www.apa.org/topics/grief", "desc": "The American Psychological Association's guide on grief. It explains the psychology of loss and healthy ways to navigate the grieving process."},
                {"name": "BYU CAPS (Grief Support)", "url": "https://caps.byu.edu/", "desc": "Free counseling and psychology services for students. Therapists can help you process the complex emotions of grief and adjust to life after a significant loss."},
                {"name": "Crisis Text Line (For late nights)", "url": "https://www.crisistextline.org/topics/loneliness/", "desc": "24/7 support for overwhelming waves of sadness. Connect with a crisis counselor whenever grief feels too heavy to carry alone, day or night."}
            ]
        },
        6: {
            "topic": "finding a community where you belong",
            "resources": [
                {"name": "The Trevor Project", "url": "https://www.thetrevorproject.org/", "desc": "A leading organization providing crisis intervention and support for LGBTQ young people. Connect with a safe, welcoming community 24/7 via text, chat, or phone."},
                {"name": "BYU CAPS (Safe Space)", "url": "https://caps.byu.edu/", "desc": "Free counseling and psychology services for students. This is a confidential, safe space to explore your identity without fear of judgment or rejection."},
                {"name": "End Social Isolation", "url": "https://www.endsocialisolation.org/support/", "desc": "Articles on belonging and community. Learn how to find your 'tribe' and foster relationships where you don't have to mask your true self."}
            ]
        },
        7: {
            "topic": "feelings of burnout and overwhelm",
            "resources": [
                {"name": "Mayo Clinic: Burnout Symptoms & Causes", "url": "https://www.mayoclinic.org/healthy-lifestyle/adult-health/in-depth/burnout/art-20046642", "desc": "A trusted medical resource to help you distinguish between normal stress and burnout, with clear strategies for recovery."},
                {"name": "EduMed Balance Resources", "url": "https://www.edumed.org/resources/student-loneliness-help-and-support/", "desc": "A guide specifically for student mental health. It offers strategies to harmonize your study schedule with essential self-care and social time."},
                {"name": "BYU CAPS (Stress Management)", "url": "https://caps.byu.edu/", "desc": "Free counseling and psychology services for students. Learn stress management techniques to balance academic rigor with the social rest you need."}
            ]
        },
        8: {
            "topic": "ongoing feelings of heaviness or depression",
            "resources": [
                {"name": "NAMI: Depression Support", "url": "https://www.nami.org/About-Mental-Illness/Mental-Health-Conditions/Depression", "desc": "The National Alliance on Mental Illness provides extensive resources on living with and treating depression."},
                {"name": "Mental Health America: Screening Tools", "url": "https://mhanational.org/conditions/depression", "desc": "Information and tools to help you understand your symptoms and how to advocate for your mental health."},
                {"name": "BYU CAPS (Make an Appointment)", "url": "https://caps.byu.edu/", "desc": "Free counseling and psychology services for students. Regular therapy is often the most effective treatment for persistent depression or long-term struggles."}
            ]
        },
        9: {
            "topic": "negative comparisons on social media",
            "resources": [
                {"name": "The Jed Foundation: Social Media & Mental Health", "url": "https://jedfoundation.org/resource/social-media-and-mental-health/", "desc": "A deep dive into how online habits affect your mood, with tips on how to curate a feed that serves you rather than drains you."},
                {"name": "End Social Isolation (Social Media Limits)", "url": "https://www.endsocialisolation.org/support/", "desc": "Guides on managing social media usage. Learn to curate your digital environment to reduce FOMO and focus on genuine, offline connections."},
                {"name": "CDC: Building Self-Worth", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html", "desc": "Tools for building self-worth independent of external validation. Strengthening your internal confidence helps break the cycle of comparing yourself to others."}
            ]
        },
        10: {
            "topic": "connection and general well-being",
            "resources": [
                {"name": "Mental Health America: Connect with Others", "url": "https://mhanational.org/resources/connect-with-others", "desc": "A broad guide on the benefits of social connection and simple steps to start building a support network."},
                {"name": "CDC: Improving Social Connectedness", "url": "https://www.cdc.gov/social-connectedness/improving/", "desc": "Strategies to improve your social health. It provides a broad range of coping strategies and facts to help you understand what you are feeling."},
                {"name": "BYU CAPS", "url": "https://caps.byu.edu/", "desc": "Free counseling and psychology services for students. A general consultation can help you untangle complex feelings and determine the best path forward."}
            ]
        }
    }
    
    # Iterate through all matches found
    for group_id in matches:
        data = results_content[group_id]
        
        # Section Header
        st.subheader(f"To help with {data['topic']}, consider these resources:")
        
        # Render Cards
        for res in data['resources']:
            desc_html = f'<div class="resource-desc">{res["desc"]}</div>' if "desc" in res else ""
            st.markdown(f"""
            <div class="resource-box">
                <div class="resource-title">{res['name']}</div>
                {desc_html}
                <a href="{res['url']}" target="_blank" class="resource-link">Visit Website -></a>
            </div>
            """, unsafe_allow_html=True)
            
        st.write("") # Spacing between sections
        
    st.markdown("---")
    if st.button("Start Over"):
        restart()
        st.rerun()

    # Footer Disclaimer
    st.markdown("""
    <div class="disclaimer">
        Disclaimer: This tool is a student-created project and is not officially affiliated with Brigham Young University. 
        It is designed for educational and resource-finding purposes only and does not constitute professional medical advice or diagnosis.
    </div>
    """, unsafe_allow_html=True)
