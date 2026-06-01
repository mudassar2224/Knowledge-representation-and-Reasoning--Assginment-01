from pathlib import Path
from functools import lru_cache

import streamlit as st

from aiml_bot import load_aiml
from chatbot import handle_input
from prolog_engine import load_kb, query
from utils import PROPERTY_RELATIONS, RELATION_NAMES


APP_TITLE = "Family Knowledge Base Chatbot"
APP_SUBTITLE = (
    "A polished Streamlit front-end for the same Prolog + AIML brain used by the "
    "console app."
)
WELCOME_MESSAGE = (
    "Hello! I’m your family knowledge-base chatbot. Ask about relationships, "
    "properties, cities, religion, or a full profile."
)

ASSET_DIR = Path(__file__).resolve().parent / "assets"
PROFILE_IMAGE_CANDIDATES = (
    ASSET_DIR / "profile.png",
    ASSET_DIR / "profile.jpg",
    ASSET_DIR / "profile.jpeg",
    ASSET_DIR / "profile.webp",
)


def _find_profile_image():
    for candidate in PROFILE_IMAGE_CANDIDATES:
        if candidate.exists():
            return str(candidate)
    return None


def _extract_values(raw, var="X"):
    values = []
    for item in raw or []:
        if isinstance(item, dict):
            value = item.get(var, "")
            if value:
                values.append(str(value))
        elif isinstance(item, str) and item.lower() not in {"yes", "no", "false"}:
            values.append(item)

    seen = set()
    unique_values = []
    for value in values:
        if value not in seen:
            seen.add(value)
            unique_values.append(value)
    return unique_values


def _family_members():
    members = _extract_values(query("male", ["X"])) + _extract_values(query("female", ["X"]))
    return sorted(set(members))


def _family_cities():
    return sorted(set(_extract_values(query("lives_in", ["X", "Y"]), var="Y")))


def _family_occupations():
    return sorted(set(_extract_values(query("occupation", ["X", "Y"]), var="Y")))


def _family_religions():
    return sorted(set(_extract_values(query("religion", ["X", "Y"]), var="Y")))


def build_suggested_queries():
    members = _family_members()
    cities = _family_cities()
    focus = "ali" if "ali" in members else (members[0] if members else "ali")
    city = "lahore" if "lahore" in cities else (cities[0] if cities else "lahore")
    focus_name = focus.title()
    city_name = city.title()

    return [
        f"Who is {focus_name}'s father?",
        f"What is {focus_name}'s dob?",
        f"Who lives in {city_name}?",
        f"Tell me about {focus_name}",
    ]


@lru_cache(maxsize=1)
def init_bot():
    load_kb()
    load_aiml()
    return True


@lru_cache(maxsize=1)
def kb_overview():
    members = _family_members()
    cities = _family_cities()
    occupations = _family_occupations()
    religions = _family_religions()

    return {
        "people_count": len(members),
        "city_count": len(cities),
        "occupation_count": len(occupations),
        "religion_count": len(religions),
        "relation_count": len(RELATION_NAMES),
        "property_count": len(PROPERTY_RELATIONS),
    }


def reset_chat():
    st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]


def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})


def ask_bot(prompt):
    add_message("user", prompt)
    add_message("assistant", handle_input(prompt))


