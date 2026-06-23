
from google.cloud import language_v1
from google.oauth2 import service_account

# Set up the Google Cloud Language API client with credentials
credentials = service_account.Credentials.from_service_account_file('path_to_your_service_account_file.json')
client = language_v1.LanguageServiceClient(credentials=credentials)

def analyze_sentiment(text):
    """
    Sends a request to the Google Natural Language API to analyze
    the sentiment of the given piece of text.
    """
    if not text:
        raise ValueError("Input text cannot be empty")
    
    # Create the document object with type PLAIN_TEXT
    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Call the API to analyze the sentiment of the document
    try:
        response = client.analyze_sentiment(request={'document': document})

        # Extract sentiment score and magnitude from the response
        sentiment_score = response.document_sentiment.score
        sentiment_magnitude = response.document_sentiment.magnitude

        return {
            'score': sentiment_score,
            'magnitude': sentiment_magnitude
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# Example usage
text = "I love programming! It's so exciting and fun."
sentiment = analyze_sentiment(text)
if sentiment:
    print(f"Sentiment score: {sentiment['score']}, Magnitude: {sentiment['magnitude']}")
