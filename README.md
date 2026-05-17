# University Hall Booking

A lightweight, real-time desktop application designed for university class representatives to manage and book lecture and tutorial halls. Built with a focus on speed and simplicity, the interface is inspired by the minimalist, high-contrast design philosophy of Lichess.

## Features

* **Real-Time Booking:** Integrates with Firebase Cloud Firestore to instantly update hall availability and prevent double-booking overlaps.
* **Minimalist UI:** A distraction-free, grid-based layout for quick decision-making.
* **Theme Support:** Native toggle for Lichess-inspired Light and Dark modes.
* **Lightweight Footprint:** Built cleanly with PyQt6 to avoid UI freezing and heavy resource consumption.

## Technology Stack

* **Language:** Python 3
* **GUI Framework:** PyQt6
* **Database / Backend:** Firebase Admin SDK (Cloud Firestore)

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/hall-registry-app.git](https://github.com/YOUR-USERNAME/hall-registry-app.git)
   cd hall-registry-app

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   
3. **Add Firebase Credentials:**
   * Obtain your `serviceAccountKey.json` from your Firebase project console.
   * Place the file directly in the root directory of this project. 
   * *Note: This file is tracked in `.gitignore` to prevent accidental uploads of secure credentials.*

4. **Run the application:**
   ```bash
   python main.py
