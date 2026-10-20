import os
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image
from google import genai

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Food Calories Estimator",
    page_icon="🍕",
    layout="wide",
)

# =========================================================
# PROFESSIONAL HEADER
# =========================================================

st.markdown(
    """
    <h1 style="color:#d35400; text-align:center; font-size:42px; font-weight:800; margin-bottom:5px;">
        🍕 AI Food Calories Estimator
    </h1>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h3 style="color:#6d4c41; text-align:center;">
        🤖 AI-Powered Nutrition Tracking
    </h3>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p style="color:#5d4037; text-align:center; font-size:17px;">
        Upload a food image and instantly get calories, protein, carbohydrates and fat.
    </p>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# GEMINI AI
# =========================================================

import os

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None
# =========================================================
# LOAD FOOD DATABASE
# =========================================================

DATA_FILE = Path("calories.csv")
HISTORY_FILE = Path("meal_history.csv")

if not DATA_FILE.exists():
    st.error("❌ calories.csv was not found in the project folder.")
    st.stop()

try:
    data = pd.read_csv(DATA_FILE)
except Exception as e:
    st.error(f"❌ Could not read calories.csv: {e}")
    st.stop()

required_columns = {"Food", "Calories", "Protein", "Carbs", "Fat"}
missing_columns = required_columns - set(data.columns)

if missing_columns:
    st.error(
        "❌ calories.csv is missing these columns: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()

# Clean database values.
data = data.dropna(subset=["Food"]).copy()
data["Food"] = data["Food"].astype(str).str.strip()
food_list = data["Food"].tolist()

for column in ["Calories", "Protein", "Carbs", "Fat"]:
    data[column] = pd.to_numeric(data[column], errors="coerce").fillna(0)

# =========================================================
# MEAL HISTORY
# =========================================================

if "meal_history" not in st.session_state:
    if HISTORY_FILE.exists():
        try:
            saved_history = pd.read_csv(HISTORY_FILE)
            st.session_state.meal_history = saved_history.to_dict("records")
        except Exception:
            st.session_state.meal_history = []
    else:
        st.session_state.meal_history = []

# =========================================================
# DAILY CALORIE GOAL
# =========================================================

st.sidebar.header("🎯 Daily Calorie Goal")

calorie_goal = st.sidebar.number_input(
    "Set your daily calorie goal",
    min_value=500,
    max_value=5000,
    value=2000,
    step=50,
    key="calorie_goal",
)

st.sidebar.write(f"🎯 Your goal: **{calorie_goal} kcal**")

# =========================================================
# FOOD SCANNER
# =========================================================

st.markdown(
    '<h2 style="color:#d35400;">📷 Food Scanner</h2>',
    unsafe_allow_html=True,
)

st.write(
    "Upload a clear food image and let AI identify the food and estimate its nutrition."
)

uploaded_file = st.file_uploader(
    "📷 Choose a food image",
    type=["jpg", "jpeg", "png"],
    key="food_uploader",
)

# =========================================================
# MAIN SCANNER
# =========================================================

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        image.load()
    except Exception as e:
        st.error(f"❌ Could not open the uploaded image: {e}")
        st.stop()

    st.image(image, caption="Uploaded Food Image", width="stretch")

    detected_food = None
    ai_worked = False

    # -----------------------------------------------------
    # AI DETECTION
    # -----------------------------------------------------

    if client is not None:
        with st.spinner("🤖 AI is identifying your food..."):
            prompt = f"""
You are a food recognition AI.

Look carefully at the uploaded food image.

Identify the MAIN food item visible in the image.

You MUST choose exactly ONE food from this list:
{", ".join(food_list)}

Return ONLY the exact food name from the list.
Do not provide explanations, punctuation, or extra text.
"""

            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=[prompt, image],
                )

                detected_food = (response.text or "").strip()
                detected_food = detected_food.splitlines()[0].strip()
                detected_food = detected_food.strip("`*\"'")

                matching_food = data[
                    data["Food"].str.lower() == detected_food.lower()
                ]

                if not matching_food.empty:
                    ai_worked = True
                    detected_food = matching_food.iloc[0]["Food"]
                    st.success(f"🤖 AI Detected Food: {detected_food}")
                else:
                    st.warning(
                        f"⚠️ AI detected '{detected_food}', but this food is not available in your database."
                    )

            except Exception as e:
                st.error("❌ AI detection failed.")
                st.caption(f"Technical error: {e}")
    else:
        st.warning(
            "⚠️ Gemini API key is not configured. Manual food selection is available."
        )

    # -----------------------------------------------------
    # MANUAL FALLBACK
    # -----------------------------------------------------

    if not ai_worked:
        st.info("🔄 You can select your food manually.")
        detected_food = st.selectbox(
            "🍽️ Select Food",
            food_list,
            key="manual_food_select",
        )

    # -----------------------------------------------------
    # FIND FOOD
    # -----------------------------------------------------

    matching_food = data[
        data["Food"].str.lower() == str(detected_food).lower()
    ]

    if not matching_food.empty:
        food_data = matching_food.iloc[0]

        # -------------------------------------------------
        # MEAL TYPE
        # -------------------------------------------------

        meal_type = st.selectbox(
            "🍽️ Select Meal Type",
            ["Breakfast", "Lunch", "Dinner", "Snack"],
            key="meal_type_select",
        )

        # -------------------------------------------------
        # QUANTITY
        # -------------------------------------------------

        quantity = st.number_input(
            "🔢 How many servings/pieces?",
            min_value=1,
            max_value=20,
            value=1,
            step=1,
            key="quantity_input",
        )

        # -------------------------------------------------
        # NUTRITION CALCULATION
        # -------------------------------------------------

        total_calories = float(food_data["Calories"]) * quantity
        total_protein = float(food_data["Protein"]) * quantity
        total_carbs = float(food_data["Carbs"]) * quantity
        total_fat = float(food_data["Fat"]) * quantity

        # -------------------------------------------------
        # NUTRITION DASHBOARD
        # -------------------------------------------------

        st.subheader("📊 Nutrition Information")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🔥 Calories", f"{total_calories:.1f} kcal")
        with col2:
            st.metric("🥩 Protein", f"{total_protein:.1f} g")
        with col3:
            st.metric("🍚 Carbs", f"{total_carbs:.1f} g")
        with col4:
            st.metric("🥑 Fat", f"{total_fat:.1f} g")

        # -------------------------------------------------
        # ADD MEAL
        # -------------------------------------------------

        if st.button("➕ Add to Today's Meals", key="add_meal_button"):
            meal_record = {
                "Date": str(pd.Timestamp.now().date()),
                "Meal Type": meal_type,
                "Food": detected_food,
                "Quantity": quantity,
                "Calories": total_calories,
                "Protein": total_protein,
                "Carbs": total_carbs,
                "Fat": total_fat,
            }

            st.session_state.meal_history.append(meal_record)

            pd.DataFrame(st.session_state.meal_history).to_csv(
                HISTORY_FILE,
                index=False,
            )

            st.success("✅ Meal added to today's history!")
            st.rerun()
    else:
        st.error("❌ Food could not be found in the database.")
else:
    st.info("📷 Please upload a food image to start.")

# =========================================================
# HISTORY & DASHBOARD — ONLY ONE SECTION
# =========================================================

st.markdown("---")
st.header("🍽️ Meal History")

# Default empty dashboard variables prevent NameError.
today_df = pd.DataFrame()
total_today = 0.0
total_protein_today = 0.0
total_carbs_today = 0.0
total_fat_today = 0.0

if st.session_state.meal_history:
    history_df = pd.DataFrame(st.session_state.meal_history)

    if "Date" not in history_df.columns:
        history_df["Date"] = str(pd.Timestamp.now().date())

    history_df["Date"] = history_df["Date"].astype(str).str[:10]
    today = str(pd.Timestamp.now().date())

    # =====================================================
    # TODAY'S MEALS
    # =====================================================

    st.subheader("📅 Today's Meals")

    today_df = history_df[history_df["Date"] == today].copy()

    if not today_df.empty:
        st.dataframe(today_df, width="stretch", hide_index=True)

        total_today = float(today_df["Calories"].sum())
        total_protein_today = float(today_df["Protein"].sum())
        total_carbs_today = float(today_df["Carbs"].sum())
        total_fat_today = float(today_df["Fat"].sum())

        # =================================================
        # TODAY'S NUTRITION SUMMARY
        # =================================================

        st.subheader("🔥 Today's Nutrition Summary")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Calories", f"{total_today:.1f} kcal")
        with col2:
            st.metric("Protein", f"{total_protein_today:.1f} g")
        with col3:
            st.metric("Carbs", f"{total_carbs_today:.1f} g")
        with col4:
            st.metric("Fat", f"{total_fat_today:.1f} g")

        # =================================================
        # NUTRITION GRAPH
        # =================================================

        st.subheader("📊 Nutrition Breakdown")

        chart_data = pd.DataFrame(
            {
                "Nutrient": ["Protein", "Carbs", "Fat"],
                "Grams": [
                    total_protein_today,
                    total_carbs_today,
                    total_fat_today,
                ],
            }
        )

        st.bar_chart(chart_data.set_index("Nutrient"))

        # =================================================
        # SMART FOOD SUGGESTION
        # =================================================

        st.subheader("💡 Smart Food Suggestion")

        suggestions = {
            "Pizza": "🥗 Try balancing your next meal with vegetables, dal, or another nutrient-rich food.",
            "Burger": "🥗 Consider adding vegetables or a protein-rich side.",
            "Apple": "🍎 You can pair apple with a protein-rich food.",
            "Banana": "🍌 Pair banana with milk, curd, or another protein-rich food.",
            "Rice": "🍚 Pair rice with dal, vegetables, or curd.",
            "Paneer": "🥛 Paneer provides protein. Pair it with vegetables or whole grains.",
            "Dosa": "🥣 Pair dosa with sambar and vegetables.",
            "Idli": "🥣 Pair idli with sambar or another protein-rich side.",
        }

        latest_food = str(today_df.iloc[-1]["Food"])
        suggestion = suggestions.get(
            latest_food,
            "🥗 Try to include a variety of nutritious foods in your meals.",
        )
        st.info(suggestion)

        # =================================================
        # SMART DAILY HEALTH INSIGHT
        # =================================================

        st.subheader("🧠 Smart Daily Health Insight")

        if total_today < calorie_goal * 0.5:
            st.info(
                "💡 You have consumed less than half of your daily calorie goal. "
                "Make sure your meals include enough nutritious foods."
            )
        elif total_today <= calorie_goal:
            st.success(
                "🎯 You are currently within your daily calorie goal. "
                "Try to keep your meals balanced with vegetables, protein, whole grains, "
                "and other nutritious foods."
            )
        else:
            st.warning(
                "⚠️ Your current calorie intake is above your daily calorie goal. "
                "For your next meals, consider choosing lighter and nutrient-rich foods."
            )

        if total_protein_today < 20:
            st.info(
                "🥩 Your protein intake is currently low. "
                "Dal, paneer, curd, beans and soy can help."
            )
        elif total_protein_today >= 40:
            st.success("💪 Nice! Your meals today include a good amount of protein.")

        # =================================================
        # DAILY CALORIE GOAL
        # =================================================

        st.subheader("🎯 Daily Calorie Goal")

        progress = min(total_today / calorie_goal, 1.0)
        st.progress(progress)

        remaining = calorie_goal - total_today

        if remaining > 0:
            st.info(
                f"🔥 Consumed: **{total_today:.1f} kcal**\n\n"
                f"🎯 Goal: **{calorie_goal:.1f} kcal**\n\n"
                f"🥗 Remaining: **{remaining:.1f} kcal**"
            )
        else:
            st.warning(
                f"🔥 You have reached your daily calorie goal of {calorie_goal:.1f} kcal."
            )
    else:
        st.info("📅 No meals added today yet.")
else:
    st.info("📅 No meal history available.")

# =========================================================
# WEEKLY PROGRESS
# =========================================================

st.subheader("📈 Weekly Progress")

if st.session_state.meal_history:
    weekly_data = pd.DataFrame(st.session_state.meal_history)

    if "Date" in weekly_data.columns:
        weekly_data["Date"] = pd.to_datetime(
            weekly_data["Date"], errors="coerce"
        )
        weekly_data = weekly_data.dropna(subset=["Date"])

        today_date = pd.Timestamp.now().normalize()
        seven_days_ago = today_date - pd.Timedelta(days=6)

        weekly_df = weekly_data[
            weekly_data["Date"].between(seven_days_ago, today_date)
        ]

        if not weekly_df.empty:
            weekly_summary = (
                weekly_df.groupby("Date")["Calories"]
                .sum()
                .reset_index()
            )

            weekly_summary["Date"] = weekly_summary["Date"].dt.strftime(
                "%d %b"
            )
            weekly_summary = weekly_summary.set_index("Date")

            st.bar_chart(weekly_summary)
            st.write("🔥 **Weekly calorie intake**")

            weekly_total = float(weekly_df["Calories"].sum())
            weekly_average = float(
                weekly_df.groupby("Date")["Calories"].sum().mean()
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric("🔥 Weekly Total", f"{weekly_total:.1f} kcal")
            with col2:
                st.metric("📊 Daily Average", f"{weekly_average:.1f} kcal")
        else:
            st.info("📅 No meal data available for the last 7 days.")
else:
    st.info("📅 Add meals to see your weekly progress.")

# =========================================================
# DOWNLOAD REPORT
# =========================================================

st.subheader("📥 Download Nutrition Report")

if not today_df.empty:
    report_df = today_df.copy()

    if "Date" in report_df.columns:
        report_df["Date"] = pd.to_datetime(
            report_df["Date"], errors="coerce"
        ).dt.strftime("%d-%b-%Y")

    report_csv = report_df.to_csv(index=False)

    st.download_button(
        label="📥 Download Today's Nutrition Report",
        data=report_csv,
        file_name="nutrition_report.csv",
        mime="text/csv",
        key="download_report",
    )

    st.success("✅ Your nutrition report is ready!")
else:
    st.info("📅 Add a meal to generate today's report.")

# =========================================================
# CLEAR MEAL HISTORY — ONLY ONE BUTTON
# =========================================================

st.subheader("🗑️ Meal History")

if st.button("🗑️ Clear Today's Meals", key="clear_meal_history_final"):
    # This version intentionally clears the complete saved history,
    # matching the behaviour of the previous app.
    st.session_state.meal_history = []

    empty_df = pd.DataFrame(
        columns=[
            "Date",
            "Meal Type",
            "Food",
            "Quantity",
            "Calories",
            "Protein",
            "Carbs",
            "Fat",
        ]
    )

    empty_df.to_csv(HISTORY_FILE, index=False)
    st.success("🗑️ Meal history cleared!")
    st.rerun()
