# 🍕 AI Food Calories Estimator

### AI-Powered Food Recognition & Nutrition Tracking Application

An intelligent food calorie estimation application built using **Python, Streamlit, and Google Gemini AI**. The application allows users to upload a food image, identify the food using AI, and estimate its nutritional values, including calories, protein, carbohydrates, and fat.

It also provides daily nutrition summaries, calorie-goal tracking, weekly progress visualization, smart food suggestions, and downloadable nutrition reports — all through an interactive web interface.

**Live Demo:** [Try AI Food Calories Estimator](https://ai-food-calorie-estimator.streamlit.app)

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Installation and Setup](#-installation-and-setup)
- [Gemini API Configuration](#-gemini-api-configuration)
- [How to Use](#-how-to-use)
- [Sample Output](#-sample-output)
- [Future Enhancements](#-future-enhancements)
- [Limitations](#-limitations)
- [Disclaimer](#-disclaimer)
- [Author](#-author)

---

## 🌟 Overview

Tracking daily food intake is important for understanding eating habits and making informed nutrition choices. However, manually searching for the nutritional value of every meal can be time-consuming.

The **AI Food Calories Estimator** simplifies this process by combining image-based food recognition with AI-assisted nutrition estimation.

Users can upload an image of their meal and receive an estimated nutritional breakdown. The application also helps users monitor their daily calorie intake against a personalized calorie goal.

The project demonstrates the practical integration of generative AI into a user-friendly Python application.

## 🎯 Problem Statement

Manually tracking food calories and macronutrients can be inconvenient because:

- Looking up the nutritional information of individual foods takes time.
- Estimating portion sizes and calorie intake can be difficult.
- Maintaining a consistent record of daily meals requires effort.
- Understanding daily calorie and macronutrient intake can be confusing for beginners.

## 💡 Solution

This project provides an interactive application that combines AI-powered food identification with nutrition tracking.

Users can upload a food image, obtain an AI-generated food identification and nutrition estimate, review daily totals, monitor their progress, and download a nutrition report.

The application also supports manual food selection when AI functionality is unavailable.

---

## ✨ Key Features

### 1. 📷 AI-Powered Food Recognition
- Upload a food image in a supported format.
- Use Google Gemini AI to identify the food.
- Display the detected food name.
- Provide an AI-assisted nutrition estimate.

### 2. 🔥 Calorie Estimation
Estimate the following nutritional values for identified food:

- Calories (kcal)
- Protein (g)
- Carbohydrates (g)
- Fat (g)

### 3. 🎯 Daily Calorie Goal
- Set a daily calorie target.
- Track calories consumed.
- Calculate the remaining calories against the target.
- Review progress toward the daily goal.

### 4. 🍽️ Meal History
- Review recorded meals.
- View daily nutritional totals.
- Manage or clear meal-history records using the available controls.

### 5. 📊 Nutrition Visualization
- View a macronutrient breakdown.
- Compare protein, carbohydrate, and fat values.
- Understand the nutritional composition of recorded meals.

### 6. 📈 Weekly Progress Tracking
- Visualize calorie intake over time.
- Review weekly calorie totals.
- Calculate average daily intake from the available records.

### 7. 🧠 Smart Daily Health Insights
Receive general, automated observations based on recorded nutrition data, such as progress toward a calorie goal and estimated protein intake.

### 8. 🥗 Smart Food Suggestions
Get general food-pairing suggestions based on the detected food and available nutrition information.

### 9. 📥 Downloadable Nutrition Report
Download a nutrition report to review or retain the application's available tracking data.

### 10. 🛠️ Manual Food Selection
Use manual food selection when the Gemini API is not configured or AI-based identification is unavailable, subject to the application's available food data.

---

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web application interface |
| Google Gemini API | AI-assisted food identification and nutrition estimation |
| Google Gen AI SDK | Communication with the Gemini API |
| Pandas | Tabular data handling and CSV operations |
| Pillow (PIL) | Image loading and processing |
| CSV | Food data and nutrition records |
| Git | Version control |
| GitHub | Source-code hosting and project version history |

---

## ⚙️ How It Works

1. **Upload an image:** The user selects a food image from their device.
2. **Process the image:** The application loads the uploaded image using Pillow.
3. **Identify the food:** The application sends the required image and prompt to Gemini AI when the API is configured.
4. **Estimate nutrition:** The AI generates the food identification and estimated nutritional information.
5. **Display results:** The application displays the detected food and its estimated nutrition values.
6. **Track meals:** Available meal records contribute to the daily nutrition summary.
7. **Analyze progress:** The application presents calorie-goal progress, macronutrient visualizations, and weekly summaries.
8. **Export data:** The user can download the available nutrition report.

**Note:** The nutrition values are estimates and can vary depending on portion size, ingredients, cooking methods, and the AI's interpretation of the image.

---

## 📂 Project Structure

```text
AI-Food-Calorie-Estimator/
│
├── app.py          # Main Streamlit application
├── calories.csv    # Food and nutrition reference data
├── test_ai.py      # Gemini API test script
├── README.md       # Project documentation
└── .gitignore      # Excludes sensitive and unnecessary files
```

Local files such as `.env`, `meal_history.csv`, and backup files may be excluded from GitHub through `.gitignore`, depending on the repository configuration.

---

## 🚀 Installation and Setup

### Prerequisites

Make sure you have:

- Python installed
- Git installed (optional, for cloning the repository)
- A Google Gemini API key for AI-powered functionality

### Step 1: Clone the Repository

Open Command Prompt or a terminal and run:

```bash
git clone https://github.com/riyasingh765432-oss/AI-Food-Calorie-Estimator.git
```

### Step 2: Open the Project Folder

```bash
cd AI-Food-Calorie-Estimator
```

### Step 3: Install Dependencies

Install the packages used by the application:

```bash
pip install streamlit pandas pillow google-genai
```

### Step 4: Configure the API Key

Set your Gemini API key as an environment variable. See the configuration section below.

### Step 5: Run the Application

```bash
streamlit run app.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser to use the application.

---
**Security best practices:**

- Never write your actual API key directly in `app.py` or `test_ai.py`.
- Never commit API keys, `.env` files, or secrets to GitHub.
- Keep local configuration files excluded through `.gitignore`.
- If an API key is exposed, revoke it and generate a replacement through the provider's official console.

If the API key is not configured, AI functionality may be unavailable. Manual food selection can be used if supported by the application.

---

## 🖥️ How to Use

1. Launch the application.
2. Set your daily calorie goal.
3. Open the Food Scanner section.
4. Upload a clear image of your meal.
5. Allow the application to identify the food and estimate its nutrition, if AI is configured.
6. Review the estimated calories, protein, carbohydrates, and fat.
7. Record or review meals using the available controls.
8. Check the daily nutrition summary and progress visualizations.
9. Review food suggestions and general nutrition insights.
10. Download the available nutrition report when required.

---

## 📊 Sample Output

The following is an illustrative example of the type of nutrition information the application may display.

| Nutritional Metric | Example Value |
|---|---:|
| Calories | 348 kcal |
| Protein | 12 g |
| Carbohydrates | 72 g |
| Fat | 2.4 g |

These values are examples, not guaranteed results. Actual outputs depend on the food image, portion size, ingredients, and AI estimation.

The dashboard may also display:

- Daily calories consumed
- Remaining calories relative to the goal
- Macronutrient breakdown
- Weekly calorie intake and average
- General food suggestions and nutrition insights

---

## 🔮 Future Enhancements

Potential improvements include:

- **Improved portion estimation:** Estimate serving size more accurately using image analysis.
- **Expanded food database:** Add more regional dishes and verified nutritional references.
- **User accounts:** Enable individual nutrition profiles and personalized settings.
- **Persistent meal history:** Store records in a database for reliable long-term tracking.
- **Enhanced AI validation:** Validate model responses and handle uncertain food identification more effectively.
- **More detailed analytics:** Add meal-wise trends and customizable date ranges.
- **Mobile-friendly interface:** Improve usability across mobile devices.
- **Deployment:** Host the application online so users can access it without running it locally.
- **Automated testing:** Add tests for nutrition calculations, API errors, and data-handling functionality.

These are proposed enhancements and are not necessarily implemented in the current version.

---

## ⚠️ Limitations

- Food recognition depends on image clarity and the AI model's interpretation.
- Nutrition estimates may not match laboratory-verified values.
- Portion size, hidden ingredients, oils, sauces, and preparation methods can affect accuracy.
- AI-powered features require a valid API key, network access, and an available API service.
- Manual food selection depends on the food entries available in the application.
- Long-term data persistence depends on the application's current storage implementation.

---

## 🩺 Disclaimer

This application is intended for educational, informational, and personal food-tracking purposes only.

The nutritional values generated by AI are estimates and should not be treated as medically verified measurements or professional dietary advice. For medical nutrition requirements, consult a qualified healthcare professional or registered dietitian.

---

## 👩‍💻 Author

**Riya Singh**

B.Tech Student | AI & Software Development Enthusiast

## ⭐ Support

If you find this project interesting, consider giving the repository a star on GitHub.

Thank you for checking out the **AI Food Calories Estimator**! 🍕💚
