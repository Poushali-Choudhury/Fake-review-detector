# Fake Review Detection Dashboard

A interactive Streamlit web application designed to analyze product review datasets and identify potentially fake or spam reviews based on heuristic rules.

## Features

- **CSV Upload**: Easily upload your review data for analysis.
- **Heuristic Analysis**: Flags reviews based on multiple criteria:
  - **User Repetitiveness**: Users who have posted an unusually high number of reviews.
  - **Extreme Sentiment**: Reviews containing an excessive number of overly positive or negative keywords.
  - **One-Time Reviewers**: Users who have only posted a single review.
- **Interactive Dashboard**: Visualize results with summary statistics and charts.
- **Data Export**: Download the results flagged as "mostly fake" for further investigation.

## Installation & Usage

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/Poushali-Choudhury/fake-review-detector.git
    cd fake-review-detector
    ```

2.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit app**:

    ```bash
    streamlit run app.py
    ```

4.  **Open your browser** and go to the local URL shown in the terminal (usually `http://localhost:8501`).

5.  **Upload a CSV file** with the required columns (see Data Format below).

## Data Format

Your CSV file should at minimum contain the following columns for the app to function correctly:

- `review_content`: (Required) The text of the review.
- `user_id`: (Required) A unique identifier for the user who wrote the review.

Other useful columns that will be used if present:

- `product_id`, `product_name`, `category`, `rating`, `review_id`, `review_title`

## How It Works

The application calculates a "Fake Score" by assigning points for each red flag detected in a review:

- `+1` point: User has posted more than 5 reviews (`repetitive_user`)
- `+1` point: Review contains 3+ overly positive keywords (`too_positive`)
- `+1` point: Review contains 3+ overly negative keywords (`too_negative`)
- `+1` point: User has only posted this one review (`one_time_reviewer`)

A review is classified as **"mostly_fake"** if its total score is **2 or higher**.

**Note:** This is a heuristic-based approach and serves as an initial filter. It may yield both false positives and false negatives and should be used as an aid for human investigation, not as a sole arbiter of truth.
