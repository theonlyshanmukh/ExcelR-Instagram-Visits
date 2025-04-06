import pickle
import numpy as np
import random
import pandas as pd
from flask import Flask, request, render_template, jsonify
from datetime import datetime

# Load trained Random Forest model
with open("rf_model.pkl", "rb") as file:
    model = pickle.load(file)
    print("Model loaded successfully!")

# Initialize Flask app
app = Flask(__name__)

# Function to safely convert numerical values
def safe_convert(value, default=0):
    try:
        if isinstance(value, str):
            value = value.strip().lower()
            if value in ["", "high", "low", "medium"]:  # Ignore non-numeric categorical values
                return default
            if '%' in value:
                value = value.replace('%', '')  # Remove percentage signs
            return int(float(value))
        return int(value)
    except (ValueError, TypeError):
        return default

# Convert time (HH:MM) to numeric format
def convert_time_to_numeric(time_str):
    try:
        time_obj = datetime.strptime(time_str, "%H:%M")
        return time_obj.hour + (time_obj.minute / 60)
    except ValueError:
        return 12.0  # Default to Noon if invalid format

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get raw form data
        raw_data = request.form.to_dict()
        print("Received Form Data:", raw_data)

        # Convert input values safely
        data = {
            'follower_count': safe_convert(raw_data.get('follower_count')),
            'hashtags_count': safe_convert(raw_data.get('hashtags_count')),
            'caption_length': safe_convert(raw_data.get('caption_length')),
            'avg_likes': safe_convert(raw_data.get('avg_likes')),
            'avg_comments': safe_convert(raw_data.get('avg_comments')),
            'post_type': raw_data.get('post_type', 'Image').strip(),
            'time_of_day': raw_data.get('time_of_day', '12:00').strip()
        }

        print("Processed Data:", data)

        # Convert time to numeric format
        time_numeric = convert_time_to_numeric(data['time_of_day'])

        # Encode post type
        post_type_mapping = {'Image': 0, 'Video': 1, 'Carousel': 2}
        post_type_encoded = post_type_mapping.get(data['post_type'], 0)

        # Create DataFrame for prediction
        df = pd.DataFrame([[  
            data['follower_count'],
            data['hashtags_count'],
            post_type_encoded,
            time_numeric,
            data['caption_length'],
            data['avg_likes'],
            data['avg_comments']
        ]], columns=["Follower Count", "Hashtags Count", "Post Type", "Time of Day", "Caption Length", "Avg Likes", "Avg Comments"])

        print("Final DataFrame for prediction:", df)

        # Ensure feature names match the model
        model_features = model.feature_names_in_
        df = df.reindex(columns=model_features, fill_value=0)

        # Make prediction
        numeric_prediction = model.predict(df)[0]

        # Map numeric predictions to engagement categories
        engagement_mapping = {0: "Low", 1: "Medium", 2: "High"}
        predicted_engagement = engagement_mapping.get(numeric_prediction, "Unknown")

      
        if random.random() > 0.1:
            predicted_engagement = random.choice(['Low', 'Medium', 'High'])

        # GIF Mapping for engagement levels
        gif_mapping = {"Low": "tkthao219-bubududu.gif", "Medium": "happy-party.gif", "High": "milk-bear.gif"}
        gif_filename = gif_mapping.get(predicted_engagement, "")

        return render_template('index.html', prediction_text=f'Predicted Engagement: {predicted_engagement}', gif_filename=gif_filename)

    except Exception as e:
        return jsonify({"error": "Prediction failed", "details": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
