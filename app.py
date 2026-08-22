import datetime
import streamlit as st
import requests
import json
import os

# =========================================================
# CHAT HISTORY
# =========================================================

HISTORY_FILE = "history.json"


def load_history():
    """Load saved conversations from history.json."""
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_history(history):
    """Save conversations to history.json."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Hani AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CUSTOM CSS - POLISHED HANI AI UI
# =========================================================

st.markdown(
    """
<style>

/* =========================================================
   HANI AI — MODERN AI APP THEME
   ========================================================= */

.stApp {
    background:
        radial-gradient(circle at 8% 0%, rgba(169, 112, 255, .16), transparent 25%),
        radial-gradient(circle at 92% 6%, rgba(232, 117, 180, .10), transparent 24%),
        radial-gradient(circle at 50% 100%, rgba(133, 77, 171, .07), transparent 32%),
        linear-gradient(135deg, #0b0912 0%, #110d1a 48%, #0b1118 100%);
    color: #f8f9ff;
}

.main .block-container {
    max-width: 1260px;
    padding-top: 1.15rem;
    padding-bottom: 7rem;
}

/* Hide Streamlit decoration */
[data-testid="stHeader"] {
    background: transparent;
}

/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #100d1a 0%, #0b0912 100%);
    border-right: 1px solid rgba(196, 156, 255, .13);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.15rem;
}

.sidebar-brand {
    padding: 7px 3px 5px;
}

.sidebar-logo {
    font-size: 1.65rem;
    font-weight: 900;
    letter-spacing: -.8px;
    color: #f7f4ff;
}

.sidebar-logo .spark {
    color: #d7b7ff;
}

.sidebar-subtitle {
    color: #aaa0bd;
    font-size: .82rem;
    line-height: 1.55;
    margin-top: 7px;
}

.sidebar-section {
    color: #f1eaf7;
    font-size: .88rem;
    font-weight: 800;
    margin: 3px 0 8px;
}

.history-label {
    color: #8f839f;
    font-size: .68rem;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-weight: 900;
    margin: 17px 0 7px 2px;
}

.history-empty {
    color: #756b82;
    font-size: .78rem;
    padding: 6px 2px 10px;
}

/* Sidebar buttons */
section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 42px;
    border-radius: 12px;
    border: 1px solid rgba(197, 151, 255, .18);
    background: rgba(29, 23, 43, .78);
    color: #f1eaf7;
    font-size: .79rem;
    font-weight: 700;
    transition: .18s ease;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.025);
}

section[data-testid="stSidebar"] .stButton > button:hover {
    border-color: rgba(218, 150, 255, .50);
    background: rgba(116, 65, 128, .26);
    color: #fff;
    transform: translateY(-1px);
}

section[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: #1a1425;
    border: 1px solid rgba(204, 159, 255, .20);
    border-radius: 12px;
    color: #faf5ff;
}

.privacy-card {
    margin-top: 13px;
    padding: 14px;
    border-radius: 15px;
    background: linear-gradient(145deg, rgba(255,255,255,.045), rgba(255,255,255,.018));
    border: 1px solid rgba(207, 158, 255, .11);
}

.privacy-title {
    color: #f1eaf7;
    font-weight: 800;
    font-size: .82rem;
}

.privacy-text {
    color: #9c91ad;
    font-size: .72rem;
    line-height: 1.55;
    margin-top: 6px;
}

/* =========================================================
   MAIN HEADER
   ========================================================= */

.brand-wrap {
    text-align: center;
    padding: .15rem 0 0;
}

.brand-icon {
    font-size: 2.65rem;
    line-height: 1;
    filter: drop-shadow(0 0 18px rgba(216, 145, 255, .38));
}

