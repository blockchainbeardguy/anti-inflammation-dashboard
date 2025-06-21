import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NourishWell: Food Discovery",
    layout="wide",
    initial_sidebar_state="collapsed" # No sidebar filters needed here
)

# --- CUSTOM CSS FOR MODERN UI (Repeated for consistency across pages) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="st-emotion"] {
        font-family: 'Inter', sans-serif;
        color: #334155; /* Slate-700 for text */
    }

    .stApp {
        background-color: #FEFBF6; /* Warm neutral background */
    }

    h1, h2, h3, h4, h5, h6 {
        color: #1E293B; /* Slate-900 for headings */
    }

    /* General button styling */
    .stButton>button {
        background-color: #0d9488; /* Teal-600 */
        color: white;
        border-radius: 0.5rem;
        padding: 0.75rem 1.25rem;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: none;
        font-size: 1rem;
    }
    .stButton>button:hover {
        background-color: #0f766e; /* Darker Teal */
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stButton>button:active {
        transform: translateY(0);
        box_shadow: none;
    }

    /* Secondary button style (e.g., View Details, Reset) */
    .stButton button[kind="secondary"] {
        background-color: #e2e8f0; /* Slate-200 */
        color: #475569; /* Slate-600 */
        box-shadow: none;
        border: 1px solid #cbd5e1; /* Slate-300 border */
    }
    .stButton button[kind="secondary"]:hover {
        background-color: #cbd5e1; /* Slate-300 */
        color: #1e293b; /* Slate-900 */
        transform: translateY(-1px);
        box_shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Detail Card styling (simulated modal) */
    .detail-card {
        background-color: white;
        border-radius: 0.75rem;
        padding: 2.5rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        margin-top: 2rem;
        border-left: 6px solid #0d9488;
        margin-bottom: 2rem;
    }
    .detail-card h3 {
        font-size: 2rem;
        font-weight: 700;
        color: #0d9488;
        margin-bottom: 1rem;
    }
    .detail-item-title {
        font-weight: 600;
        color: #1e293b;
        margin-top: 1rem;
        margin-bottom: 0.35rem;
        font-size: 1.05rem;
    }
    .detail-item-content {
        color: #475569;
        line-height: 1.5;
    }
    .flag-badge {
        display: inline-block;
        background-color: #ECFDF5;
        color: #047857;
        padding: 0.3rem 0.9rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 0.6rem;
        margin-bottom: 0.6rem;
        border: 1px solid #10B981;
    }

    /* Meal Plan Section styling (for the other page) */
    .meal-plan-section {
        background-color: white;
        border-radius: 0.75rem;
        padding: 2rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-top: 2rem;
    }
    .meal-plan-item {
        margin-bottom: 1.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px dashed #e2e8f0;
    }
    .meal-plan-item:last-child {
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }

    /* Custom styles for filter bar and data table */
    .filter-bar-container {
        background-color: white;
        padding: 1.25rem;
        border-radius: 0.75rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
        display: flex; /* Flexbox for horizontal layout */
        flex-wrap: wrap; /* Allow wrapping on small screens */
        gap: 1rem; /* Space between filter elements */
        align-items: center;
        justify-content: space-between;
    }
    .filter-item {
        flex: 1; /* Distribute space evenly initially */
        min-width: 150px; /* Minimum width before wrapping */
    }
    /* Specific styling for Streamlit widgets to fit the horizontal bar */
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 0.5rem;
        border: 1px solid #E2E8F0;
        background-color: #F8FAFC;
    }
    .stTextInput>div>div>input {
        border-radius: 0.5rem;
        border: 1px solid #E2E8F0;
        background-color: #F8FAFC;
    }
    .stSlider .stSliderVertical {
        padding-top: 0.5rem; /* Adjust padding for slider */
    }

    /* Table row styling using columns to mimic a table */
    .st_row {
        background-color: white;
        padding: 0.75rem 1rem;
        margin-bottom: 0.25rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        display: flex; /* Ensure inner columns behave as flex items */
        align-items: center;
        border: 1px solid #E2E8F0;
    }
    .st_row:hover {
        background-color: #F8FAFC;
    }
    .table-header {
        font-weight: 600;
        color: #1E293B;
        padding: 0.75rem 1rem;
        border-bottom: 2px solid #CBD5E1;
        margin-bottom: 0.5rem;
    }
    /* Style for buttons within the manually created table rows */
    .st_row .stButton button {
        padding: 0.3rem 0.6rem;
        font-size: 0.8rem;
        min-height: 28px; /* Standardize button height */
    }
</style>
""", unsafe_allow_html=True)

# --- CSV DATA LOADING ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('anti_inflammatory_foods.csv', encoding='utf-8-sig')
    except UnicodeDecodeError:
        df = pd.read_csv('anti_inflammatory_foods.csv', encoding='ISO-8859-1')
    return df

df = load_data()

# --- SESSION STATE INITIALIZATION ---
if 'selected_foods_for_plan' not in st.session_state:
    st.session_state.selected_foods_for_plan = []
if 'detailed_food_id' not in st.session_state:
    st.session_state.detailed_food_id = None


# --- HEADER SECTION ---
st.title("📊 Anti-Inflammatory Foods Dashboard")
st.markdown("""
<p style='font-size: 1.15rem; color: #475569; margin-bottom: 2rem;'>
    Explore foods that reduce inflammation, categorized and scored for women's health needs.
</p>
""", unsafe_allow_html=True)


# --- FILTER AND SEARCH BAR (Top of Page, Horizontal Row) ---
st.subheader("Filter & Search")

filter_cols = st.columns([1.5, 1, 1.5, 1, 0.5]) # Adjust column ratios for filter elements

all_categories = ['All Categories'] + sorted(df['Category'].dropna().unique().tolist())
all_health_flags = ['All Concerns'] + sorted({flag.strip() for row in df['Flags (Female Health Issues)'].dropna() for flag in str(row).split(',') if flag.strip()})
sort_options = {"Highest Score": "desc", "Lowest Score": "asc", "Alphabetical (A-Z)": "alpha_asc"}

with filter_cols[0]:
    selected_category = st.selectbox(
        "By Category:",
        options=all_categories,
        index=0,
        key='discovery_category_filter'
    )
with filter_cols[1]:
    sort_by = st.selectbox(
        "Sort By:",
        options=list(sort_options.keys()),
        index=0,
        key='discovery_sort_by'
    )
with filter_cols[2]:
    search_term = st.text_input(
        "Search Foods:",
        placeholder="e.g., salmon, magnesium, PCOS",
        key='discovery_search_term'
    )
with filter_cols[3]:
    min_score = st.slider(
        "Min Score:",
        min_value=0,
        max_value=10,
        value=0,
        key='discovery_min_score'
    )
with filter_cols[4]:
    if st.button("Reset", key='discovery_reset_filters', type="secondary", help="Clear all filters"):
        st.session_state.discovery_category_filter = 'All Categories'
        st.session_state.discovery_sort_by = 'Highest Score'
        st.session_state.discovery_search_term = ''
        st.session_state.discovery_min_score = 0
        st.rerun() # Rerun to apply reset


# --- APPLY FILTERS ---
filtered_df = df.copy()

# Category Filter
if selected_category != 'All Categories':
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

# Minimum Score Filter
filtered_df = filtered_df[filtered_df['Score (0–10)'] >= min_score]

# Search Filter
if search_term:
    search_term_lower = search_term.lower()
    # Apply search across relevant text columns using .get() for safety
    filtered_df = filtered_df[
        filtered_df.apply(lambda row:
            (str(row.get('Food Item', '')).lower().find(search_term_lower) != -1) or
            (str(row.get('Why Anti-Inflammatory', '')).lower().find(search_term_lower) != -1) or
            (str(row.get('Key Vitamins & Minerals', '')).lower().find(search_term_lower) != -1) or
            (str(row.get('Flags (Female Health Issues)', '')).lower().find(search_term_lower) != -1),
        axis=1)
    ]

# Sorting
if sort_by == "Highest Score":
    filtered_df = filtered_df.sort_values(by='Score (0–10)', ascending=False)
elif sort_by == "Lowest Score":
    filtered_df = filtered_df.sort_values(by='Score (0–10)', ascending=True)
elif sort_by == "Alphabetical (A-Z)":
    filtered_df = filtered_df.sort_values(by='Food Item', ascending=True)


st.markdown(f"<p style='font-size: 1.1rem; margin-bottom: 1.5rem; color: #475569;'>Showing <b>{len(filtered_df)}</b> foods.</p>", unsafe_allow_html=True)

# --- MAIN TABLE/LIST DISPLAY (Manually constructed with st.columns and st.button) ---
st.subheader("Food Database")

if filtered_df.empty:
    st.info("No foods match your current filter and search criteria. Try broadening your selection!")
else:
    # Define column widths for the manual table to make it responsive
    col_widths = [2, 1, 2, 3, 2, 0.75, 1] # Food Item, Category, Nutrients, Benefit, Best For, Score, Button

    # Table Header Row
    header_cols = st.columns(col_widths)
    header_cols[0].markdown("<div class='table-header'>Food Item</div>", unsafe_allow_html=True)
    header_cols[1].markdown("<div class='table-header'>Category</div>", unsafe_allow_html=True)
    header_cols[2].markdown("<div class='table-header'>Key Nutrients/Compounds</div>", unsafe_allow_html=True)
    header_cols[3].markdown("<div class='table-header'>Mechanism/Benefit</div>", unsafe_allow_html=True)
    header_cols[4].markdown("<div class='table-header'>Specific Benefit for Women</div>", unsafe_allow_html=True)
    header_cols[5].markdown("<div class='table-header'>Score</div>", unsafe_allow_html=True)
    header_cols[6].markdown("<div class='table-header'>Action</div>", unsafe_allow_html=True)


    # Data Rows
    for index, food in filtered_df.iterrows():
        row_cols = st.columns(col_widths)
        
        # Using .get() for robust column access, providing empty string if column is missing/NaN
        food_item = food.get('Food Item', '')
        category = food.get('Category', '')
        key_nutrients = food.get('Key Vitamins & Minerals', '')
        why_anti_inflammatory = food.get('Why Anti-Inflammatory', '')
        best_for = food.get('Best For', '')
        score = food.get('Score (0–10)', 'N/A')

        with row_cols[0]:
            st.markdown(f"<div class='st_row_item'><b>{food_item}</b></div>", unsafe_allow_html=True)
        with row_cols[1]:
            st.markdown(f"<div class='st_row_item'>{category}</div>", unsafe_allow_html=True)
        with row_cols[2]:
            st.markdown(f"<div class='st_row_item'>{key_nutrients}</div>", unsafe_allow_html=True)
        with row_cols[3]:
            # Display only a snippet of the mechanism for table view, full in details
            snippet = why_anti_inflammatory.split('. ')[0]
            if snippet and not snippet.strip().endswith('.'): snippet += '.'
            st.markdown(f"<div class='st_row_item'>{snippet}</div>", unsafe_allow_html=True)
        with row_cols[4]:
            st.markdown(f"<div class='st_row_item'>{best_for}</div>", unsafe_allow_html=True)
        with row_cols[5]:
            st.markdown(f"<div class='st_row_item'>**{score}**</div>", unsafe_allow_html=True)
        with row_cols[6]:
            add_button_key = f"add_to_plan_{food_item}_{index}" # Unique key for each button
            if st.button("Add to Plan", key=add_button_key, type="primary"):
                if food_item not in st.session_state.selected_foods_for_plan:
                    st.session_state.selected_foods_for_plan.append(food_item)
                    st.toast(f"'{food_item}' added to your plan! 🎉", icon="✅")
                else:
                    st.toast(f"'{food_item}' is already in your plan!", icon="ℹ️")
                st.rerun() # Rerun to update the selected foods list immediately

# --- VIEW MY PLAN BUTTON (Conditional) ---
st.markdown("---") # Separator
if st.session_state.selected_foods_for_plan:
    st.subheader("Your Meal Plan Awaits!")
    st.markdown(f"<p style='color: #475569;'>You have <b>{len(st.session_state.selected_foods_for_plan)}</b> foods selected for your plan.</p>", unsafe_allow_html=True)
    st.page_link("pages/2_Meal_Plan.py", label="Go to My Meal Plan →", icon="➡️", type="primary")
else:
    st.info("Select foods from the list above to start building your personalized meal plan.")


# --- DETAILED FOOD INFORMATION (SIMULATED MODAL/EXPANDABLE PANEL - Triggered by button) ---
# For simplicity, this is not directly linked to a button in the manual table above,
# as managing two buttons per row (View Details + Add to Plan) in the manual approach
# adds significant complexity with Streamlit's rerunning nature for multiple buttons.
# If "View Details" is crucial on the main table, consider `streamlit-aggrid`.
# For now, this detail view can be expanded conceptually or triggered differently.
# Example: st.expander could be used to show details if you wanted it right in the list.

# If you still need a View Details for each row, we'd need to add a second button
# in the loop. The current design prioritizes "Add to Plan" as the primary CTA per row.
# The `detailed_food_id` logic can still be used if you decide to add a separate
# mechanism to trigger it (e.g., a multi-select for "view details" and then a global button).

st.caption("Developed by Hanif | Powered by Streamlit")
