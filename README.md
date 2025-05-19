# **AX-CPT Eye Tracking Data Processing**

This repository (https://github.com/DylanDiaz101/AXCPT-GazeAnalysis) contains scripts for processing **eye-tracking data** collected during an **AX-CPT (AX Continuous Performance Task)** experiment. The study examines **proactive cognitive control** using **ocular measures** and is based on research conducted by **Jason F. Reimer (PI)**. 
> Link to Open Science Framework (OSF) repository of study: https://osf.io/z69pq/

## **Overview**
The scripts process eye-tracking data collected using a **Tobii eye-tracker**. The output provides **aggregated trial data** with metrics such as:

- **Visit counts** for specific **Areas of Interest (AOIs)**, including top and bottom probe fixation points.
- **Total Visit Duration (TVD)**, measured in seconds for each AOI during the cue-probe delay.
- **Time to First Fixation**, indicating how quickly participants looked at key AOIs (e.g., bottom-right probe in BX trials).
- **Proportion of trials with first fixations in specific AOIs**, reflecting proactive vs. reactive control strategies.
- **Correct and incorrect trials analysis**, allowing comparisons between performance and gaze behavior.

The data output includes **trial-level** and **aggregated task-level** metrics that help quantify how participants engaged in **proactive cognitive control** based on their eye movement patterns.

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
📂 5_TVD_Visits_Within_Correct_Trials_Scripts  # Outputs trial level data for TVD and AOI Visit Counts for correct trials (cue and probe conditions)
    ├── Windows_XLSX/
    ├── Windows_NON_XLSX/
📄 README.md                    # Documentation (this file)
📄 requirements.txt              # Dependencies for the Python scripts
```

## **Study Context**
The study titled:
> **"Ocular Measures of Controlled Processing: Examining the Role of Cue Maintenance and Working Memory Capacity in Proactive Cognitive Control"**  
> **PI: Jason F. Reimer, California State University, San Bernardino**  
examines **how eye movement patterns during the cue-probe delay of the AX-CPT** reflect **proactive control engagement**.

> OSF: https://osf.io/z69pq/

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
   - **Gaze data files** → `1_ALL_TRIALS_nonxlsx/` or `3_CORRECT_TRIALS_ONLY_nonxlsx/` into `/!INPUT`
   - **Excel-based files (XLSX)** → `2_ALL_TRIALS_xlsx/` or `4_CORRECT_TRIALS_ONLY_xlsx/` into `/!INPUT`
  
2. Run the corresponding script (recommended to run using Python IDLE):
   ```sh
   python main.py
   ```

3. Processed **output files** will be stored in the `/!OUTPUT/` folder.

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
This project is based on the AX-CPT study on proactive cognitive control and was developed as part of research conducted at California State University, San Bernardino's Learning Research Institute (LRI) under the Department of Psychology.

For further correspondence: jreimer@csusb.edu
