import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://localhost:8000"

def fetch_companies():
    try:
        response = requests.get(f"{BASE_URL}/companies/")
        response.raise_for_status()
        return response.json().get('companies', [])
    except requests.RequestException as e:
        st.error(f"Error fetching companies: {e}")
        return []

def run_dtw_analysis(target_company):
    try:
        response = requests.get(f"{BASE_URL}/run-dtw/", params={'target_company_name': target_company})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error in DTW analysis: {e}")
        return None

def run_clustering_analysis(target_company):
    try:
        response = requests.get(f"{BASE_URL}/run-clustering/", params={'target_company_name': target_company})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error in Clustering analysis: {e}")
        return None

def main():
    st.set_page_config(page_title="Companies Comparables Analysis", page_icon="📊", layout="wide")

    st.markdown("""
    # Companies Comparables Analysis
    This application identifies comparable companies using two complementary approaches:

    1. **Clustering Analysis (K-Means & Gaussian Mixture Models):**  
       Groups companies by evaluating multiple fundamental and financial metrics. This approach helps you quickly discover firms with similar characteristics, facilitating sector-level insights and comparative analysis.

    2. **Market Pattern Analysis (Dynamic Time Warping):**  
       Analyzes historical stock price patterns to find companies with time-series trends that closely resemble the chosen target. This method focuses on market behavior, uncovering peers that move similarly in response to market conditions.
    """)

    st.sidebar.image("logo.png", width=100)
    st.sidebar.markdown("## Companies Comparables Finder")
   
    
    st.sidebar.header("Analysis Parameters")
    companies = fetch_companies()
    target_company = st.sidebar.selectbox("Select Target Company", options=companies)
    analysis_type = st.sidebar.radio("Select Analysis Type", options=["Dynamic Time Warping", "Clustering"])

    if st.sidebar.button("Run Analysis"):
        with st.spinner(f"Running {analysis_type} Analysis..."):
            if analysis_type == "Dynamic Time Warping":
                dtw_results = run_dtw_analysis(target_company)
                if dtw_results:
                    st.subheader(f"DTW Results for {target_company}")
                    variables = ['Adj Close', 'Close', 'High', 'Low', 'Open'] 
                    tabs = st.tabs(variables)
                    for i, var in enumerate(variables):
                        with tabs[i]:
                            similar_companies = pd.DataFrame(dtw_results['results'][var], columns=['Symbol', 'Similarity Distance'])
                            st.dataframe(similar_companies.style.background_gradient(cmap='Blues'), use_container_width=True)
            else:
                clustering_results = run_clustering_analysis(target_company)
                if clustering_results:
                    st.subheader(f"Clustering Results for {target_company}")
                    st.write(f"**Target Company:** {clustering_results['target company']}")
                    st.write(f"**Symbol:** {clustering_results['target company symbol']}")
                    st.write(f"**Sector:** {clustering_results['target sector']}")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("### Similar Companies (K-Means)")
                        kmeans_df = pd.DataFrame({'Company': clustering_results['similar companies Names (Using K-means)']})
                        st.dataframe(kmeans_df, use_container_width=True)

                    with col2:
                        st.markdown("### Similar Companies (GMM)")
                        gmm_df = pd.DataFrame({'Company': clustering_results['similar companies Names (Using GMM)']})
                        st.dataframe(gmm_df, use_container_width=True)

    st.markdown("""
    <style>
    .stApp {
        background-color: #f4f4f4;
    }
    .stDataFrame {
        background-color: white;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 0.375rem;
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
