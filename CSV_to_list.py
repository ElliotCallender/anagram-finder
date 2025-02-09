import csv
from typing import List, Optional
from pathlib import Path
import os
import unidecode
import pandas as pd

def remove_accents(text):
    if pd.isna(text):  # Handle NaN/None values
        return text
    return unidecode.unidecode(str(text))

def csv_to_list(filepath: str, encoding: str = 'utf-8', strip: bool = True) -> List[str]:
    """
    Converts a single-column CSV file into a list of strings.
    
    Args:
        filepath (str): Path to the CSV file
        encoding (str, optional): File encoding. Defaults to 'utf-8'.
        strip (bool, optional): Whether to strip whitespace from values. Defaults to True.
    
    Returns:
        List[str]: List containing the values from the CSV file
        
    Raises:
        FileNotFoundError: If the specified file doesn't exist
        ValueError: If the CSV file contains more than one column
        csv.Error: If there are issues parsing the CSV file
    """
    df = pd.read_csv(filepath)
    print("Available columns:", df.columns.tolist())
    df['Word'] = df['Word'].apply(remove_accents)
    print("Applied remove_accents()")
    df.to_csv(filepath, index=False)
    print("Allegedly wrote to csv")
    file_path = Path(filepath)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    result = []
    
    try:
        with open(file_path, 'r', encoding=encoding, newline='') as file:
            reader = csv.reader(file)
            
            for row in reader:
                # Skip empty rows
                if not row:
                    continue
                    
                # Check if there's more than one column
                if len(row) > 1:
                    raise ValueError("CSV file contains more than one column")
                
                # Add the value to our result list
                value = row[0].strip() if strip else row[0]
                result.append(value)
                
        return result
        
    except csv.Error as e:
        raise csv.Error(f"Error parsing CSV file: {str(e)}")