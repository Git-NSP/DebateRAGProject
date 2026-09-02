import streamlit as st

# ==========================================================
# STREAMLIT CONFIG
# ==========================================================

st.set_page_config(
    page_title="Debate",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================================
# CUSTOM UI
# ==========================================================

st.markdown(
    """
    <style>

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(
                circle at 15% 0%,
                rgba(48, 67, 61, 0.14),
                transparent 28%
            ),
            radial-gradient(
                circle at 85% 0%,
                rgba(72, 48, 51, 0.12),
                transparent 25%
            ),
            #0d0f12;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    p {
        color: #b8bcc4;
    }

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }

    .hero {
        padding: 1rem 0 1.6rem 0;
    }

    .hero-label {
        color: #7e858e;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.45rem;
    }

    .hero-title {
        color: #f2f3f5;
        font-size: 2.4rem;
        font-weight: 700;
        letter-spacing: -0.04em;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        color: #9197a0;
        font-size: 0.95rem;
        max-width: 760px;
        line-height: 1.55;
    }

    .topic-label {
        color: #747b84;
        font-size: 0.73rem;
        font-weight: 700;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }

    .topic-title {
        color: #e8eaed;
        font-size: 1.35rem;
        font-weight: 650;
        margin-bottom: 0.25rem;
    }

    .topic-caption {
        color: #858c95;
        font-size: 0.87rem;
        margin-bottom: 0.8rem;
    }

    [data-testid="stTextInput"] input {
        background: #111419;
        border: 1px solid #30353d;
        border-radius: 9px;
        color: #eef0f3;
    }

    [data-testid="stTextInput"] input:focus {
        border-color: #59616c;
        box-shadow: none;
    }

    .stButton > button {
        background: #1d2228;
        color: #e8eaed;
        border: 1px solid #343a43;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.55rem 1rem;
        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        background: #252b32;
        border-color: #4b535e;
        color: #ffffff;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #262a30 !important;
        border-radius: 14px !important;
        background: rgba(19, 22, 26, 0.88);
        box-shadow: 0 8px 26px rgba(0, 0, 0, 0.14);
    }

    .round-label {
        color: #777e87;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }

    .speaker-header {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin-bottom: 0.65rem;
    }

    .speaker-name {
        color: #eceef1;
        font-size: 1.08rem;
        font-weight: 650;
    }

    .pro-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: #6f9b83;
        display: inline-block;
        box-shadow: 0 0 0 4px rgba(111, 155, 131, 0.10);
    }

    .con-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: #a06f73;
        display: inline-block;
        box-shadow: 0 0 0 4px rgba(160, 111, 115, 0.10);
    }

    .argument-label {
        color: #737a83;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .evidence-count {
        color: #838a93;
        font-size: 0.82rem;
        margin-top: 0.7rem;
        margin-bottom: 0.4rem;
    }

    [data-testid="stExpander"] {
        border: 1px solid #292e35;
        border-radius: 9px;
        background: #111419;
    }

    [data-testid="stAlert"] {
        border-radius: 9px;
    }

    hr {
        border-color: #23272d !important;
        margin: 2rem 0 !important;
    }

    .complete-card {
        border: 1px solid #292e35;
        border-radius: 14px;
        background:
            linear-gradient(
                120deg,
                rgba(30, 35, 41, 0.92),
                rgba(18, 21, 25, 0.92)
            );
        padding: 1.4rem 1.6rem;
        margin-bottom: 0.8rem;
    }

    .complete-label {
        color: #777e87;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .complete-title {
        color: #edf0f3;
        font-size: 1.3rem;
        font-weight: 650;
        margin-bottom: 0.25rem;
    }

    .complete-caption {
        color: #8f969f;
        font-size: 0.88rem;
    }

    [data-testid="stPageLink"] a {
        background: #1d2228;
        border: 1px solid #353b44;
        border-radius: 9px;
        padding: 0.65rem 1rem;
        text-decoration: none;
        transition: all 0.15s ease;
    }

    [data-testid="stPageLink"] a:hover {
        background: #262c33;
        border-color: #555d67;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-label">Debate Workspace</div>
        <div class="hero-title">AI Debate</div>
        <div class="hero-subtitle">
            Pro and Con agents retrieve evidence independently and respond to
            each other across five evidence-grounded rounds.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# TOPIC INPUT
# ==========================================================

with st.container(border=True):

    st.markdown(
        """
        <div class="topic-label">Debate Setup</div>
        <div class="topic-title">Choose the proposition</div>
        <div class="topic-caption">
            Enter the topic that both agents should debate using their respective repositories.
        </div>
        """,
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "Debate Topic",
        label_visibility="collapsed",
        placeholder="Example: Artificial intelligence will create more jobs than it eliminates"
    )

    if st.button(
        "Start Debate",
        use_container_width=False
    ):

        if not topic.strip():

            st.warning(
                "Please enter a debate topic."
            )

        else:

            from utils.debate import Debate

            debate = Debate()

            with st.spinner(
                "Running the debate..."
            ):

                result = debate.run(
                    topic
                )

            st.session_state[
                "debate_result"
            ] = result

            st.session_state[
                "topic"
            ] = topic

            st.success(
                "Debate completed."
            )


# ==========================================================
# DEBATE RESULT
# ==========================================================

if "debate_result" in st.session_state:

    result = st.session_state[
        "debate_result"
    ]

    history = result[
        "history"
    ]

    debate_topic = st.session_state.get(
        "topic",
        ""
    )

    st.divider()

    st.markdown(
        f"""
        <div class="topic-label">Active Debate</div>
        <div class="topic-title">{debate_topic}</div>
        <div class="topic-caption">
            Five rounds · Evidence-grounded Pro vs Con
        </div>
        """,
        unsafe_allow_html=True
    )


    # ======================================================
    # GROUP TURNS BY ROUND
    # ======================================================

    rounds = {}

    for turn in history:

        round_no = turn["round"]

        if round_no not in rounds:

            rounds[round_no] = {}

        rounds[round_no][
            turn["speaker"]
        ] = turn


    # ======================================================
    # DISPLAY ROUNDS
    # ======================================================

    for round_no in sorted(
        rounds.keys()
    ):

        with st.container(
            border=True
        ):

            st.markdown(
                f"""
                <div class="round-label">
                    Round {round_no:02d}
                </div>
                """,
                unsafe_allow_html=True
            )

            pro_col, con_col = st.columns(
                2,
                gap="large"
            )


            # ==================================================
            # PRO
            # ==================================================

            with pro_col:

                pro_turn = rounds[
                    round_no
                ].get(
                    "Pro"
                )

                st.markdown(
                    """
                    <div class="speaker-header">
                        <span class="pro-dot"></span>
                        <span class="speaker-name">Pro</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if pro_turn:

                    st.markdown(
                        """
                        <div class="argument-label">
                            Argument
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.write(
                        pro_turn[
                            "argument"
                        ]
                    )

                    pro_sources = (
                        pro_turn.get(
                            "sources",
                            []
                        )
                    )

                    st.markdown(
                        f"""
                        <div class="evidence-count">
                            Evidence · {len(pro_sources)} source{"s" if len(pro_sources) != 1 else ""}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if pro_sources:

                        for source in pro_sources:

                            source_id = source[
                                "id"
                            ]

                            source_file = source[
                                "source_file"
                            ]

                            page = source[
                                "page"
                            ]

                            content = source[
                                "content"
                            ]

                            with st.expander(
                                f"{source_id} · {source_file} · Page {page}"
                            ):

                                st.markdown(
                                    "**Retrieved evidence**"
                                )

                                st.write(
                                    content
                                )

                    else:

                        st.caption(
                            "No retrieved document was explicitly cited."
                        )


            # ==================================================
            # CON
            # ==================================================

            with con_col:

                con_turn = rounds[
                    round_no
                ].get(
                    "Con"
                )

                st.markdown(
                    """
                    <div class="speaker-header">
                        <span class="con-dot"></span>
                        <span class="speaker-name">Con</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if con_turn:

                    st.markdown(
                        """
                        <div class="argument-label">
                            Counterargument
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.write(
                        con_turn[
                            "argument"
                        ]
                    )

                    con_sources = (
                        con_turn.get(
                            "sources",
                            []
                        )
                    )

                    st.markdown(
                        f"""
                        <div class="evidence-count">
                            Evidence · {len(con_sources)} source{"s" if len(con_sources) != 1 else ""}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if con_sources:

                        for source in con_sources:

                            source_id = source[
                                "id"
                            ]

                            source_file = source[
                                "source_file"
                            ]

                            page = source[
                                "page"
                            ]

                            content = source[
                                "content"
                            ]

                            with st.expander(
                                f"{source_id} · {source_file} · Page {page}"
                            ):

                                st.markdown(
                                    "**Retrieved evidence**"
                                )

                                st.write(
                                    content
                                )

                    else:

                        st.caption(
                            "No retrieved document was explicitly cited."
                        )


    # ======================================================
    # DEBATE COMPLETE
    # ======================================================

    st.divider()

    st.markdown(
        """
        <div class="complete-card">
            <div class="complete-label">Debate Complete</div>
            <div class="complete-title">Five rounds concluded</div>
            <div class="complete-caption">
                Continue to the Judge workspace to review the final evaluation.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.page_link(
        "pages/judge_show.py",
        label="Open Judge Workspace",
        icon="🏆"
    )













