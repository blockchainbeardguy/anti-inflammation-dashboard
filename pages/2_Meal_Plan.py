import streamlit as st
import pandas as pd
import random # For randomizing meal plan suggestions

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NourishWell: Meal Plan",
    layout="wide",
    initial_sidebar_state="collapsed" # Sidebar not needed on meal plan page
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

    /* Food card specific styling (not directly used on this page, but kept for general app consistency) */
    .food-card {
        background-color: white;
        border-radius: 0.75rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.2s ease-in-out;
        margin-bottom: 1.5rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border: 1px solid #f0f4f8;
    }
    .food-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
    }
    .food-card-score {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0d9488;
        text-align: right;
        line-height: 1;
    }
    .food-card-name {
        font-size: 1.625rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    .food-card-category {
        font-size: 0.875rem;
        color: #64748B;
        margin-top: 0.25rem;
        font-weight: 500;
    }
    .food-card-why {
        font-size: 0.95rem;
        color: #475569;
        margin-top: 1rem;
        flex-grow: 1;
        line-height: 1.4;
    }
    .food-card-buttons {
        display: flex;
        gap: 0.75rem;
        margin-top: 1.5rem;
        justify-content: space-between;
    }
    .food-card-buttons button {
        flex-grow: 1;
    }

    /* Detail Card styling (simulated modal) (not directly used on this page) */
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

# --- SESSION STATE INITIALIZATION (Ensure consistency with Food Discovery) ---
if 'selected_foods_for_plan' not in st.session_state:
    st.session_state.selected_foods_for_plan = []
if 'generated_meal_plan' not in st.session_state:
    st.session_state.generated_meal_plan = []


# --- HEADER ---
st.title("🍽️ Your Custom Meal Plan")
st.markdown("Review your selected foods and generate a personalized meal plan suggestion.")

# --- NAVIGATION BUTTONS ---
nav_cols = st.columns(2)
with nav_cols[0]:
    st.page_link("pages/1_Food_Discovery.py", label="← Back to Food Discovery", icon="⬅️")
with nav_cols[1]:
    if st.button("Start Over (Clear All)", type="secondary", use_container_width=True):
        st.session_state.selected_foods_for_plan = []
        st.session_state.generated_meal_plan = []
        st.toast("Your plan has been reset!", icon="🗑️")
        st.rerun()

st.markdown("---") # Separator

# --- DISPLAY SELECTED FOODS ---
if not st.session_state.selected_foods_for_plan:
    st.info("Your meal plan is currently empty. Go to 'Food Discovery' to add some foods!")
else:
    plan_df = df[df['Food Item'].isin(st.session_state.selected_foods_for_plan)]
    
    st.subheader("Selected Foods for Your Plan:")
    
    # Display selected foods as small, clean list items or cards
    for food_item in st.session_state.selected_foods_for_plan:
        food_row = plan_df[plan_df['Food Item'] == food_item].iloc[0]
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; background-color: #F8FAFC; border-radius: 0.5rem; padding: 0.75rem 1rem; margin-bottom: 0.5rem; border: 1px solid #E2E8F0;">
            <span style="font-weight: 600; color: #1E293B;">{food_item}</span>
            <span style="font-size: 0.9rem; color: #64748B;">Score: {food_row['Score (0–10)']}/10</span>
            {st.button("Remove", key=f"remove_from_plan_{food_item}", args=(food_item,), type="secondary", help=f"Remove {food_item} from plan")}
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.get(f"remove_from_plan_{food_item}"):
            st.session_state.selected_foods_for_plan.remove(food_item)
            st.toast(f"'{food_item}' removed from plan. 👋", icon="🗑️")
            del st.session_state[f"remove_from_plan_{food_item}"]
            st.rerun()

    st.markdown("---")

    # --- GENERATE MEAL PLAN BUTTON ---
    if st.button("Generate My Daily Meal Plan", type="primary", use_container_width=True):
        st.session_state.generated_meal_plan = []
        # Simple meal plan generation: assign random selected foods/recipes to meals
        meals = ["Breakfast", "Lunch", "Dinner", "Snack"] # Added Snack
        
        # Get all recipe ideas from selected foods, ensure uniqueness if multiple foods have same idea
        available_recipes = plan_df['Sample Recipe/Usage'].dropna().unique().tolist()
        
        if not available_recipes:
            st.warning("No sample recipes available for your selected foods to generate a meal plan. Try adding foods with recipe suggestions.")
        else:
            for meal_time in meals:
                # Randomly pick a recipe from the available ones
                if available_recipes:
                    chosen_recipe = random.choice(available_recipes)
                    st.session_state.generated_meal_plan.append({
                        "meal_time": meal_time,
                        "recipe_idea": chosen_recipe
                    })
                else: # Fallback if for some reason available_recipes becomes empty during loop
                    st.session_state.generated_meal_plan.append({
                        "meal_time": meal_time,
                        "recipe_idea": "No suitable recipe idea available for this meal."
                    })
            st.toast("Meal plan generated! 🥗✨", icon="🎉")
        st.rerun() # Rerun to display the generated plan

    # --- DISPLAY GENERATED MEAL PLAN ---
    if st.session_state.generated_meal_plan:
        st.subheader("Your Suggested Daily Plan:")
        st.markdown('<div class="meal-plan-section">', unsafe_allow_html=True)
        for meal in st.session_state.generated_meal_plan:
            st.markdown(f"""
            <div class="meal-plan-item">
                <h4 style="color: #0d9488; margin-bottom: 0.5rem; font-size: 1.3rem;">{meal['meal_time']}</h4>
                <p style="color: #475569; font-size: 1rem;">{meal['recipe_idea']}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        
        # Combined Plan Insights: Nutrients and Cautions
        insight_cols = st.columns(2)
        with insight_cols[0]:
            st.subheader("Nutrients Covered:")
            nutrients = set()
            for val in plan_df['Key Vitamins & Minerals']:
                if pd.notna(val):
                    for n in str(val).split(','):
                        nutrients.add(n.strip())
            if nutrients:
                st.write(", ".join(sorted(nutrients)))
            else:
                st.info("No specific nutrients listed for selected foods.")

        with insight_cols[1]:
            st.subheader("Important Cautions:")
            cautions = set()
            for val in plan_df['Cautions']:
                if pd.notna(val) and val.strip() != "None specific." and val.strip() != "":
                    cautions.add(val.strip())
            if cautions:
                for caution in sorted(cautions):
                    st.warning(f"⚠️ {caution}")
            else:
                st.info("No major cautions listed for the selected foods. Always consult a healthcare professional.")

        # --- COPY TO CLIPBOARD BUTTON ---
        plan_text = "Your Daily Meal Plan Suggestion (from NourishWell):\n\n"
        for meal in st.session_state.generated_meal_plan:
            plan_text += f"{meal['meal_time']}: {meal['recipe_idea']}\n"
        plan_text += "\n--- Always consult a healthcare professional before making significant dietary changes. ---"
        
        st.markdown(
            f"""
            <button 
                onclick="navigator.clipboard.writeText(`{plan_text.replace('`', '\\`')}`); alert('Meal plan copied to clipboard!');"
                style="
                    background-color: #10B981; /* Green-500 */
                    color: white;
                    border-radius: 0.75rem;
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

st.caption("Developed by Hanif | Powered by Streamlit")
