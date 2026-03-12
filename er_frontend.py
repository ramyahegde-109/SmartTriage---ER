import streamlit as st
import pandas as pd
import json
import os
import re
from verify import schedule_patients, Patient

# --- UI SETTINGS ---
st.set_page_config(page_title="Smart ER Triage System", layout="wide")
st.title("🏥 Smart ER Triage & Risk Management")

CSV_FILE = "patients.csv"

# --- IMPROVED LOGIC: GET NEXT ID FROM LAST ROW ---
def get_next_patient_id():
    """Reads the last line of the CSV to find the current highest ID."""
    if not os.path.exists(CSV_FILE):
        return "P101" # Default only if file doesn't exist
    
    try:
        # We read only the last few rows to be fast
        df = pd.read_csv(CSV_FILE, on_bad_lines='skip')
        if df.empty:
            return "P101"
        
        # Get the absolute last ID in the 'patient_id' column
        last_id_val = str(df['patient_id'].iloc[-1])
        
        # Use regex to find all digits in the string (e.g., "P105" -> "105")
        numbers = re.findall(r'\d+', last_id_val)
        if numbers:
            # Take the last number found in the string, increment it
            last_number = int(numbers[-1])
            new_number = last_number + 1
            
            # Keep the prefix (e.g., if it was 'P', keep 'P')
            prefix = re.match(r'([a-zA-Z]+)', last_id_val)
            prefix_str = prefix.group(1) if prefix else "P"
            
            return f"{prefix_str}{new_number}"
        
        return "P101" # Fallback if no numbers found
    except Exception:
        return "P101"

# Dynamically calculate the ID for the form
next_id = get_next_patient_id()

# --- SIDEBAR: DATA ENTRY ---
st.sidebar.header("Add Single Patient")
with st.sidebar.form("patient_form", clear_on_submit=True):
    # Disabled so the user cannot manually break the sequence
    p_id = st.text_input("Patient ID (Auto-increment)", value=next_id, disabled=True)
    
    sev = st.slider("Severity", 1, 10, 5)
    arr = st.number_input("Arrival Time", min_value=0, step=1)
    dur = st.number_input("Treatment Duration (mins)", min_value=1, step=1)
    spec = st.selectbox("Specialization", ["GENERAL", "TRAUMA", "CARDIO", "NEURO"])
    submit_btn = st.form_submit_button("Append Patient")

if submit_btn:
    new_data = pd.DataFrame([[p_id, sev, arr, dur, spec]], 
                            columns=['patient_id', 'severity', 'arrival_time', 'treatment_time', 'required_specialization'])
    
    # Ensure a fresh line for the append
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'ab+') as f:
            f.seek(0, os.SEEK_END)
            if f.tell() > 0:
                f.seek(-1, os.SEEK_END)
                if f.read(1) != b'\n':
                    f.write(b'\n')
        new_data.to_csv(CSV_FILE, mode='a', header=False, index=False, lineterminator='\n')
    else:
        new_data.to_csv(CSV_FILE, index=False, lineterminator='\n')
    
    st.sidebar.success(f"Patient {p_id} added!")
    st.rerun() # This triggers the ID calculation for the next entry immediately

# --- RESET LOGIC ---
if st.sidebar.button("🗑️ Reset All Data"):
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)
        st.sidebar.warning("CSV Deleted. Resetting to P101.")
        st.rerun()

# --- MAIN DISPLAY ---
st.subheader("Patient Queue Management")
if os.path.exists(CSV_FILE):
    df_display = pd.read_csv(CSV_FILE, on_bad_lines='skip')
    st.dataframe(df_display, width='stretch')
    
    if st.button("🚀 Run Triage Simulation"):
        try:
            # Convert UI rows to Logic objects
            patients_list = [
                Patient(row['patient_id'], row['severity'], row['arrival_time'], 
                        row['treatment_time'], row['required_specialization'])
                for _, row in df_display.iterrows()
            ]
            
            # Import and run from verify.py
            final_schedule, final_risk = schedule_patients(patients_list)
            
            # Show Results
            st.divider()
            c1, c2 = st.columns(2)
            c1.metric("Total System Risk", f"{final_risk}")
            c2.success("Logic execution complete.")
            
            st.write("### Calculated Schedule")
            st.table(pd.DataFrame(final_schedule))
            
        except Exception as e:
            st.error(f"Error calling verify.py: {e}")
else:
    st.info("The queue is currently empty.")