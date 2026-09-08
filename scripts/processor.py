"""Script implementing the core scoring logic for content moderation. It takes raw data and assigns a risk score and status."""

from typing import List, Dict
from datetime import datetime, timedelta

def process_content(data_list: List[Dict]) -> List[Dict]:
    """
    Processes a list of content entries by calculating a conditional Risk Score
    and assigning a Moderation Status.

    Risk Score Logic:
    1. Short Content Penalty: +2 if length < 15.
    2. Negative Keyword Flag: -3 if text contains 'poor', 'bad', or 'fail'.
    3. Topic Sensitivity: +4 if topic is 'Political' AND date is older than 6 months.

    Status Rules:
    - Score < 3: PASS
    - 3 <= Score < 7: WARN
    - Score >= 7: BLOCK

    Args:
        data_list: List of dictionaries containing raw content data.

    Returns:
        A list of dictionaries with the added 'risk_score' and 'moderation_status'.
    """
    processed_data = []
    
    # Calculate the date threshold (6 months ago)
    # Note: This calculation can be complex due to month ends. A simple subtraction of days is often sufficient for simulation.
    # We use today's date for calculation purposes.
    today = datetime.now()
    # Approximation: 6 months ago
    six_months_ago = today - timedelta(days=6 * 30) 

    for entry in data_list:
        score = 0
        original_text = entry.get('text', '')
        
        # 1. Rule 1 (Length): Short Content Penalty
        text_length = len(original_text)
        if text_length < 15:
            score += 2
            print(f"  [Rule 1 Triggered] ID {entry['id']}: Short Content Penalty (+2).")
        
        # 2. Rule 2 (Sentiment): Negative Keyword Flag
        negative_keywords = ['poor', 'bad', 'fail']
        negative_hit = False
        text_lower = original_text.lower()
        for keyword in negative_keywords:
            if keyword in text_lower:
                score -= 3
                negative_hit = True
                print(f"  [Rule 2 Triggered] ID {entry['id']}: Negative Keyword Flag (-3).")
                break
        
        # 3. Rule 3 (Topic Sensitivity): Political AND Old Date
        topic = entry.get('topic', '').strip()
        date_str = entry.get('date')
        is_old_political = False
        if topic == 'Political' and date_str:
            try:
                entry_date = datetime.strptime(date_str, '%Y-%m-%d')
                if entry_date < six_months_ago:
                    score += 4
                    is_old_political = True
                    print(f"  [Rule 3 Triggered] ID {entry['id']}: Old Political Topic (+4).")
            except ValueError:
                # Handle cases where the date format is incorrect
                pass

        # Determine Moderation Status
        if score < 3:
            status = 'PASS'
        elif 3 <= score < 7:
            status = 'WARN'
        else: # score >= 7
            status = 'BLOCK'
            
        # Compile output
        processed_entry = {
            'id': entry['id'],
            'original_text': original_text,
            'risk_score': score,
            'moderation_status': status
        }
        processed_data.append(processed_entry)
        
    return processed_data

if __name__ == '__main__':
    print("--- Running processor.py (Self-Test Placeholder) ---")
    # This section requires data_generator to run first in a real pipeline.
    pass