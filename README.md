# Nutrixa:  Health Companion

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/AI-Google_Gemini-blueviolet.svg)](https://deepmind.google/technologies/gemini/)

**Nutrixa** is a premium, AI-powered Health Companion built with Streamlit and the Google Gemini API. It provides personalized meal planning, instant nutritional analysis from food images, and expert health insights in a modern dark-mode interface.

## ✨ Features
- **🥗 Personalized Meal Plans:** 7-day schedules tailored precisely to your goals and dietary needs.
- **🔍 Image-Based Analysis:** Upload food photos for instant calorie calculations and macro estimates.
- **🧠 Expert Insights:** Real-time AI-driven health advice and reliable nutritional logic.
- **⚡ Offline Fallback:** Seamlessly switches to a rich local dataset (`foods.csv`) during API outages to guarantee zero downtime.

## 🚀 Quick Start

1. **Clone & Install:**
   ```bash
   git clone https://github.com/rajuperumalla951515/Nutrixa.git
   cd Nutrixa
   pip install -r requirements.txt
   ```
   *(We recommend setting up a virtual environment before installing.)*

2. **Environment Setup:** 
   Create a `.env` file in the root directory and add your key:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

3. **Run the App:** 
   ```bash
   streamlit run app.py
   ```

## 🛠️ Tech Stack
- **Frontend/Backend:** Streamlit (Python)
- **AI/Data Services:** Google Gemini API, Pandas, Pillow

Dont Forget to star my repo ⭐
