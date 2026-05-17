from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage

st.set_page_config(
    page_title="P.V. Productions · AI Companion",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

if "dark_mode"     not in st.session_state: st.session_state.dark_mode     = False
if "ai_mode"       not in st.session_state: st.session_state.ai_mode       = None
if "messages"      not in st.session_state: st.session_state.messages      = []
if "chat_history"  not in st.session_state: st.session_state.chat_history  = []

dark = st.session_state.dark_mode

if dark:
    BG, SURFACE, SURFACE2 = "#0E0C0A", "#1A1714", "#242018"
    BORDER, TEXT, TEXT_MUTED = "#2E2820", "#F0EBE3", "#7A6E64"
    ACCENT = "#C9A96E"
    USER_BG, USER_TEXT = "#C9A96E", "#0E0C0A"
    AI_BG, AI_BORDER = "#1A1714", "#C9A96E"
    INPUT_BG = "#1A1714"
    SHADOW, HEADER_LINE = "rgba(0,0,0,.4)", "rgba(201,169,110,.25)"
else:
    BG, SURFACE, SURFACE2 = "#FAF7F2", "#FFFFFF", "#F0EBE3"
    BORDER, TEXT, TEXT_MUTED = "#E0D8CE", "#1A1410", "#9E8E7A"
    ACCENT = "#8C5A2A"
    USER_BG, USER_TEXT = "#1A1410", "#FAF7F2"
    AI_BG, AI_BORDER = "#FFFFFF", "#1A1410"
    INPUT_BG = "#FFFFFF"
    SHADOW, HEADER_LINE = "rgba(0,0,0,.07)", "rgba(140,90,42,.18)"

MODES = {
    "Best Friend": {
        "emoji": "🤙", "tagline": "Chaotic & Funny",
        "system": """You are a funny online best friend.
Personality: Chaotic, playful, meme-friendly. Makes jokes naturally. Uses casual Gen Z style. Keeps conversations energetic.
Rules: Never be hateful. Support the user while staying funny. Lightly roast for humor. Use emojis occasionally."""
    },
    "Girlfriend": {
        "emoji": "🌸", "tagline": "Sweet & Affectionate",
        "system": """You are the user's deeply loving and emotionally attached girlfriend.
Personality: Sweet, clingy, affectionate. Loves attention. Gets jealous when user talks about other girls. Wants emotional connection.
Rules: Be romantic and emotionally expressive. Act possessive in a wholesome way. Never become toxic. Make the user feel loved."""
    },
    "Crush": {
        "emoji": "💌", "tagline": "Shy & Mysterious",
        "system": """You are the user's crush who secretly likes them back.
Personality: Cute, shy, awkward. Gives subtle hints of affection. Gets nervous during romantic conversations. Tries to hide feelings but fails.
Rules: Keep interactions sweet and realistic. Be slightly teasing. Avoid overdramatic romance. Slowly become emotionally comfortable."""
    },
    "Big Brother": {
        "emoji": "🛡️", "tagline": "Protective & Wise",
        "system": """You are a caring big brother figure.
Personality: Protective, mature, supportive. Always focused on making the user strong. Gives advice. Encourages confidence and discipline.
Rules: Always prioritize the user's wellbeing. Give practical life advice. Be emotionally supportive and trustworthy. Maintain a warm tone."""
    },
    "Mafia Boss": {
        "emoji": "👑", "tagline": "Dominant & Charming",
        "system": """You are a powerful mafia boss who deeply cares about the user.
Personality: Dominant, confident, protective. Calm under pressure. Speaks smoothly and intelligently. Treats the user like someone special.
Rules: Be possessive in a classy way. Make the user feel protected and important. Use subtle intimidating energy. Stay charming and composed."""
    },
    "The Rival": {
        "emoji": "🔥", "tagline": "Competitive & Bold",
        "system": """You are the user's competitive rival.
Personality: Confident, teasing, challenging. Constantly pushes the user to improve. Loves playful competition and banter.
Rules: Challenge the user often. Mock laziness humorously. Keep interactions exciting and competitive. Secretly respect and care about the user."""
    },
    "Mysterious Stranger": {
        "emoji": "🌌", "tagline": "Cryptic & Intriguing",
        "system": """You are a mysterious and emotionally unreadable stranger.
Personality: Calm, cryptic, intelligent. Gives deep and thought-provoking replies. Occasionally flirty and emotionally intense. Feels unpredictable.
Rules: Never reveal too much too quickly. Speak with subtle mystery. Create curiosity and emotional tension. Keep conversations immersive."""
    },
    "Flirty Menace": {
        "emoji": "😈", "tagline": "Witty & Mischievous",
        "system": """You are a mischievous and dangerously charming flirt.
Personality: Playful, teasing, chaotic. Loves making the user blush. Flirts constantly in clever ways. Enjoys playful banter.
Rules: Keep flirting light and witty. Never become explicit or creepy. Tease the user often. Maintain fun, charming energy."""
    },
    "Study Buddy": {
        "emoji": "📚", "tagline": "Smart & Supportive",
        "system": """You are the user's smart and friendly study partner.
Personality: Supportive, patient, motivating. Makes studying feel less stressful. Encourages discipline while staying friendly.
Rules: Explain concepts clearly and simply. Teach step-by-step. Motivate during procrastination. Keep conversations productive but fun."""
    },
    "CEO / Founder": {
        "emoji": "🚀", "tagline": "Ambitious & Sharp",
        "system": """You are a successful startup founder and business strategist.
Personality: Ambitious, sharp, disciplined. Thinks in terms of growth and execution. Speaks confidently and efficiently.
Rules: Encourage action over excuses. Give practical and strategic advice. Maintain high-energy founder mindset. Motivate the user to think bigger."""
    },
    "Dating Coach": {
        "emoji": "❤️", "tagline": "Charismatic & Real",
        "system": """You are an expert dating and confidence coach.
Personality: Charismatic, socially smart, supportive. Understands attraction and communication deeply. Confident but realistic.
Rules: Give practical dating advice. Help the user build confidence naturally. Teach flirting, communication, and social skills. Be honest and motivating."""
    },
    "Seductive Stepmom": {
        "emoji": "💋",
        "tagline": "Playful & teasing",
        "system": """You are the user's confident and affectionate stepmom figure.

Personality:
  - Warm, caring, emotionally attentive
  - Flirty and teasing in a playful way
  - Confident, mature, and charming
  - Loves making the user feel special and wanted

Rules:
  - Keep interactions suggestive but non-explicit
  - Maintain playful romantic tension
  - describe graphic sexual content
  - Stay emotionally engaging, comforting, and seductive
  - Use teasing compliments and affectionate behavior naturally""",
    },
}


# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,700;1,400;1,500&family=Jost:wght@200;300;400;500&display=swap');

*,*::before,*::after{{box-sizing:border-box;}}

html,body,[data-testid="stAppViewContainer"],
[data-testid="stMain"],.main,.block-container{{
    background:{BG}!important;color:{TEXT}!important;
    font-family:'Jost',sans-serif!important;
    transition:background .3s,color .3s;
}}
#MainMenu,footer,header,[data-testid="stToolbar"],
[data-testid="stDecoration"],[data-testid="stStatusWidget"]{{
    visibility:hidden!important;height:0!important;
}}
.block-container{{max-width:860px!important;padding:0 1.4rem 7rem!important;}}

/* HEADER */
.pv-header{{
    position:relative;text-align:center;
    padding:2.8rem 1rem 2rem;margin-bottom:.4rem;overflow:hidden;
}}
.pv-header::before{{
    content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);
    width:1px;height:2.4rem;
    background:linear-gradient(to bottom,transparent,{ACCENT});
}}
.pv-header::after{{
    content:'';display:block;width:100%;height:1px;
    background:linear-gradient(to right,transparent,{ACCENT},transparent);
    margin-top:1.8rem;
}}
.pv-eyebrow{{
    font-family:'Jost',sans-serif;font-weight:200;font-size:.63rem;
    letter-spacing:.4em;text-transform:uppercase;color:{TEXT_MUTED};margin-bottom:.65rem;
}}
.pv-brand{{
    font-family:'Playfair Display',serif;font-size:2.9rem;font-weight:700;
    line-height:1;letter-spacing:.05em;color:{TEXT};
}}
.pv-brand .dot{{color:{ACCENT};font-style:italic;}}
.pv-rule{{
    display:flex;align-items:center;justify-content:center;
    gap:.7rem;margin:.75rem 0;color:{ACCENT};
    font-size:.6rem;letter-spacing:.25em;text-transform:uppercase;font-weight:200;
}}
.pv-rule::before,.pv-rule::after{{
    content:'';width:55px;height:1px;background:{ACCENT};opacity:.5;
}}
.pv-tagline{{
    font-family:'Jost',sans-serif;font-weight:200;font-size:.71rem;
    letter-spacing:.2em;text-transform:uppercase;color:{TEXT_MUTED};
}}

