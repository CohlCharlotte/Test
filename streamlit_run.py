import os
import pandas as pd
import numpy as np
import streamlit as st
from supabase import create_client
from supabase import create_client, Client
from dotenv import load_dotenv

# ------------------------
# Supabase client setup
# ------------------------
def get_client() -> Client:
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in .env")
    return create_client(url, key)


@st.cache_data
def load_data():
    supabase = get_client()
    # Query all rows from your models_upload table
    response = supabase.table("models_upload").select("*").execute()

    if not response.data:
        st.warning("No data returned from Supabase.")
        return pd.DataFrame()

    df = pd.DataFrame(response.data)

    # Make sure data types are correct
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df['wins'] = pd.to_numeric(df['wins'], errors='coerce')
    df['losses'] = pd.to_numeric(df['losses'], errors='coerce')
    df['ot_losses'] = pd.to_numeric(df['ot_losses'], errors='coerce')
    df['win_percentage'] = pd.to_numeric(df['win_percentage'], errors='coerce')
    df['goals_for'] = pd.to_numeric(df['goals_for'], errors='coerce')
    df['goals_against'] = pd.to_numeric(df['goals_against'], errors='coerce')
    df['plus_minus'] = pd.to_numeric(df['plus_minus'], errors='coerce')

    return df

# ------------------------
# Streamlit App
# ------------------------
def main():
    st.title("🏒 NHL Team Stats Dashboard (from Supabase)")

    st.write("Data loaded live from Supabase table: `models_upload`")

    data_load_state = st.text("Loading data...")
    df = load_data()
    data_load_state.text("✅ Data loaded!")

    if df.empty:
        st.stop()

    if st.checkbox("Show raw data"):
        st.subheader("Raw data")
        st.dataframe(df)

    # Example visualization: Average win percentage by year
    st.subheader("Average Win Percentage by Year")
    avg_win_by_year = df.groupby("year")["win_percentage"].mean()
    st.bar_chart(avg_win_by_year)

    # Dropdown to choose a specific team
    team_list = df["team_name"].unique()
    team = st.selectbox("Select a team", options=team_list)

    team_df = df[df["team_name"] == team]

    st.subheader(f"Performance of {team}")
    st.line_chart(team_df.set_index("year")[["wins", "losses"]])

    # Example scatterplot: goals_for vs goals_against
    st.subheader("Goals For vs Goals Against (All Teams)")
    st.scatter_chart(df, x="goals_for", y="goals_against")


if __name__ == "__main__":
    main()
