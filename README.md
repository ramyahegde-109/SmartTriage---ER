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


Core Logic & Algorithmic Strategy
=================================

The Smart ER Triage system is built on a specialized scheduling strategy designed to minimize **Risk Accumulation**. Below is the breakdown of the mathematical and logical principles used in verify.py.

1\. The Optimization Goal
-------------------------

The objective is to minimize the **Estimated Total Risk (ETR)**, defined as:

$$\\text{ETR} = \\sum\_{i=1}^{n} (\\text{Start Time}\_i - \\text{Arrival Time}\_i) \\times \\text{Severity}\_i$$

In scheduling theory, this is known as minimizing the **Weighted Sum of Completion Times**.

2\. The Strategy: Smith's Rule (WSPT)
-------------------------------------

To achieve the lowest possible risk score, we use the **Weighted Shortest Processing Time (WSPT)** logic. Instead of just looking at severity, we look at the "Risk Density" of each patient.

### The Formula

Every time a doctor becomes available, the system calculates a priority score for all waiting patients:

$$\\text{Priority Score} = \\frac{\\text{Severity}}{\\text{Treatment Time}}$$

### Why it works:

*   **High Severity + Short Time:** These patients are handled immediately. They carry high risk, and clearing them quickly stops their "risk clock" without keeping the doctor busy for long.
    
*   **High Severity + Long Time:** Even if a patient is critical, if they require a very long surgery, the system may prioritize 2–3 "quicker" high-severity patients first to prevent the total risk of the queue from exploding.
    

3\. Data Structures & Efficiency
--------------------------------

The application manages the patient flow using a **Priority Queue (Min-Heap)**.

*   **Heap Logic:** We store patients in a heap using the negative of their priority score ($-\\text{Score}$). Because Python’s heapq is a min-heap, this ensures the highest priority patient is always at the top ($O(\\log n)$ efficiency).
    
*   **Tie-breaking:** If two patients have the exact same priority score, the system defaults to the **earlier Arrival Time** to ensure fairness.
    

4\. Doctor Assignment Logic
---------------------------

The system handles four doctors with a specific hierarchy to ensure maximum **Future Flexibility**:

**Doctor TypeLogicSpecialists (Trauma, Cardio, Neuro)**Prioritized for their specific match. If a Specialist is free, they MUST take their matching patient first.**Generalist**The "Flex Resource." Only assigned a patient if no specialist is available or if a patient's requirement is "GENERAL."

> **The "Conservation of Specialists" Rule:** > We sort the available doctors so that the Generalist is the **last** to be picked. This keeps the Generalist free as long as possible in case a patient with a different specialization arrives unexpectedly.

5\. Implementation Details
--------------------------

*   **Event-Based Simulation:** The logic doesn't iterate second-by-second. It "jumps" between events (new arrivals or doctors becoming free) to ensure high performance even with thousands of patients.
    
*   **Sequential IDs:** To maintain data integrity for the judges, the UI automatically reads the last line of patients.csv and uses Regex to increment the serial number (e.g., P105 → P106).
    
*   **Submission Formatting:** The final output is automatically sorted by start\_time to comply with competition requirements.