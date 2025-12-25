# 🌿 DietVeda — Intelligent Ayurvedic Wellness System

**Ancient Ayurveda × Modern AI — Your Path to Perfect Balance**

## ✨ Overview

DietVeda is a comprehensive wellness platform that combines traditional Ayurvedic wisdom with modern artificial intelligence. The system provides personalized dosha diagnosis, dietary recommendations, yoga guidance, routine tracking, and AI-powered wellness coaching.

## 🎨 Design Philosophy

The entire platform is designed with an **Ayurvedic, serene, nature-inspired aesthetic** featuring:

- **Color Palette**: Vata (lavender, brown, sky blue), Pitta (green, rose, white, beige), Kapha (earthy green, turmeric, brown)
- **Typography**: Elegant serif headings (Cormorant Garamond) with soft sans-serif body text (Inter)
- **Visual Elements**: Mandala animations, lotus patterns, copper accents, herbal textures
- **User Experience**: Calming, peaceful interface inspired by an Ayurvedic clinic

## 🚀 Features

### 🔮 Dosha Diagnosis
- Interactive quiz to determine your Ayurvedic constitution
- Beautiful mandala visualization of results
- Confidence scoring and detailed analysis

### 🥗 Food & Lifestyle Recommendations
- Personalized diet plans based on dosha and season
- Premium PDF downloads with Ayurvedic styling
- Meal filtering (Breakfast, Lunch, Dinner, Snacks)
- Suitability scoring for each dish

### 📸 Live Tongue Scanner
- Computer vision-based tongue analysis
- Real-time dosha imbalance detection
- Color analysis for Pitta, Kapha, and Agni assessment

### 📅 Sattva Routine Tracker
- Daily habit checklist with Ayurvedic practices
- Dosha-specific recommendations
- Sattva score calculation with ranking system
- Beautiful notebook-style interface

### 📈 Wellness Analytics
- Progress tracking over 30 days
- Nadi Pariksha-inspired visualizations
- AI-generated wellness insights

### 🧘 Yoga Coach
- Dosha-specific yoga sequences
- Video integration with automatic playback
- Mandala-style countdown timers

### 🤖 Dr. Veda Chatbot
- AI-powered Ayurvedic guru interface
- Personalized advice based on dosha
- Warm, concise responses with lifestyle tips

## 📋 Installation

### Prerequisites
- Python 3.8+
- pip
- Webcam (for tongue scanner)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd DietVeda
   ```

2. **Create and activate virtual environment** (recommended)
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-cors pandas scikit-learn opencv-python reportlab google-generativeai
   ```

4. **Ensure data files are present**
   - `dishes_dataset.csv` - Food recommendations database
   - `ayurvedic_dosha_dataset.csv` - Dosha training data
   - `dietveda_complex_model.pkl` - Trained ML model
   - `dietveda_encoders.pkl` - Feature encoders

## 🎯 Running the Application

### Start the Flask Server

```bash
python flask_backend.py
```

The server will start on `http://localhost:5000`

### Access the Web Interface

Open your browser and navigate to:
- **Home**: http://localhost:5000/
- **Dosha Diagnosis**: http://localhost:5000/dosha
- **Diet Recommendations**: http://localhost:5000/diet
- **Tongue Scanner**: http://localhost:5000/tongue
- **Routine Tracker**: http://localhost:5000/routine
- **Analytics**: http://localhost:5000/analytics
- **Yoga Coach**: http://localhost:5000/yoga
- **Dr. Veda Chatbot**: http://localhost:5000/chatbot

## 📁 Project Structure

```
DietVeda/
├── templates/          # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── dosha_diagnosis.html
│   ├── diet_recommendations.html
│   ├── tongue_scanner.html
│   ├── routine_tracker.html
│   ├── analytics.html
│   ├── yoga_coach.html
│   └── chatbot.html
├── static/
│   ├── css/
│   │   └── ayurvedic.css    # Main stylesheet
│   ├── js/
│   │   ├── main.js
│   │   ├── dosha.js
│   │   ├── diet.js
│   │   ├── scanner.js
│   │   ├── routine.js
│   │   ├── analytics.js
│   │   ├── yoga.js
│   │   └── chatbot.js
│   └── images/
├── DietVeda_Reports/   # Generated PDFs
├── flask_backend.py    # Main Flask application
├── predictor.py        # ML dosha prediction
├── recommender.py      # Diet recommendations
├── yoga_coach.py       # Yoga sequences
├── tongue_scanner.py   # Computer vision
├── routine_tracker.py  # Habit tracking
├── analytics.py        # Progress analytics
├── chatbot.py          # AI chatbot
├── diet_pdf.py         # PDF generation
└── progress_db.py      # Database for tracking
```

## 🔧 Configuration

### API Keys

The chatbot uses Google's Gemini API. Update the API key in `chatbot.py`:

```python
self.api_key = "YOUR_GEMINI_API_KEY"
```

Get your API key from: https://makersuite.google.com/app/apikey

## 📄 PDF Generation

The system generates beautiful Ayurvedic-styled PDFs with:
- Mandala headers on each page
- Soft pastel green card backgrounds
- Copper borders
- Sanskrit-inspired typography

PDFs are saved in the `DietVeda_Reports/` directory.

## 🎨 Customization

### Colors
Edit `static/css/ayurvedic.css` to customize the color palette:
- Vata colors: `--vata-lavender`, `--vata-brown`, `--vata-sky`
- Pitta colors: `--pitta-green`, `--pitta-rose`, `--pitta-beige`
- Kapha colors: `--kapha-green`, `--kapha-turmeric`, `--kapha-brown`

### Typography
Fonts are loaded from Google Fonts. Modify the `@import` statement in `ayurvedic.css` to change fonts.

## 🌟 Features in Detail

### Dosha Diagnosis Flow
1. User answers 6 questions about digestion, sleep, energy, temperature, mood, and body frame
2. ML model predicts dosha type with confidence score
3. Results displayed with beautiful mandala visualization
4. Dosha stored in browser localStorage for personalization

### Diet Recommendations
- Filters dishes by dosha compatibility
- Scores each dish for Ayurvedic suitability
- Shows season compatibility
- Generates downloadable PDF charts

### Tongue Scanner
- Uses webcam to capture tongue image
- Analyzes RGB values in center region
- Detects:
  - High Pitta (redness)
  - Kapha Ama (white coating)
  - Healthy Pink (balanced Agni)

## 🤝 Contributing

This is a personal wellness project. Feel free to fork and customize for your own use!

## 📜 License

This project is for personal/educational use.

## 🙏 Acknowledgments

- Ayurvedic wisdom from ancient texts (Charaka Samhita, Sushruta Samhita)
- Modern AI powered by Google Gemini
- Design inspired by traditional Indian wellness practices

---

**🌿 Balance is the essence of health — Sushruta Samhita 🌿**

