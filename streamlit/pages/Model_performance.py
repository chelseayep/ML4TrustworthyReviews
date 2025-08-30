import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Model Performance on Test Data")

st.write("Evaluation results of the review evaluator model on a curated test dataset of 200 reviews.")

# Create a dictionary for all policy violation metrics
violation_metrics = {
    "Policy": [
        "Non-credible",
        "Irrelevant",
        "Spam"
    ],
    "Precision": [
        0.59,  # Non-credible (credibility class 0)
        0.53,  # Irrelevant (relevance class 0)
        0.67   # Spam (spam class 1)
    ],
    "Recall": [
        0.93,
        1.00,
        1.00
    ],
    "F1-score": [
        0.72,
        0.69,
        0.80
    ],
    "Support": [
        14,
        9,
        4
    ],
    "Total Reviews": [
        200,
        200,
        200
    ],
    "Accuracy": [
        0.95,  # overall credibility accuracy
        0.96,  # overall relevance accuracy
        0.99   # overall spam accuracy
    ],
    "Macro Avg F1": [
        0.85,
        0.84,
        0.90
    ],
    "Weighted Avg F1": [
        0.96,
        0.97,
        0.99
    ]
}

# Convert to DataFrame
df_violations = pd.DataFrame(violation_metrics)

st.subheader("Performance Metrics by Policy Type")
st.dataframe(df_violations)

st.subheader("Key Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Model Strengths**")
    st.write("""
    -  **High recall (93-100%)**: Catches nearly all policy violations
    - **Strong overall accuracy (95-99%)**: Performs well across all policy types
    - **Excellent spam detection**: Best performance with 67% precision, 100% recall
    """)

with col2:
    st.markdown("**Limitations**")
    st.write("""
    - **Moderate precision (53-67%)**: Some false positives occur
    - **Independent evaluation**: Each policy is assessed separately, leading to contradictory results (e.g., flagged as "not relevant" but "high quality")
    - **Non-credible detection**: Most challenging with 59% precision
    - **Trade-off consideration**: Balance between catching violations vs. false alarms
    """)

st.subheader("Recommended Usage")
st.info("""
**Best suited for first-pass filtering with human review.** The model's high recall ensures comprehensive violation detection, 
while human reviewers can efficiently filter out false positives. This approach maximizes content safety while maintaining operational efficiency.
""")

st.header("Flagged Reviews Dataset")
st.write(
    "Reviews identified as policy violations, with manually verified ground truth labels for validation."
)

violated_policies = "data/output/violated_reviews.csv"
try:
    df_violations_data = pd.read_csv(violated_policies)
    st.dataframe(df_violations_data, use_container_width=True)
except FileNotFoundError:
    st.error("Violated reviews dataset not found. Please ensure the file exists at the specified path.")
except Exception as e:
    st.error(f"Error loading dataset: {str(e)}")