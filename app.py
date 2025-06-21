import streamlit as st
import pandas as pd

# Set Streamlit page configuration for a wider layout
st.set_page_config(layout="wide")

# --- Robust CSV loading ---
# Assuming 'anti_inflammatory_foods.csv' is in the same directory as app.py
try:
    df = pd.read_csv('anti_inflammatory_foods.csv', encoding='utf-8-sig')
except UnicodeDecodeError:
    df = pd.read_csv('anti_inflammatory_foods.csv', encoding='ISO-8859-1')
except FileNotFoundError:
    st.error("Error: 'anti_inflammatory_foods.csv' not found. Please ensure the CSV file is in the same directory as this script.")
    st.stop() # Stop the app execution if file is not found

# --- Initialize Streamlit session state for managing selections ---
if 'selected_foods_for_plan' not in st.session_state:
    st.session_state.selected_foods_for_plan = []
if 'detailed_food_id' not in st.session_state:
    st.session_state.detailed_food_id = None

# --- Custom CSS for visual improvements ---
st.markdown("""
<style>
    /* General styling */
    body { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #FEFBF6; color: #334155; }

    /* Header and subheader fonts */
    h1, h2, h3, h4, h5, h6 { color: #1E293B; }

    /* Buttons */
    .stButton>button {
        background-color: #0d9488; /* Teal-600 */
        color: white;
        border-radius: 0.5rem;
        padding: 0.75rem 1.25rem;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #0f766e; /* Darker Teal */
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stButton>button:active {
        transform: translateY(0);
        box-shadow: none;
    }
    /* Secondary buttons (e.g., View Details) */
    .stButton button[kind="secondary"] {
        background-color: #e2e8f0; /* Slate-200 */
        color: #475569; /* Slate-600 */
    }
    .stButton button[kind="secondary"]:hover {
        background-color: #cbd5e1; /* Slate-300 */
        color: #1e293b; /* Slate-900 */
    }

    /* Card styling */
    .food-card {
        background-color: white;
        border-radius: 0.75rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.2s ease-in-out;
        margin-bottom: 1rem;
        height: 100%; /* Ensure cards in columns have equal height */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .food-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.15);
    }
    .food-card-score {
        font-size: 2.25rem; /* text-4xl */
        font-weight: 700; /* font-bold */
        color: #0d9488; /* teal-600 */
        text-align: right;
    }
    .food-card-name {
        font-size: 1.5rem; /* text-2xl */
        font-weight: 700; /* font-bold */
        color: #1E293B;
    }
    .food-card-category {
        font-size: 0.875rem; /* text-sm */
        color: #64748B; /* slate-500 */
        margin-top: 0.25rem;
    }
    .food-card-why {
        font-size: 1rem; /* text-base */
        color: #475569; /* slate-600 */
        margin-top: 1rem;
        flex-grow: 1; /* Allows content to push buttons to bottom */
    }
    .food-card-buttons {
        display: flex;
        gap: 0.75rem;
        margin-top: 1.5rem;
    }

    /* Detail Modal styling (simulated) */
    .detail-card {
        background-color: white;
        border-radius: 0.75rem;
        padding: 2rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        margin-top: 2rem;
        border-left: 5px solid #0d9488; /* Teal accent */
    }
    .detail-card h3 {
        font-size: 1.875rem; /* text-3xl */
        font-weight: 700;
        color: #0d9488;
        margin-bottom: 1rem;
    }
    .detail-item-title {
        font-weight: 600;
        color: #1e293b;
        margin-top: 1rem;
        margin-bottom: 0.25rem;
    }
    .detail-item-content {
        color: #475569;
    }
    .flag-badge {
        display: inline-block;
        background-color: #ECFDF5; /* Green-50 */
        color: #047857; /* Green-700 */
        padding: 0.25rem 0.75rem;
        border-radius: 9999px; /* Full rounded */
        font-size: 0.75rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid #10B981;
    }
</style>
""", unsafe_allow_html=True)


# --- Page Header ---
st.title("NourishWell: Anti-Inflammatory Food Guide for Women")

st.markdown("""
Welcome to **NourishWell**, your personalized guide to anti-inflammatory eating specifically designed for women's health.
This app helps you discover foods that support various health goals, from menstrual health to menopause and general well-being.
Explore foods, understand their unique benefits, and build a custom nutritional plan tailored to your needs.
""")

