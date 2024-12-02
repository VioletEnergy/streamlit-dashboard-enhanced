import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="School Learning Modalities Dashboard", layout="wide")
st.title("📊 School Learning Modalities Dashboard")
st.caption("Exploring NCES data on learning modalities for the 2020-2021 school year.")
st.markdown("""
### Observations
- The majority of students followed the "In Person" learning modality.
- Hybrid learning was consistently less popular compared to other modalities.
""")


# ## https://healthdata.gov/National/School-Learning-Modalities-2020-2021/a8v3-a3m3/about_data
df = pd.read_csv("https://healthdata.gov/resource/a8v3-a3m3.csv?$limit=50000") ## first 1k 

## data cleaning 
df['week_recoded'] = pd.to_datetime(df['week'])
df['zip_code'] = df['zip_code'].astype(str)

df['week'].value_counts()


# Dropdown to filter by district
districts = df['district_name'].dropna().unique()
selected_district = st.selectbox("Select a District:", options=["All"] + list(districts))

if selected_district != "All":
    df = df[df['district_name'] == selected_district]

# Show the filtered dataset
st.write(f"Showing data for **{selected_district}**")
st.dataframe(df)



# Pivot data for visualization
table = pd.pivot_table(df, values='student_count', index='week_recoded', columns='learning_modality', aggfunc="sum").reset_index()

# Create an interactive line chart
fig = px.line(
    table,
    x='week_recoded',
    y=['Hybrid', 'In Person', 'Remote'],
    labels={'value': 'Student Count', 'week_recoded': 'Week'},
    title="Learning Modalities Over Time",
    markers=True
)
st.plotly_chart(fig)

# Display summary stats
st.write("### Key Insights")
st.metric("Total Students", df['student_count'].sum())
st.metric("Average Students per Week", df.groupby('week')['student_count'].sum().mean())

# Add a pie chart for modality distribution
modality_distribution = df['learning_modality'].value_counts()
st.write("### Learning Modality Distribution")
st.write(modality_distribution)

fig = px.pie(names=modality_distribution.index, values=modality_distribution.values, title="Learning Modality Distribution")
st.plotly_chart(fig)


with st.sidebar:
    st.header("Filters")
    selected_modality = st.radio("Select Learning Modality:", options=["All", "Hybrid", "In Person", "Remote"])

if selected_modality != "All":
    df = df[df['learning_modality'] == selected_modality]


