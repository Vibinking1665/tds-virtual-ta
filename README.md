# 🧠 TDS Virtual TA

A **Virtual Teaching Assistant** API built using **FastAPI** to automatically respond to student questions from the **TDS (Tools for Data Science)** course of IIT Madras Online Degree program.

This project uses scraped posts from the [TDS Discourse Forum](https://discourse.onlinedegree.iitm.ac.in/) (between **Jan 1, 2025 – Apr 14, 2025**) to generate responses.

---

## 📦 Features

- 🔍 Matches questions using text similarity
- 🔗 Returns top 3 relevant Discourse links
- 🖼️ Supports optional image input (Base64 encoded)
- ⚡ FastAPI-based lightweight backend
- 🧹 Strips HTML content from forum posts

---

## 🛠️ Tech Stack

- Python 🐍
- FastAPI ⚡
- Uvicorn (for ASGI server)
- Requests (for scraping)
- difflib & regex (for matching & cleanup)

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/Vibinking1665/tds-virtual-ta.git
cd tds-virtual-ta
