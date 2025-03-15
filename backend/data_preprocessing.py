import pandas as pd
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder

def load_and_clean_data(filepath):
    """Load the dataset, handle missing values, encode categorical data, and scale numerical features."""
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        raise RuntimeError(f"Error reading the CSV file: {e}")
    
    # Handle missing values
    df.fillna(method='ffill', inplace=True)
    
    # Encode categorical features and store encoders
    label_encoders = {}
    for col in df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    
    # Scale numerical features and store the scaler
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
    
    return df_scaled, label_encoders, scaler

if __name__ == "__main__":
    try:
        csv_file = "../data/health_data.csv"
        print("Loading and cleaning data...")
        data, encoders, scaler = load_and_clean_data(csv_file)

        # Ensure the output directory exists
        output_dir = "../data"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "processed_data.csv")

        data.to_csv(output_file, index=False)
        print(f"Data preprocessing complete. Processed data saved at {output_file}.")

    except Exception as e:
        print(f"Error during processing: {e}")
