import streamlit as st
import pandas as pd

# Robust CSV loading
try:
    df = pd.read_csv('anti_inflammatory_foods.csv', encoding='utf-8-sig')
except UnicodeDecodeError:
    df = pd.read_csv('anti_inflammatory_foods.csv', encoding='ISO-8859-1')

st.title("Anti-Inflammatory Foods for Women")

st.markdown("""
This dashboard helps women explore, filter, and select anti-inflammatory foods based on category and health goals.
Select the foods you like to build a custom plan with tailored recipe ideas!
""")

# Sidebar filters
categories = df['Category'].dropna().unique()

# Corrected column name for flags
flags = sorted({flag.strip() for row in df['flags'].dropna() for flag in str(row).split(',') if flag.strip()})

selected_category = st.sidebar.multiselect("Filter by Food Category", categories)
selected_flags = st.sidebar.multiselect("Filter by Health Issue", flags)

filtered = df.copy()
if selected_category:
    filtered = filtered[filtered['Category'].isin(selected_category)]
if selected_flags:
    # Corrected column name for flags
    filtered = filtered[filtered['flags'].apply(
        lambda x: any(flag in str(x) for flag in selected_flags) if pd.notna(x) else False
    )]

st.subheader("Explore Foods")
st.dataframe(
    # Corrected column names: 'Name' instead of 'Food Item', 'score' instead of 'Score (0–10)', 'flags' instead of 'Flags (Female Health Issues)'
    filtered[['Name', 'Category', 'score', 'Best For', 'flags', 'Sample Recipe/Usage']],
    use_container_width=True
)

# Corrected column name for filtered['Name']
selected_foods = st.multiselect("Choose foods for your custom plan:", filtered['Name'].unique())

if selected_foods:
    st.header("Your Custom Anti-Inflammatory Plan")
    # Corrected column name for filtered['Name']
    plan = filtered[filtered['Name'].isin(selected_foods)]
    st.dataframe(plan[['Name', 'Best Type/Form', 'Sample Recipe/Usage', 'Key Vitamins & Minerals', 'score', 'Cautions']], use_container_width=True) # Corrected 'score'
    st.write("**Recipe ideas from your selected foods:**")
    for _, row in plan.iterrows():
        # Corrected column name for 'Name'
        st.markdown(f"- **{row['Name']}**: {row['Sample Recipe/Usage']}")

    st.write("**Main Nutrients Covered:**")
    nutrients = set()
    for val in plan['Key Vitamins & Minerals']:
        if pd.notna(val):
            for n in str(val).split(','):
                nutrients.add(n.strip())
    st.write(", ".join(sorted(nutrients)))

else:
    st.info("Select at least one food item above to see your custom anti-inflammatory plan and recipe ideas.")

st.caption("Developed by Hanif | Powered by Streamlit")
