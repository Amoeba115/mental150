import streamlit as st

# 1. Configure the page
st.set_page_config(
    page_title="The Whispering Woods",
    page_icon="🌲",
    layout="centered"
)

# 2. Define the Game Data (The Story Graph)
# Each key is a "node" in the story.
# Each node has 'text', 'image' (optional emoji/text art), and 'choices'.
# Choices are a list of tuples: ("Button Label", "Next Node Key")
story_nodes = {
    "start": {
        "text": "You stand at the edge of the Whispering Woods. The wind howls, sounding almost like human voices. To your left is a dense, dark thicket. To your right, a mossy stone path winds into the fog.",
        "choices": [
            ("Enter the thicket", "thicket"),
            ("Follow the stone path", "path"),
        ]
    },
    "thicket": {
        "text": "You push through the thorny branches. They seem to grab at your clothes. Suddenly, you stumble into a clearing containing a glowing blue mushroom.",
        "choices": [
            ("Eat the mushroom", "eat_mushroom"),
            ("Ignore it and keep walking", "deep_woods"),
        ]
    },
    "path": {
        "text": "The stone path is slippery. You hear footsteps behind you. You freeze.",
        "choices": [
            ("Turn around to fight", "fight_shadow"),
            ("Run forward blindly", "run_cliff"),
        ]
    },
    "eat_mushroom": {
        "text": "You take a bite. The world spins into kaleidoscopic colors. You realize you can now understand the language of the squirrels. They lead you to safety. \n\n**YOU WIN!**",
        "choices": [
            ("Play Again", "start")
        ]
    },
    "deep_woods": {
        "text": "You walk past the mushroom. The trees grow tighter together until you can no longer move. The forest has claimed you.",
        "choices": [
            ("Try Again", "start")
        ]
    },
    "fight_shadow": {
        "text": "You turn around and swing your fist! You punch... thin air. It was just a shadow. However, you lost your balance and fell into a mud pit.",
        "choices": [
            ("Climb out", "mud_pit_climb"),
            ("Wait for help", "wait_mud")
        ]
    },
    "run_cliff": {
        "text": "You run so fast you don't see the edge of the cliff. luckily, you catch a vine just in time.",
        "choices": [
            ("Climb up", "path"),
            ("Let go", "game_over_fall")
        ]
    },
    "mud_pit_climb": {
        "text": "You struggle, but the mud is too thick. You are stuck until a ranger finds you three days later. Embarrassing, but you survived.",
        "choices": [
            ("Play Again", "start")
        ]
    },
    "wait_mud": {
        "text": "You wait. And wait. Night falls. The wolves come out.",
        "choices": [
            ("Try Again", "start")
        ]
    },
    "game_over_fall": {
        "text": "You let go of the vine. It's a long way down.\n\n**GAME OVER**",
        "choices": [
            ("Restart", "start")
        ]
    }
}

# 3. Initialize Session State
# Streamlit reruns the script on every interaction, so we use session_state to remember where we are.
if 'current_node' not in st.session_state:
    st.session_state.current_node = 'start'

# 4. Custom CSS for styling
# We inject CSS to hide the default Streamlit menu and style the buttons/text.
st.markdown("""
<style>
    /* Import a retro font */
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

    /* Main background and text colors */
    .stApp {
        background-color: #0e1111;
        color: #33ff33;
        font-family: 'VT323', monospace;
    }
    
    /* Title styling */
    h1 {
        color: #33ff33;
        text-shadow: 0 0 10px #33ff33;
        font-family: 'VT323', monospace;
        text-align: center;
        font-size: 4rem !important;
    }
    
    /* Main text styling */
    .story-text {
        background-color: #1a1d1d;
        padding: 2rem;
        border: 2px solid #33ff33;
        border-radius: 10px;
        font-size: 1.5rem;
        line-height: 1.6;
        margin-bottom: 2rem;
        box-shadow: 0 0 15px rgba(51, 255, 51, 0.2);
    }

    /* Button Styling */
    .stButton button {
        width: 100%;
        background-color: #000000;
        color: #33ff33;
        border: 1px solid #33ff33;
        font-family: 'VT323', monospace;
        font-size: 1.5rem;
        padding: 10px;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        background-color: #33ff33;
        color: #000000;
        box-shadow: 0 0 15px #33ff33;
        transform: scale(1.02);
    }
    
    /* Hide standard Streamlit elements for immersion */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# 5. Game Logic Functions
def update_node(new_node):
    st.session_state.current_node = new_node

# 6. Render the Game
def render_game():
    current_key = st.session_state.current_node
    node_data = story_nodes[current_key]
    
    st.title("THE WHISPERING WOODS")
    
    # Display the story text in a container
    st.markdown(f'<div class="story-text">{node_data["text"]}</div>', unsafe_allow_html=True)
    
    # Create columns for the choices
    choices = node_data["choices"]
    
    # Dynamic column creation based on number of choices
    cols = st.columns(len(choices))
    
    for i, (label, next_node_key) in enumerate(choices):
        with cols[i]:
            # Each button triggers the update_node function
            st.button(
                label, 
                key=f"btn_{current_key}_{i}", 
                on_click=update_node, 
                args=(next_node_key,)
            )

if __name__ == "__main__":
    render_game()