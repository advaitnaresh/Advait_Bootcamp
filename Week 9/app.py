import streamlit as st
import pandas as pd
import sqlite3
import time
import altair as alt

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Aries | Brand Intel",
    page_icon="♈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- UI STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    div[data-testid="stMetric"] {
        background-color: #262730;
        border: 1px solid #41444C;
        padding: 15px;
        border-radius: 10px;
    }
    h1 {
        background: -webkit-linear-gradient(45deg, #7C3AED, #DB2777);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADER ---
def get_data():
    try:
        conn = sqlite3.connect("aries_data.db")
        # Fetch fewer records for the chart to keep the "Zoom" tight
        df = pd.read_sql("SELECT * FROM sentiment_data ORDER BY id DESC LIMIT 200", conn)
        conn.close()
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values(by='timestamp', ascending=True)
        return df
    except:
        return pd.DataFrame()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/aries.png", width=60)
    st.markdown("## Team Science")
    st.markdown("### Project Aries")
    st.divider()
    
    TARGET_BRANDS = ["All Brands", "Apple", "Nike", "Tesla", "Samsung", "Disney", "Google", "Amazon", "Microsoft", "Sony", "Netflix"]
    selected_brand = st.selectbox("Select Brand Focus", TARGET_BRANDS)
    
    # Increase default speed for smoother visualization
    refresh_rate = st.slider("Refresh Speed (sec)", 0.5, 5.0, 1.0)
    st.success("● System Online")

# --- MAIN DASHBOARD ---
st.title("Aries Brand Intelligence")
st.markdown(f"### Real-Time Social Sentiment Monitor | **{selected_brand}**")

placeholder = st.empty()

while True:
    df = get_data()
    
    with placeholder.container():
        if df.empty:
            st.warning("⚠️ No data stream detected. Please run 'python3 backend.py' in your terminal.")
        else:
            # 1. FILTER
            if selected_brand != "All Brands":
                filtered_df = df[df['brand'] == selected_brand].copy()
            else:
                filtered_df = df.copy()

            if filtered_df.empty:
                st.info(f"Waiting for new data regarding **{selected_brand}**...")
            else:
                # 2. CALCULATE EMA (Signal Smoothing)
                # We calculate this AFTER filtering so the EMA is specific to the brand's trend line
                filtered_df['smooth_trend'] = filtered_df['sentiment'].ewm(span=10, adjust=False).mean()
                
                health_score = filtered_df['smooth_trend'].iloc[-1]

                # 3. METRICS
                if health_score < -0.2:
                    status_label = "CRITICAL"
                    status_color = "inverse"
                elif health_score > 0.2:
                    status_label = "EXCELLENT"
                    status_color = "normal"
                else:
                    status_label = "STABLE"
                    status_color = "off"

                k1, k2, k3, k4 = st.columns(4)
                k1.metric("Live Posts (Buffer)", len(filtered_df))
                k2.metric("Latest Raw Score", f"{filtered_df['sentiment'].iloc[-1]:.2f}")
                k3.metric("HEALTH STATUS", status_label, delta=f"EMA: {health_score:.2f}", delta_color=status_color)
                k4.metric("Focus", selected_brand)

                st.divider()

                # 4. CHARTING
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.subheader(f"Sentiment Trend (EMA)")
                    
                    # 1. Base Chart
                    base = alt.Chart(filtered_df).encode(
                        x=alt.X('timestamp', title='Time', axis=alt.Axis(format='%H:%M:%S'))
                    )

                    # 2. The Line (Trend) - NOW LOCKED TO [-1, 1]
                    line = base.mark_line(strokeWidth=4, color='#29B5E8').encode(
                        y=alt.Y('smooth_trend', 
                                title='Sentiment Score', 
                                scale=alt.Scale(domain=[-1, 1])) # <--- THIS LOCKS THE AXIS
                    )

                    # 3. The Points (Raw Data)
                    points = base.mark_circle(size=60, opacity=0.8).encode(
                        y=alt.Y('sentiment', scale=alt.Scale(domain=[-1, 1])), # Ensure points respect the same scale
                        color=alt.Color('sentiment', 
                                      scale=alt.Scale(domain=[-1, 0, 1], range=['#FF4B4B', '#FFD700', '#2ECC71']),
                                      legend=None),
                        tooltip=['brand', 'text', 'sentiment']
                    )

                    # 4. Combine
                    chart = (line + points).properties(
                        height=400
                    ).interactive()

                    st.altair_chart(chart, use_container_width=True)

                with col2:
                    st.subheader("📢 Live Feed")
                    # Get the 4 most recent posts, reversed so newest is on top
                    recent_posts = filtered_df.tail(4).iloc[::-1]
                    
                    for _, row in recent_posts.iterrows():
                        score = row['sentiment']
                        text_display = f"**{row['brand']}**: {row['text']}"
                        
                        # RESTORED: Colored boxes with explicit weights
                        if score > 0.05:
                            # Green box for positive
                            st.success(f"{text_display} \n\n *(Score: {score:.2f})*")
                        elif score < -0.05:
                            # Red box for negative
                            st.error(f"{text_display} \n\n *(Score: {score:.2f})*")
                        else:
                            # Blue/Grey box for neutral
                            st.info(f"{text_display} \n\n *(Score: {score:.2f})*")

    time.sleep(refresh_rate)