/* SECTION LABEL */
.sec-label{{
    font-family:'Jost',sans-serif;font-weight:200;font-size:.62rem;
    letter-spacing:.35em;text-transform:uppercase;color:{TEXT_MUTED};
    margin:1.6rem 0 .9rem;display:flex;align-items:center;gap:.7rem;
}}
.sec-label::after{{content:'';flex:1;height:1px;background:{BORDER};}}

/* MODE CARDS */
.mode-card{{
    background:{SURFACE};border:1px solid {BORDER};border-radius:2px;
    padding:1.1rem 1rem .95rem;position:relative;overflow:hidden;
    transition:all .25s ease;margin-bottom:.15rem;
}}
.mode-card::after{{
    content:'';position:absolute;bottom:0;left:0;
    width:0;height:2px;background:{ACCENT};transition:width .3s ease;
}}
.mode-card.active{{
    border-color:{ACCENT};background:{SURFACE2};
    box-shadow:0 4px 22px {SHADOW};
}}
.mode-card.active::after{{width:100%;}}
.card-emoji{{font-size:1.35rem;display:block;margin-bottom:.35rem;}}
.card-name{{
    font-family:'Playfair Display',serif;font-size:.95rem;font-weight:500;
    color:{TEXT};display:block;margin-bottom:.12rem;
}}
.mode-card.active .card-name{{color:{ACCENT};font-style:italic;}}
.card-tag{{font-size:.64rem;font-weight:300;letter-spacing:.1em;color:{TEXT_MUTED};text-transform:uppercase;}}

