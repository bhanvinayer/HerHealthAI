# HerHealth AI

HerHealth AI is a comprehensive application designed to assist women in tracking their menstrual health, predicting PCOD risk, and providing personalized health insights. The application leverages AI to offer accurate predictions and valuable health information.

## Features

- **PCOD Risk Detection**: Analyze your health data to predict the risk of PCOD.
- **Menstrual Calendar**: Track your menstrual cycle, predict upcoming periods, and log symptoms.
- **Health Reports**: Generate detailed health reports based on your input data.
- **Sakhi Chatbot**: Get expert advice on PCOD, periods, and general wellness.
- **FAQs**: Access common questions and answers about PCOD and menstrual health.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/herhealthai.git
    ```

2. Navigate to the project directory:
    ```bash
    cd herhealthai
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the root directory.
    - Add your Together AI API key:
        ```
        TOGETHER_API_KEY=your_api_key_here
        ```

## Usage

1. Run the Streamlit application:
    ```bash
    streamlit run frontend/front.py
    ```

2. Open your web browser and navigate to `http://localhost:8501` to access the application.

## Project Structure

- `frontend/`: Contains the Streamlit frontend code.
- `backend/`: Contains the backend API code (if applicable).
- `README.md`: Project documentation.

## Contributing

We welcome contributions to improve HerHealth AI. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m "Add your commit message"
    ```
4. Push to the branch:
    ```bash
    git push origin feature/your-feature-name
    ```
5. Create a pull request.


