from flask import Flask, request, jsonify
import pandas as pd
import joblib
import together
import os
import dotenv
from dotenv import load_dotenv

load_dotenv()
# Initialize Together AI client
client = together.Together(api_key=os.getenv("TOGETHER_API_KEY"))

app = Flask(__name__)

# Load trained models
scaler = joblib.load("scaler.pkl")
pca = joblib.load("pca_model.pkl")
kmeans = joblib.load("kmeans_model.pkl")

# Define endpoint for predictions
@app.route('/predict_cluster', methods=['POST'])
def predict_cluster():
    data = request.json
    df = pd.DataFrame([data])

    # Preprocess data
    df_scaled = scaler.transform(df)
    df_pca = pca.transform(df_scaled)

    # Predict cluster
    cluster = kmeans.predict(df_pca)[0]

    # Define health insights based on clusters
    insights = {
        0: "Generally healthy but monitor hormone levels for any changes.",
        1: "Mild cycle irregularities detected. Track menstrual cycles regularly.",
        2: "Significant hormonal imbalances. Consult a healthcare professional.",
        3: "Higher risk of PCOD with metabolic symptoms. Seek medical advice.",
        4: "Moderate PCOD risk with some symptoms. Lifestyle changes may help manage risks.",
        5: "Severe PCOD risk detected. Immediate medical evaluation is recommended.",
        6: "Healthy reproductive cycle, maintain a balanced diet."
    }

    cluster_message = insights.get(cluster, "Unknown cluster")

    # Generate AI-based deep insights using Together AI
    prompt = f"Provide detailed medical insights for someone in PCOD Risk Cluster {cluster}. Include recommendations on diet, exercise, stress management, and hormonal balance."

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert in PCOD and women's health providing deep insights."},
                {"role": "user", "content": prompt}
            ],
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            temperature=0.3
        )
        ai_insights = response.choices[0].message.content.strip()
    except Exception as e:
        ai_insights = "Error generating AI insights. Please try again later."

    return jsonify({
        "Predicted_Cluster": int(cluster),
        "Health_Insight": cluster_message,
        "AI_Insights": ai_insights
    })



@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    prompt = f"Give deep insights on health-related issues, especially PCOD and menstrual health:\n\n'{user_message}'"

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert in health-related issues, especially PCOD and menstrual health."},
                {"role": "user", "content": prompt}
            ],
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            temperature=0.3
        )
        
        bot_response = response.choices[0].message.content.strip()
        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