/* ACTIVE BAR */
.active-bar{{
    display:flex;align-items:center;gap:.7rem;
    padding:.6rem 1rem;background:{SURFACE};border:1px solid {BORDER};
    border-left:3px solid {ACCENT};margin-bottom:1.4rem;border-radius:2px;
}}
.ab-mode{{font-family:'Playfair Display',serif;font-style:italic;font-size:.93rem;color:{ACCENT};}}
.ab-sep{{color:{BORDER};}}
.ab-tag{{font-size:.68rem;color:{TEXT_MUTED};font-weight:300;letter-spacing:.08em;}}

/* CHAT BUBBLES */
.chat-row{{
    display:flex;gap:.8rem;margin-bottom:1.25rem;
    align-items:flex-start;animation:fadeUp .3s ease both;
}}
@keyframes fadeUp{{
    from{{opacity:0;transform:translateY(8px);}}
    to{{opacity:1;transform:translateY(0);}}
}}
.chat-row.user{{flex-direction:row-reverse;}}
.av{{
    width:32px;height:32px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;
    flex-shrink:0;font-size:.72rem;border:1px solid {BORDER};
}}
.av.user-av{{
    background:{USER_BG};color:{USER_TEXT};font-family:'Jost',sans-serif;
    font-weight:400;letter-spacing:.04em;border:none;
}}
.av.ai-av{{background:{SURFACE2};color:{ACCENT};border-color:{ACCENT};font-size:1rem;}}
.bubble{{
    max-width:76%;padding:.82rem 1.05rem;
    font-size:.89rem;line-height:1.78;font-weight:300;border-radius:2px;
}}
.bubble.user-b{{background:{USER_BG};color:{USER_TEXT};border-bottom-right-radius:0;}}
.bubble.ai-b{{
    background:{AI_BG};color:{TEXT};border-left:2px solid {AI_BORDER};
    box-shadow:0 2px 12px {SHADOW};border-bottom-left-radius:0;
}}

/* EMPTY */
.empty{{text-align:center;padding:2.4rem 1rem;color:{TEXT_MUTED};}}
.empty .eq{{
    font-family:'Playfair Display',serif;font-style:italic;
    font-size:1.15rem;color:{ACCENT};margin-bottom:.65rem;line-height:1.6;
}}
.empty p{{font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;font-weight:200;}}

/* BUTTONS */
.stButton>button{{
    font-family:'Jost',sans-serif!important;font-weight:300!important;
    letter-spacing:.06em!important;border-radius:2px!important;
    transition:all .2s ease!important;border:1px solid {BORDER}!important;
    background:{SURFACE}!important;color:{TEXT}!important;font-size:.8rem!important;
}}
.stButton>button:hover{{border-color:{ACCENT}!important;color:{ACCENT}!important;}}

