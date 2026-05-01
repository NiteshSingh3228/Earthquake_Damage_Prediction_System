# Earthquake_Damage_Prediction_System
Seismic Guard V1 is an AI-powered earthquake damage prediction system that analyzes building structure, materials, location, and seismic factors to classify damage risk (Low, Moderate, High). Built with ML ensemble models, Python, and modern web dashboard for disaster preparedness and risk assessment.


This project contains two ways to predict earthquake damage based on structural data:
1. **Web Dashboard**: A modern, interactive Next.js application.
2. **Desktop App**: A lightweight Python application using Tkinter.

---

## 🚀 1. Web Dashboard (Recommended)

### Prerequisites
- [Node.js](https://nodejs.org/) (v18 or higher recommended)

### Setup & Run
1. Open your terminal in the `richter-web-2` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🖥️ 2. Desktop Application

### Prerequisites
- [Python 3.x](https://www.python.org/)

### Setup & Run
1. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python desktop_app.py
   ```

---

## 📊 Project Structure
- `richter-web-2/`: Source code for the Next.js web application.
- `desktop_app.py`: Python script for the desktop interface.
- `rfc_pipeline.pkl`: The trained machine learning model (Required for both apps).
- `requirements.txt`: Python dependency list.

---

## 💡 Notes for Distribution
- **Important**: Ensure `rfc_pipeline.pkl` is in the same directory as `desktop_app.py` when running the desktop version.
- **Node Modules**: When sending the folder to someone else, you can delete the `richter-web-2/node_modules` folder to save space. The recipient will recreate it using `npm install`.
