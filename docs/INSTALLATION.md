# Installation Guide - LifeBridge AI

This document provides detailed setup instructions for developers and researchers.

---

## 1. Prerequisites
- Python 3.12+
- Node.js 18+
- Git

---

## 2. Local Backend Installation
1. Clone the repository.
2. Initialize virtual environment:
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate   # On Windows
   source .venv/bin/activate # On Unix
   ```
3. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Set environment variables:
   Create a `.env` file in `backend/` and add:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
5. Launch FastAPI:
   ```bash
   python app/main.py
   ```

---

## 3. Local Frontend Installation
1. Install Node modules:
   ```bash
   cd frontend
   npm install
   ```
2. Start development server:
   ```bash
   npm run dev
   ```
   *Visit the app at `http://localhost:3000`.*
