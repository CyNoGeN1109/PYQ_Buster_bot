# 📚 PYQ Telegram Bot (India)

A Telegram bot built to solve a common problem faced by students across India —  
**difficulty in finding organized, reliable, and easily accessible Previous Year Question Papers (PYQs)** for competitive exams.

This project currently focuses on **NEET PYQs** and is designed as a **strong foundation** for a much larger exam-preparation platform in the future.

---

## ❓ Problem Statement

Students preparing for competitive exams like **NEET** often face the following issues:

- Question papers are scattered across multiple websites and Telegram channels  
- No single, organized place to find papers year-wise or set-wise  
- Too many fake, incomplete, or poorly scanned PDFs  
- Last-minute preparation becomes stressful due to poor accessibility  

Finding the *right paper at the right time* becomes harder than solving the questions themselves.

---

## ✅ Solution

This project solves the problem by providing:

- A **Telegram-based interface** (no new app required)
- A **guided button-based flow** to select exam → year → paper
- **Instant delivery** of PDFs using Telegram’s `file_id` system
- A **secure admin mode** to manage and extract new papers

The goal is to make PYQs **simple, fast, and distraction-free** for students.

---

## 🚀 Features

### 👨‍🎓 Student Mode (Default)
- `/start` command to begin
- Interactive buttons (no typing needed)
- Select exam → year → paper/set
- Receive the required PDF instantly
- Clean and minimal user experience

### 👑 Admin Mode (Protected)
- Password-based admin login
- Extract `file_id` from any uploaded PDF
- Helps maintain a controlled and scalable paper database
- Admin features are completely hidden from normal users

---

## 📌 Current Exam Coverage

### 🇮🇳 National Exams
- **NEET**
  - 2017: Set A, B, C, D
  - 2018 – 2025: Single paper per year

> More exams will be added in future versions.

---

## 🧠 Key Technical Concepts Used

- Telegram Bot API
- Inline keyboards for navigation
- Separation of **admin logic** and **student logic**
- Telegram `file_id` reuse (fast & efficient delivery)
- Virtual environments for dependency isolation
- Clean, modular Python code

---

## 🛠️ Tech Stack

- **Python 3.12**
- **python-telegram-bot v20.7**
- Telegram Bot API

---

## 📂 Project Structure

```text
pyq-telegram-bot/
│
├── pyq_bot.py          # Main bot logic
├── bot_token.py        # Stores Telegram bot token (ignored in Git)
├── requirements.txt    # Project dependencies
├── README.md           # Documentation
└── venv/               # Virtual environment (not committed)
