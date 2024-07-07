import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()
API_ENDPOINT = os.getenv('AWS_ACCESS_KEY_ID')

def generate_blog(topics, word_count, tone, target_audience):
    # Prepare the request payload
    payload = json.dumps({
        "topics": topics,
        "word_count": word_count,
        "tone": tone,
        "target_audience": target_audience
    })
    
    # Set the headers
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        # Make the POST request to the API
        response = requests.post(API_ENDPOINT, headers=headers, data=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.RequestException as e:
        return f"Error: {str(e)}"

def submit_feedback(blog_id, rating, feedback):
    payload = json.dumps({
        "feedback": True,
        "blog_id": blog_id,
        "rating": rating,
        "feedback": feedback
    })
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(API_ENDPOINT, headers=headers, data=payload)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException:
        return False

# Streamlit app
st.set_page_config(page_title="AI Blog Generator", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    .main {
        background-color: #2e2e2e;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 AI Blog Generator with Feedback")

# Initialize session state variables
if 'generated_blog' not in st.session_state:
    st.session_state.generated_blog = None
if 'blog_id' not in st.session_state:
    st.session_state.blog_id = None
if 's3_location' not in st.session_state:
    st.session_state.s3_location = None

# Input fields for multiple topics
st.subheader("Blog Topics")
num_topics = st.number_input("Number of topics", min_value=1, max_value=5, value=1)
topics = []
for i in range(num_topics):
    topic = st.text_input(f"Topic {i+1}", key=f"topic_{i}")
    topics.append(topic)

# Input for word count
word_count = st.slider("Approximate word count", min_value=100, max_value=2000, value=500, step=100)

# Input for tone
tone = st.selectbox("Tone", ["formal", "casual", "humorous", "professional", "neutral"])

# Input for target audience
target_audience = st.text_input("Target Audience", "general")

# Button to generate the blog
if st.button("Generate Blog"):
    if API_ENDPOINT:
        if all(topics):  # Ensure all topic fields are filled
            with st.spinner("Generating blog..."):
                result = generate_blog(topics, word_count, tone, target_audience)
                
                if isinstance(result, dict) and 'blog_content' in result:
                    st.success("Blog generated successfully!")
                    st.session_state.generated_blog = result['blog_content']
                    st.session_state.blog_id = result['blog_id']
                    st.session_state.s3_location = result['s3_location']
                else:
                    st.error(f"Failed to generate blog: {result}")
        else:
            st.warning("Please enter all blog topics.")
    else:
        st.error("API_ENDPOINT is not set. Please check your configuration.")

# Display the generated blog if it exists in session state
if st.session_state.generated_blog:
    st.subheader("Generated Blog:")
    st.markdown(st.session_state.generated_blog)
    st.subheader("S3 Location:")
    st.write(st.session_state.s3_location)
    
    # Word count of generated blog
    generated_word_count = len(st.session_state.generated_blog.split())
    st.info(f"Generated blog word count: {generated_word_count}")
    
    # Feedback section
    st.subheader("Provide Feedback")
    rating = st.slider("Rate this blog (1-5 stars)", 1, 5, 3)
    feedback = st.text_area("Your feedback (optional)")
    
    if st.button("Submit Feedback"):
        if submit_feedback(st.session_state.blog_id, rating, feedback):
            st.success("Thank you for your feedback!")
        else:
            st.error("Failed to submit feedback. Please try again.")

# Add some information about the app
st.sidebar.header("About")
st.sidebar.info("This advanced AI blog generator creates coherent blog posts on multiple topics. You can customize the word count, tone, and target audience for a tailored blog experience.")