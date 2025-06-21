import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NourishWell: Home",
    layout="centered", # Centered layout for a minimalist home page
    initial_sidebar_state="collapsed" # Sidebar not needed on home
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
        padding: 1rem 2rem; /* Larger padding for main CTA */
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: none;
        font-size: 1.25rem; /* Larger font for CTA */
    }
    .stButton>button:hover {
        background-color: #0f766e; /* Darker Teal */
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
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
        padding: 0.75rem 1.25rem; /* Standard padding */
        font-size: 1rem;
    }
    .stButton button[kind="secondary"]:hover {
        background-color: #cbd5e1; /* Slate-300 */
        color: #1e293b; /* Slate-900 */
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Food card specific styling (minimal, mainly for Detail Modal) */
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

    /* Meal Plan Section styling */
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

    /* Custom container for home page */
    .home-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 80vh; /* Make it vertically centered */
        text-align: center;
        padding: 2rem;
    }
    .home-headline {
        font-size: 3.5rem; /* Larger for impact */
        font-weight: 700;
        color: #0d9488; /* Teal for main message */
        margin-bottom: 1.5rem;
        line-height: 1.1;
    }
    .home-subheadline {
        font-size: 1.5rem;
        color: #475569;
        margin-bottom: 2.5rem;
        max-width: 700px;
        line-height: 1.4;
    }

    /* Streamlit widgets for consistent look */
    .stMultiSelect, .stSlider, .stTextInput {
        margin-bottom: 0.5rem;
    }
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# --- HOME PAGE CONTENT ---
st.markdown("""
<div class="home-container">
    <h1 class="home-headline">NourishWell: Your Guide to Anti-Inflammatory Eating 🌿</h1>
    <p class="home-subheadline">
        Discover foods that empower women's health. Personalize your diet, manage inflammation, and thrive at every life stage.
    </p>
    <div style="margin-top: 2rem;">
        <a href="/Food_Discovery" target="_self">
            <button class="stButton" style="min-width: 250px;">
                <span>Start Exploring Foods</span>
            </button>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# Optional: How It Works Section
st.markdown("""
<div style="text-align: center; padding: 4rem 2rem; background-color: #F0F4F8; border-radius: 1rem; margin-top: 4rem;">
    <h2 style="color: #0d9488;">How It Works</h2>
    <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 250px; max-width: 350px; padding: 1.5rem; background-color: white; border-radius: 0.75rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <h3 style="color: #1E293B; margin-bottom: 0.5rem;">1. Discover</h3>
            <p style="color: #475569; font-size: 0.95rem;">Filter our extensive database of anti-inflammatory foods by category or specific health concerns.</p>
        </div>
        <div style="flex: 1; min-width: 250px; max-width: 350px; padding: 1.5rem; background-color: white; border-radius: 0.75rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <h3 style="color: #1E293B; margin-bottom: 0.5rem;">2. Select</h3>
            <p style="color: #475569; font-size: 0.95rem;">Add your favorite and most beneficial foods to your personalized meal plan with a single click.</p>
        </div>
        <div style="flex: 1; min-width: 250px; max-width: 350px; padding: 1.5rem; background-color: white; border-radius: 0.75rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <h3 style="color: #1E293B; margin-bottom: 0.5rem;">3. Plan</h3>
            <p style="color: #475569; font-size: 0.95rem;">Generate a custom meal plan with recipe ideas and essential nutritional insights for your selections.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
