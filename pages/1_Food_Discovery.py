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
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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

    /* Custom style for Add to Plan button in dataframe if not using column_config */
    .stDataFrame .add-to-plan-btn {
        background-color: #0d9488; /* Teal-600 */
        color: white;
        border-radius: 0.5rem;
        padding: 0.35rem 0.75rem;
        font-size: 0.8rem;
        font-weight: 500;
        border: none;
        cursor: pointer;
    }
    .stDataFrame .add-to-plan-btn:hover {
        background-color: #0f766e;
    }

    /* Sticky filter bar (Streamlit native doesn't fully support, but this is a common trick) */
    div.stSpinner + div {
        margin-top: 2rem; /* Give space for spinner if used */
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

# --- DEBUGGING LINE: PRINT ALL COLUMN NAMES ---
st.write("DEBUG: Columns loaded from CSV:", df.columns.tolist())
# --- END DEBUGGING LINE ---

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
            (row.get('Food Item', '').lower().find(search_term_lower) != -1) or
            (row.get('Why Anti-Inflammatory', '').lower().find(search_term_lower) != -1) or
            (row.get('Key Vitamins & Minerals', '').lower().find(search_term_lower) != -1) or
            (row.get('Flags (Female Health Issues)', '').lower().find(search_term_lower) != -1),
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

# --- MAIN TABLE/LIST DISPLAY ---
st.subheader("Food Database")

if filtered_df.empty:
    st.info("No foods match your current filter and search criteria. Try broadening your selection!")
else:
    # Prepare DataFrame for display with custom columns and buttons
    # Using .get() for safety when accessing columns, providing N/A default for display
    display_df = pd.DataFrame({
        'Food Item': filtered_df['Food Item'],
        'Category': filtered_df['Category'],
        'Key Nutrients/Compounds': filtered_df.get('Key Vitamins & Minerals', 'N/A'),
        'Mechanism/Benefit': filtered_df.get('Why Anti-Inflammatory', 'N/A'),
        'Specific Benefit for Women': filtered_df.get('Best For', 'N/A'),
        'Anti-Inflammation Score': filtered_df['Score (0–10)'],
        # These are for internal use by the buttons, not directly displayed as column data
        'Sample Recipe/Usage_hidden': filtered_df.get('Sample Recipe/Usage', 'N/A'),
        'Cautions_hidden': filtered_df.get('Cautions', 'N/A')
    })

    # Add dummy columns for action buttons which will trigger Streamlit's internal button handling
    display_df['View Details'] = 'View Details'
    display_df['Add to Plan'] = 'Add to Plan'

    # Display the DataFrame with column configurations
    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True,
        column_order=[
            'Food Item', 'Category', 'Key Nutrients/Compounds',
            'Mechanism/Benefit', 'Specific Benefit for Women', 'Anti-Inflammation Score',
            'View Details', 'Add to Plan' # Order action buttons at the end
        ],
        column_config={
            "Food Item": st.column_config.TextColumn(
                "Food Item", width="medium"
            ),
            "Category": st.column_config.TextColumn(
                "Category", width="small"
            ),
            "Key Nutrients/Compounds": st.column_config.TextColumn(
                "Key Nutrients/Compounds", width="medium"
            ),
            "Mechanism/Benefit": st.column_config.TextColumn(
                "Mechanism/Benefit", width="large"
            ),
            "Specific Benefit for Women": st.column_config.TextColumn(
                "Specific Benefit for Women", width="medium"
            ),
            "Anti-Inflammation Score": st.column_config.NumberColumn(
                "Score", format="%d", width="small"
            ),
            "View Details": st.column_config.ButtonColumn(
                "View Details", width="small"
            ),
            "Add to Plan": st.column_config.ButtonColumn(
                "Add to Plan", width="small"
            ),
            "Sample Recipe/Usage_hidden": None, # Hide internal columns
            "Cautions_hidden": None # Hide internal columns
        },
        on_select="rerun", # Rerun the app when a selection is made
        selection_mode="single-row" # Only allow one selection at a time for button click
    )

    # Process button clicks from the dataframe
    if st.session_state.get('dataframe_selected_rows') and st.session_state.dataframe_selected_rows['added_rows']:
        selected_row_index = st.session_state.dataframe_selected_rows['added_rows'][0]
        selected_food_data = filtered_df.iloc[selected_row_index] # Get full row data

        # Determine which button was clicked based on the column name (which is the label of the ButtonColumn)
        if st.session_state.dataframe_selected_rows['column_name'] == 'Add to Plan':
            if selected_food_data['Food Item'] not in st.session_state.selected_foods_for_plan:
                st.session_state.selected_foods_for_plan.append(selected_food_data['Food Item'])
                st.toast(f"'{selected_food_data['Food Item']}' added to your plan! 🎉", icon="✅")
            else:
                st.toast(f"'{selected_food_data['Food Item']}' is already in your plan!", icon="ℹ️")
        elif st.session_state.dataframe_selected_rows['column_name'] == 'View Details':
            st.session_state.detailed_food_id = selected_food_data['Food Item']
        
        # Clear selection after processing to avoid re-triggering on next rerun
        st.session_state.dataframe_selected_rows = {'added_rows': [], 'removed_rows': [], 'column_name': None}
        st.rerun() # Rerun to update state or display details


