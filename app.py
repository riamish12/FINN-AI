
import streamlit as st

# --- Invite Code Validation ---
def check_invite():
    code = st.text_input("Enter Invite Code", type="password")
    if code == "INVITE-CODE-2025":
        st.session_state['authorized'] = True
    elif code:
        st.error("Invalid Invite Code.")

# --- Main App ---
def main():
    st.set_page_config(page_title="FINN – AI Hedge Fund", page_icon="💠", layout="wide")
    
    if 'authorized' not in st.session_state:
        st.session_state['authorized'] = False

    if not st.session_state['authorized']:
        st.title("🔒 Welcome to FINN")
        st.subheader("Private AI Hedge Fund Access")
        check_invite()
        return

    # --- Sidebar ---
    with st.sidebar:
        st.title("💠 FINN")
        st.write("AI Hedge Fund Pro")
        st.markdown("---")
        st.write("Built by Ria Mishra © 2025")

    # --- Main Content ---
    st.title("📊 AI Portfolio Analysis")
    st.write("Welcome to your private AI-powered hedge fund app. Select your investment mode, enter tickers, and view AI insights.")
    # Placeholder content
    st.info("Portfolio Mode, Signal Scoring, Backtest Visualization & Prediction will appear here.")

    # --- Footer ---
    st.markdown(
        "<hr><center>Built by Ria Mishra © 2025 – FINN</center>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
