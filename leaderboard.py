import streamlit as st
from google.cloud import datastore
import pandas as pd
from google.api_core import exceptions

# Initialize Datastore client
client = datastore.Client()

def fetch_leaderboard_data():
    try:
        query = client.query(kind='Test123')
        query.order = ['-percentage_score', 'total_time']
        results = list(query.fetch(limit=100))

        leaderboard_data = []
        for rank, entity in enumerate(results, start=1):
            medal = ""
            if rank == 1:
                medal = "🥇 "
            elif rank == 2:
                medal = "🥈 "
            elif rank == 3:
                medal = "🥉 "
            
            leaderboard_data.append({
                'Rank': f"{medal}{rank}",
                'Nickname': entity['nickname'],
                'Score': entity['score'],
                'Percentage': f"{entity['percentage_score']}%",
                'Time': f"{entity['total_time']:.2f} sec"  # Format time to 2 decimal places
            })
        
        return pd.DataFrame(leaderboard_data)
    except exceptions.FailedPrecondition as e:
        st.error(f"An index error occurred: {str(e)}")
        st.info("Please create the required index in your Datastore. Follow the instructions below:")
        st.code("""
1. Create a file named 'index.yaml' with the following content:

indexes:
- kind: Test123
  properties:
  - name: percentage_score
    direction: desc
  - name: total_time

2. Deploy the index using the following command in your terminal:
   gcloud datastore indexes create index.yaml

3. Wait for the index to finish building. You can check the status in the Google Cloud Console under Datastore > Indexes.
        """)
        return pd.DataFrame()

def main():
    st.title("🏆 Quiz Leaderboard 🏆")

    leaderboard_df = fetch_leaderboard_data()
    
    if not leaderboard_df.empty:
        # Apply custom styling
        st.markdown("""
        <style>
        table {
            font-size: 20px;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #ddd;
        }
        </style>
        """, unsafe_allow_html=True)

        # Display the table
        st.table(leaderboard_df)

        # Display congratulatory message for top 3
        top_3 = leaderboard_df.head(3)
        st.success("🎉 Congratulations to our top performers! 🎉")
        for i, (index, row) in enumerate(top_3.iterrows(), 1):
            st.markdown(f"**{i}. {row['Nickname']}** - Score: {row['Score']}, Time: {row['Time']}")
    else:
        st.write("No quiz results available or an index error occurred.")

    if st.button("🔄 Refresh Leaderboard"):
        st.rerun()

if __name__ == "__main__":
    main()
