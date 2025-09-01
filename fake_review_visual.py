
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Fake Review Detector",layout="wide")

st.title(" Fake Review Detection Dashboard")
st.markdown("""
    Upload a CSV file of product reviews to analyze and identify potentially fake entries.
    The algorithm flags reviews based on repetitiveness, extreme positivity/negativity, and user history.
""")


uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:

        df = pd.read_csv(uploaded_file)
        

        original_count = len(df)
        

        required_text_column = 'review_content'
        required_id_column = 'user_id'
        
        if required_text_column not in df.columns:
            st.error(f"The required column '{required_text_column}' was not found in the uploaded file.")
            st.stop()
            
        df_clean = df.dropna(subset=[required_text_column, required_id_column])
        
        df_clean = df_clean.drop_duplicates(subset=[required_text_column])
        
        cleaned_count = len(df_clean)
        rows_removed = original_count - cleaned_count
        

        df_clean['text_len'] = df_clean[required_text_column].astype(str).apply(len)
        df_clean['word_count'] = df_clean[required_text_column].astype(str).apply(lambda x: len(x.split()))
        

        user_review_counts = df_clean[required_id_column].value_counts()
        df_clean['user_review_count'] = df_clean[required_id_column].map(user_review_counts)
        df_clean['repetitive_user'] = (df_clean['user_review_count'] > 5).astype(int)  
        

        positive_words = {'best', 'perfect', 'amazing', 'flawless', 'fantastic', 'incredible', 'excellent', 'love', 'awesome'}
        negative_words = {'worst', 'terrible', 'awful', 'horrible', 'useless', 'poor', 'waste', 'broken', 'scam', 'fake'}
        

        df_clean['review_lower'] = df_clean[required_text_column].astype(str).str.lower()
        
        df_clean['positive_count'] = df_clean['review_lower'].apply(
            lambda x: sum(1 for word in x.split() if word in positive_words)
        )
        df_clean['too_positive'] = (df_clean['positive_count'] >= 3).astype(int)  
        
        df_clean['negative_count'] = df_clean['review_lower'].apply(
            lambda x: sum(1 for word in x.split() if word in negative_words)
        )
        df_clean['too_negative'] = (df_clean['negative_count'] >= 3).astype(int)  
        

        df_clean['one_time_reviewer'] = (df_clean['user_review_count'] == 1).astype(int)
        

        df_clean['score'] = (
            df_clean['repetitive_user'] +
            df_clean['too_positive'] +
            df_clean['too_negative'] +
            df_clean['one_time_reviewer']
        )

        df_clean['mostly_fake'] = (df_clean['score'] >= 2).astype(int)
        

        potential_keep_cols = [
            'product_id', 'product_name', 'category', 'rating',
            'review_id', 'review_title', 'review_content', 'user_id',
            'score', 'mostly_fake', 'user_review_count'
        ]

        keep_cols = [col for col in potential_keep_cols if col in df_clean.columns]
        df_display = df_clean[keep_cols].copy()
        

        st.success(f"File successfully loaded and processed. {rows_removed} rows were removed during cleaning.")
        

        st.subheader(" Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Reviews", cleaned_count)
        with col2:
            st.metric("Fake Reviews", df_display['mostly_fake'].sum())
        with col3:
            fake_percentage = (df_display['mostly_fake'].sum() / cleaned_count) * 100
            st.metric("Fake %", f"{fake_percentage:.2f}%")
        with col4:
            st.metric("Avg. Fake Score", f"{df_display['score'].mean():.2f}")
        

        tab1, tab2, tab3 = st.tabs([" Charts", " All Reviews", " Fake Reviews"])
        
        with tab1:
            st.subheader("Rating Distribution")
            rating_counts = df_display['rating'].value_counts().sort_index()
            st.bar_chart(rating_counts)
            
            st.subheader("Fake Score Distribution")
            score_counts = df_display['score'].value_counts().sort_index()
            st.bar_chart(score_counts)
            
        with tab2:
            st.dataframe(df_display, use_container_width=True)
            
        with tab3:
            st.dataframe(df_display[df_display['mostly_fake'] == 1], use_container_width=True)
      
            csv = df_display[df_display['mostly_fake'] == 1].to_csv(index=False)
            st.download_button(
                label=" Download Fake Reviews as CSV",
                data=csv,
                file_name="fake_reviews.csv",
                mime="text/csv",
            )
    
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info(" Please upload a CSV file to begin analysis.")