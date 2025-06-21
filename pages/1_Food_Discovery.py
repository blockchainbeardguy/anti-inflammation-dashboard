import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NourishWell: Food Discovery",
    layout="wide",
    initial_sidebar_state="expanded"
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
        border-radius: 0.75rem; /* More rounded */
        padding: 0.75rem 1.25rem; /* Standard padding */
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
        box-shadow: none;
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

    /* Food card specific styling for Food Discovery page */
    .food-card {
        background-color: white;
        border-radius: 0.75rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); /* Lighter shadow */
        transition: all 0.2s ease-in-out;
        margin-bottom: 1.5rem; /* More space between cards */
        height: 100%; /* Ensure cards in columns have equal height */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border: 1px solid #f0f4f8; /* Light border */
    }
    .food-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.1); /* Stronger hover shadow */
    }
    .food-card-score {
        font-size: 2.5rem; /* Larger score */
        font-weight: 700;
        color: #0d9488; /* Teal-600 */
        text-align: right;
        line-height: 1; /* Adjust line height for big number */
    }
    .food-card-name {
        font-size: 1.625rem; /* text-xl to 2xl */
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    .food-card-category {
        font-size: 0.875rem; /* text-sm */
        color: #64748B; /* slate-500 */
        margin-top: 0.25rem;
        font-weight: 500;
    }
    .food-card-why {
        font-size: 0.95rem; /* Slightly smaller for snippet */
        color: #475569; /* slate-600 */
        margin-top: 1rem;
        flex-grow: 1;
        line-height: 1.4;
    }
    .food-card-buttons {
        display: flex;
        gap: 0.75rem;
        margin-top: 1.5rem;
        justify-content: space-between; /* Distribute buttons */
    }
    .food-card-buttons button {
        flex-grow: 1; /* Make buttons fill space */
    }

    /* Detail Card styling (simulated modal) for Food Discovery page */
    .detail-card {
        background-color: white;
        border-radius: 0.75rem;
        padding: 2.5rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        margin-top: 2rem;
        border-left: 6px solid #0d9488; /* Stronger teal accent */
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

    /* Meal Plan Section styling for Meal Plan page */
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

    /* Ensure specific Streamlit elements blend */
    .stMultiSelect, .stSlider {
        margin-bottom: 1rem;
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
if 'generated_meal_plan' not in st.session_state:
    st.session_state.generated_meal_plan = []


# --- HEADER ---
st.title("🌱 Food Discovery")
st.markdown("Explore a wide range of anti-inflammatory foods. Use the filters in the sidebar to refine your search and click 'Add to Plan' for your favorites.")

# --- MAIN CONTENT LAYOUT ---
# Using columns for main content vs. sidebar filters
main_content_col, _ = st.columns([1, 0.01]) # Main content takes most space

with main_content_col:
    # --- Sidebar Filters (Moved to sidebar in this multipage structure) ---
    with st.sidebar:
        st.header("🔍 Filter Foods")
        
        all_categories = df['Category'].dropna().unique()
        all_flags = sorted({flag.strip() for row in df['Flags (Female Health Issues)'].dropna() for flag in str(row).split(',') if flag.strip()})

        # Using unique keys for persistent filter states across pages
        selected_categories_filter = st.multiselect(
            "Food Categories:",
            options=all_categories,
            default=st.session_state.get('selected_categories_filter', []),
            key='selected_categories_filter',
            help="Select one or more categories to narrow down foods."
        )

        selected_flags_filter = st.multiselect(
            "Health Concerns:",
            options=all_flags,
            default=st.session_state.get('selected_flags_filter', []),
            key='selected_flags_filter',
            help="Choose specific health issues you want to address."
        )

        min_score_filter = st.slider(
            "Minimum Anti-Inflammatory Score:",
            min_value=0,
            max_value=10,
            value=st.session_state.get('min_score_filter', 0),
            key='min_score_filter',
            help="Only show foods with a score equal to or higher than this value."
        )

        if st.button("Reset Filters", type="secondary", use_container_width=True):
            st.session_state.selected_categories_filter = []
            st.session_state.selected_flags_filter = []
            st.session_state.min_score_filter = 0
            st.session_state.detailed_food_id = None # Also reset detailed view
            st.rerun() # Use rerun to clear filters visually

    # --- Apply filters ---
    filtered_df = df.copy()
    
    if selected_categories_filter:
        filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories_filter)]

    if selected_flags_filter:
        filtered_df = filtered_df[filtered_df['Flags (Female Health Issues)'].apply(
            lambda x: any(flag in str(x) for flag in selected_flags_filter) if pd.notna(x) else False
        )]

    filtered_df = filtered_df[filtered_df['Score (0–10)'] >= min_score_filter]

    filtered_df = filtered_df.sort_values(by='Score (0–10)', ascending=False)

    st.markdown(f"<p style='font-size: 1.1rem; margin-bottom: 1.5rem; color: #475569;'>Found <b>{len(filtered_df)}</b> anti-inflammatory foods matching your criteria.</p>", unsafe_allow_html=True)

    # --- FOOD ITEM DISPLAY (CARDS) ---
    if filtered_df.empty:
        st.info("No foods match your current filter selections. Try adjusting your filters!")
    else:
        # Create columns for the grid layout
        food_cols = st.columns(3) # Display 3 cards per row

        for index, food in filtered_df.iterrows():
            with food_cols[index % 3]: # Cycle through the columns for distribution
                # Get snippet and ensure it ends with a period
                why_anti_inflammatory_full = food.get('Why Anti-Inflammatory', '')
                why_anti_inflammatory_snippet = why_anti_inflammatory_full.split('. ')[0]
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
                        <div class="food-card-why">{why_anti_inflammatory_snippet if why_anti_inflammatory_snippet else 'Brief description not available.'}</div>
                    </div>
                    <div class="food-card-buttons">
                        {st.button("View Details", key=f"view_{food['Food Item']}", args=(food['Food Item'],), type="secondary", use_container_width=True)}
                        {st.button("Add to Plan", key=f"add_{food['Food Item']}", args=(food['Food Item'],), use_container_width=True)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Handle button clicks (must be outside the markdown for Streamlit's internal logic)
                if st.session_state.get(f"view_{food['Food Item']}"):
                    st.session_state.detailed_food_id = food['Food Item']
                    # Clear button state after action
                    del st.session_state[f"view_{food['Food Item']}"]
                    st.rerun() # Rerun to display the detailed food section

                if st.session_state.get(f"add_{food['Food Item']}"):
                    if food['Food Item'] not in st.session_state.selected_foods_for_plan:
                        st.session_state.selected_foods_for_plan.append(food['Food Item'])
                        st.toast(f"'{food['Food Item']}' added to your plan! 🎉", icon="✅")
                    else:
                        st.toast(f"'{food['Food Item']}' is already in your plan!", icon="ℹ️")
                    # Clear button state after action
                    del st.session_state[f"add_{food['Food Item']}"]
                    st.rerun() # Rerun to update the plan button below


    # --- View My Plan Button (Conditional) ---
    if st.session_state.selected_foods_for_plan:
        st.markdown("---") # Separator
        st.subheader("Ready to build your plan?")
        st.markdown(f"<p style='color: #475569;'>You have <b>{len(st.session_state.selected_foods_for_plan)}</b> foods selected.</p>", unsafe_allow_html=True)
        # Use a Streamlit native link button to navigate
        st.page_link("pages/2_Meal_Plan.py", label="View My Plan", icon="➡️")
    else:
        st.info("Add some foods to your plan to enable the 'View My Plan' button!")


# --- DETAILED FOOD INFORMATION (SIMULATED MODAL/EXPANDABLE PANEL) ---
# This section will appear below the food grid when "View Details" is clicked
if st.session_state.detailed_food_id:
    detailed_food = df[df['Food Item'] == st.session_state.detailed_food_id].iloc[0]
    st.markdown(f"""
    <div class="detail-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h3>{detailed_food['Food Item']}</h3>
            {st.button("Close Details", key="close_details")}
        </div>
        <p class="text-sm text-gray-500">{detailed_food['Category']} > {detailed_food.get('Sub-category', 'N/A')}</p>
        <div class="detail-item-title">Why Anti-Inflammatory (for Women):</div>
        <div class="detail-item-content">{detailed_food.get('Why Anti-Inflammatory', 'N/A')}</div>
        <div class="detail-item-title">Key Vitamins & Minerals:</div>
        <div class="detail-item-content">{detailed_food['Key Vitamins & Minerals']}</div>
        <div class="detail-item-title">Best Type/Form:</div>
        <div class="detail-item-content">{detailed_food['Best Type/Form']}</div>
        <div class="detail-item-title">Anti-Inflammatory Score:</div>
        <div class="detail-item-content">{detailed_food['Score (0–10)']}/10</div>
        <div class="detail-item-title">Best For:</div>
        <div class="detail-item-content">{detailed_food['Best For']}</div>
        <div class="detail-item-title">Beneficial For:</div>
        <div class="detail-item-content">{' '.join([f'<span class="flag-badge">{flag.strip()}</span>' for flag in str(detailed_food['Flags (Female Health Issues)']).split(',') if flag.strip()])}</div>
        <div class="detail-item-title">Regional Availability:</div>
        <div class="detail-item-content">{detailed_food['Regional Availability']}</div>
        <div class="detail-item-title">Cautions:</div>
        <div class="detail-item-content" style="color: #EF4444;">{detailed_food['Cautions']}</div>
        <div class="detail-item-title">Sample Recipe/Usage:</div>
        <div class="detail-item-content">{detailed_food['Sample Recipe/Usage']}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("close_details"):
        st.session_state.detailed_food_id = None
        del st.session_state["close_details"]
        st.rerun() # Rerun to hide the detailed food section
