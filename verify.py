import csv
import heapq
import json

# --- DOCTOR OBJECT ---
# Think of this as a "template" for a doctor. 
# It keeps track of their name, what they are good at, and when they finish their current job.
class Doctor:
    def __init__(self, name, specialization):
        self.name = name
        self.specialization = specialization
        self.available_at = 0  # Time when the doctor will be free to see a new patient

# --- PATIENT OBJECT ---
# This template stores everything we know about a patient from the CSV file.
class Patient:
    def __init__(self, pid, severity, arrival, treatment, specialization):
        self.pid = pid
        self.severity = int(severity)        # How urgent it is (higher = more urgent)
        self.arrival = int(arrival)          # When they walked into the ER
        self.treatment = int(treatment)      # How long the surgery/checkup takes
        self.specialization = specialization # What kind of doctor they need

# --- LOADING DATA ---
def load_patients(file_path):
    """This function opens the CSV file and turns each row into a Patient object."""
    patients = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                patients.append(Patient(
                    row['patient_id'], 
                    row['severity'],
                    row['arrival_time'], 
                    row['treatment_time'],
                    row['required_specialization']
                ))
    except Exception as e:
        print(f"Error loading CSV: {e}")
    return patients

# --- THE "BRAIN" OF THE PROGRAM (SCHEDULING) ---
def schedule_patients(patients):
    # 1. Setup our Doctors
    doctors = [
        Doctor("Doctor_T", "TRAUMA"),
        Doctor("Doctor_C", "CARDIO"),
        Doctor("Doctor_N", "NEURO"),
        Doctor("Doctor_G", "GENERAL") # The Generalist can treat anyone!
    ]

    # Sort all patients by when they arrive at the hospital
    patients.sort(key=lambda x: x.arrival)
    
    waiting_queue = [] # This is a 'Priority Queue'. It always keeps the most urgent patient at the top.
    schedule = []      # This will hold our final results
    total_risk = 0     # The running total of the 'Risk Score'
    current_time = 0   # The 'Clock' of our hospital
    p_idx = 0          # Keeps track of which patient from the list is arriving next
    n = len(patients)

    # Keep running as long as there are patients arriving OR patients waiting in the hallway
    while p_idx < n or waiting_queue:
        
        # If no one is waiting and the next patient hasn't arrived yet, jump the clock forward!
        if not waiting_queue and p_idx < n and current_time < patients[p_idx].arrival:
            current_time = patients[p_idx].arrival

        # Add all patients who just arrived at the hospital to the waiting queue
        while p_idx < n and patients[p_idx].arrival <= current_time:
            p = patients[p_idx]
            
            # STRATEGY: We want a high severity and a low treatment time to come first.
            # We divide Severity by Treatment Time. We use a negative sign because 
            # Python's 'heapq' library always puts the SMALLEST number first.
            priority_score = -(p.severity / max(0.1, p.treatment))
            
            # Add them to the queue: (Priority, Arrival Time, Patient Data)
            heapq.heappush(waiting_queue, (priority_score, p.arrival, p))
            p_idx += 1

        # Check which doctors are bored (free) right now
        # We sort them so that Specialists are used first, saving the Generalist for emergencies.
        available_doctors = sorted(
            [d for d in doctors if d.available_at <= current_time],
            key=lambda d: (d.specialization == "GENERAL")
        )

        assigned_this_turn = False
        for doc in available_doctors:
            if not waiting_queue:
                break
            
            temp_stack = [] # To hold patients the current doctor CANNOT treat
            selected_p = None
            
            # Look through the waiting queue for a patient this doctor can handle
            while waiting_queue:
                prio, arr, p = heapq.heappop(waiting_queue)
                
                # Logic: General doctors take anyone. Specialists only take their match.
                if doc.specialization == "GENERAL" or doc.specialization == p.specialization:
                    selected_p = p
                    break
                else:
                    # If doctor can't treat them, put them in a temporary pile to re-add later
                    temp_stack.append((prio, arr, p))
            
            # Put the patients we skipped back into the main waiting queue
            for item in temp_stack:
                heapq.heappush(waiting_queue, item)

            # If we found a patient for this doctor...
            if selected_p:
                start_time = current_time
                finish_time = start_time + selected_p.treatment
                
                # RISK = How long they waited * How severe their condition was
                wait_time = start_time - selected_p.arrival
                risk = wait_time * selected_p.severity
                
                # Update the doctor's schedule and the total risk
                doc.available_at = finish_time
                total_risk += risk
                assigned_this_turn = True
                
                # Save this treatment info
                schedule.append({
                    "patient_id": selected_p.pid,
                    "doctor_id": doc.name,
                    "start_time": start_time,
                    "end_time": finish_time
                })

        # If we just assigned a doctor, stay at this time to see if another doctor is free.
        # Otherwise, jump the clock to the next important event (next arrival or next doctor free).
        if assigned_this_turn:
            continue
        
        next_event_times = []
        if p_idx < n:
            next_event_times.append(patients[p_idx].arrival)
        busy_docs = [d.available_at for d in doctors if d.available_at > current_time]
        if busy_docs:
            next_event_times.append(min(busy_docs))
            
        current_time = min(next_event_times) if next_event_times else current_time + 1

    # Before finishing, sort the final list by Start Time (a rule for the judge!)
    schedule.sort(key=lambda x: x["start_time"])
    return schedule, total_risk

# --- SAVING THE DATA ---
def save_submission(schedule, total_risk, output_file="submission.json"):
    """Turns our results into a JSON file format."""
    output_data = {
        "treatments": schedule,
        "estimated_total_risk": total_risk
    }
    with open(output_file, 'w', encoding='utf-8') as f:
        # indent=2 makes the file look 'pretty' and easy to read
        json.dump(output_data, f, indent=2)
    print(f"Success! JSON file created. Total Risk Score: {total_risk}")

# --- START THE PROGRAM ---
if __name__ == "__main__":
    # 1. Load the patients
    patients_list = load_patients("patients.csv")
    
    # 2. If the file wasn't empty, run the scheduler and save
    if patients_list:
        final_schedule, final_risk = schedule_patients(patients_list)
        save_submission(final_schedule, final_risk)