# --- VIEW MY PLAN BUTTON (Conditional) ---
st.markdown("---") # Separator
if st.session_state.selected_foods_for_plan:
    st.subheader("Your Meal Plan Awaits!")
    st.markdown(f"<p style='color: #475569;'>You have <b>{len(st.session_state.selected_foods_for_plan)}</b> foods selected for your plan.</p>", unsafe_allow_html=True)
    st.page_link("pages/2_Meal_Plan.py", label="Go to My Meal Plan →", icon="➡️", type="primary")
else:
    st.info("Select foods from the list above to start building your personalized meal plan.")


# --- DETAILED FOOD INFORMATION (SIMULATED MODAL/EXPANDABLE PANEL) ---
if st.session_state.detailed_food_id:
    detailed_food = df[df['Food Item'] == st.session_state.detailed_food_id].iloc[0]
    st.markdown(f"""
    <div class="detail-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h3>{detailed_food['Food Item']}</h3>
            {st.button("Close Details", key="close_details_modal")}
        </div>
        <p class="text-sm text-gray-500">{detailed_food['Category']} > {detailed_food.get('Sub-category', 'N/A')}</p>
        <div class="detail-item-title">Why Anti-Inflammatory (for Women):</div>
        <div class="detail-item-content">{detailed_food.get('Why Anti-Inflammatory', 'N/A')}</div>
        <div class="detail-item-title">Key Vitamins & Minerals:</div>
        <div class="detail-item-content">{detailed_food.get('Key Vitamins & Minerals', 'N/A')}</div>
        <div class="detail-item-title">Best Type/Form:</div>
        <div class="detail-item-content">{detailed_food.get('Best Type/Form', 'N/A')}</div>
        <div class="detail-item-title">Anti-Inflammatory Score:</div>
        <div class="detail-item-content">{detailed_food.get('Score (0–10)', 'N/A')}/10</div>
        <div class="detail-item-title">Best For:</div>
        <div class="detail-item-content">{detailed_food.get('Best For', 'N/A')}</div>
        <div class="detail-item-title">Beneficial For:</div>
        <div class="detail-item-content">{' '.join([f'<span class="flag-badge">{flag.strip()}</span>' for flag in str(detailed_food.get('Flags (Female Health Issues)', '')).split(',') if flag.strip()])}</div>
        <div class="detail-item-title">Regional Availability:</div>
        <div class="detail-item-content">{detailed_food.get('Regional Availability', 'N/A')}</div>
        <div class="detail-item-title">Cautions:</div>
        <div class="detail-item-content" style="color: #EF4444;">{detailed_food.get('Cautions', 'N/A')}</div>
        <div class="detail-item-title">Sample Recipe/Usage:</div>
        <div class="detail-item-content">{detailed_food.get('Sample Recipe/Usage', 'N/A')}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("close_details_modal"):
        st.session_state.detailed_food_id = None
        st.rerun() # Rerun to hide the detailed food section

st.caption("Developed by Hanif | Powered by Streamlit")