# --- Section 1: Discover Your Anti-Inflammatory Foods ---
st.header("1. Discover Your Anti-Inflammatory Foods")
st.markdown("Start by selecting your primary health focus or browse by food category.")

# --- Sidebar Filters ---
st.sidebar.header("Filter Options")

all_categories = df['Category'].dropna().unique()
# --- Use the exact column name 'Flags (Female Health Issues)' from CSV ---
all_flags = sorted({flag.strip() for row in df['Flags (Female Health Issues)'].dropna() for flag in str(row).split(',') if flag.strip()})

selected_categories_filter = st.sidebar.multiselect(
    "Filter by Food Category:",
    options=all_categories,
    default=[]
)

selected_flags_filter = st.sidebar.multiselect(
    "Filter by Health Concern:",
    options=all_flags,
    default=[]
)

# --- Apply filters ---
filtered_df = df.copy()

if selected_categories_filter:
    filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories_filter)]

if selected_flags_filter:
    # --- Use the exact column name 'Flags (Female Health Issues)' from CSV ---
    filtered_df = filtered_df[filtered_df['Flags (Female Health Issues)'].apply(
        lambda x: any(flag in str(x) for flag in selected_flags_filter) if pd.notna(x) else False
    )]

# --- Sort by score for better visibility ---
filtered_df = filtered_df.sort_values(by='Score (0–10)', ascending=False)


# --- Display Food Cards ---
st.subheader("Explore Foods by Your Selection")

if filtered_df.empty:
    st.info("No foods match your current filter selections. Try adjusting your filters!")