def apply_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(255, 162, 125, 0.20), transparent 30%),
                radial-gradient(circle at top right, rgba(145, 197, 255, 0.18), transparent 30%),
                linear-gradient(180deg, #fffdf9 0%, #fff8f4 50%, #f7fbff 100%);
        }

        section[data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.78);
            backdrop-filter: blur(18px);
        }

        .hero-card {
            padding: 1.25rem 1.45rem;
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.85);
            background: rgba(255, 255, 255, 0.62);
            box-shadow: 0 14px 40px rgba(31, 41, 55, 0.08);
            margin-bottom: 1rem;
        }

        .hero-title {
            font-size: 2.15rem;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 0.35rem;
            color: #1f2937;
        }

        .hero-subtitle {
            font-size: 1rem;
            color: #586477;
            margin-bottom: 0.85rem;
        }

        .pill {
            display: inline-block;
            padding: 0.38rem 0.78rem;
            margin: 0.15rem 0.28rem 0 0;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.78);
            border: 1px solid rgba(255, 255, 255, 0.92);
            color: #405066;
            font-size: 0.82rem;
            font-weight: 600;
        }

        .section-label {
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #6b7280;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(assistant_avatar, overview):
    with st.sidebar:
        st.markdown("## Family Knowledge Base")
        if assistant_avatar:
            st.image(assistant_avatar, width=92)
        else:
            st.markdown(
                "<div style='font-size:3rem;line-height:1;text-align:center;'>💬</div>",
                unsafe_allow_html=True,
            )

        st.caption("Console and Streamlit share the same `handle_input()` logic.")
        st.markdown("<div class='section-label'>Live status</div>", unsafe_allow_html=True)
        st.success("Prolog knowledge base loaded")
        st.success("AIML patterns loaded")

        stat_row_one = st.columns(2)
        stat_row_one[0].metric("People", overview["people_count"])
        stat_row_one[1].metric("Cities", overview["city_count"])

        stat_row_two = st.columns(2)
        stat_row_two[0].metric("Relations", overview["relation_count"])
        stat_row_two[1].metric("Properties", overview["property_count"])

        st.markdown("<div class='section-label'>Manage chat</div>", unsafe_allow_html=True)
        if st.button("Clear chat", use_container_width=True):
            reset_chat()
            st.rerun()

        with st.expander("What this bot can answer"):
            st.markdown(
                "- Relationships: father, mother, sibling, uncle, aunt, cousin\n"
                "- Urdu relations: chacha, phoophi, maamu, khala, dada, nani\n"
                "- Properties: date of birth, occupation, city, religion\n"
                "- Lists and yes/no queries from the family KB\n"
                "- Full profile summaries"
            )

        st.caption(
            "Add your image as `assets/profile.png` (or `.jpg`, `.jpeg`, `.webp`) and push it to GitHub."
        )


def render_header(assistant_avatar, suggested_queries):
    left_col, right_col = st.columns([0.84, 0.16])
    with left_col:
        st.markdown(
            f"""
            <div class="hero-card">
                <div class="hero-title">Hi, I’m Family Chatbot 👋</div>
                <div class="hero-subtitle">
                    {APP_SUBTITLE} Ask family knowledge-base questions and get answers
                    from the same rules and facts used by the console app.
                </div>
                <div>
                    <span class="pill">father</span>
                    <span class="pill">mother</span>
                    <span class="pill">siblings</span>
                    <span class="pill">ancestor</span>
                    <span class="pill">occupation</span>
                    <span class="pill">city</span>
                    <span class="pill">religion</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right_col:
        if assistant_avatar:
            st.image(assistant_avatar, width=96)
        else:
            st.markdown(
                "<div class='hero-card' style='text-align:center;font-size:3rem;'>💬</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<div class='section-label'>Suggested questions</div>", unsafe_allow_html=True)
    sample_cols = st.columns(2)
    for index, sample in enumerate(suggested_queries):
        with sample_cols[index % 2]:
            if st.button(sample, key=f"sample_{index}", use_container_width=True):
                ask_bot(sample)


def render_conversation(assistant_avatar):
    st.markdown("<div class='section-label'>Conversation</div>", unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message["role"] == "assistant" and assistant_avatar:
            avatar = assistant_avatar
        elif message["role"] == "assistant":
            avatar = "💬"
        else:
            avatar = "🧑‍💻"

        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])


def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=_find_profile_image() or "💬",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_bot()

    if "messages" not in st.session_state:
        reset_chat()

    assistant_avatar = _find_profile_image()
    overview = kb_overview()
    suggested_queries = build_suggested_queries()

    apply_styles()
    render_sidebar(assistant_avatar, overview)

    prompt = st.chat_input(
        "Ask about father, sibling, ancestor, occupation, city, religion, or profile..."
    )
    if prompt:
        ask_bot(prompt)

    render_header(assistant_avatar, suggested_queries)
    render_conversation(assistant_avatar)


if __name__ == "__main__":
    main()
