import streamlit as st

st.set_page_config(page_title="ML4TrustworthyReviews", layout="wide")

st.title("ML4TrustworthyReviews")
st.write("Member: Chelsea Yep")
st.header("Problem Statement")
st.write(
    """
    Online reviews significantly influence public perception of local businesses. 
    Irrelevant, misleading, or low-quality reviews can distort a business's reputation. 
    This system leverages ML and NLP to automatically evaluate review quality, relevance, 
    and credibility according to defined policies.
    """
)

st.header("Policy Framework")
st.write("Our system detects the following types of policy violations and quality indicators:")

st.table({
    "Policy": ["Advertisement/Spam", "Irrelevant Content", "Credible Reviews", "Quality Assessment*"],
    "Description": [
        "Promotional content, URLs, contact info",
        "Content unrelated to business/location",
        "Reviews from users who haven't visited",
        "Reference metric for review informativeness"
    ],

    "Example": [
        "Visit www.deals.com for 50% off!",
        "Love my new phone, restaurant is okay",
        "Never been here but heard it's bad",
        "Good vs detailed experience description"
    ]
})

st.caption("*Quality assessment is for reference only, not a strict policy violation")

st.subheader("Evaluation Policies")

st.markdown("""
1. **Spam / Advertisement Detection**  
   - Uses regex and keyword matching to identify promotional content, URLs, or repeated advertising phrases.  
   - Example keywords: 'buy', 'discount', 'free', 'click here'.  
   - Fast, rule-based, and executed first to quickly flag obvious spam.
""")



st.markdown("""
2. **Relevance Evaluation**  
   - Checks whether the review content is related to the business or location.
   - Considers the type of business: restaurant, hotel, tourist attraction, etc.
   - LLM-based evaluation with carefully crafted prompts to capture context-specific relevancy.
""")

st.markdown("""
3. **Credibility Assessment**  
   - Determines whether the review represents a genuine user experience.
   - Flags overly generic or vague reviews and statements where the reviewer admits not visiting.
   - Uses LLM to distinguish natural, credible language from non-credible or bot-like patterns.
""")

st.markdown("""
4. **Quality Assessment** *(Reference Metric)*
       - Determines review quality ('low', 'medium', 'high') based on:
       - Text length
       - Informativeness (specific details about service, product, or location)
       - Coherence (alignment between rating and sentiment expressed)
   - Uses a **shared LLM model** (Qwen 3B) to evaluate coherence and informativeness for nuanced judgments.
   - **Not a strict policy violation** but useful for:
       - Filtering and prioritizing review displays
       - Incentivizing users to provide more detailed, helpful reviews
       - Understanding overall review dataset quality
""")
st.header("System Overview")
st.write(
    """
    Input reviews are parsed, standardized, and passed through a policy evaluation pipeline 
    combining rule-based checks and ML/LLM models. Violations are detected automatically 
    and summarized for inspection.
    """
)
st.subheader("Policy Evaluator Workflow")

st.write("""
The **PolicyEvaluator** orchestrates the evaluation:

1. **Quick Spam Detection**: Rule-based, fast. If flagged as spam, review is marked 'low quality' and other evaluations may be skipped.  
2. **LLM-Based Evaluation**: For non-spam reviews, the LLM evaluates each policy independently:
    - Relevance
    - Credibility
    - Quality (for reference and filtering purposes)
3. **Output Consolidation**: All policy results are stored in the `evaluation` attribute of the `Review` object.

> Note: Each policy is evaluated independently, so a review can be credible but irrelevant, or relevant but low quality, without one affecting the others. Quality scores serve as additional context rather than strict violation flags.
""")

st.header("Data Source")
st.write(
    """
    Reviews are sourced from the Google Local Reviews dataset ([McAuley Lab, UCSD](https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/)).
    A subset is randomly selected for evaluation, annotated, and processed for model input.
    """
)


st.header("Data Structure & Standardization")

st.write(
    """
    Reviews are standardized into a unified format to ensure consistency across the dataset. 
    Each review contains:
    - **Text**: The written content of the review.
    - **Rating**: The numeric score provided by the user.
    - **Images**: Any attached media (if available).
    - **Timestamp**: When the review was created.
    - **User**: A structured object representing the reviewer.
    - **Business**: A structured object representing the business being reviewed.
    
    This standardized representation allows downstream pipelines to process reviews uniformly 
    for feature extraction, policy evaluation, and ML predictions.
    """
)

st.subheader("Business & User Objects")

st.write(
    """
    **Business** and **User** are reusable dataclasses that can be leveraged for 
    additional analysis, such as:
    - Tracking trends across individual businesses (e.g., average review quality, spam rate)
    - Monitoring user-specific behavior (e.g., frequent reviewers, suspicious activity)
    
    While our current dataset does not include rich user or business history, 
    this design allows easy extension when more data becomes available.
    """
)



col1,col2= st.columns(2)
with col1:
    if st.button("View Model Performance", type="primary", use_container_width=True):
        st.switch_page("pages/Model_performance.py") 
with col2:
    if st.button("Go to Testing Page", type="primary", use_container_width=True):
        st.switch_page("pages/Try_the_model.py") 

        