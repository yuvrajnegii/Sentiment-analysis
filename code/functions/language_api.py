import os
import time
import json
import csv  # Use standard csv module
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import pandas as pd

# Download the VADER lexicon
nltk.download('vader_lexicon')

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the given piece of text using NLTK's VADER.
    
    Parameters:
        text (str): The input text to analyze.
    
    Returns:
        dict: A dictionary containing sentiment scores (positive, neutral, negative, compound).
    """
    # Initialize SentimentIntensityAnalyzer once
    sia = SentimentIntensityAnalyzer()
    
    # Perform sentiment analysis
    sentiment_scores = sia.polarity_scores(text)
    
    return sentiment_scores


def download_sentiments(videos, output_file='sentiments.csv'):
    """
    Analyzes sentiment scores for the given videos using NLTK's VADER
    and stores the results in a CSV file.
    """
    # Initialize SentimentIntensityAnalyzer once
    sia = SentimentIntensityAnalyzer()

    # Create or open the CSV file
    file_exists = os.path.isfile(output_file)
    with open(output_file, 'a' if file_exists else 'w', newline='', encoding='utf-8', errors='ignore') as f:
        writer = csv.writer(f)
        
        # Write headers only if creating a new file
        if not file_exists:
            writer.writerow(['youtube_id', 'sentiment','sentiment_score'])

        i = 0
        n_videos = videos.shape[0]
        print(f"Start processing {n_videos} videos...")

        while i < n_videos:
            video = videos.iloc[i]  # Get the current video row
            try:
                # Analyze sentiment of the video's title
                sentiment = sia.polarity_scores(video['title'])
                
                # Write sentiment scores to the CSV file, ensuring all are strings
                writer.writerow([
                    video['youtube_id'], 
                    sia,
                    str(sentiment['compound'])  # Convert to string
                ])
                
                # Move to the next video
                i += 1
            except Exception as e:
                # Handle unexpected errors (e.g., issues with the data)
                print(f"Error processing video {video['youtube_id']}: {e}")
                i += 1  # Skip to the next video

    print(f"Finished processing {n_videos} videos.")
