import streamlit as st
import pandas as pd

# Load the data
df = pd.read_csv('anti_inflammatory_foods.csv')

st.title("Anti-Inflammatory Foods for Women")

# Sidebar filters
categories = df['Category'].dropna().unique()
flags = sorted({flag.strip() for row in df['Flags (Female Health Issues)'].dropna() for flag in row.split(',')})

selected_category = st.sidebar.multiselect("Filter by Food Category", categories)
selected_flags = st.sidebar.multiselect("Filter by Health Issue", flags)

filtered = df.copy()
if selected_category:
    filtered = filtered[filtered['Category'].isin(selected_category)]
if selected_flags:
    filtered = filtered[filtered['Flags (Female Health Issues)'].apply(
        lambda x: any(flag in x for flag in selected_flags) if pd.notna(x) else False
    )]

st.dataframe(
    filtered[['Food Item', 'Category', 'Score (0–10)', 'Best For', 'Flags (Female Health Issues)', 'Sample Recipe/Usage']]
)

selected_foods = st.multiselect("Choose foods for your custom plan:", filtered['Food Item'].unique())

if selected_foods:
    st.header("Your Custom Anti-Inflammatory Plan")
    plan = filtered[filtered['Food Item'].isin(selected_foods)]
    st.dataframe(plan[['Food Item', 'Best Type/Form', 'Sample Recipe/Usage', 'Key Vitamins & Minerals', 'Score (0–10)', 'Cautions']])
    st.write("**Recipe ideas:**")
    for _, row in plan.iterrows():
        st.markdown(f"- **{row['Food Item']}**: {row['Sample Recipe/Usage']}")
