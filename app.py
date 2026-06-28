import json

import joblib
import numpy as np
import pandas as pd
import requests
import streamlit as st
from streamlit_geolocation import streamlit_geolocation


st.set_page_config(
    page_title="Kerala Travel Planner",
    page_icon="KT",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --ink: #12211c;
            --muted: #60736a;
            --leaf: #0f7b54;
            --leaf-dark: #075c3e;
            --aqua: #00a7a0;
            --gold: #f2b84b;
            --shell: #fffaf0;
            --mist: #e8f7f0;
            --line: rgba(18, 33, 28, 0.12);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            color: var(--ink);
            background:
                radial-gradient(circle at 10% 8%, rgba(242, 184, 75, 0.22), transparent 28%),
                radial-gradient(circle at 92% 18%, rgba(0, 167, 160, 0.22), transparent 30%),
                linear-gradient(135deg, #fffaf0 0%, #e8f7f0 48%, #f8fbff 100%);
        }

        .block-container {
            max-width: 1220px;
            padding-top: 2rem;
            padding-bottom: 2.5rem;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .hero {
            position: relative;
            overflow: hidden;
            border-radius: 22px;
            padding: 3rem;
            margin-bottom: 1.3rem;
            min-height: 280px;
            border: 1px solid rgba(255, 255, 255, 0.7);
            box-shadow: 0 24px 70px rgba(18, 33, 28, 0.14);
            background:
                linear-gradient(105deg, rgba(5, 64, 44, 0.88), rgba(13, 111, 78, 0.72)),
                url("https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1800&q=80");
            background-size: cover;
            background-position: center;
        }

        .hero::after {
            content: "";
            position: absolute;
            inset: auto -5% -35% auto;
            width: 420px;
            height: 420px;
            border-radius: 999px;
            background: rgba(242, 184, 75, 0.32);
            filter: blur(6px);
        }

        .eyebrow {
            width: fit-content;
            padding: 0.45rem 0.75rem;
            border-radius: 999px;
            color: #f9ffe9;
            background: rgba(255, 255, 255, 0.14);
            border: 1px solid rgba(255, 255, 255, 0.24);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .hero h1 {
            max-width: 760px;
            margin: 1rem 0 0.8rem 0;
            color: white !important;
            font-size: clamp(2.4rem, 6vw, 4.8rem) !important;
            line-height: 0.95;
            font-weight: 800 !important;
            letter-spacing: 0 !important;
        }

        .hero p {
            max-width: 620px;
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.08rem;
            line-height: 1.7;
            margin: 0;
        }

        .metric-strip {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.8rem;
            margin-top: 1.6rem;
            max-width: 680px;
        }

        .mini-metric {
            padding: 0.9rem 1rem;
            border-radius: 16px;
            color: white;
            background: rgba(255, 255, 255, 0.13);
            border: 1px solid rgba(255, 255, 255, 0.22);
            backdrop-filter: blur(12px);
        }

        .mini-metric strong {
            display: block;
            font-size: 1.35rem;
            line-height: 1;
        }

        .mini-metric span {
            display: block;
            margin-top: 0.35rem;
            color: rgba(255, 255, 255, 0.78);
            font-size: 0.78rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        section[data-testid="stSidebar"] {
            background: #fffaf0;
        }

        div[data-testid="stVerticalBlock"] > div:has(.panel) {
            height: 100%;
        }

        .panel {
            height: 100%;
            padding: 1.4rem;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.78);
            border: 1px solid rgba(255, 255, 255, 0.85);
            box-shadow: 0 18px 45px rgba(18, 33, 28, 0.10);
            backdrop-filter: blur(18px);
        }

        .panel-title {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            margin-bottom: 0.2rem;
            color: var(--ink);
            font-size: 1.35rem;
            font-weight: 800;
        }

        .panel-subtitle {
            margin-bottom: 1.2rem;
            color: var(--muted);
            line-height: 1.55;
        }

        .stSlider [data-baseweb="slider"] > div {
            color: var(--leaf);
        }

        .stSelectbox div[data-baseweb="select"] > div {
            border-radius: 14px;
            border-color: var(--line);
            background: rgba(255, 255, 255, 0.92);
        }

        .stButton > button,
        .stLinkButton > a {
            min-height: 3rem;
            border-radius: 14px !important;
            border: 0 !important;
            color: white !important;
            font-weight: 800 !important;
            box-shadow: 0 12px 28px rgba(15, 123, 84, 0.25);
            background: linear-gradient(135deg, var(--leaf), var(--aqua)) !important;
        }

        .stButton > button:hover,
        .stLinkButton > a:hover {
            transform: translateY(-1px);
            box-shadow: 0 16px 34px rgba(15, 123, 84, 0.32);
        }

        .result-card {
            margin-top: 1rem;
            padding: 1.25rem;
            border-radius: 18px;
            color: white;
            background:
                linear-gradient(135deg, rgba(7, 92, 62, 0.94), rgba(0, 167, 160, 0.82)),
                url("https://images.unsplash.com/photo-1593693397690-362cb9666fc2?auto=format&fit=crop&w=1200&q=80");
            background-size: cover;
            background-position: center;
            box-shadow: 0 16px 38px rgba(7, 92, 62, 0.24);
        }

        .result-card small {
            color: rgba(255, 255, 255, 0.74);
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .result-card h2 {
            margin: 0.4rem 0 0.25rem 0;
            color: white !important;
            font-size: 2.1rem !important;
            font-weight: 800 !important;
            letter-spacing: 0 !important;
        }

        .result-card p {
            margin: 0.35rem 0 0 0;
            color: rgba(255, 255, 255, 0.88);
        }

        .nearby-card {
            padding: 1rem;
            margin-bottom: 0.8rem;
            border-radius: 16px;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(232, 247, 240, 0.88));
            border: 1px solid var(--line);
        }

        .nearby-card strong {
            display: block;
            margin-bottom: 0.25rem;
            font-size: 1.02rem;
        }

        .nearby-card span {
            color: var(--muted);
            font-size: 0.92rem;
            line-height: 1.5;
        }

        .hint-box {
            padding: 1rem;
            border-radius: 16px;
            color: var(--leaf-dark);
            background: rgba(242, 184, 75, 0.16);
            border: 1px solid rgba(242, 184, 75, 0.32);
        }

        [data-testid="stMetricValue"] {
            color: var(--leaf-dark);
            font-weight: 800;
        }

        .stMap {
            overflow: hidden;
            border-radius: 18px;
            border: 1px solid var(--line);
            box-shadow: 0 14px 35px rgba(18, 33, 28, 0.08);
        }

        hr {
            border-color: rgba(18, 33, 28, 0.1);
        }

        @media (max-width: 760px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .hero {
                padding: 1.6rem;
                border-radius: 18px;
            }

            .metric-strip {
                grid-template-columns: 1fr;
            }

            .panel {
                padding: 1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def calculate_distance(lat1, lon1, lat2, lon2):
    radius_km = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return radius_km * c


@st.cache_resource
def load_assets():
    model = joblib.load("models/kerala_model.joblib")
    encoder = joblib.load("models/vibe_encoder.joblib")
    with open("models/config.json", "r", encoding="utf-8") as file:
        config = json.load(file)
    return model, encoder, config


@st.cache_data
def load_places():
    return pd.read_csv("data/data/kerala_spots.csv")


def fetch_weather(destination):
    try:
        response = requests.get(f"https://wttr.in/{destination}?format=3", timeout=4)
        if response.status_code == 200:
            return response.text.strip()
    except requests.RequestException:
        return None
    return None


def maps_url(origin_lat, origin_lon, dest_lat, dest_lon):
    return (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={origin_lat},{origin_lon}"
        f"&destination={dest_lat},{dest_lon}"
        "&travelmode=driving"
    )


def panel_open(title, subtitle):
    st.markdown(
        f"""
        <div class="panel">
            <div class="panel-title">{title}</div>
            <div class="panel-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def panel_close():
    st.markdown("</div>", unsafe_allow_html=True)


try:
    model, encoder, config = load_assets()
    df_places = load_places()

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Smart Kerala Travel Planner</div>
            <h1>Plan Your Perfect Kerala Trip.</h1>
            <p>
                Explore Kerala, Your Way—with personalized travel recommendations tailored to your budget, trip duration, and travel preferences.
            </p>
            <div class="metric-strip">
                <div class="mini-metric"><strong>14+</strong><span>Travel moods</span></div>
                <div class="mini-metric"><strong>Live</strong><span>Route links</span></div>
                <div class="mini-metric"><strong>Smart</strong><span>ML match</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.02, 0.98], gap="large")

    with left:
        panel_open(
            "Plan your match",
            "Tune the sliders and let the model choose a destination that matches your travel style.",
        )

        budget = st.slider(
            "Budget in INR",
            int(config["min_budget"]),
            int(config["max_budget"]),
            int(config["min_budget"]),
            step=500,
        )
        days = st.slider("Trip length in days", 1, int(config["max_days"]), 2)
        selected_vibe = st.selectbox("Preferred vibe", config["vibes"])

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Generate recommendation", type="primary", use_container_width=True):
            encoded_vibe = encoder.transform([selected_vibe])[0]
            input_data = np.array([[budget, days, encoded_vibe]])
            prediction = model.predict(input_data)[0]

            weather = fetch_weather(prediction)
            weather_line = weather if weather else "Weather feed unavailable right now."

            st.markdown(
                f"""
                <div class="result-card">
                    <small>Your destination match</small>
                    <h2>{prediction}</h2>
                    <p>{weather_line}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            predicted_row = df_places[df_places["destination"] == prediction]
            if not predicted_row.empty:
                p_lat = float(predicted_row["latitude"].values[0])
                p_lon = float(predicted_row["longitude"].values[0])

                route_ready = (
                    "user_latitude" in st.session_state
                    and st.session_state["user_latitude"] is not None
                    and "user_longitude" in st.session_state
                )

                if route_ready:
                    st.link_button(
                        "Open navigation",
                        maps_url(
                            st.session_state["user_latitude"],
                            st.session_state["user_longitude"],
                            p_lat,
                            p_lon,
                        ),
                        use_container_width=True,
                    )

                st.map(pd.DataFrame({"lat": [p_lat], "lon": [p_lon]}), zoom=10)
            else:
                st.warning("The predicted destination was not found in kerala_spots.csv.")

        panel_close()

    with right:
        panel_open(
            "Nearby radar",
            "Allow browser location access to see the closest Kerala spots and direct driving routes.",
        )

        location = streamlit_geolocation()

        if location and location.get("latitude") is not None:
            user_lat = location["latitude"]
            user_lon = location["longitude"]

            st.session_state["user_latitude"] = user_lat
            st.session_state["user_longitude"] = user_lon

            df_nearby = df_places.copy()
            df_nearby["Distance_KM"] = df_nearby.apply(
                lambda row: calculate_distance(
                    user_lat,
                    user_lon,
                    row["latitude"],
                    row["longitude"],
                ),
                axis=1,
            )
            df_sorted = df_nearby.sort_values(by="Distance_KM").head(3)

            metric_cols = st.columns(3)
            metric_cols[0].metric("Latitude", f"{user_lat:.3f}")
            metric_cols[1].metric("Longitude", f"{user_lon:.3f}")
            metric_cols[2].metric("Nearest", f"{df_sorted.iloc[0]['Distance_KM']:.1f} km")

            st.markdown("#### Closest picks")
            for _, row in df_sorted.iterrows():
                st.markdown(
                    f"""
                    <div class="nearby-card">
                        <strong>{row['destination']}</strong>
                        <span>{row['vibe']} | {row['Distance_KM']:.1f} km away</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.link_button(
                    "Route to this place",
                    maps_url(user_lat, user_lon, row["latitude"], row["longitude"]),
                    use_container_width=True,
                )

            map_data = df_sorted[["latitude", "longitude"]].rename(
                columns={"latitude": "lat", "longitude": "lon"}
            )
            st.map(map_data, zoom=7)
        else:
            st.markdown(
                """
                <div class="hint-box">
                    Location permission is waiting. Click the browser prompt to unlock nearby places and route buttons.
                </div>
                """,
                unsafe_allow_html=True,
            )

        panel_close()

except FileNotFoundError as error:
    st.error(
        "Missing project file. Make sure models/kerala_model.joblib, "
        "models/vibe_encoder.joblib, models/config.json, and data/data/kerala_spots.csv "
        f"exist beside this app. Details: {error}"
    )
except Exception as error:
    st.error(f"Something went wrong while running the app: {error}")
