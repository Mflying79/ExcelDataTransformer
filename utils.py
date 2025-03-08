import pandas as pd
import io

def load_excel(file):
    """
    Load Excel file into pandas DataFrame
    """
    try:
        return pd.read_excel(file)
    except Exception as e:
        raise Exception(f"Error reading Excel file: {str(e)}")

def save_excel(df):
    """
    Save DataFrame to Excel file in memory
    """
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        return output
    except Exception as e:
        raise Exception(f"Error saving Excel file: {str(e)}")
