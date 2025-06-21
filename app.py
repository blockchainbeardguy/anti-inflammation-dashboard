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

# --- CORRECTED: Use the full column name 'Flags (Female Health Issues)' ---
flags = sorted({flag.strip() for row in df['Flags (Female Health Issues)'].dropna() for flag in str(row).split(',') if flag.strip()})

selected_category = st.sidebar.multiselect("Filter by Food Category", categories)
selected_flags = st.sidebar.multiselect("Filter by Health Issue", flags)

filtered = df.copy()
if selected_category:
    filtered = filtered[filtered['Category'].isin(selected_category)]
if selected_flags:
    # --- CORRECTED: Use the full column name 'Flags (Female Health Issues)' ---
    filtered = filtered[filtered['Flags (Female Health Issues)'].apply(
        lambda x: any(flag in str(x) for flag in selected_flags) if pd.notna(x) else False
    )]

st.subheader("Explore Foods")
st.dataframe(
    # --- CORRECTED: Use 'Score (0–10)' and 'Flags (Female Health Issues)' ---
    filtered[['Food Item', 'Category', 'Score (0–10)', 'Best For', 'Flags (Female Health Issues)', 'Sample Recipe/Usage']],
    use_container_width=True
)

selected_foods = st.multiselect("Choose foods for your custom plan:", filtered['Food Item'].unique())

if selected_foods:
    st.header("Your Custom Anti-Inflammatory Plan")
    plan = filtered[filtered['Food Item'].isin(selected_foods)]
    # --- CORRECTED: Use 'Score (0–10)' ---
    st.dataframe(plan[['Food Item', 'Best Type/Form', 'Sample Recipe/Usage', 'Key Vitamins & Minerals', 'Score (0–10)', 'Cautions']], use_container_width=True)
    st.write("**Recipe ideas from your selected foods:**")
    for _, row in plan.iterrows():
        st.markdown(f"- **{row['Food Item']}**: {row['Sample Recipe/Usage']}")

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
