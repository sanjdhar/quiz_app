import streamlit as st
from google.cloud import datastore
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Datastore client
client = datastore.Client()
kind = "Test123"
quiz_id = "quiz123"


def check_datastore_data(kind):
    query = client.query(kind=kind)
    results = list(query.fetch(limit=1))
    if results:
        logger.info(f"Datastore contains data for kind: {kind}")
        logger.debug(f"Sample entity: {dict(results[0].items())}")
    else:
        logger.warning(f"No data found in Datastore for kind: {kind}")

# Call this function in your main() before get_leaderboard_data()
check_datastore_data(kind)


def get_leaderboard_data(kind):
    logger.info(f"Querying Datastore for kind: {kind}")
    query = client.query(kind=kind)
    results = list(query.fetch())
    logger.info(f"Retrieved {len(results)} entities from Datastore")

    if not results:
        logger.warning(f"No entities found for kind: {kind}")
        return pd.DataFrame()

    leaderboard_data = []
    for entity in results:
        logger.debug(f"Processing entity: {entity.key.id_or_name}")
        try:
            leaderboard_data.append({
                'nickname': str(entity.get('nickname', 'Unknown')),
                'percentage_score': int(entity.get('percentage_score', 0)),
                'total_time': float(entity.get('total_time', 0)),
                'quiz_id': str(entity.get('quiz_id', 'Unknown'))
            })
        except Exception as e:
            logger.error(f"Error processing entity: {entity.key.id_or_name}. Error: {str(e)}")
            logger.debug(f"Raw entity data: {dict(entity.items())}")

    df = pd.DataFrame(leaderboard_data)
    logger.info(f"Created DataFrame with {len(df)} rows")

    if df.empty:
        logger.warning("DataFrame is empty after processing entities")
        return df

    # ... (rest of the function remains the same)

    # Query the datastore
    query = client.query(kind=kind)
    results = list(query.fetch())
    
    # Process the data
    leaderboard_data = []
    for entity in results:
        try:
            leaderboard_data.append({
                'nickname': str(entity.get('nickname', 'Unknown')),
                'percentage_score': int(entity.get('percentage_score', 0)),
                'total_time': float(entity.get('total_time', 0)),
                'quiz_id': str(entity.get('quiz_id', 'Unknown'))
            })
        except Exception as e:
            logger.error(f"Error processing entity: {entity.key.id_or_name}. Error: {str(e)}")
            logger.debug(f"Raw entity data: {dict(entity.items())}")
    
    # Convert to DataFrame and sort
    df = pd.DataFrame(leaderboard_data)
    if df.empty:
        logger.warning("No data retrieved from Datastore")
        return df

    # Check if required columns exist
    required_columns = ['percentage_score', 'total_time']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        logger.error(f"Missing required columns: {missing_columns}")
        return pd.DataFrame()  # Return empty DataFrame if required columns are missing

    df = df.sort_values(by=['percentage_score', 'total_time'], ascending=[False, True])
    
    # Add rank column
    df['rank'] = df['percentage_score'].rank(method='min', ascending=False)
    
    return df

def main():
    st.title("Quiz Leaderboard")

    # Sidebar for filtering
    st.sidebar.header("Filters")
    kind = st.sidebar.text_input("Entity Kind", "QuizResult")
    top_n = st.sidebar.number_input("Show Top N", min_value=1, value=10)

    # Get and display leaderboard
    leaderboard = get_leaderboard_data(kind)
    
    if leaderboard.empty:
        st.warning("No data available for the leaderboard.")
        return

    st.subheader(f"Top {top_n} Players")
    st.table(leaderboard.head(top_n).style.format({
        'percentage_score': '{:.0f}%',  # Changed to integer format
        'total_time': '{:.2f} sec',
        'rank': '{:.0f}'
    }))

    # Display full leaderboard
    st.subheader("Full Leaderboard")
    st.dataframe(leaderboard.style.format({
        'percentage_score': '{:.0f}%',  # Changed to integer format
        'total_time': '{:.2f} sec',
        'rank': '{:.0f}'
    }))

if __name__ == "__main__":
    check_datastore_data(kind)
    main()
