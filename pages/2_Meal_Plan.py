import streamlit as st
import pandas as pd
import random
import json # For parsing LLM response
import requests # For making HTTP requests to LLM API

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NourishWell: Meal Plan",
    layout="wide",
    initial_sidebar_state="collapsed" # No sidebar needed on meal plan page
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
    .stTextInput {
        border-radius: 0.5rem;
        border: 1px solid #E2E8F0;
        background-color: #F8FAFC;
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
if 'generated_meal_plan_llm' not in st.session_state: # Renamed to avoid conflict with previous simple plan
    st.session_state.generated_meal_plan_llm = None


# --- LLM API Call Function ---
def get_gemini_meal_plan(selected_foods_df, api_key):
    if not api_key:
        st.error("API Key not found. Please set your Google API Key in Streamlit secrets.toml.")
        return "Error: API Key not configured."

    food_details_list = selected_foods_df.to_dict(orient='records')

    # Constructing a detailed prompt for the LLM
    prompt = f"""
    You are an expert nutritionist specializing in anti-inflammatory diets for women's health.
    Based ONLY on the following list of anti-inflammatory foods selected by the user, create a personalized one-day meal plan.
    The meal plan should include Breakfast, Lunch, Dinner, and optionally 1-2 snacks.
    For each meal, suggest a specific dish or usage idea that clearly incorporates 1-3 of the provided foods.
    Briefly explain *why* the suggested meal is beneficial for women's anti-inflammatory needs, referencing the anti-inflammatory properties of the ingredients from the list.
    Be creative and practical, using the 'Sample Recipe/Usage' column from the data where appropriate, but feel free to combine ideas.
    Focus on balancing meals and ensuring they are genuinely anti-inflammatory.
    The output should be in a clear, easy-to-read Markdown format.

    Selected Anti-Inflammatory Foods (with their properties):
    {json.dumps(food_details_list, indent=2)}

    Please generate the meal plan:
    """

    headers = {
        'Content-Type': 'application/json'
    }
    # Using gemini-2.0-flash as specified by general instructions
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.7, # Moderate creativity
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 1500 # Sufficient length for a detailed plan
        }
    }

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        result = response.json()

        if result and 'candidates' in result and result['candidates']:
            generated_text = result['candidates'][0]['content']['parts'][0]['text']
            return generated_text
        else:
            return "No meal plan could be generated by the AI at this time. Please try again or adjust your selected foods."
    except requests.exceptions.RequestException as e:
        return f"Error communicating with AI: {e}"
    except json.JSONDecodeError:
        return "Error: Could not decode AI response (invalid JSON)."
    except KeyError:
        return "Error: Unexpected AI response format."


# --- HEADER ---
st.title("🍽️ Your Custom Meal Plan")
st.markdown("Review your selected foods and generate a personalized meal plan suggestion using AI.")

# --- NAVIGATION BUTTONS ---
nav_cols = st.columns(2)
with nav_cols[0]:
    st.page_link("pages/1_Food_Discovery.py", label="← Back to Food Discovery", icon="⬅️", type="secondary")
with nav_cols[1]:
    if st.button("Start Over (Clear All)", type="secondary", use_container_width=True):
        st.session_state.selected_foods_for_plan = []
        st.session_state.generated_meal_plan_llm = None
        st.toast("Your plan has been reset! 👋", icon="🗑️")
        st.rerun()

st.markdown("---") # Separator

# --- DISPLAY SELECTED FOODS ---
if not st.session_state.selected_foods_for_plan:
    st.info("Your meal plan is currently empty. Go to 'Food Discovery' to add some foods!")
else:
    plan_df = df[df['Food Item'].isin(st.session_state.selected_foods_for_plan)]
    
    st.subheader("Foods Selected for Your Plan:")
    
    # Display selected foods in a clean table format
    st.dataframe(
        plan_df[['Food Item', 'Category', 'Score (0–10)', 'Best For', 'Sample Recipe/Usage']],
        hide_index=True,
        use_container_width=True,
        column_config={
            "Food Item": st.column_config.TextColumn("Food Item", width="medium"),
            "Category": st.column_config.TextColumn("Category", width="small"),
            "Score (0–10)": st.column_config.NumberColumn("Score", format="%d", width="small"),
            "Best For": st.column_config.TextColumn("Benefit for Women", width="medium"),
            "Sample Recipe/Usage": st.column_config.TextColumn("Usage Idea", width="large"),
        }
    )

    # Allow removing items
    foods_to_remove = st.multiselect(
        "Select foods to remove from your plan:",
        options=st.session_state.selected_foods_for_plan,
        key='remove_foods_multiselect'
    )
    if foods_to_remove:
        if st.button("Remove Selected Foods", type="secondary"):
            for food_item in foods_to_remove:
                if food_item in st.session_state.selected_foods_for_plan:
                    st.session_state.selected_foods_for_plan.remove(food_item)
            st.session_state.generated_meal_plan_llm = None # Reset generated plan if foods change
            st.toast("Foods removed. Plan updated. 👍", icon="✅")
            st.rerun()

    st.markdown("---")

    # --- GENERATE MEAL PLAN BUTTON (LLM Integration) ---
    st.subheader("Generate Personalized Meal Plan")
    st.markdown("<p style='font-size: 1.1rem; color: #475569;'>Click below to get an AI-powered meal plan suggestion based on your selected anti-inflammatory foods.</p>", unsafe_allow_html=True)
    
    if st.button("Generate Custom Meal Plan with AI", type="primary", use_container_width=True):
        if len(st.session_state.selected_foods_for_plan) > 0:
            with st.spinner("Generating your personalized meal plan... this might take a moment."):
                google_api_key = st.secrets["GOOGLE_API_KEY"] # Access API key from secrets
                generated_plan_text = get_gemini_meal_plan(plan_df, google_api_key)
                st.session_state.generated_meal_plan_llm = generated_plan_text
            st.toast("Meal plan generated! 🎉", icon="✨")
        else:
            st.warning("Please add some foods to your plan first to generate a meal plan!")
        st.rerun() # Rerun to display the generated plan

    # --- DISPLAY GENERATED MEAL PLAN ---
    if st.session_state.generated_meal_plan_llm:
        st.subheader("Your AI-Suggested Daily Plan:")
        st.markdown('<div class="meal-plan-section">', unsafe_allow_html=True)
        st.markdown(st.session_state.generated_meal_plan_llm) # LLM output is already Markdown
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        
        # --- COPY TO CLIPBOARD BUTTON ---
        copy_text_area = st.text_area("Copyable Plan Text:", st.session_state.generated_meal_plan_llm, height=200, label_visibility="collapsed")
        
        copy_button_label = "Copy Plan to Clipboard"
        st.markdown(
            f"""
            <button
                onclick="navigator.clipboard.writeText(`{copy_text_area.replace('`', '\\`')}`); alert('Meal plan copied to clipboard!');"
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
                {copy_button_label}
            </button>
            """,
            unsafe_allow_html=True
        )

st.caption("Developed by Hanif | Powered by Streamlit")
