import streamlit as st
import sys
sys.path.append('../src')
from policies.evaluators import PolicyEvaluator
from policies.review_selector import select_violated_reviews
from objects import Review, Business, OutputData, InputData

st.set_page_config(layout="wide")
st.title("Testing the Review Evaluator")

# Initialize session state for form data
if 'text' not in st.session_state:
    st.session_state.text = ""
if 'rating' not in st.session_state:
    st.session_state.rating = 1
if 'business_selection' not in st.session_state:
    st.session_state.business_selection = "KFC - Restaurant chain known for its buckets of fried chicken, plus combo meals & sides."
if 'results' not in st.session_state:
    st.session_state.results = None

# Input form
with st.form("review_evaluation_form"):
    text = st.text_area(
        "Enter a review text to evaluate:",
        value=st.session_state.text,
        height=100
    )
    
    rating = st.number_input(
        "Rating", 
        min_value=1, 
        max_value=5, 
        step=1,
        value=st.session_state.rating
    )
    
    business = st.selectbox(
        "Location to review:",
        (
            "KFC - Restaurant chain known for its buckets of fried chicken, plus combo meals & sides.",
            "West Coast Park - Sprawling neighbourhood destination with expansive green space, trails & playgrounds.",
            "CHIJMES - A former convent & school, this 19th-century structure now houses restaurants, bars & event space."
        ),
        index=0 if st.session_state.business_selection == "KFC - Restaurant chain known for its buckets of fried chicken, plus combo meals & sides." else 
              1 if st.session_state.business_selection == "West Coast Park - Sprawling neighbourhood destination with expansive green space, trails & playgrounds." else 2
    )
    
    st.write("*Google maps location and metadata would ideally be retrieved using Google Maps API, however this is not implemented in this demo.")
    
    # Form buttons
    col1, col2 = st.columns(2)
    with col1:
        evaluate_button = st.form_submit_button("Evaluate", type="primary",use_container_width=True)
    with col2:
        clear_button = st.form_submit_button("Clear", use_container_width=True)

# Handle clear button
if clear_button:
    st.session_state.text = ""
    st.session_state.rating = 1
    st.session_state.business_selection = "KFC - Restaurant chain known for its buckets of fried chicken, plus combo meals & sides."
    st.session_state.results = None
    st.rerun()

# Handle evaluate button
if evaluate_button:
    # Validation
    if not text.strip():
        st.error("Please enter a review text.")
    elif not rating:
        st.error("Please enter a rating between 1 and 5.")
    else:
        # Update session state
        st.session_state.text = text
        st.session_state.rating = rating
        st.session_state.business_selection = business
        
        # Create business object
        if business == "KFC - Restaurant chain known for its buckets of fried chicken, plus combo meals & sides.":
            b = Business(name="KFC", description="Restaurant chain known for its buckets of fried chicken, plus combo meals & sides.")
        elif business == "West Coast Park - Sprawling neighbourhood destination with expansive green space, trails & playgrounds.":
            b = Business(name="West Coast Park", description="Sprawling neighbourhood destination with expansive green space, trails & playgrounds.")
        else:
            b = Business(name="CHIJMES", description="A former convent & school, this 19th-century structure now houses restaurants, bars & event space.")
        
        # Evaluate review
        with st.spinner("Evaluating review..."):
            review = Review(1, input=InputData(text=text, rating=rating, business=b))
            evaluator = PolicyEvaluator()
            results = evaluator.evaluate(review)
            st.session_state.results = results

# Display results if available
if st.session_state.results:
    st.header("Evaluation Results")
    
    results = st.session_state.results
    quality = results.evaluation['review_quality']
    
    # Quality score
    st.subheader(f"Review Quality Score: **{quality}**")

    
    # Policy violations
    st.subheader("Policy Violation Analysis")
    
    violations = []
    
    if results.evaluation.get('spam', False):
        violations.append("Spam/Advertisement")
    
    if not results.evaluation.get('relevance', True):
        violations.append("Irrelevant Content")
    
    if not results.evaluation.get('credible', True):
        violations.append("Non-credible")
    
    if violations:
        st.error("Policy Violations Detected")
        for violation in violations:
            st.write(f"• **{violation}** policy violation detected")
    else:
        st.success("No Policy Violations Detected")
        st.write("This review passes all policy checks and appears to be legitimate.")
    
    # Detailed breakdown
    with st.expander("Detailed Policy Breakdown"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            spam_status = "Violation" if results.evaluation.get('spam', False) else "Pass"
            st.metric("Spam Detection", spam_status)
        
        with col2:
            relevance_status = "Pass" if results.evaluation.get('relevance', True) else "Violation"
            st.metric("Relevance Check", relevance_status)
        
        with col3:
            credibility_status = "Pass" if results.evaluation.get('credible', True) else "Violation"
            st.metric("Credibility Check", credibility_status)