# **AX-CPT Eye Tracking Data Processing**

This repository contains scripts for processing **eye-tracking data** collected during an **AX-CPT (AX Continuous Performance Task)** experiment. The study examines **proactive cognitive control** using **ocular measures** and is based on research conducted by **Jason F. Reimer (PI)**.

## **Overview**
The scripts process eye-tracking data collected using a **Tobii eye-tracker** and recorded in **Inquisit (Millisecond Software)**. The output provides **aggregated trial data** with metrics such as:
- **Visit counts** for specific Areas of Interest (AOIs)
- **Total visit duration (TVD)**
- **Time to first fixation**
- **Proportion of trials with first fixations in specific AOIs**
- **Correct and incorrect trials analysis**

The tasks are adapted for **Windows & MacOS** and handle both:
- **Gaze data files** (non-XLSX)
- **Excel-based files** (XLSX)

## **Repository Structure**
```
📂 1_ALL_TRIALS_nonxlsx/        # Outputs all trials data (gaze files as input)
📂 2_ALL_TRIALS_xlsx/           # Outputs all trials data (XLSX files as input)
    ├── Windows/                # Windows-compatible script
    ├── MacOS/                  # Mac-compatible script
📂 3_CORRECT_TRIALS_ONLY_nonxlsx/  # Outputs only correct trials (gaze files as input)
📂 4_CORRECT_TRIALS_ONLY_xlsx/      # Outputs only correct trials (XLSX input)
    ├── Windows/
    ├── MacOS/
📂 output/                      # Stores processed results
📂 scripts/                      # Python processing scripts
📄 README.md                    # Documentation (this file)
📄 requirements.txt              # Dependencies for the Python scripts
```

## **Study Context**
The study titled:
> **"Ocular Measures of Controlled Processing: Examining the Role of Cue Maintenance and Working Memory Capacity in Proactive Cognitive Control"**  
> **PI: Jason F. Reimer, California State University, San Bernardino**  

examines **how eye movement patterns during the cue-probe delay of the AX-CPT** reflect **proactive control engagement**.

### **Key Findings**
- **Eye movement patterns** predict proactive control and the ability to **override prepotent responses**.
- **Cue maintenance** (measured via **fixations on cue-related AOIs**) can be a **biomarker of proactive control**.
- **Working memory capacity (WMC) and proactive control** appear to be **independent cognitive processes**.

## **Data Collection**
- **Tobii Eye Tracker** (60 Hz sampling rate, 0.35° resolution, 0.5° accuracy)
- **5-Point Calibration** for each participant using **Tobii Studio software**
- **Eye-tracking data extraction** via **Tobii Studio & Python scripts**
- Data includes:
  - **Fixation counts, durations, first fixation latency**
  - **Gaze positions for AOIs (cue, top probe, bottom probe)**

## **Usage**
### **Running the Scripts**
1. Place **input files** into the correct subfolders:
   - **Gaze data files** → `1_ALL_TRIALS_nonxlsx/` or `3_CORRECT_TRIALS_ONLY_nonxlsx/`
   - **Excel-based files (XLSX)** → `2_ALL_TRIALS_xlsx/` or `4_CORRECT_TRIALS_ONLY_xlsx/`
  
2. Run the corresponding script from the `scripts/` folder:
   ```sh
   python main.py
   ```

3. Processed **output files** will be stored in the `/output/` folder.

### **File Paths in Scripts**
Each script defines:
```python
excel_input_path = "./!INPUT//"  # Location of Excel files
csv_input_path = "./!CONVERTED_INPUT//"  # Temporary folder for converted CSVs
output_path = "./!OUTPUT//"  # Final results location
```
Ensure the correct **input files** are placed before running the script.

## **Dependencies**
To install required Python libraries:
```sh
pip install -r requirements.txt
```

## **Acknowledgments**
This project is based on the **AX-CPT study on proactive cognitive control** and was developed as part of **research conducted at California State University, San Bernardino**.
