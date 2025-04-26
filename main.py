import streamlit as st
import pandas as pd
import math
import statistics
from scipy import stats


def calculate_statistics(data, confidence=0.95):
    if len(data) == 0:
        return None

    mean = statistics.mean(data)
    variance = statistics.variance(data)
    std_dev = statistics.stdev(data)

    n = len(data)
    stderr = std_dev / math.sqrt(n)

    t_score = stats.t.ppf((1 + confidence) / 2, n - 1)
    margin_of_error = t_score * stderr
    confidence_interval = (mean - margin_of_error, mean + margin_of_error)

    return {
        "Mean": mean,
        "Variance": variance,
        "Standard Deviation": std_dev,
        f"{int(confidence * 100)}% Confidence Interval": confidence_interval
    }


# --- Streamlit App ---
st.set_page_config(page_title="Statistical Calculator", layout="centered")

st.title('📈 Statistical Calculator')

uploaded_file = st.file_uploader("Upload your CSV or TXT file", type=["csv", "txt"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            st.success('CSV file loaded successfully!')

            column = st.selectbox('Select the column for analysis', df.columns)
            data = df[column].dropna().tolist()

        elif uploaded_file.name.endswith('.txt'):
            data = [float(line.decode('utf-8').strip()) for line in uploaded_file.readlines()]
            st.success('TXT file loaded successfully!')

        else:
            st.error('Unsupported file format.')
            data = None

        if data:
            confidence_percent = st.selectbox('Select Confidence Level', [90, 95, 99])
            confidence = confidence_percent / 100

            if st.button('Calculate Statistics'):
                results = calculate_statistics(data, confidence)
                if results:
                    st.subheader('Results:')
                    for key, value in results.items():
                        st.write(f"**{key}**: {value}")
                else:
                    st.warning('No data to analyze.')

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info('Please upload a dataset file (.csv or .txt)')
