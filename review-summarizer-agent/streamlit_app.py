import streamlit as st
import json
from review_summarizer import ReviewSummarizer
from data_handler import DataHandler
import pandas as pd


def main():
    st.title("🏪 Place Review Summarizer AI Agent")
    st.write("Powered by Gemma 2:1B via Ollama")

    # Initialize
    if 'summarizer' not in st.session_state:
        st.session_state.summarizer = ReviewSummarizer()

    # Check Ollama status
    if not st.session_state.summarizer.client.is_available():
        st.error("❌ Ollama service is not available. Please ensure Ollama is running.")
        st.code("ollama serve", language="bash")
        return

    st.success("✅ Connected to Ollama")

    # Sidebar
    st.sidebar.header("Options")
    input_method = st.sidebar.radio("Input Method", ["Manual Entry", "File Upload"])

    if input_method == "Manual Entry":
        manual_input_interface()
    else:
        file_upload_interface()


def manual_input_interface():
    st.header("Manual Review Entry")

    place_name = st.text_input("Place Name (optional)")

    # Dynamic review input
    if 'reviews' not in st.session_state:
        st.session_state.reviews = [""]

    st.write("Enter reviews:")
    for i, review in enumerate(st.session_state.reviews):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.session_state.reviews[i] = st.text_area(
                f"Review {i + 1}",
                value=review,
                key=f"review_{i}",
                height=100
            )
        with col2:
            if st.button("Remove", key=f"remove_{i}") and len(st.session_state.reviews) > 1:
                st.session_state.reviews.pop(i)
                st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Another Review"):
            st.session_state.reviews.append("")
            st.rerun()

    with col2:
        if st.button("Clear All"):
            st.session_state.reviews = [""]
            st.rerun()

    # Filter out empty reviews
    valid_reviews = [r.strip() for r in st.session_state.reviews if r.strip()]

    if valid_reviews and st.button("Generate Summary", type="primary"):
        generate_and_display_summary(valid_reviews, place_name)


def file_upload_interface():
    st.header("File Upload")

    uploaded_file = st.file_uploader("Upload Reviews", type=['json', 'csv'])
    place_name = st.text_input("Place Name (optional)")

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.json'):
                data = json.loads(uploaded_file.read().decode('utf-8'))
                if isinstance(data, dict) and 'reviews' in data:
                    reviews = data['reviews']
                    if not place_name:
                        place_name = data.get('place_name', '')
                elif isinstance(data, list):
                    reviews = [str(item) for item in data]
                else:
                    reviews = [str(data)]

            elif uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                st.write("CSV Preview:")
                st.dataframe(df.head())

                review_column = st.selectbox("Select review column:", df.columns.tolist())
                reviews = df[review_column].dropna().astype(str).tolist()

            st.write(f"Found {len(reviews)} reviews")

            if reviews and st.button("Generate Summary", type="primary"):
                generate_and_display_summary(reviews, place_name)

        except Exception as e:
            st.error(f"Error processing file: {e}")


def generate_and_display_summary(reviews, place_name):
    with st.spinner("Generating summary..."):
        result = st.session_state.summarizer.summarize_reviews(reviews, place_name)

    if "error" in result:
        st.error(result["error"])
        return

    # Display results
    st.success("Summary Generated!")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Reviews", result['total_reviews'])
    with col2:
        st.metric("Sentiment", result['sentiment'])
    with col3:
        if result['place_name']:
            st.metric("Place", result['place_name'])

    st.subheader("Summary")
    st.write(result['summary'])

    # Download option
    st.download_button(
        "Download Summary (JSON)",
        data=json.dumps(result, indent=2),
        file_name="review_summary.json",
        mime="application/json"
    )


if __name__ == "__main__":
    main()