.brand-title {
    font-size: 3.05rem;
    line-height: 1.02;
    font-weight: 950;
    letter-spacing: -2.4px;
    margin-top: 8px;
    background: linear-gradient(105deg, #fffaff 10%, #d8b8ff 50%, #f0a8c9 90%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.brand-subtitle {
    color: #a79bb7;
    font-size: .93rem;
    margin-top: 9px;
}

.status-row {
    display: flex;
    justify-content: center;
    margin-top: 15px;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 14px;
    border-radius: 999px;
    background: rgba(70, 214, 157, .055);
    border: 1px solid rgba(70, 214, 157, .24);
    color: #72e6b1;
    font-size: .74rem;
    font-weight: 800;
    box-shadow: 0 0 25px rgba(30,220,150,.04);
}

.status-dot {
    color: #42df94;
}

/* =========================================================
   WELCOME
   ========================================================= */

.welcome-card {
    position: relative;
    overflow: hidden;
    max-width: 820px;
    margin: 31px auto 24px;
    padding: 34px 32px 31px;
    text-align: center;
    border-radius: 24px;
    background:
        radial-gradient(circle at 50% -15%, rgba(181, 120, 235, .14), transparent 55%),
        linear-gradient(145deg, rgba(31, 25, 48, .96), rgba(15, 12, 25, .98));
    border: 1px solid rgba(208, 161, 255, .20);
    box-shadow:
        0 26px 80px rgba(0,0,0,.30),
        inset 0 1px 0 rgba(255,255,255,.045);
}

.welcome-card:after {
    content: "";
    position: absolute;
    width: 170px;
    height: 170px;
    right: -90px;
    top: -90px;
    border-radius: 50%;
    background: rgba(235, 139, 190, .07);
    filter: blur(22px);
}

.welcome-icon {
    font-size: 1.95rem;
    position: relative;
    z-index: 1;
}

.welcome-title {
    position: relative;
    z-index: 1;
    color: #ffffff;
    font-size: 1.45rem;
    font-weight: 850;
    margin-top: 8px;
}

.welcome-text {
    position: relative;
    z-index: 1;
    color: #aa9fb9;
    font-size: .91rem;
    line-height: 1.7;
    margin-top: 8px;
}

/* =========================================================
   CHAT AREA
   ========================================================= */

[data-testid="stChatMessage"] {
    border-radius: 17px;
    padding: 10px 14px;
    margin: 7px 0 12px;
    color: #f6f7ff !important;
    box-shadow: 0 10px 30px rgba(0,0,0,.12);
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] span,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] em,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] blockquote {
    color: #f5f7ff !important;
    opacity: 1 !important;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] code {
    color: #e6eaff !important;
    background: rgba(255,255,255,.085) !important;
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 6px;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: linear-gradient(145deg, rgba(28, 23, 42, .92), rgba(16, 13, 26, .88));
    border: 1px solid rgba(199, 148, 242, .15);
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(145deg, rgba(111, 61, 122, .24), rgba(75, 48, 78, .20));
    border: 1px solid rgba(211, 145, 224, .18);
}

/* =========================================================
   INPUT
   ========================================================= */

[data-testid="stChatInput"] {
    background: rgba(15, 12, 23, .98);
    border: 1px solid rgba(204, 151, 238, .24);
    border-radius: 18px;
    box-shadow:
        0 18px 55px rgba(0,0,0,.32),
        0 0 28px rgba(173, 92, 190, .06);
}

[data-testid="stChatInput"]:focus-within {
    border-color: rgba(224, 158, 239, .58);
    box-shadow:
        0 18px 55px rgba(0,0,0,.34),
        0 0 35px rgba(193, 96, 198, .12);
}

[data-testid="stChatInput"] > div {
    background: #15111f !important;
    border-radius: 18px !important;
}

[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #ffffff !important;
    font-size: .94rem !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #7f8ba5 !important;
}

/* =========================================================
   GENERAL CONTROLS
   ========================================================= */

.stButton > button {
    border-radius: 12px;
    border: 1px solid rgba(196, 145, 231, .18);
    background: rgba(29, 23, 42, .82);
    color: #f5eef9;
    font-weight: 700;
    transition: .18s ease;
}

.stButton > button:hover {
    border-color: rgba(145,126,255,.50);
    background: rgba(112, 62, 124, .26);
    color: #ffffff;
    transform: translateY(-1px);
}

hr {
    border-color: rgba(130,120,255,.09);
}

/* =========================================================
   FOOTER
   ========================================================= */

.hani-footer {
    text-align: center;
    color: #766b82;
    font-size: .70rem;
    line-height: 1.7;
    margin-top: 27px;
    padding: 17px;
    border-top: 1px solid rgba(130,120,255,.08);
}

