import streamlit as st
import requests
import pandas as pd
import datetime
from fpdf import FPDF

# Streamlit page config
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
            justify-content: center;
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
    st.title("📅 Menstrual Calendar & Tracker")
    st.write("Track your menstrual cycle, predict upcoming periods, and log symptoms.")
    
    # Select or mark period dates
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

# **Home Page**
elif choice == "🏠 Home":
    st.title("🩺 HerHealth AI - Your Menstrual Health Companion")
    st.write("HerHealth AI provides insights into your menstrual health and predicts PCOD risk.")

    features = [
        ("🔬 PCOD Risk Detection", "Analyze PCOD Risk", "🔬 PCOD Risk Detection"),
        ("📄 Generate Report", "Get Health Report", "📄 Generate Report"),
        ("📅 Menstrual Calendar", "Track Your Cycle", "📅 Menstrual Calendar"),
        ("💬 Sakhi Chatbot", "Ask Health Questions", "💬 Sakhi Chatbot"),
        ("❓ FAQs", "Common Questions", "❓ FAQs")
    ]

    st.markdown("<div class='card-container'>", unsafe_allow_html=True)
    for feature in features:
        st.markdown(f"""
            <div class='card'>
                <div class='card-inner'>
                    <div class='card-front'>{feature[0]}</div>
                    <div class='card-back'>
                        <p>{feature[1]}</p>
                        <button onclick="window.location.href='#{feature[2]}'">Go</button>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
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
            
            st.success(f"🧬 **Predicted Cluster:** {cluster}")
            st.info(f"💡 **Health Insight:** {insight}")
            
            # Save result for report generation
            st.session_state["report_data"] = {"cluster": cluster, "insight": insight}
        else:
            st.error("❌ Error in API request. Please try again.")
    st.header("📄 Generate Your PCOD Risk Report")
    if "report_data" in st.session_state:
        cluster = st.session_state["report_data"]["cluster"]
        insight = st.session_state["report_data"]["insight"]

        class PDF(FPDF):
            def header(self):
                self.set_font("Arial", "B", 16)
                self.cell(200, 10, "HerHealth AI - PCOD Risk Report", ln=True, align="C")
                self.ln(10)

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Predicted Cluster: {cluster}", ln=True)
        pdf.multi_cell(0, 10, f"Health Insight: {insight}")
        
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
    user_question = st.text_input("Ask Sakhi anything about your health:")
    if user_question:
        chat_api_url = "http://127.0.0.1:5000/chat"
        chat_response = requests.post(chat_api_url, json={"question": user_question})
        if chat_response.status_code == 200:
            sakhi_reply = chat_response.json().get("reply", "I'm here to help!")
            st.write("💬 Sakhi Says:", sakhi_reply)
        else:
            st.error("❌ Unable to fetch response. Please try again.")
