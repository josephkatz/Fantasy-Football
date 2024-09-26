import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Fantasy Football Player Comparison", page_icon="🏈", layout="wide")  # Move this line to the top

st.title("🏈 Jewish Fantasy Football League")

# Excel file handling
excel_file_path = "Groves.xlsx"
try:
    xls = pd.ExcelFile(excel_file_path)
    sheet_names = xls.sheet_names
    selected_sheet = st.selectbox("🔍 What Are You Looking For?", sheet_names, key='sheet_select')
    df = pd.read_excel(xls, sheet_name=selected_sheet)
    st.write(f"### 📄 {selected_sheet}")
    st.dataframe(df, use_container_width=True)
except FileNotFoundError:
    st.error(f"🚨 Excel file `{excel_file_path}` not found.")
except Exception as e:
    st.error(f"🛑 Error loading Excel file: {e}")

# Load the Excel file (from your file path)
file_path = 'Groves.xlsx'
xls = pd.ExcelFile(file_path)

# Load the "All Time Stats" sheet
all_time_stats_df = pd.read_excel(xls, sheet_name="All Time Stats", header=None)

# Parse the data manually based on provided structure
players = ['Alex S.', 'Dylan D.', 'Ethan L.', 'Grant B.', 'Jack G.', 'Joey K.', 'Max T.', 'Michael P.', 'Nick L.', 'Riley D.']

# Extract specific stats for each player
player_data = {}

for i, player in enumerate(players):
    player_data[player] = {
        'Regular Season Points': all_time_stats_df.iloc[1, 3*i+2],
        'Wins': all_time_stats_df.iloc[3, 3*i],
        'Losses': all_time_stats_df.iloc[3, 3*i+1],
        'Playoff Points': all_time_stats_df.iloc[4, 3*i+2],
        'Playoff Wins': all_time_stats_df.iloc[6, 3*i],
        'Playoff Losses': all_time_stats_df.iloc[6, 3*i+1],
        'Championships': all_time_stats_df.iloc[7, 3*i+1] + (1 if player in ['Joey K.', 'Riley D.'] else 0) 
    }

# Set up the Streamlit page
st.title("Fantasy Football Player Comparison")
# st.markdown("Compare stats like wins, losses, and points across different players.")

# Multiselect widget for users to choose players
selected_players = st.multiselect('Select Players to Compare:', players)

# Create a dropdown for selecting stats (Regular Season Points, Wins, Losses, etc.)
stats_options = ['Regular Season Points', 'Playoff Points', 'Wins', 'Losses', 'Playoff Wins', 'Playoff Losses', 'Championships']
selected_stat = st.selectbox("Select Stat to Compare:", stats_options)

# Plot comparison charts if players are selected
if selected_players:
    # Prepare data for visualization
    comparison_data = {player: player_data[player][selected_stat] for player in selected_players}

    # Create a DataFrame for the selected players and stats
    comparison_df = pd.DataFrame(list(comparison_data.items()), columns=['Player', selected_stat])

    # Plot bar chart with enhancements
    fig = px.bar(comparison_df, x='Player', y=selected_stat, 
                 title=f"{selected_stat} Comparison", 
                 labels={selected_stat:selected_stat, 'Player':'Player'},
                 color=selected_stat,  # Add color based on the selected stat
                 color_continuous_scale=px.colors.sequential.Viridis)  # Use a color scale

    # Update layout for better appearance
    fig.update_layout(
        title_font_size=24,
        xaxis_title_font_size=18,
        yaxis_title_font_size=18,
        legend_title_font_size=16,
        margin=dict(l=40, r=40, t=40, b=40)  # Adjust margins
    )

    # Add data labels to bars
    fig.update_traces(texttemplate='%{y}', textposition='outside')

    st.plotly_chart(fig)

