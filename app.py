import os
import threading
from flask import Flask, request, jsonify
import pandas as pd
import joblib
import together
from dotenv import load_dotenv
import streamlit as st
from fpdf import FPDF
import requests




# Load environment variables
load_dotenv()

# Initialize Together AI client
client = together.Together(api_key=os.getenv("TOGETHER_API_KEY"))

# Flask backend setup
app = Flask(__name__)

# Load trained models
scaler = joblib.load("backend/scaler.pkl")
pca = joblib.load("backend/pca_model.pkl")
kmeans = joblib.load("backend/kmeans_model.pkl")

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

def run_flask():
    app.run(debug=True, use_reloader=False)

def run_streamlit():
    st.set_page_config(page_title="HerHealth AI", page_icon="❤️", layout="wide")

    # Navigation Bar
    menu = ["🏠 Home", "🔬 PCOD Risk Detection", "📅 Menstrual Calendar",  "💬 Sakhi Chatbot", "❓ FAQs"]
    choice = st.sidebar.radio("Navigation", menu)

    st.markdown("""
        <style>
            .navbar {
                background-color: #FF69B4;
                padding: 10px;
                text-align: center;
                font-size: 20px;
                color: white;
                font-weight: bold;
            }
            .card-container {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                gap: 20px;
            }
            .card {
                width: 250px;
                height: 150px;
                perspective: 1000px;
            }
            .card-inner {
                width: 100%;
                height: 100%;
                position: relative;
                transform-style: preserve-3d;
                transition: transform 0.5s;
            }
            .card:hover .card-inner {
                transform: rotateY(180deg);
            }
            .card-front, .card-back {
                position: absolute;
                width: 100%;
                height: 100%;
                backface-visibility: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            .card-front {
                background: #FFB6C1;
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
            .card-back {
                background: #FF69B4;
                color: white;
                transform: rotateY(180deg);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            .card-back button {
                background: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                color: #FF69B4;
                cursor: pointer;
                font-weight: bold;
            }
        </style>
        <div class='navbar'>HerHealth AI - Your Menstrual Health Companion</div>
    """, unsafe_allow_html=True)


    # **Menstrual Calendar Page**
    if choice == "📅 Menstrual Calendar":
        import datetime
        from datetime import date, timedelta
        st.title("📅 Menstrual Calendar & Tracker")
        st.write("Track your menstrual cycle, predict upcoming periods, and log symptoms.")
        
        # Ensure proper initialization of datetime.date.today()
        selected_date = st.date_input("Mark your period date:", datetime.date.today())
        if "period_dates" not in st.session_state:
            st.session_state["period_dates"] = []
        
        if st.button("Add Period Date"):
            st.session_state["period_dates"].append(selected_date)
            st.success(f"Added {selected_date} to your period history.")
        
        # Show period history
        if st.session_state["period_dates"]:
            st.write("### 📜 Period History")
            st.write(pd.DataFrame(st.session_state["period_dates"], columns=["Date"]))
        
        # Predict next period
        if len(st.session_state["period_dates"]) > 1:
            last_two_periods = sorted(st.session_state["period_dates"], reverse=True)[:2]
            cycle_length = (last_two_periods[0] - last_two_periods[1]).days
            next_period = last_two_periods[0] + datetime.timedelta(days=cycle_length)
            st.info(f"🔮 Predicted Next Period: {next_period}")
        
        # Set reminder
        reminder_date = st.date_input("Set Reminder for Next Cycle:", datetime.date.today())
        reminder_note = st.text_input("Reminder Note:")
        if st.button("Set Reminder"):
            st.success(f"Reminder set for {reminder_date}: {reminder_note}")
        
        # Symptom logging
        st.write("### 📝 Log Symptoms & Notes")
        symptoms = st.text_area("Describe any symptoms or observations:")
        if st.button("Save Notes"):
            st.success("Symptoms and notes saved!")

    # **Home Page**
    elif choice == "🏠 Home":
        st.title("🩺 HerHealth AI - Your Menstrual Health Companion")
        st.write("HerHealth AI provides insights into your menstrual health and predicts PCOD risk.")


        # Add an engaging intro
        st.image("frontend/banner.jpg", use_container_width=True)  # Automatically fits width
        st.markdown(
            """<style> img { height: 340px !important; object-fit: cover; } </style>""",
            unsafe_allow_html=True
        )
        st.markdown(
        """
        <style>
            .welcome-text {
                text-align: center;
                font-size: 36px;
                font-weight: bold;
                color: #4A4A4A;  /* Dark gray for better visibility */
            }
        </style>
        <p class="welcome-text">
            🌸 <b>Welcome to HerHealth AI!</b> 🌸<br> 
            Your <b>personal AI-powered assistant</b> for menstrual health and PCOD risk assessment.<br> 
            Whether you want to <b>track your cycle, understand PCOD risks, or get expert recommendations</b>, we’ve got you covered! ✅
        </p>
        """,
        unsafe_allow_html=True
    )


        # Features Section
        st.write("## 🌟 Key Features")
        features = [
            "📊 **PCOD Risk Prediction** - AI-based analysis of menstrual health data.",
            "🔬 **Menstrual Health Insights** - Personalized reports based on your input.",
            "💬 **Sakhi Chatbot** - Get expert advice on PCOD, periods, and wellness.",
            "📄 **Generate Health Reports** - Download AI-powered menstrual health reports.",
            "❓ **FAQs** - Common Questions on HerHealth AI, PCOD, menstrual cycle, and hormonal balance."
        ]
        for feature in features:
            st.write(feature)

        # Call to Action
        st.markdown(
            """
            ---
            🎯 **Start Your Journey to Better Menstrual Health!**  
            👉 **Select an option from the sidebar** to get started.
            """
        )


        features = [
            ("🔬 PCOD Risk Detection", "Analyze PCOD Risk", "🔬 PCOD Risk Detection"),
            ("📄 Generate Report", "Get Health Report", "📄 Generate Report"),
            ("📅 Menstrual Calendar", "Track Your Cycle", "📅 Menstrual Calendar"),
            ("💬 Sakhi Chatbot", "Ask Health Questions", "💬 Sakhi Chatbot"),
            ("❓ FAQs", "Common Questions", "❓ FAQs")
        ]

        
    # **PCOD Risk Prediction Section**
    elif choice == "🔬 PCOD Risk Detection":
        st.header("🔬 PCOD Risk Detection & Menstrual Health Insights")
        st.write("Enter your health details below to receive a personalized health assessment.")

        # User Input Fields
        number_of_peak = st.number_input("Number of Peak Fertility Days", min_value=0, max_value=10, value=2)
        age = st.number_input("Age", min_value=12, max_value=60, value=25)
        length_of_cycle = st.number_input("Length of Cycle (days)", min_value=20, max_value=50, value=28)
        estimated_day_of_ovulation = st.number_input("Estimated Day of Ovulation", min_value=10, max_value=25, value=14)
        length_of_leutal_phase = st.number_input("Length of Luteal Phase (days)", min_value=10, max_value=20, value=14)
        length_of_menses = st.number_input("Length of Menses (days)", min_value=2, max_value=10, value=5)
        unusual_bleeding = st.selectbox("Unusual Bleeding?", ["No", "Yes"])
        height = st.number_input("Height (cm)", min_value=120, max_value=200, value=165)
        weight = st.number_input("Weight (kg)", min_value=30, max_value=150, value=60)
        bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=22.5)
        mean_length_of_cycle = st.number_input("Mean Length of Cycle (days)", min_value=20, max_value=50, value=28)
        menses_score = st.number_input("Menses Score (Pain Severity)", min_value=0, max_value=10, value=5)

        # Convert categorical input
        unusual_bleeding = 1 if unusual_bleeding == "Yes" else 0

        # Submit button
        if st.button("Predict PCOD Risk & Menstrual Health Cluster"):
            user_data = {
                "number_of_peak": number_of_peak,
                "Age": age,
                "Length_of_cycle": length_of_cycle,
                "Estimated_day_of_ovulution": estimated_day_of_ovulation,
                "Length_of_Leutal_Phase": length_of_leutal_phase,
                "Length_of_menses": length_of_menses,
                "Unusual_Bleeding": unusual_bleeding,
                "Height": height,
                "Weight": weight,
                "Income": 1000,
                "BMI": bmi,
                "Mean_of_length_of_cycle": mean_length_of_cycle,
                "Menses_score": menses_score
            }

            # Send data to backend API
            api_url = "http://127.0.0.1:5000/predict_cluster"
            response = requests.post(api_url, json=user_data)

            if response.status_code == 200:
                result = response.json()
                cluster = result["Predicted_Cluster"]
                insight = result["Health_Insight"]
                ai_insights= result["AI_Insights"]
                
                st.success(f"🧬 **Predicted Cluster:** {cluster}")
                st.info(f"💡 **Health Insight:** {insight}")
                
                # Save result for report generation
                st.session_state["report_data"] = {"cluster": cluster, "insight": insight, "AI_Insights": ai_insights}
                
            else:
                st.error("❌ Error in API request. Please try again.")
        st.header("📄 Generate Your PCOD Risk Report")
        if "report_data" in st.session_state:
            cluster = st.session_state["report_data"]["cluster"]
            insight = st.session_state["report_data"]["insight"]
            ai_insight = st.session_state["report_data"].get("AI_Insights", "No AI insights available.")
            from datetime import datetime
            report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            class PDF(FPDF):
                def header(self):
                    pass  # No header to maintain a clean first-page design

            pdf = PDF()
            pdf.set_auto_page_break(auto=True, margin=15)

            # First Page: Title Centered
            pdf.add_page()
            pdf.set_font("Arial", "B", 24)
            pdf.cell(200, 200, "HerHealth AI - PCOD Risk Report", ln=True, align="C")

            # Second Page: Report Details
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, "Report Details", ln=True, align="C")
            pdf.ln(10)

            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, f"Report Generated On: {report_time}", ln=True)
            pdf.cell(200, 10, f"Predicted Cluster: {cluster}", ln=True)
            pdf.multi_cell(0, 10, f"Health Insight: {insight}")
            pdf.ln(5)

            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, "AI-Generated Deep Insights", ln=True, align="C")
            pdf.ln(10)

            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, ai_insight)

            # Save and provide download option
            pdf_file = "herhealth_report.pdf"
            pdf.output(pdf_file)

            with open(pdf_file, "rb") as file:
                st.download_button("📥 Download Report", file, file_name=pdf_file, mime="application/pdf")

        else:
            st.warning("⚠️ No prediction data available. Please run the PCOD risk assessment first.")


    # **FAQs Section**
    elif choice == "❓ FAQs":
        st.header("🙋 Frequently Asked Questions (FAQs)")
        st.write("Here are some common questions about PCOD and menstrual health:")
        
        faqs = {
            "What is PCOD?": "Polycystic Ovary Syndrome (PCOS) is a hormonal disorder common among women of reproductive age, leading to irregular periods and hormonal imbalances.",
            "How do I track my menstrual cycle?": "You can use the Menstrual Calendar in this app to log your period dates, track symptoms, and predict future cycles.",
            "Can PCOD be cured?": "PCOD cannot be completely cured, but symptoms can be managed through lifestyle changes, diet, and medical treatment.",
            "What are common symptoms of PCOD?": "Symptoms include irregular periods, excessive hair growth, acne, weight gain, and difficulty in conceiving.",
            "How does this app help with PCOD detection?": "Our AI-based system analyzes menstrual health parameters to predict PCOD risk and provide personalized insights."
        }
        
        for question, answer in faqs.items():
            with st.expander(question):
                st.write(answer)
    # **Sakhi Chatbot**
    elif choice == "💬 Sakhi Chatbot":
        st.header("💬 Sakhi - Your AI Health Assistant")

        st.write("Ask me anything about menstrual health, PCOD, and general well-being.")

        # User input
        user_query = st.text_input("Enter your question:")

        if st.button("Ask"):
            if user_query:
                api_url = "http://127.0.0.1:5000/chat"
                response = requests.post(api_url, json={"message": user_query})

                if response.status_code == 200:
                    result = response.json()
                    bot_response = result.get("response", "Sorry, I couldn't process your request.")
                    st.markdown(f"**💬 Sakhi Says:** {bot_response}")
                else:
                    st.error("Error fetching response from the chatbot.")
                

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_streamlit()
