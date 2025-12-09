import streamlit as st
import streamlit.components.v1 as components
import time
import os
import json
import re # Added for robust JSON parsing

# Try to import the Google Generative AI library
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

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
st.markdown('<div id="top_of_page"></div>', unsafe_allow_html=True)

if 'scroll_to_top' not in st.session_state:
    st.session_state.scroll_to_top = False

if st.session_state.scroll_to_top:
    js = """
    <script>
        setTimeout(function() {
            try {
                var anchor = window.parent.document.getElementById("top_of_page");
                if (anchor) {
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

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #0b101d; color: #c9d1d9; font-family: 'Helvetica', sans-serif; }
    h1 { color: #ffffff; text-align: center; }
    .subtitle { text-align: center; color: #58a6ff; font-weight: bold; margin-bottom: 20px; }
    h2, h3 { color: #58a6ff; }
    p, li, .stMarkdown { color: #c9d1d9; font-size: 1.05rem; }
    .stRadio > label { color: #ffffff; font-size: 1.1rem; padding-bottom: 10px; display: block; }
    div.row-widget.stRadio > div { background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d; }
    .stTextInput > div > div > input { border-radius: 5px; background-color: #0d1117; color: white; border: 1px solid #30363d; }
    .stButton > button { background-color: #002E5D; color: white; border-radius: 50px; padding: 10px 24px; font-weight: bold; border: 1px solid #1f6feb; width: 100%; }
    .stButton > button:hover { background-color: #001f3f; border-color: #58a6ff; color: white; }
    .stProgress > div > div > div > div { background-color: #002E5D; }
    .resource-box { background-color: #161b22; padding: 15px; border-radius: 8px; border-left: 5px solid #002E5D; margin-bottom: 15px; border: 1px solid #30363d; }
    .resource-title { font-weight: bold; color: #58a6ff; font-size: 1.1rem; margin-bottom: 5px; }
    .resource-desc { color: #c9d1d9; font-size: 0.9rem; margin-bottom: 8px; font-style: italic; }
    .resource-link { color: #58a6ff; text-decoration: none; font-weight: bold; }
    .resource-link:hover { color: #ffffff; text-decoration: underline; }
    .info-box { background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d; color: #e0e0e0; }
    .disclaimer { font-size: 0.8rem; color: #6e7681; text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #30363d; }
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
    st.session_state.scroll_to_top = True

def restart():
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.scroll_to_top = True

# -----------------------------------------------------------------------------
# 3. QUESTIONNAIRE DATA
# -----------------------------------------------------------------------------
questions = {
    "q0": { "text": "Before we begin, who are you looking for resources for today?", "options": ["For myself.", "I want to learn how to support a friend or classmate."], "keys": ["SELF", "OTHER_PERSON"] },
    "q1": { "text": "How are you feeling about your safety right now?", "options": ["I’m managing okay, just working through some difficult emotions.", "I feel overwhelmed, but I am safe.", "I don't feel safe, or I'm having thoughts about hurting myself or others."], "keys": ["A", "B", "C"] },
    "q2": { "text": "Which statement resonates most with your current social experience?", "options": ["I’m around people often (roommates, classmates), but I don't feel a deep connection with them.", "I spend a lot of time alone and haven't found my group yet.", "I had a close connection, but that has recently changed (due to a breakup, loss, or drift).", "I want to socialize, but nervousness often holds me back.", "I have friends, but I feel I can't be my full, authentic self around them.", "Other (please explain)"], "keys": ["A", "B", "C", "D", "E", "OTHER"] },
    "q3": { "text": "When you think about reaching out to make new friends, what comes to mind?", "options": ["I worry that I won't be fully understood.", "I’m not quite sure where to begin.", "I want to, but I feel anxious about saying the wrong thing.", "I honestly feel too drained or busy to try right now.", "I find myself missing a specific connection I used to have.", "Other (please explain)"], "keys": ["A", "B", "C", "D", "E", "OTHER"] },
    "q4": { "text": "How long have you been navigating these feelings?", "options": ["This has been a familiar feeling for a long time.", "It mostly started during this phase of my life (college/BYU).", "It is very recent and linked to a specific event.", "It tends to come and go.", "Other (please explain)"], "keys": ["A", "B", "C", "D", "OTHER"] },
    "q5": { "text": "How is this affecting your day-to-day well-being?", "options": ["I'm managing my daily tasks, but I feel a bit empty when I'm alone.", "I find it difficult to find motivation, and things feel heavier than usual.", "I feel physically anxious (racing heart, shakiness) in social situations.", "I feel physically exhausted or drained.", "Other (please explain)"], "keys": ["A", "B", "C", "D", "OTHER"] },
    "q6": { "text": "When you are by yourself, where does your focus tend to go?", "options": ["I often check social media and compare my life to others.", "I tend to sleep or zone out to escape.", "I distract myself with work or study.", "I find myself replaying thoughts about what I could do differently.", "Other (please explain)"], "keys": ["A", "B", "C", "D", "OTHER"] },
    "q7": { "text": "If you could change one aspect of your situation today, what would it be?", "options": ["To find someone who truly understands me.", "To have a community to do things with.", "To feel more confident and calm when talking to people.", "To lift this feeling of heaviness or sadness.", "Other (please explain)"], "keys": ["A", "B", "C", "D", "OTHER"] }
}

# -----------------------------------------------------------------------------
# 4. AI & LOGIC ENGINE
# -----------------------------------------------------------------------------

def analyze_other_responses(answers):
    """
    If the user typed custom answers for 'Other', send them to Gemini 
    to classify into one of the 10 buckets.
    """
    # 1. Collect all custom text
    custom_text = []
    for q_id, key in answers.items():
        if key == 'OTHER':
            # Retrieve the text input from session state using the text key
            text_val = st.session_state.get(f"text_{q_id}", "").strip()
            if text_val:
                custom_text.append(f"Question: {questions[q_id]['text']}\nUser Answer: {text_val}")
    
    if not custom_text:
        return []

    # 2. Check for API Key (Streamlit Secrets or Env Var)
    api_key = st.secrets.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    
    if not HAS_GENAI:
        st.warning("⚠️ AI Library not found. Please add 'google-generativeai' to requirements.txt.")
        return []
        
    if not api_key:
        st.warning("⚠️ No Google API Key found. 'Other' responses cannot be analyzed.")
        return []

    # 3. Call AI
    try:
        genai.configure(api_key=api_key)
        # Using specific preview model for this environment. 
        # If running locally/deployed elsewhere, you can switch to 'gemini-1.5-flash'
        model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')
        
        prompt = f"""
        You are a mental health triage assistant for university students. 
        Analyze the following student responses and map them to the most relevant Category IDs from the list below.
        
        CATEGORIES:
        1: Crisis/Safety (Harm to self or others)
        2: Emotional Loneliness (Feels invisible/misunderstood)
        3: New Student/Transition (Homesick, adjusting to college)
        4: Social Anxiety (Fear of judgment, nervousness)
        5: Grief/Loss (Breakup, death, lost friendship)
        6: Identity/Belonging (LGBTQ+, minority, feeling like an outsider)
        7: Burnout (Overwhelmed, exhausted, too busy)
        8: Depression (Chronic heaviness, lack of motivation)
        9: Comparison (Social media, feeling inadequate)
        10: General/Unsure

        STUDENT RESPONSES:
        {chr(10).join(custom_text)}

        INSTRUCTIONS:
        - Return ONLY a raw JSON list of integers, e.g. [4, 7].
        - Do not include markdown formatting like ```json.
        - If the text is vague, return [10].
        """
        
        response = model.generate_content(prompt)
        text_result = response.text.strip()
        
        # Robust parsing: Find the list pattern [1, 2] in the text
        match = re.search(r'\[.*?\]', text_result)
        if match:
            clean_json = match.group(0)
            return json.loads(clean_json)
        else:
            return [10]
        
    except Exception as e:
        # Show error to user for debugging (remove in final production if desired)
        st.error(f"AI Analysis Error: {str(e)}")
        return []

def determine_matches(answers):
    """
    Analyzes answers and collects ALL matching categories.
    Combines Rule-Based Logic + AI Analysis of 'Other' text.
    """
    matches = []

    # --- RULE BASED LOGIC ---
    # 1. CRISIS CASE (Safety First) - Exclusive
    if answers.get('q1') == 'C':
        return [1]
    
    # 2. Chronic / Clinical Struggle
    if answers.get('q4') == 'A' or answers.get('q5') == 'B':
        matches.append(8)
        
    # 3. Situational / Grief
    if answers.get('q2') == 'C' or answers.get('q4') == 'C' or answers.get('q3') == 'E':
        matches.append(5)

    # 4. Social Anxiety
    if answers.get('q2') == 'D' or answers.get('q3') == 'C' or answers.get('q5') == 'C':
        matches.append(4)
        
    # 5. Identity Isolated
    if answers.get('q2') == 'E':
        matches.append(6)
        
    # 6. Burnout
    if answers.get('q3') == 'D':
        matches.append(7)
        
    # 7. Freshman / Isolation
    if answers.get('q2') == 'B' or answers.get('q4') == 'B':
        matches.append(3)
        
    # 8. Emotional Loneliness
    if answers.get('q2') == 'A' or answers.get('q7') == 'A':
        matches.append(2)

    # 9. Comparison Trap
    if answers.get('q6') == 'A':
        matches.append(9)

    # --- AI ANALYSIS (Process 'Other' text) ---
    ai_matches = analyze_other_responses(answers)
    if ai_matches:
        matches.extend(ai_matches)
        
    # --- FALLBACK ---
    if not matches:
        # If pure rule-based didn't find anything AND AI didn't find anything
        matches.append(10)
        
    # Deduplicate and limit to top 3
    final_matches = list(set(matches))
    
    # If Safety (1) was found via AI, it must override everything else
    if 1 in final_matches:
        return [1]
        
    return final_matches[:3]

def render_question(key_id):
    q = questions[key_id]
    response = st.radio(q['text'], q['options'], index=None, key=f"rad_{key_id}")
    
    if response and "Other" in response:
        st.text_input("Please explain (optional):", key=f"text_{key_id}", placeholder="Type your answer here...", max_chars=100)
        st.caption("Note: Your anonymous response will be analyzed by AI to better match you with resources.")
        
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

    st.markdown("""
    <div class="disclaimer">
        Disclaimer: This tool is a student-created project and is not officially affiliated with Brigham Young University. 
        It is designed for educational and resource-finding purposes only and does not constitute professional medical advice or diagnosis.
    </div>
    """, unsafe_allow_html=True)

# --- STEP 1: PURPOSE ---
elif st.session_state.step == 1:
    st.subheader("Welcome")
    q = questions['q0']
    response = st.radio(q['text'], q['options'], index=None)
    
    if st.button("Next"):
        if response:
            key = q['keys'][q['options'].index(response)]
            st.session_state.answers['q0'] = key
            if key == "OTHER_PERSON":
                st.session_state.step = 88 
            else:
                next_step()
            st.rerun()
        else:
            st.error("Please select an option to continue.")

# --- STEP 2: SAFETY ---
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

# --- STEP 3: ROOT CAUSE ---
elif st.session_state.step == 3:
    st.progress(33)
    st.subheader("Understanding Your Situation")
    
    a2 = render_question('q2')
    a3 = render_question('q3')
    a4 = render_question('q4')

    if st.button("Next"):
        if a2 and a3 and a4:
            st.session_state.answers['q2'] = 'OTHER' if "Other" in a2 else questions['q2']['keys'][questions['q2']['options'].index(a2)]
            st.session_state.answers['q3'] = 'OTHER' if "Other" in a3 else questions['q3']['keys'][questions['q3']['options'].index(a3)]
            st.session_state.answers['q4'] = 'OTHER' if "Other" in a4 else questions['q4']['keys'][questions['q4']['options'].index(a4)]
            next_step()
            st.rerun()
        else:
            st.error("Please answer all questions to continue.")

# --- STEP 4: SYMPTOMS ---
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
    st.markdown("It takes courage and kindness to look out for others. Research shows that social support is one of the most critical factors in mental health.")
    st.markdown("**Here are a few ways you can support someone who might be struggling:**")
    st.markdown("* **Listen without solving:** Often, people just need to be heard.\n* **Invite them along:** Keep inviting them to low-pressure activities.\n* **Know your limits:** It is okay to ask for professional help.")
    
    st.subheader("Resources to Share or Use")
    helper_resources = [
        {"name": "BYU CAPS (Referring a Student)", "url": "https://caps.byu.edu/", "desc": "Free counseling and psychology services for students. They can guide you on how to set boundaries and effectively support a friend in crisis."},
        {"name": "Seize the Awkward", "url": "https://seizetheawkward.org/", "desc": "A guide to starting conversations about mental health. It provides practical icebreakers to help you move past the awkwardness and offer real support."},
        {"name": "End Social Isolation: How to Help", "url": "https://www.endsocialisolation.org/support/", "desc": "An educational hub on the signs of loneliness. It helps you recognize subtle distress signals in friends so you can reach out sooner."}
    ]
    for res in helper_resources:
        st.markdown(f'<div class="resource-box"><div class="resource-title">{res["name"]}</div><div class="resource-desc">{res["desc"]}</div><a href="{res["url"]}" target="_blank" class="resource-link">Visit Website -></a></div>', unsafe_allow_html=True)
    
    st.write("")
    st.subheader("Deep Dive: The Science of Connection")
    research_resources = [
        {"name": "Surgeon General's Advisory on Loneliness", "url": "https://www.hhs.gov/about/news/2023/05/03/new-surgeon-general-advisory-raises-alarm-about-devastating-impact-epidemic-loneliness-isolation-united-states.html", "desc": "The 2023 advisory declaring loneliness a public health epidemic and detailing its physical health consequences."},
        {"name": "BYU Research: Social Connection as a Vital Sign", "url": "https://news.byu.edu/intellect/byu-researchers-show-social-connection-is-still-underappreciated-as-a-medically-relevant-health-factor", "desc": "Research from BYU's Julianne Holt-Lunstad showing that social connection is as critical to physical health as exercise or diet."},
        {"name": "Research Square: Student Loneliness", "url": "https://www.researchsquare.com/article/rs-93878/v2", "desc": "Studies analyzing the specific impact of the pandemic and transition periods on university student loneliness."}
    ]
    for res in research_resources:
        st.markdown(f'<div class="resource-box"><div class="resource-title">{res["name"]}</div><div class="resource-desc">{res["desc"]}</div><a href="{res["url"]}" target="_blank" class="resource-link">Read Article -></a></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("Start Over"):
        restart()
        st.rerun()

# --- STEP 99: IMMEDIATE CRISIS ---
elif st.session_state.step == 99:
    st.markdown("""
    <div class="info-box">
        <h2 style="color: #58a6ff; margin-top:0;">Support Resources</h2>
        <p style="font-size: 1.1rem;">It sounds like you are carrying a really heavy burden right now. We want to make sure you have someone to talk to who can help you navigate this safely.</p>
        <ul>
            <li><strong>Crisis Text Line:</strong> Text <strong>HOME</strong> to <strong>741741</strong> (Free, 24/7)</li>
            <li><strong>BYU CAPS:</strong> Call <strong>801.422.3035</strong>.<br><em>Free counseling for students.</em><br><a href="https://caps.byu.edu/" target="_blank" style="color:#58a6ff;">Visit Website</a></li>
            <li><strong>University Police:</strong> Call <strong>801.422.2222</strong> (If you are in immediate danger)</li>
        </ul>
        <p>You do not have to do this alone.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Restart"):
        restart()
        st.rerun()

# --- STEP 5: RESULTS ---
elif st.session_state.step == 5:
    st.progress(100)
    
    with st.spinner("Analyzing your responses..."):
        matches = determine_matches(st.session_state.answers)
    
    st.header("Your Personalized Resources")
    st.markdown("Based on your answers, we have identified a few specific areas where support might be helpful.")
    st.write("")
    
    results_content = {
        1: { "topic": "a crisis", "resources": [] },
        2: { "topic": "feelings of loneliness despite being around others", "resources": [
            {"name": "CDC: Ways to Improve Social Connectedness", "url": "https://www.cdc.gov/social-connectedness/improving/", "desc": "Practical, science-backed strategies specifically for improving the quality of your social connections, rather than just increasing the quantity."},
            {"name": "BYU CAPS (Group Therapy)", "url": "https://caps.byu.edu/", "desc": "Free counseling and psychology services for students. Group therapy provides a safe environment to practice connecting with others who also feel isolated."},
            {"name": "Psychology Today: Loneliness Basics", "url": "https://www.psychologytoday.com/us/basics/loneliness", "desc": "A clear guide to understanding why we feel lonely and how to distinguish between solitude and isolation."}
        ]},
        3: { "topic": "the transition to a new environment", "resources": [
            {"name": "The Jed Foundation: Transitioning to College", "url": "https://jedfoundation.org/resource/transitioning-to-college/", "desc": "A guide specifically for the college transition. It validates the awkwardness of the freshman experience and offers tips for finding your footing."},
            {"name": "BYU Clubs & Associations", "url": "https://clubs.byu.edu/", "desc": "The central directory for student organizations. Finding a group based on shared interests is the fastest way to build a new support system."},
            {"name": "End Social Isolation: Breaking the Ice", "url": "https://www.endsocialisolation.org/support/", "desc": "Guides on breaking the ice and starting conversations. These tips help overcome the initial friction of meeting new people."}
        ]},
        4: { "topic": "social anxiety and nervousness", "resources": [
            {"name": "ADAA: Understanding Social Anxiety", "url": "https://adaa.org/understanding-anxiety/social-anxiety-disorder", "desc": "The Anxiety & Depression Association of America provides clinical-grade information to help you understand social anxiety disorder."},
            {"name": "BYU CAPS (Anxiety Services)", "url": "https://caps.byu.edu/", "desc": "Free counseling and psychology services for students. Licensed professionals can teach you biofeedback and strategies to manage anxiety."},
            {"name": "Crisis Text Line (Text HOME to 741741)", "url": "https://www.crisistextline.org/topics/loneliness/", "desc": "Immediate, anonymous support via text. It provides a non-judgmental space to de-escalate panic attacks or intense anxiety."}
        ]},
        5: { "topic": "recent loss or heartbreak", "resources": [
            {"name": "APA: Coping with Loss", "url": "https://www.apa.org/topics/grief", "desc": "The American Psychological Association's guide on grief. It explains the psychology of loss and healthy ways to navigate the grieving process."},
            {"name": "BYU CAPS (Grief Support)", "url": "https://caps.byu.edu/", "desc": "Free counseling and psychology services for students. Therapists can help you process the complex emotions of grief."},
            {"name": "Crisis Text Line (For late nights)", "url": "https://www.crisistextline.org/topics/loneliness/", "desc": "24/7 support for overwhelming waves of sadness. Connect with a crisis counselor whenever grief feels too heavy to carry alone."}
        ]},
        6: { "topic": "the search for a community where you belong", "resources": [
            {"name": "The Trevor Project", "url": "https://www.thetrevorproject.org/", "desc": "A leading organization providing crisis intervention and support for LGBTQ young people. Connect with a safe, welcoming community 24/7."},
            {"name": "BYU CAPS (Safe Space)", "url": "https://caps.byu.edu/", "desc": "Free counseling and psychology services for students. This is a confidential, safe space to explore your identity without fear of judgment."},
            {"name": "End Social Isolation", "url": "https://www.endsocialisolation.org/support/", "desc": "Articles on belonging and community. Learn how to find your 'tribe' and foster relationships where you don't have to mask your true self."}
        ]},
        7: { "topic": "feelings of burnout and overwhelm", "resources": [
            {"name": "Mayo Clinic: Burnout Symptoms & Causes", "url": "https://www.mayoclinic.org/healthy-lifestyle/adult-health/in-depth/burnout/art-20046642", "desc": "A trusted medical resource to help you distinguish between normal stress and burnout, with clear strategies for recovery."},
            {"name": "EduMed Balance Resources", "url": "https://www.edumed.org/resources/student-loneliness-help-and-support/", "desc": "A guide specifically for student mental health. It offers strategies to harmonize your study schedule with essential self-care."},
            {"name": "BYU CAPS (Stress Management)", "url": "https://caps.byu.edu/", "desc": "Free counseling and psychology services for students. Learn stress management techniques to balance academic rigor."}
        ]},
        8: { "topic": "ongoing feelings of heaviness or depression", "resources": [
            {"name": "NAMI: Depression Support", "url": "https://www.nami.org/About-Mental-Illness/Mental-Health-Conditions/Depression", "desc": "The National Alliance on Mental Illness provides extensive resources on living with and treating depression."},
            {"name": "Mental Health America: Screening Tools", "url": "https://mhanational.org/conditions/depression", "desc": "Information and tools to help you understand your symptoms and how to advocate for your mental health."},
            {"name": "BYU CAPS (Make an Appointment)", "url": "https://caps.byu.edu/", "desc": "Free counseling and psychology services for students. Regular therapy is often the most effective treatment for persistent struggles."}
        ]},
        9: { "topic": "negative comparisons and social media pressure", "resources": [
            {"name": "The Jed Foundation: Social Media & Mental Health", "url": "https://jedfoundation.org/resource/social-media-and-mental-health/", "desc": "A deep dive into how online habits affect your mood, with tips on how to curate a feed that serves you rather than drains you."},
            {"name": "End Social Isolation (Social Media Limits)", "url": "https://www.endsocialisolation.org/support/", "desc": "Guides on managing social media usage. Learn to curate your digital environment to reduce FOMO and focus on genuine connections."},
            {"name": "CDC: Building Self-Worth", "url": "https://www.cdc.gov/howrightnow/emotion/loneliness/index.html", "desc": "Tools for building self-worth independent of external validation. Strengthening your internal confidence helps break the comparison cycle."}
        ]},
        10: { "topic": "general feelings of loneliness", "resources": [
            {"name": "Mental Health America: Connect with Others", "url": "https://mhanational.org/resources/connect-with-others", "desc": "A broad guide on the benefits of social connection and simple steps to start building a support network."},
            {"name": "CDC: Improving Social Connectedness", "url": "https://www.cdc.gov/social-connectedness/improving/", "desc": "Strategies to improve your social health. It provides a broad range of coping strategies and facts to help you understand what you are feeling."},
            {"name": "BYU CAPS", "url": "https://caps.byu.edu/", "desc": "Free counseling and psychology services for students. A general consultation can help you untangle complex feelings."}
        ]}
    }
    
    for group_id in matches:
        data = results_content[group_id]
        st.subheader(f"It looks like you may be navigating {data['topic']}. Here are some resources for you:")
        for res in data['resources']:
            st.markdown(f'<div class="resource-box"><div class="resource-title">{res["name"]}</div><div class="resource-desc">{res["desc"]}</div><a href="{res["url"]}" target="_blank" class="resource-link">Visit Website -></a></div>', unsafe_allow_html=True)
        st.write("")
        
    st.markdown("---")
    if st.button("Start Over"):
        restart()
        st.rerun()

    st.markdown("""
    <div class="disclaimer">
        Disclaimer: This tool is a student-created project and is not officially affiliated with Brigham Young University. 
        It is designed for educational and resource-finding purposes only and does not constitute professional medical advice or diagnosis.
    </div>
    """, unsafe_allow_html=True)
