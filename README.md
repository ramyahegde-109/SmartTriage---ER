# 🏥 Smart ER Triage & Risk Management System

An AI-driven Emergency Room (ER) scheduling application designed to minimize patient risk through optimized resource allocation. This system uses **Smith's Rule (Weighted Shortest Processing Time)** to dynamically prioritize patients based on severity and treatment duration.

---

## 🚀 Features

* **Smart Triage Logic:** Implements an optimized scheduling algorithm that balances medical urgency ($Severity$) against clinical efficiency ($Treatment Time$).
* **Live Dashboard:** A real-time Streamlit UI to monitor the current patient queue and system metrics.
* **Automated ID Management:** Sequential Patient ID generation (e.g., P101, P102) that reads the last entry of the CSV and increments it automatically, preventing manual entry errors.
* **Flexible Data Entry:** Supports bulk CSV uploads or single-patient manual entry with robust "new-line" data protection to prevent file corruption.
* **Specialization Mapping:** Intelligently assigns patients to specialized doctors (Trauma, Cardio, Neuro) or Generalists to maximize ER throughput.
* **JSON Export:** Automatically generates a `submission.json` file containing the optimized treatment schedule and total risk score.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit (Python-based Web Framework)
* **Data Handling:** Pandas (CSV parsing and state management)
* **Algorithm:** Python `heapq` (Min-heap for $O(\log n)$ priority queueing)
* **Data Format:** JSON (Standardized competition output)

---

## 📂 Project Structure

```text
├── er_frontend.py    # The Streamlit UI application
├── verify.py         # Backend logic (Scheduling algorithm & Patient class)
├── patients.csv      # Local database (Auto-generated/Appended)
├── submission.json   # Output file for judge verification
└── README.md         # Documentation