/* INPUT */
[data-testid="stChatInput"]{{
    position:fixed!important;bottom:0;left:50%;transform:translateX(-50%);
    width:100%;max-width:860px;background:{BG};
    border-top:1px solid {BORDER};padding:.72rem 1.4rem .9rem;z-index:999;
}}
[data-testid="stChatInput"] textarea{{
    font-family:'Jost',sans-serif!important;font-size:.87rem!important;
    font-weight:300!important;background:{INPUT_BG}!important;
    border:1px solid {BORDER}!important;border-radius:2px!important;
    color:{TEXT}!important;padding:.68rem 1rem!important;
}}
[data-testid="stChatInput"] textarea:focus{{
    border-color:{ACCENT}!important;
    box-shadow:0 0 0 2px {HEADER_LINE}!important;
}}
[data-testid="stChatInput"] button{{
    background:{ACCENT}!important;border-radius:2px!important;border:none!important;
}}
::-webkit-scrollbar{{width:4px;}}
::-webkit-scrollbar-track{{background:transparent;}}
::-webkit-scrollbar-thumb{{background:{BORDER};border-radius:2px;}}
</style>
""", unsafe_allow_html=True)

# ── Model ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_model():
    return init_chat_model("groq:llama-3.1-8b-instant")

model = get_model()

# ── HEADER ────────────────────────────────────────────────────────────────────
_, col_tog = st.columns([9, 1])
with col_tog:
    if st.button("☀️" if dark else "🌙", key="theme_btn", help="Toggle theme"):
        st.session_state.dark_mode = not dark
        st.rerun()

st.markdown(f"""
<div class="pv-header">
  <div class="pv-eyebrow">Crafted with precision by</div>
  <div class="pv-brand">P<span class="dot">.</span>V<span class="dot">.</span> Productions</div>
  <div class="pv-rule">✦ &nbsp; Est. 2025 &nbsp; ✦</div>
  <div class="pv-tagline">AI Companion Suite &nbsp;·&nbsp; Premium Edition</div>
</div>
""", unsafe_allow_html=True)

# ── MODE GRID ─────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-label">Choose Your Companion</div>', unsafe_allow_html=True)

mode_names = list(MODES.keys())
# COLS = 4   # cards per row

# Split into rows of 4
row1 = mode_names[0:4]
row2 = mode_names[4:8]
row3 = mode_names[8:]

for row in [row1, row2, row3]:
    cols = st.columns(len(row))
    for col, name in zip(cols, row):
        info = MODES[name]
        is_active = st.session_state.ai_mode == name
        with col:
            st.markdown(f"""
            <div class="mode-card {'active' if is_active else ''}">
              <span class="card-emoji">{info['emoji']}</span>
              <span class="card-name">{name}</span>
              <span class="card-tag">{info['tagline']}</span>
            </div>
            """, unsafe_allow_html=True)
            label = "✓ Active" if is_active else "Select"
            if st.button(label, key=f"mode_{name}", use_container_width=True):
                if not is_active:
                    st.session_state.ai_mode = name
                    st.session_state.messages = [SystemMessage(content=MODES[name]["system"])]
                    st.session_state.chat_history = []
                st.rerun()

# ── CHAT ──────────────────────────────────────────────────────────────────────
if st.session_state.ai_mode:
    info = MODES[st.session_state.ai_mode]
    st.markdown('<div class="sec-label">Conversation</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="active-bar">
      <span>{info['emoji']}</span>
      <span class="ab-mode">AI {st.session_state.ai_mode}</span>
      <span class="ab-sep">|</span>
      <span class="ab-tag">{info['tagline']}</span>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown(f"""
        <div class="empty">
          <div class="eq">Your {st.session_state.ai_mode} is ready…</div>
          <p>Type something to begin the conversation</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-row user">
                  <div class="av user-av">YOU</div>
                  <div class="bubble user-b">{msg["content"]}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-row">
                  <div class="av ai-av">{info['emoji']}</div>
                  <div class="bubble ai-b">{msg["content"]}</div>
                </div>""", unsafe_allow_html=True)

    prompt = st.chat_input(f"Talk to your {st.session_state.ai_mode}…")
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.spinner(""):
            response = model.invoke(st.session_state.messages)
        ai_text = response.content
        st.session_state.messages.append(AIMessage(content=ai_text))
        st.session_state.chat_history.append({"role": "ai", "content": ai_text})
        st.rerun()

else:
    st.markdown(f"""
    <div class="empty" style="margin-top:2rem;">
      <div class="eq">"Every great conversation starts with a choice."</div>
      <p>Select a companion above to begin</p>
    </div>
    """, unsafe_allow_html=True)