else:
    # Create columns for the grid layout
    cols = st.columns(3) # Display 3 cards per row

    for index, food in filtered_df.iterrows():
        with cols[index % 3]: # Cycle through the columns for distribution
            # Get the first sentence of "Why Anti-Inflammatory"
            why_anti_inflammatory_snippet = food['Why Anti-Inflammatory'].split('. ')[0]
            # Add a period if the snippet exists and doesn't already end with one.
            if why_anti_inflammatory_snippet.strip() and not why_anti_inflammatory_snippet.strip().endswith('.'):
                why_anti_inflammatory_snippet += '.'

            st.markdown(f"""
            <div class="food-card">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div class="food-card-name">{food['Food Item']}</div>
                        <div class="food-card-score">{food['Score (0–10)']}</div>
                    </div>
                    <div class="food-card-category">{food['Category']}</div>
                    <div class="food-card-why">{why_anti_inflammatory_snippet}</div>
                </div>
                <div class="food-card-buttons">
                    {st.button("View Details", key=f"view_{food['Food Item']}", args=(food['Food Item'],))}
                    {st.button("Add to Plan", key=f"add_{food['Food Item']}", args=(food['Food Item'],), type="secondary")}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Handle button clicks
            # View Details Button
            if st.session_state.get(f"view_{food['Food Item']}"):
                st.session_state.detailed_food_id = food['Food Item']
                # Clear other button states to avoid re-triggering
                del st.session_state[f"view_{food['Food Item']}"]
                st.rerun() # Rerun to display the detailed food section

            # Add to Plan Button
            if st.session_state.get(f"add_{food['Food Item']}"):
                if food['Food Item'] not in st.session_state.selected_foods_for_plan:
                    st.session_state.selected_foods_for_plan.append(food['Food Item'])
                    st.toast(f"'{food['Food Item']}' added to your plan!")
                else:
                    st.toast(f"'{food['Food Item']}' is already in your plan!", icon="ℹ️")
                # Clear button state after action
                del st.session_state[f"add_{food['Food Item']}"]
                st.rerun() # Rerun to update the plan section


# --- Section 2: Detailed Food Information (Simulated Modal) ---
if st.session_state.detailed_food_id:
    detailed_food = df[df['Food Item'] == st.session_state.detailed_food_id].iloc[0]
    st.markdown(f"""
    <div class="detail-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3>{detailed_food['Food Item']}</h3>
            {st.button("Close Details", key="close_details")}
        </div>
        <p class="text-sm text-gray-500">{detailed_food['Category']} > {detailed_food['Sub-category']}</p>
        <div class="detail-item-title">Anti-Inflammatory Mechanism for Women:</div>
        <div class="detail-item-content">{detailed_food['Why Anti-Inflammatory']}</div>
        <div class="detail-item-title">Key Vitamins & Minerals:</div>
        <div class="detail-item-content">{detailed_food['Key Vitamins & Minerals']}</div>
        <div class="detail-item-title">Best Type/Form:</div>
        <div class="detail-item-content">{detailed_food['Best Type/Form']}</div>
        <div class="detail-item-title">Anti-Inflammatory Score:</div>
        <div class="detail-item-content">{detailed_food['Score (0–10)']}/10 (Justification: {detailed_food.get('Score Justification', 'N/A')})</div>
        <div class="detail-item-title">Best For:</div>
        <div class="detail-item-content">{detailed_food['Best For']}</div>
        <div class="detail-item-title">Beneficial For:</div>
        <div class="detail-item-content">{' '.join([f'<span class="flag-badge">{flag.strip()}</span>' for flag in str(detailed_food['Flags (Female Health Issues)']).split(',') if flag.strip()])}</div>
        <div class="detail-item-title">Regional Availability:</div>
        <div class="detail-item-content">{detailed_food['Regional Availability']}</div>
        <div class="detail-item-title">Cautions:</div>
        <div class="detail-item-content text-red-700">{detailed_food['Cautions']}</div>
        <div class="detail-item-title">Sample Recipe/Usage:</div>
        <div class="detail-item-content">{detailed_food['Sample Recipe/Usage']}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("close_details"):
        st.session_state.detailed_food_id = None
        del st.session_state["close_details"]
        st.rerun() # Rerun to hide the detailed food section

# --- Section 3: Your Custom Anti-Inflammatory Plan ---
st.header("2. Your Custom Anti-Inflammatory Plan")
if not st.session_state.selected_foods_for_plan:
    st.info("Add foods to your plan from the 'Discover Your Anti-Inflammatory Foods' section above.")
else:
    plan_df = df[df['Food Item'].isin(st.session_state.selected_foods_for_plan)]
    
    st.subheader("Selected Foods:")
    st.dataframe(
        plan_df[['Food Item', 'Category', 'Score (0–10)', 'Best For', 'Sample Recipe/Usage']],
        use_container_width=True
    )

    st.subheader("Combined Plan Insights:")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Recipe Ideas from Your Plan:")
        for _, row in plan_df.iterrows():
            st.markdown(f"- **{row['Food Item']}**: {row['Sample Recipe/Usage']}")
        
        if st.button("Clear My Plan", key="clear_plan_btn"):
            st.session_state.selected_foods_for_plan = []
            st.toast("Your plan has been cleared!")
            st.rerun()

    with col2:
        st.markdown("#### Main Nutrients Covered:")
        nutrients = set()
        for val in plan_df['Key Vitamins & Minerals']:
            if pd.notna(val):
                for n in str(val).split(','):
                    nutrients.add(n.strip())
        if nutrients:
            st.write(", ".join(sorted(nutrients)))
        else:
            st.info("No specific nutrients listed for selected foods.")

        st.markdown("#### General Cautions for Your Plan:")
        cautions = set()
        for val in plan_df['Cautions']:
            if pd.notna(val) and val.strip() != "None specific." and val.strip() != "":
                cautions.add(val.strip())
        if cautions:
            for caution in sorted(cautions):
                st.warning(f"- {caution}")
        else:
            st.info("No major cautions listed for the selected foods. Always consult a healthcare professional.")


# --- Section 4: Visual Data Insights (Existing Charts - Can be integrated with Chart.js if needed) ---
st.header("3. Visual Data Insights")
st.markdown("Get a quick overview of the dataset's characteristics.")

# --- Prepare data for charts ---
top_foods = df.sort_values(by='Score (0–10)', ascending=False).head(10)
category_counts = df['Category'].value_counts()
# --- Use the exact column name 'Flags (Female Health Issues)' from CSV ---
health_flag_counts = df['Flags (Female Health Issues)'].dropna().apply(lambda x: [f.strip() for f in str(x).split(',')]).explode().value_counts()

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Top 10 Anti-Inflammatory Foods by Score")
    st.bar_chart(top_foods.set_index('Food Item')['Score (0–10)'])

with col_chart2:
    st.subheader("Food Category Distribution")
    st.pie_chart(category_counts)

st.subheader("Health Concern Coverage (Number of Foods Benefitting Each)")
# Streamlit's native charts don't have a Polar Area Chart, so we'll use a bar chart for now
st.bar_chart(health_flag_counts)


st.caption("Developed by Hanif | Powered by Streamlit")
