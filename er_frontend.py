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

# --- HELPER: GET NEXT ID ---
def get_next_patient_id():
    if not os.path.exists(CSV_FILE):
        return "P101"
    try:
        df = pd.read_csv(CSV_FILE, on_bad_lines='skip')
        if df.empty: return "P101"
        last_id_val = str(df['patient_id'].iloc[-1])
        numbers = re.findall(r'\d+', last_id_val)
        if numbers:
            new_number = int(numbers[-1]) + 1
            prefix = re.match(r'([a-zA-Z]+)', last_id_val)
            prefix_str = prefix.group(1) if prefix else "P"
            return f"{prefix_str}{new_number}"
        return "P101"
    except:
        return "P101"

next_id = get_next_patient_id()

# --- SIDEBAR: MANUAL ENTRY ---
st.sidebar.header("Add Single Patient")
with st.sidebar.form("patient_form", clear_on_submit=True):
    p_id = st.text_input("Patient ID (Auto)", value=next_id, disabled=True)
    sev = st.slider("Severity", 1, 10, 5)
    arr = st.number_input("Arrival Time", min_value=0, step=1)
    dur = st.number_input("Treatment Duration", min_value=1, step=1)
    spec = st.selectbox("Specialization", ["GENERAL", "TRAUMA", "CARDIO", "NEURO"])
    submit_btn = st.form_submit_button("Append Patient")

if submit_btn:
    new_row = pd.DataFrame([[p_id, sev, arr, dur, spec]], 
                            columns=['patient_id', 'severity', 'arrival_time', 'treatment_time', 'required_specialization'])
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'ab+') as f:
            f.seek(0, os.SEEK_END)
            if f.tell() > 0:
                f.seek(-1, os.SEEK_END)
                if f.read(1) != b'\n': f.write(b'\n')
        new_row.to_csv(CSV_FILE, mode='a', header=False, index=False, lineterminator='\n')
    else:
        new_row.to_csv(CSV_FILE, index=False, lineterminator='\n')
    st.sidebar.success(f"Added {p_id}")
    st.rerun()

# --- MAIN AREA: FILE UPLOAD ---
st.subheader("Data Import")
uploaded_file = st.file_uploader("Upload a CSV file (This will replace current data)", type="csv")

if uploaded_file is not None:
    # Read the uploaded file
    try:
        uploaded_df = pd.read_csv(uploaded_file)
        
        # Standardize and save as patients.csv
        uploaded_df.to_csv(CSV_FILE, index=False, lineterminator='\n')
        st.success("File uploaded successfully and saved as 'patients.csv'!")
        st.rerun() # Refresh to show the new data in the table below
    except Exception as e:
        st.error(f"Error processing CSV: {e}")

# --- RESET DATA ---
if st.sidebar.button("🗑️ Reset All Data"):
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)
        st.rerun()

# --- DISPLAY & RUN ---
st.divider()
if os.path.exists(CSV_FILE):
    df_display = pd.read_csv(CSV_FILE, on_bad_lines='skip')
    st.write(f"### Current Patient Queue ({len(df_display)} patients)")
    st.dataframe(df_display, width='stretch')
    
    if st.button("🚀 Run Triage Simulation"):
        try:
            patients_list = [
                Patient(row['patient_id'], row['severity'], row['arrival_time'], 
                        row['treatment_time'], row['required_specialization'])
                for _, row in df_display.iterrows()
            ]
            final_schedule, final_risk = schedule_patients(patients_list)
            
            # Save results
            with open("submission.json", "w") as f:
                json.dump({"treatments": final_schedule, "estimated_total_risk": final_risk}, f, indent=2)

            st.divider()
            c1, c2 = st.columns(2)
            c1.metric("Total System Risk", f"{final_risk}")
            c2.success("Logic complete. submission.json generated.")
            st.table(pd.DataFrame(final_schedule))
        except Exception as e:
            st.error(f"Simulation Error: {e}")
else:
    st.info("Queue is empty. Use the sidebar to add patients or upload a CSV file.")