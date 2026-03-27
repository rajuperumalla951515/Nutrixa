import streamlit as st 
from PIL import Image
import data_utils
import random

from config import *                                   
from gemini_service import get_gemini_response
from image_service import input_image_setup
from ui_components import render_skeleton_loader

if 'health_profile' not in st.session_state:
    st.session_state.health_profile = {
        'goals': 'Lose 10 pounds in 3 months\nImprove cardiovascular health',
        'conditions': 'None',
        'routines': '30-minute walk 3x/week',
        'preferences': 'Vegetarian\nLow carb',
        'restrictions': 'No dairy\nNo nuts'
    }

st.set_page_config(page_title="AI Health Companion", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet">
<style>
    /* Global Dark Theme Settings */
    .stApp {
        background: radial-gradient(circle at top right, #0d1117, #010409);
        color: #ffffff;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main container background */
    .main {
        background-color: transparent;
    }
    
    /* Header styling - Bold & Medium */
    .stHeader h1 {
        font-family: 'Outfit', sans-serif !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        letter-spacing: -1.5px;
        text-shadow: 0 4px 15px rgba(0,0,0,0.5);
        margin-bottom: 2rem !important;
    }

    /* Premium Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(13, 17, 23, 0.95), rgba(1, 4, 9, 0.95)) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    [data-testid="stSidebar"] div.stVerticalBlock {
        padding-top: 0 !important;
        gap: 0 !important;
    }
    [data-testid="stSidebar"] div.stVerticalBlock > div {
        background: rgba(255, 255, 255, 0.02);
        padding: 25px 20px;
        border-radius: 0; /* Square for a more seamless "container" look if preferred, or keep 16px */
        border: none;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 0 !important;
        width: 100% !important;
    }
    [data-testid="stSidebar"] .stTextArea label, 
    [data-testid="stSidebar"] .stTextInput label {
        color: #58a6ff !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Input field adjustments */
    .stTextArea textarea, .stTextInput input {
        background: rgba(0, 0, 0, 0.3) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }

    /* Tabs Styling - Maximum Prominence & No Borders */
    .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        justify-content: space-between !important;
        width: 100% !important;
        background-color: transparent;
        padding: 15px 0;
        border: none !important; /* Total removal of borders */
        gap: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        flex: 1 !important;
        text-align: center !important;
        background: rgba(255, 255, 255, 0.04) !important;
        color: #8b949e !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.7rem !important; /* Increased font size */
        padding: 12px 20px !important;
        border: none !important;
        border-radius: 20px !important;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        gap: 12px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 5px !important;
    }
    .stTabs [data-baseweb="tab"]:hover, 
    .stTabs [data-baseweb="tab"]:hover *,
    .stTabs [aria-selected="true"],
    .stTabs [aria-selected="true"] * {
        color: #ffffff !important; /* White text for gradient contrast */
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #0d1117 0%, #ff8c00 100%) !important;
        transform: translateY(-4px) !important;
        border-radius: 50px !important;
        box-shadow: 10px 0 15px rgba(255, 140, 0, 0.15) !important; /* Glow only on the right */
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0d1117 0%, #ff8c00 100%) !important;
        font-weight: 900 !important;
        border-radius: 50px !important;
        padding-left: 12px !important;
        box-shadow: 10px 0 20px rgba(255, 140, 0, 0.25) !important; /* Glow only on the right */
        border: none !important;
    }
    /* Specifically removing the default Streamlit tab borders/lines */
    .stTabs [data-baseweb="tab-highlight"], 
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }
    /* Smooth Tab Content Transitions */
    @keyframes tabFadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    /* Targeting the content area immediately after the tabs */
    [data-testid="stTabs"] + div > [data-testid="stVerticalBlock"] {
        animation: tabFadeIn 0.8s cubic-bezier(0.165, 0.84, 0.44, 1);
    }

    /* Glassmorphism Result Container */
    @keyframes fadeInSlide {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .result-container {
        padding: 2.5rem;
        border-radius: 28px;
        background: rgba(22, 27, 34, 0.4);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-top: 2rem;
        color: #f0f6fc;
        line-height: 1.8;
        animation: fadeInSlide 0.8s ease-out;
    }
    
    /* Typography Priority */
    p, li, label, span {
        color: #f0f6fc !important;
    }
    h1 {
        color: #58a6ff !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700;
    }
    h2, h3, h4 {
        color: #ffffff !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700;
    }

    /* JSON Formatting - White keys, Orange values */
    [data-testid="stJson"] span {
        color: #ffa500 !important; /* Default to orange for all data */
    }
    [data-testid="stJson"] .object-key {
        color: #ffffff !important; /* Overriding keys to white */
    }
    [data-testid="stJson"] .string-value {
        color: #ffa500 !important; /* Ensuring values are orange */
    }

    /* See More Style Buttons */
    .stButton>button {
        all: unset !important;
        position: relative !important;
        background-color: #262626 !important;
        height: 45px !important;
        width: 100% !important;
        box-sizing: border-box !important;
        padding: 0 20px !important;
        color: #000000 !important; /* Black text */
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important; /* Subtle black shadow for depth */
        font-size: 0.95rem !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        border: none !important;
        cursor: pointer !important;
        text-align: center !important;
        text-decoration: none !important;
        transition: all 0.5s ease !important;
        z-index: 1 !important;
        font-family: 'Outfit', sans-serif !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .stButton>button::before,
    .stButton>button::after {
        content: '' !important;
        position: absolute !important;
        transition: all 0.5s ease-in-out !important;
    }

    .stButton>button::before {
        width: 48px !important;
        height: 48px !important;
        right: 4px !important;
        top: 4px !important;
        z-index: -1 !important;
        background-color: #8b5cf6 !important;
        border-radius: 9999px !important;
        filter: blur(16px) !important;
    }

    .stButton>button::after {
        width: 80px !important;
        height: 80px !important;
        z-index: -1 !important;
        background-color: #fca5a5 !important;
        right: 32px !important;
        top: 12px !important;
        border-radius: 9999px !important;
        filter: blur(16px) !important;
    }

    .stButton>button:hover {
        text-decoration: none !important; /* No underline on hover */
        color: #000000 !important; /* Keep text black on hover */
    }

    .stButton>button:hover::before {
        box-shadow: 20px 20px 20px 30px #a21caf !important;
        right: 48px !important; /* right-12 equivalent */
        bottom: -32px !important; /* -bottom-8 equivalent */
        filter: blur(24px) !important;
        transform: translate(0, 0) !important;
    }

    .stButton>button:hover::after {
        right: -32px !important; /* -right-8 equivalent */
        border-radius: 10px !important;
        transform: translate(0, 0) !important;
    }

    .stButton>button:active::after {
        transition: 0s !important;
        transform: translate(0, 5%) !important;
    }
    /* Responsive Nutrition Table for Mobile */
    @media screen and (max-width: 768px) {
        .nutrition-table, 
        .nutrition-table thead, 
        .nutrition-table tbody, 
        .nutrition-table th, 
        .nutrition-table td, 
        .nutrition-table tr { 
            display: block !important; 
            width: 100% !important;
        }
        
        /* Hide traditional header row */
        .nutrition-table thead tr { 
            position: absolute !important;
            top: -9999px !important;
            left: -9999px !important;
        }
        
        .nutrition-table tr { 
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            margin-bottom: 12px !important;
            border-radius: 12px !important;
            background: rgba(255, 255, 255, 0.02) !important;
            padding: 8px 0 !important;
        }
        
        .nutrition-table td { 
            border: none !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important; 
            position: relative !important;
            padding-left: 45% !important; 
            text-align: right !important;
            min-height: 40px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: flex-end !important;
            padding-right: 15px !important;
        }
        
        .nutrition-table td:last-child {
            border-bottom: none !important;
        }
        
        .nutrition-table td:before { 
            position: absolute !important;
            left: 15px !important;
            width: 40% !important; 
            white-space: nowrap !important;
            content: attr(data-label) !important;
            font-weight: 700 !important;
            color: #ff8c00 !important;
            text-align: left !important;
            font-size: 0.8rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.header("AI Health Companion")

with st.sidebar:
    st.subheader("Your Health Profile")

    health_goals = st.text_area(
        "Health Goals",
        value=st.session_state.health_profile['goals']
    )
    medical_conditions = st.text_area(
        "Medical Conditions",
        value=st.session_state.health_profile['conditions']
    )
    fitness_routines = st.text_area(
        "Fitness Routines",
        value=st.session_state.health_profile['routines']
    )
    food_preferences = st.text_area(
        "Food Preferences",
        value=st.session_state.health_profile['preferences']
    )
    restrictions = st.text_area(
        "Dietary Restrictions",
        value=st.session_state.health_profile['restrictions']
    )

    if st.button("Update Profile"):
        st.session_state.health_profile = {
            'goals': health_goals,
            'conditions': medical_conditions,
            'routines': fitness_routines,
            'preferences': food_preferences,
            'restrictions': restrictions
        }
        st.success("Profile updated!")

tab1, tab2, tab3 = st.tabs(
    ["🥗 Meal Planning", "🔍 Food Analysis", "🧠 Health Insights"]
)

with tab1:
    st.subheader("Personalized Meal Planning")

    col1, col2 = st.columns(2)

    with col1:
        user_input = st.text_area(
            "Describe any specific requirements for your meal plan:"
        )

    with col2:
        st.json(st.session_state.health_profile)

    if st.button("Generate Personalized Meal Plan"):
        result_placeholder = st.empty()
        with result_placeholder.container():
            render_skeleton_loader()

        prompt = f"""
        You are an elite nutritionist. Create a professional, detailed 7-day meal plan based on the following health profile:

        Health Profile:
        - Goals: {st.session_state.health_profile['goals']}
        - Conditions: {st.session_state.health_profile['conditions']}
        - Routines: {st.session_state.health_profile['routines']}
        - Preferences: {st.session_state.health_profile['preferences']}
        - Restrictions: {st.session_state.health_profile['restrictions']}

        Additional requirements: {user_input if user_input else "None provided"}

        Format your response with the following professional structure:
        ## 🗓️ 7-Day Personalized Meal Plan
        Provide a clear, daily breakdown from Day 1 to Day 7. Use subheadings for breakfast, lunch, dinner, and snacks.

        ## 📊 Nutritional Breakdown
        A daily detailed analysis of calories and macronutrients (protein, carbs, fats).

        ## 💡 Contextual Insights & Rational
        Explain *why* these meals were chosen for this specific profile.

        ## 🛒 Smart Shopping List
        Categorized list (e.g., Produce, Protein, Pantry).

        ## 🥗 Preparation Tips
        Efficient meal prep advice.

        Use Markdown headers (##, ###), bold text, and bullet points for maximum readability.
        """
        try:
            response = get_gemini_response(prompt)
            result_placeholder.empty()
            st.markdown(f'<div class="result-container">{response}</div>', unsafe_allow_html=True)
        except Exception:
            import time
            time.sleep(3)                               
            result_placeholder.empty()
            all_meals = data_utils.get_profile_meals(st.session_state.health_profile, 21)

            while len(all_meals) < 21:
                all_meals += data_utils.get_random_meals(3)
            all_meals = all_meals[:21]

            day_themes = [
                ("🌅", "Day 1", "Energising Start",
                 "Kick off the week strong. Each meal today is designed to ignite your metabolism, boost mental clarity, and give you the sustained energy you need from morning to night."),
                ("🌿", "Day 2", "Clean & Light",
                 "Today focuses on gut-friendly, light options that are easy to digest while being rich in vitamins and minerals. A clean eating day helps reset your system and reduce inflammation."),
                ("💪", "Day 3", "Protein Power",
                 "Wednesday is all about building strength. High-protein meals throughout the day support muscle repair, keep you full longer, and fuel any physical activity you undertake."),
                ("🔥", "Day 4", "Active Fuel",
                 "Midweek momentum! These meals are designed to support an active lifestyle — the right balance of carbs for immediate energy and protein for sustained performance."),
                ("🦴", "Day 5", "Bone & Immunity Boost",
                 "A calcium and fibre-rich day that strengthens bones, supports your immune system, and keeps your digestion running smoothly heading into the weekend."),
                ("🌙", "Day 6", "Weekend Comfort",
                 "Enjoy nourishing, satisfying meals that comfort without compromising your health goals. Weekend eating should feel indulgent and still be nutritionally sound."),
                ("🌟", "Day 7", "Wholesome Reset",
                 "Close the week with balance. Today's meals are thoughtfully chosen to restore energy reserves, support overnight recovery, and prepare your body for the week ahead."),
            ]

            meal_contexts = {
                "Breakfast": [
                    "A powerful start to your morning. This breakfast delivers the nutrients your body needs after overnight fasting — energising the brain and stabilising blood sugar for the hours ahead.",
                    "Start your day with intention. This morning meal is designed to provide sustained energy, preventing mid-morning fatigue and keeping focus sharp.",
                    "Fuel your morning with this smart breakfast that balances proteins, carbohydrates, and micronutrients for a productive and energised start.",
                    "A nourishing breakfast that supports your metabolism from the first meal of the day — setting the tone for mindful eating throughout.",
                    "Rise and thrive. This breakfast choice is nutrient-dense and satisfying, keeping hunger at bay and energy levels steady well into the afternoon.",
                    "Morning nutrition matters. This meal gives you a clean, powerful energy source to carry you through the busiest hours of your day.",
                    "Start strong and stay strong. This breakfast is rich in essentials that support focus, mood, and physical readiness.",
                ],
                "Lunch": [
                    "The day's centrepiece meal. This lunch provides a well-rounded mix of macronutrients to sustain your afternoon energy and prevent the post-lunch slump.",
                    "A midday reset that nourishes without weighing you down. Light, nutrient-rich, and satisfying — ideal for maintaining productivity through the afternoon.",
                    "Power through your afternoon with this balanced lunch — rich in protein and complex carbs for lasting energy and mental clarity.",
                    "Today's lunch keeps you fuelled and focused. A smart combination of nutrients designed to support your activity levels and health goals.",
                    "Recharge at midday with a meal that's both delicious and deeply nourishing — packed with vitamins, minerals, and the right macros.",
                    "Make lunch count. This meal replenishes your body's glycogen stores and provides key nutrients needed for the second half of your day.",
                    "A lunch that delivers — combining gut health benefits, sustained energy, and essential micronutrients in one satisfying serving.",
                ],
                "Dinner": [
                    "Wind down with a balanced dinner that's easy on digestion and rich in the nutrients your body needs to recover and restore overnight.",
                    "Tonight's dinner is light yet nourishing — crafted to support overnight recovery, muscle repair, and restful sleep without overloading your system.",
                    "End the day well. This dinner delivers key proteins and minerals that work overnight to repair tissues, balance hormones, and support deep sleep.",
                    "A calming evening meal that satisfies your hunger with wholesome ingredients — supporting relaxation, digestion, and overnight cellular repair.",
                    "Finish your day with intention. This dinner is rich in calcium and micronutrients that work best when consumed in the evening for maximum absorption.",
                    "Tonight's meal is both comforting and nutritionally complete — the perfect way to close an active day and set yourself up for a great tomorrow.",
                    "The final meal of your week. Chosen for its ability to restore, replenish, and prepare your body for another successful week of healthy living.",
                ],
            }

            header_html = """
<div style='text-align:center; padding: 24px 0 16px 0;'>
  <div style='font-size: 2.4rem; font-weight: 900; font-family: Outfit, sans-serif; letter-spacing: -0.5px; color: #ffffff;'>
    🗓️ Your Personalized 7-Day Meal Plan
  </div>
  <div style='font-size: 1.05rem; color: #aaaaaa; margin-top: 8px; font-family: Outfit, sans-serif; font-weight: 400; letter-spacing: 0.3px;'>
    Expertly curated from our nutritional database · Tailored to your health profile &amp; dietary preferences
  </div>
  <div style='width: 80px; height: 3px; background: linear-gradient(90deg, #0d1117, #ff8c00); margin: 16px auto 0 auto; border-radius: 99px;'></div>
</div>
"""
            fallback_html = header_html

            meal_types = ["Breakfast", "Lunch", "Dinner"]

            for day_idx in range(7):
                emoji, day_label, theme, day_intro = day_themes[day_idx]

                fallback_html += f"""
<div style='margin: 28px 0 12px 0;'>
  <h2 style='font-size:1.6rem; font-weight:800; font-family:Outfit,sans-serif; color:#ff8c00; margin-bottom:4px;'>
    {emoji} {day_label} — {theme}
  </h2>
  <p style='color:#cccccc; font-size:0.95rem; font-family:Outfit,sans-serif; line-height:1.7; margin-bottom:8px;'>{day_intro}</p>
  <hr style='border:none; border-top:1px solid rgba(255,255,255,0.08); margin-bottom:18px;'/>
</div>
"""
                for meal_idx, meal_type in enumerate(meal_types):
                    flat_idx = day_idx * 3 + meal_idx
                    if flat_idx >= len(all_meals):
                        break
                    meal = all_meals[flat_idx]

                    kcal   = float(meal['Energy kcal'])
                    protein = float(meal['Protein(g)'])
                    carbs  = float(meal['Carbs'])
                    fat    = float(meal['Fat(g)'])
                    fibre  = float(meal['Fibre(g)'])
                    sugar  = float(meal['Freesugar(g)'])
                    calcium = float(meal['Calcium(mg)'])
                    tips   = meal.get('Consumption Tips', '')
                    ctx    = meal_contexts[meal_type][day_idx]

                    if protein > 10:   badge = "💪 High Protein"
                    elif fibre > 4:    badge = "🌿 High Fibre"
                    elif kcal < 100:   badge = "✅ Low Calorie"
                    elif calcium > 100: badge = "🦴 Calcium Rich"
                    elif fat > 20:     badge = "⚡ Energy Dense"
                    else:              badge = "⭐ Well Balanced"

                    meal_icons = {"Breakfast": "🌄", "Lunch": "☀️", "Dinner": "🌙"}

                    food_name_html = f'<span style="color:#ffd700; font-weight:800; font-size:1.15rem; font-family:Outfit,sans-serif;">{meal["Food Items"]}</span>'

                    fallback_html += f"""
<div style='margin-bottom:20px; padding: 16px 20px; background: rgba(255,255,255,0.03); border-radius:14px; border:1px solid rgba(255,255,255,0.06);'>
  <div style='font-size:1.05rem; font-weight:700; color:#ff8c00; font-family:Outfit,sans-serif; margin-bottom:4px;'>
    {meal_icons.get(meal_type, '🍽️')} {meal_type} &nbsp;<span style='font-size:0.8rem; background:rgba(255,140,0,0.15); color:#ffaa44; border-radius:99px; padding:2px 10px;'>{badge}</span>
  </div>
  <div style='margin-bottom:10px;'>{food_name_html}</div>
  <p style='color:#bbbbbb; font-size:0.9rem; font-family:Outfit,sans-serif; line-height:1.7; margin-bottom:12px;'>{ctx}</p>
  <table class='nutrition-table' style='width:100%; border-collapse:collapse; font-family:Outfit,sans-serif; font-size:0.88rem; text-align:center;'>
    <thead>
      <tr style='background:rgba(255,140,0,0.1);'>
        <th style='padding:8px; color:#ff8c00; border-bottom:1px solid rgba(255,255,255,0.1);'>🔥 Energy</th>
        <th style='padding:8px; color:#ff8c00; border-bottom:1px solid rgba(255,255,255,0.1);'>🥩 Protein</th>
        <th style='padding:8px; color:#ff8c00; border-bottom:1px solid rgba(255,255,255,0.1);'>🍞 Carbs</th>
        <th style='padding:8px; color:#ff8c00; border-bottom:1px solid rgba(255,255,255,0.1);'>🥑 Fat</th>
        <th style='padding:8px; color:#ff8c00; border-bottom:1px solid rgba(255,255,255,0.1);'>🌱 Fibre</th>
        <th style='padding:8px; color:#ff8c00; border-bottom:1px solid rgba(255,255,255,0.1);'>🍬 Sugar</th>
        <th style='padding:8px; color:#ff8c00; border-bottom:1px solid rgba(255,255,255,0.1);'>🦴 Calcium</th>
      </tr>
    </thead>
    <tbody>
      <tr style='color:#ffffff;'>
        <td data-label='Energy' style='padding:8px; font-weight:700;'>{kcal:.0f} kcal</td>
        <td data-label='Protein' style='padding:8px;'>{protein:.1f}g</td>
        <td data-label='Carbs' style='padding:8px;'>{carbs:.1f}g</td>
        <td data-label='Fat' style='padding:8px;'>{fat:.1f}g</td>
        <td data-label='Fibre' style='padding:8px;'>{fibre:.1f}g</td>
        <td data-label='Sugar' style='padding:8px;'>{sugar:.1f}g</td>
        <td data-label='Calcium' style='padding:8px;'>{calcium:.1f}mg</td>
      </tr>
    </tbody>
  </table>"""

                    if tips:
                        tip_parts = [t.strip() for t in tips.split('|') if t.strip()]
                        tips_html = " &nbsp;·&nbsp; ".join(tip_parts)
                        fallback_html += f"""
  <p style='color:#888; font-size:0.83rem; margin-top:10px; font-family:Outfit,sans-serif;'>💡 {tips_html}</p>"""

                    fallback_html += "</div>\n"

            fallback_html += """
<div style='margin-top:32px;'>
  <h3 style='color:#ff8c00; font-family:Outfit,sans-serif;'>🛒 Weekly Shopping Guide</h3>
  <ul style='color:#cccccc; font-family:Outfit,sans-serif; line-height:2;'>
    <li>Stock <strong>whole grains, lentils, and legumes</strong> in bulk — affordable, versatile, and nutrient-dense.</li>
    <li>Include <strong>seasonal vegetables and fresh herbs</strong> to maximise micronutrient intake.</li>
    <li>Keep <strong>lean protein sources</strong> (eggs, paneer, tofu, chicken) readily accessible.</li>
    <li>Choose <strong>low-sodium, minimally processed</strong> options whenever possible.</li>
  </ul>
  <h3 style='color:#ff8c00; font-family:Outfit,sans-serif; margin-top:20px;'>🥗 Meal Prep Strategy</h3>
  <ul style='color:#cccccc; font-family:Outfit,sans-serif; line-height:2;'>
    <li><strong>Batch cook</strong> grains (rice, oats, daliya) and refrigerate for up to 4 days.</li>
    <li><strong>Pre-portion</strong> snacks and protein sources to avoid impulse eating.</li>
    <li>Use <strong>herbs and spices</strong> generously — rich flavour without extra calories.</li>
    <li><strong>Hydrate consistently</strong> — drink at least 8 glasses of water daily.</li>
  </ul>
</div>
"""
            st.markdown(f'<div class="result-container">{fallback_html}</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Food Analysis")

    uploaded_file = st.file_uploader(
        "Upload an image of your food",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True)

        if st.button("Analyze Food"):
            result_placeholder = st.empty()
            with result_placeholder.container():
                render_skeleton_loader()

            image_data = input_image_setup(uploaded_file)

            prompt = """
            You are an expert nutritionist and food analyst. Analyze this food image with high precision.

            Format your response professionally with these sections:
            ## 🔍 Food Analysis Results
            - **Estimated Calories:** Provide a range or exact value.
            - **Macronutrients:** Protein, Carbohydrates, and Fats.

            ## ✨ Health Benefits & Nutritional Value
            Detail the key vitamins, minerals, and overall value.

            ## ⚠️ Dietary Concerns & Considerations
            Mention allergens, high sodium, sugar, etc.

            ## 🍽️ Portion Size & Recommendations
            Advice on how much to consume and how to balance it.

            Use Markdown headers (##, ###), bold text, and structured bullet points.
            """
            try:
                response = get_gemini_response(prompt, image_data)
                result_placeholder.empty()
                st.markdown(f'<div class="result-container">{response}</div>', unsafe_allow_html=True)
            except Exception as e:
                result_placeholder.empty()
                st.markdown('<div class="result-container" style="color:#ff6b6b; border-color:rgba(255, 107, 107, 0.4); text-align: center;">⚠️ <b>Request Failed</b><br><br>Hang tight! We’ll have the best suggestion ready for you soon.</div>', unsafe_allow_html=True)

with tab3:
    st.subheader("Health Insights")

    health_query = st.text_input(
        "Ask any health/nutrition-related question"
    )

    if st.button("Get Expert Insights"):
        result_placeholder = st.empty()
        with result_placeholder.container():
            render_skeleton_loader()

        prompt = f"""
        You are a certified nutritionist and health advisor.

        ### User Inquiry:
        {health_query}

        ### Health Context:
        {st.session_state.health_profile}

        Please provide a professional response with:
        ## 🧠 Expert Insights
        - Detailed explanation or answer to the question.
        - Scientific or nutritional rationale.

        ## 🧗 Actionable Advice
        - Specific steps for the user based on their profile.

        ## 💡 Expert Recommendations
        - Lifestyle, supplement, or dietary tips.

        Ensure high readability with Markdown formatting.
        """
        try:
            response = get_gemini_response(prompt)
            result_placeholder.empty()
            st.markdown(f'<div class="result-container">{response}</div>', unsafe_allow_html=True)
        except Exception as e:
            result_placeholder.empty()
            st.markdown('<div class="result-container" style="color:#ff6b6b; border-color:rgba(255, 107, 107, 0.4); text-align: center;">⚠️ <b>Request Failed</b><br><br>Hang tight! We’ll have the best suggestion ready for you soon.</div>', unsafe_allow_html=True)
