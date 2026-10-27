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

* **Frontend:** Streamlit (Python-based Web Framework).
* **Data Handling:** Pandas (CSV parsing and state management).
* **Algorithm:** Python `heapq` (Min-heap for $O(\log n)$ priority queueing).
* **Data Format:** JSON (Standardized competition output).

---

## 📂 Project Structure

```text
├── er_frontend.py    # The Streamlit UI application
├── verify.py         # Backend logic (Scheduling algorithm & Patient class)
├── patients.csv      # Local database (Auto-generated/Appended)
├── submission.json   # Output file for judge verification
└── README.md         # Documentation

Input and Output
~Input
The system accepts patient information through manual registration or CSV import.

Typical scheduling inputs include:
-Patient identifier
-Clinical severity or risk weight
-Estimated treatment duration
-Required medical specialization, where applicable
The exact column names and required fields must match the application's implementation.

~Output
The application generates a submission.json file containing:
-The resulting treatment schedule
-The total risk score calculated by the implementation
The precise JSON schema and risk-score formula are determined by the backend code in verify.py.

Conclusion:
The Smart ER Triage & Risk Management System improves emergency room efficiency through intelligent patient scheduling. It uses Smith’s Rule to prioritize patients based on severity and treatment duration. The Streamlit dashboard provides real-time monitoring of the patient queue and system metrics. Automated patient ID generation and CSV management ensure reliable data handling. Specialization mapping helps assign patients to suitable doctors and optimize resource utilization. JSON export enables easy evaluation of treatment schedules and total risk scores. Overall, this system supports faster, more organized emergency care while keeping clinical judgment and patient safety as the top priorities.