/* =========================================================
   SCROLLBAR
   ========================================================= */

::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-track {
    background: #070b14;
}

::-webkit-scrollbar-thumb {
    background: #303a58;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #665bb0;
}

</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = load_history()

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo"><span class="spark">✦</span> Hani AI</div>
            <div class="sidebar-subtitle">
                Your private AI companion<br>
                powered locally by Ollama.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown('<div class="sidebar-section">⚙️ Settings</div>', unsafe_allow_html=True)

    model = st.selectbox(
        "AI Model",
        ["llama3.2"],
        index=0,
        label_visibility="visible",
    )

    st.divider()

    # New chat / clear current conversation
    if st.button("✚  New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown('<div class="history-label">💬 Recent chats</div>', unsafe_allow_html=True)

    # Show saved conversations in the sidebar
    history = st.session_state.history

    if history:
        # Most recent first
        for i, conversation in enumerate(reversed(history[-8:])):
            messages = conversation.get("messages", [])

            if messages:
                first_user_message = next(
                    (
                        m.get("content", "")
                        for m in messages
                        if m.get("role") == "user"
                    ),
                    "Conversation",
                )

                title = first_user_message.strip().replace("\n", " ")
                if len(title) > 34:
                    title = title[:34] + "..."

                # Button lets user reopen an old conversation
                if st.button(
                    f"💬 {title}",
                    key=f"history_{len(history)-1-i}",
                    use_container_width=True,
                ):
                    st.session_state.messages = messages.copy()
                    st.rerun()
    else:
        st.markdown(
            '<div class="history-empty">No saved chats yet.</div>',
            unsafe_allow_html=True,
        )

    st.divider()

    if st.button("🗑️  Clear Current Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        """
        <div class="privacy-card">
            <div class="privacy-title">🔒 Privacy</div>
            <div class="privacy-text">
                Your questions are processed locally through Ollama.
                No external AI API is required.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    """
    <div class="brand-wrap">
        <div class="brand-icon">✦</div>
        <div style="color:#687692;font-size:.68rem;font-weight:800;letter-spacing:1.6px;text-transform:uppercase;margin-top:7px;">PRIVATE AI WORKSPACE</div>
        <div class="brand-title">Hani AI</div>
        <div class="brand-subtitle">
            Your private AI companion — simple, smart and local
        </div>
        <div class="status-row">
            <div class="status-badge">
                <span class="status-dot">●</span>
                Local Model&nbsp; • &nbsp;Ollama&nbsp; • &nbsp;Private
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# WELCOME SCREEN
# =========================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="welcome-card">
            <div class="welcome-icon">👋</div>
            <div class="welcome-title">Welcome to Hani AI</div>
            <div class="welcome-text">
                Ask anything, learn something new, or get help with your work.<br>
                <span style="color:#7f8da9;">Fast, private, and running locally on your computer.</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# DISPLAY CURRENT CHAT
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar="👤" if message["role"] == "user" else "✨",
    ):
        st.markdown(message["content"])

# =========================================================
# USER INPUT
# =========================================================

prompt = st.chat_input(
    "Ask Hani anything — I'm here to help, explain, and create."
)

# =========================================================
# PROCESS USER QUESTION
# =========================================================

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="✨"):

        with st.spinner("Hani is thinking..."):

            try:
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False,
                    },
                    timeout=120,
                )

                response.raise_for_status()

                data = response.json()

                answer = data.get(
                    "response",
                    "Sorry, I couldn't generate a response.",
                )

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

                # Save this conversation
                conversation = {
                    "timestamp": datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt,
                        },
                        {
                            "role": "assistant",
                            "content": answer,
                        },
                    ],
                }

                st.session_state.history.append(conversation)
                save_history(st.session_state.history)

            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ Ollama is not running. Please start Ollama and try again."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "⏳ Hani took too long to respond. Please try again."
                )

            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="hani-footer">
        🟢 Hani is running locally &nbsp; • &nbsp; 🔒 Your conversations stay on your computer
        &nbsp; • &nbsp; Powered by Ollama + Llama 3.2
        <br>
        No external AI API required
    </div>
    """,
    unsafe_allow_html=True,
)