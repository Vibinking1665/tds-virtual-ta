# Virtual TA for IITM BSc Discourse Forum

This project is a Virtual Teaching Assistant (TA) that answers student questions by searching relevant answers from the IITM BSc Discourse Forum. Built using **FastAPI** for the backend and **React** for the frontend.

---

## 🚀 Live Demo

- 🔗 **Backend API (FastAPI on Render):** [https://tds-virtual-ta-rczb.onrender.com](https://tds-virtual-ta-rczb.onrender.com)
- 📄 **API Docs:** [https://tds-virtual-ta-rczb.onrender.com/docs](https://tds-virtual-ta-rczb.onrender.com/docs)

---

## 🧠 Features

- Accepts user queries via POST request
- Matches the most relevant Discourse posts using text similarity
- Returns a clear answer + top 3 matching links
- Strips HTML from forum answers for clean display
- Frontend connected via fetch to backend API
- Deployed via **Render** (backend) and **local frontend** (React)

---

## 📦 Project Structure

