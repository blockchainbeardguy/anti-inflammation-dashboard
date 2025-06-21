import streamlit as st
import pandas as pd
import random # For randomizing meal plan suggestions

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NourishWell: Anti-Inflammatory Food Guide for Women",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSV DATA LOADING ---
# Assuming 'anti_inflammatory_foods.csv' is in the same directory as app.py
try:
    df = pd.read_csv('anti_inflammatory_foods.csv', encoding='utf-8-sig')
except UnicodeDecodeError:
    df = pd.read_csv('anti_inflammatory_foods.csv', encoding='ISO-8859-1')
except FileNotFoundError:
    st.error("Error: 'anti_inflammatory_foods.csv' not found. Please ensure the CSV file is in the same directory as this script.")
    st.stop() # Stop the app execution if file is not found

# --- SESSION STATE INITIALIZATION ---
if 'selected_foods_for_plan' not in st.session_state:
    st.session_state.selected_foods_for_plan = []
if 'detailed_food_id' not in st.session_state:
    st.session_state.detailed_food_id = None
if 'generated_meal_plan' not in st.session_state:
    st.session_state.generated_meal_plan = []

# --- CUSTOM CSS FOR MODERN UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="st-emotion"] {
        font-family: 'Inter', sans-serif;
        color: #334155; /* Slate-700 for text */
    }

    .stApp {
        background-color: #FEFBF6; /* Warm neutral background */
        padding-top: 1rem; /* Add some padding at the top */
    }

    h1, h2, h3, h4, h5, h6 {
        color: #1E293B; /* Slate-900 for headings */
    }

    /* Streamlit button overrides */
    .stButton>button {
        background-color: #0d9488; /* Teal-600 */
        color: white;
        border-radius: 0.5rem;
        padding: 0.75rem 1.25rem;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: none;
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

    /* Secondary button style (e.g., View Details) */
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
    
    /* Multiselect and slider styling */
    .stMultiSelect, .stSlider {
        margin-bottom: 1rem;
    }

    /* Card styling */
    .food-card {
        background-color: white;
        border-radius: 0.75rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); /* Lighter shadow */
        transition: all 0.2s ease-in-out;
        margin-bottom: 1.5rem; /* More space between cards */
        height: 100%;
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

    /* Detail Card styling (simulated modal) */
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
        background-color: #ECFDF5; /* Green-50 */
        color: #047857; /* Green-700 */
        padding: 0.3rem 0.9rem; /* More padding */
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 0.6rem;
        margin-bottom: 0.6rem;
        border: 1px solid #10B981;
    }

    /* Meal Plan Section */
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
</style>
""", unsafe_allow_html=True)


# --- HEADER SECTION ---
st.title("NourishWell: Anti-Inflammatory Food Guide for Women 🌿")
st.markdown("""
<p style='font-size: 1.15rem; color: #475569;'>
    Unlock the power of nutrition to enhance your well-being. Explore anti-inflammatory foods tailored for women's health needs, from hormonal balance to bone health, and build your personalized meal plan.
</p>
""", unsafe_allow_html=True)

# --- MAIN CONTENT LAYOUT ---
# Using columns for main content vs. detailed view / meal plan
main_col, side_info_col = st.columns([2.5, 1.5]) # Adjust width ratio as needed

with main_col:
    st.header("1. Discover Your Foods")
    st.markdown("Use the filters on the left sidebar to find foods that match your health goals.")

    # --- FILTERING LOGIC ---
    all_categories = df['Category'].dropna().unique()
    all_flags = sorted({flag.strip() for row in df['Flags (Female Health Issues)'].dropna() for flag in str(row).split(',') if flag.strip()})

    with st.sidebar:
        st.header("🔍 Filter Foods")
        selected_categories_filter = st.multiselect(
            "Food Categories:",
            options=all_categories,
            default=[],
            help="Select one or more categories to narrow down foods."
        )

        selected_flags_filter = st.multiselect(
            "Health Concerns:",
            options=all_flags,
            default=[],
            help="Choose specific health issues you want to address."
        )

        min_score_filter = st.slider(
            "Minimum Anti-Inflammatory Score:",
            min_value=0,
            max_value=10,
            value=0,
            help="Only show foods with a score equal to or higher than this value."
        )

        if st.button("Reset Filters", type="secondary", use_container_width=True):
            st.session_state.selected_categories_filter = []
            st.session_state.selected_flags_filter = []
            st.session_state.min_score_filter = 0
            st.session_state.detailed_food_id = None # Also reset detailed view
            st.experimental_rerun() # Use rerun to clear filters visually

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
        # Create columns for the grid layout in the main section
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
                    del st.session_state[f"view_{food['Food Item']}"] # Clear button state
                    st.rerun() # Rerun to display the detailed food section

                if st.session_state.get(f"add_{food['Food Item']}"):
                    if food['Food Item'] not in st.session_state.selected_foods_for_plan:
                        st.session_state.selected_foods_for_plan.append(food['Food Item'])
                        st.toast(f"'{food['Food Item']}' added to your plan! 🎉", icon="✅")
                    else:
                        st.toast(f"'{food['Food Item']}' is already in your plan!", icon="ℹ️")
                    del st.session_state[f"add_{food['Food Item']}"] # Clear button state
                    st.rerun() # Rerun to update the plan section

with side_info_col:
    # --- DETAILED FOOD INFORMATION (SIMULATED MODAL/EXPANDABLE PANEL) ---
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

    # --- YOUR CUSTOM ANTI-INFLAMMATORY PLAN BUILDER ---
    st.header("2. Your Custom Meal Plan")
    st.markdown("<p style='font-size: 1.1rem; color: #475569;'>Build your personalized anti-inflammatory meal plan here by adding foods from the 'Discover' section.</p>", unsafe_allow_html=True)

    if not st.session_state.selected_foods_for_plan:
        st.info("Your plan is empty. Add foods to get started!")
    else:
        plan_df = df[df['Food Item'].isin(st.session_state.selected_foods_for_plan)]
        
        st.subheader("Foods in Your Plan:")
        
        # Display selected foods as small cards or list items
        for food_item in st.session_state.selected_foods_for_plan:
            food_row = plan_df[plan_df['Food Item'] == food_item].iloc[0]
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; background-color: #F8FAFC; border-radius: 0.5rem; padding: 0.75rem 1rem; margin-bottom: 0.5rem; border: 1px solid #E2E8F0;">
                <span style="font-weight: 600; color: #1E293B;">{food_item}</span>
                <span style="font-size: 0.9rem; color: #64748B;">Score: {food_row['Score (0–10)']}/10</span>
                {st.button("Remove", key=f"remove_from_plan_{food_item}", args=(food_item,), type="secondary")}
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.get(f"remove_from_plan_{food_item}"):
                st.session_state.selected_foods_for_plan.remove(food_item)
                st.toast(f"'{food_item}' removed from plan.", icon="🗑️")
                del st.session_state[f"remove_from_plan_{food_item}"]
                st.rerun()

        st.markdown("---")
        
        # Buttons for meal plan actions
        plan_buttons_cols = st.columns(2)
        with plan_buttons_cols[0]:
            if st.button("Generate Meal Plan", use_container_width=True):
                if len(st.session_state.selected_foods_for_plan) > 0:
                    st.session_state.generated_meal_plan = []
                    # Simple meal plan generation: assign random selected foods to meals
                    meals = ["Breakfast", "Lunch", "Dinner"]
                    # Get all recipe ideas from selected foods
                    available_recipes = plan_df['Sample Recipe/Usage'].dropna().tolist()
                    
                    if not available_recipes:
                        st.warning("No sample recipes available for your selected foods to generate a meal plan.")
                    else:
                        for meal_time in meals:
                            # Randomly pick a recipe from the available ones
                            if available_recipes:
                                chosen_recipe = random.choice(available_recipes)
                                st.session_state.generated_meal_plan.append({
                                    "meal_time": meal_time,
                                    "recipe_idea": chosen_recipe
                                })
                            else:
                                st.session_state.generated_meal_plan.append({
                                    "meal_time": meal_time,
                                    "recipe_idea": "No suitable recipe idea available."
                                })
                        st.toast("Meal plan generated! 🥗", icon="✨")
                else:
                    st.warning("Please add some foods to your plan first!")
                st.rerun()

        with plan_buttons_cols[1]:
            if st.button("Clear All Foods", type="secondary", use_container_width=True):
                st.session_state.selected_foods_for_plan = []
                st.session_state.generated_meal_plan = []
                st.toast("Your entire plan has been cleared!")
                st.rerun()
        
        # Display Generated Meal Plan
        if st.session_state.generated_meal_plan:
            st.subheader("Your Daily Meal Plan Suggestion:")
            st.markdown('<div class="meal-plan-section">', unsafe_allow_html=True)
            for meal in st.session_state.generated_meal_plan:
                st.markdown(f"""
                <div class="meal-plan-item">
                    <h4 style="color: #0d9488; margin-bottom: 0.5rem;">{meal['meal_time']}</h4>
                    <p style="color: #475569;">{meal['recipe_idea']}</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Option to copy plan to clipboard (requires unsafe_allow_html=True and simple JS)
            plan_text = "Your Daily Meal Plan:\n\n"
            for meal in st.session_state.generated_meal_plan:
                plan_text += f"{meal['meal_time']}: {meal['recipe_idea']}\n"
            
            st.markdown(
                f"""
                <button 
                    onclick="navigator.clipboard.writeText(`{plan_text.replace('`', '\\`')}`); alert('Meal plan copied to clipboard!');"
                    style="
                        background-color: #10B981; /* Green-500 */
                        color: white;
                        border-radius: 0.5rem;
                        padding: 0.75rem 1.25rem;
                        font-weight: 600;
                        transition: all 0.2s ease-in-out;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border: none;
                        cursor: pointer;
                        margin-top: 1rem;
                        width: 100%;
                    "
                >
                    Copy Plan to Clipboard
                </button>
                """,
                unsafe_allow_html=True
            )

# --- VISUAL DATA INSIGHTS (at the bottom, less prominent) ---
st.markdown("---") # Separator
st.header("3. Data Insights")
st.markdown("A quick overview of the food dataset characteristics.")

insight_cols = st.columns(2)

with insight_cols[0]:
    st.subheader("Top 10 Anti-Inflammatory Foods by Score")
    # Streamlit's native bar chart is good for this
    st.bar_chart(df.sort_values(by='Score (0–10)', ascending=False).head(10).set_index('Food Item')['Score (0–10)'])

with insight_cols[1]:
    st.subheader("Food Category Distribution")
    # Streamlit's native pie chart is good for this
    st.pie_chart(df['Category'].value_counts())

st.subheader("Health Concern Coverage")
st.markdown("<p style='font-size: 0.95rem; color: #475569;'>Counts how many foods are beneficial for each health issue.</p>", unsafe_allow_html=True)
health_flag_counts = df['Flags (Female Health Issues)'].dropna().apply(lambda x: [f.strip() for f in str(x).split(',')]).explode().value_counts()
st.bar_chart(health_flag_counts) # Bar chart is the closest native to a polar area for counts

st.caption("Developed by Hanif | Powered by Streamlit")
