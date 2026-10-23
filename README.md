# Household Electricity Pattern Analysis & Predictive Modeling
### **Big Data Analytics Lab (V-Semester, CSE AI & Data Science)**
**Course:** Big Data Analytics Lab  
**Project Members:**
- **Bhomick Debiya** — Roll Number: 32
- **Shorya Chilate**

---

## 1. Project Architecture

This project implements an end-to-end distributed Big Data Analytics pipeline analyzing over **2 million smart-meter power readings** (132.9 MB) from the UCI Individual Household Electric Power Consumption dataset.

```
+---------------------------------------------------------------------------------------------------+
|                                 RAW DATASET (132.9 MB, 2,075,260 records)                         |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 1. HDFS (Hadoop Distributed File System)                                                          |
|    - Storage: /bda_electricity/input/household_power_consumption.txt                              |
|    - Cluster Daemons: NameNode (Port 9000 metadata) & DataNode (data blocks)                      |
+---------------------------------------------------------------------------------------------------+
                         |                                                  |
                         v                                                  v
+---------------------------------------------------+  +--------------------------------------------+
| 2. Hadoop MapReduce (Batch Aggregation)           |  | 3. Apache Spark / PySpark (Interactive Engine)|
|    - Input: HDFS Raw Split                        |  |    - Schema-enforced DataFrame ingestion   |
|    - Mapper: Filters nulls, extracts Hour         |  |    - In-memory distributed transformations |
|    - Shuffle & Sort: Key partitioning by Hour     |  |    - Multi-dimensional aggregations        |
|    - Reducer: Computes 24-hr Average Active Power |  |    - Random Forest Machine Learning Model  |
|    - Output: /bda_electricity/output              |  |    - Dual-engine cross validation          |
+---------------------------------------------------+  +--------------------------------------------+
                         |                                                  |
                         +------------------------+-------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 4. Apache Cassandra (Distributed NoSQL Storage)                                                   |
|    - Keyspace: bda_electricity | Tables: hourly_aggregates, model_predictions                     |
|    - Status: Live Port 9042 connector with automatic graceful local JSON persistence fallback     |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 5. Gradio Interactive Web Interface                                                               |
|    - Visual Analytics: 24-hr load curves, weekend vs weekday patterns, correlation heatmap       |
|    - Dual-Engine Validation View: Spark vs MapReduce side-by-side comparison                      |
|    - AI Forecasting: Real-time demand inference with evaluated held-out test metrics              |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Technology Stack & Responsibilities

| Technology | Role & Responsibility in Project |
| :--- | :--- |
| **HDFS** | Distributed, fault-tolerant storage for raw smart-meter readings. Eliminates single disk limits. |
| **Hadoop MapReduce** | Batch disk-based aggregation computing exact 24-hour average active power load. |
| **Apache Spark (PySpark)** | Fast in-memory analytics, temporal feature engineering, sub-metering analysis, and ML sampling. |
| **Cross-Engine Validator** | Compares MapReduce and Spark hourly aggregates to verify mathematical convergence (<0.0001 kW delta). |
| **Apache Cassandra** | Distributed NoSQL column-family database storing analytical summaries and audit logs. |
| **Machine Learning (Scikit-Learn)** | Random Forest Regressor predicting next-hour active power demand (kW). |
| **Gradio** | Demonstration dashboard serving interactive charts, real-time predictions, and viva guides. |

---

## 3. Dataset Placement

The dataset must be placed in the project folder:
`D:\hadoop-project\BDA PROJECT\household_power_consumption.txt`

- **Format**: Semicolon-delimited (`;`) text file.
- **Header**: `Date;Time;Global_active_power;Global_reactive_power;Voltage;Global_intensity;Sub_metering_1;Sub_metering_2;Sub_metering_3`
- **Missing Value Indicator**: `?` (standard UCI notation).
- **Total Records**: 2,075,260 rows (2,049,280 valid clean readings).

---

## 4. Environment Prerequisites

- **OS**: Windows 10/11
- **Java**: Java 8 (`1.8.0_202`) at `D:\BDA\java`
- **Hadoop**: Apache Hadoop 3.2.4 at `D:\BDA\hadoop-3.2.4` with `winutils.exe`
- **Python**: Python 3.11 with `pyspark`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `gradio`, `cassandra-driver`
- **HDFS Daemons**: NameNode running on port 9000, DataNode active.

---

## 5. Execution Guide (One-Click Launchers)

### Step 1: Start Hadoop HDFS (If daemons are not running)
```bash
# In an Administrator or standard command prompt:
D:\BDA\hadoop-3.2.4\sbin\start-dfs.cmd
```
*Verify via `jps` that `NameNode` and `DataNode` are active.*

### Step 2: Run Hadoop MapReduce Job on HDFS
Double-click or run:
```cmd
run_mapreduce.bat
```
*This script uploads the raw dataset to HDFS, compiles the Java MapReduce job, executes it across 2+ million rows, and extracts the 24-hour hourly averages to `mr_hourly_results\`.*

### Step 3: Run the Full Spark Pipeline & ML Training
Run:
```cmd
python run_spark_pipeline.py
```
*This executes data cleaning, temporal feature engineering, computes overall consumption and sub-metering shares, verifies Spark vs MapReduce zero-divergence, trains the Random Forest model, and saves `rf_electricity_model.pkl`.*

### Step 4: Launch the Interactive Gradio Web Dashboard
Double-click or run:
```cmd
run_app.bat
```
*Open your browser at `http://127.0.0.1:7860` to interact with the dashboard.*

### Step 5: Google Colab Deliverable
Upload and run:
`Household_Electricity_Consumption_Analysis.ipynb`
*Self-contained with pip installs, mock/local MapReduce pipeline, Spark processing, Cassandra schemas, ML evaluations, and interactive Gradio tabs.*

---

## 6. Output Files & Locations

- **HDFS Raw Input**: `/bda_electricity/input/household_power_consumption.txt`
- **HDFS MapReduce Output**: `/bda_electricity/output/mr_hourly_results/part-r-00000`
- **Local MapReduce Output**: `D:\hadoop-project\BDA PROJECT\mr_hourly_results\part-r-00000`
- **Trained Model Bundle**: `D:\hadoop-project\BDA PROJECT\rf_electricity_model.pkl`
- **Cassandra Persistence Fallback**: `D:\hadoop-project\BDA PROJECT\storage_fallback\hourly_aggregates_fallback.json`
- **Prediction Audit Logs**: `D:\hadoop-project\BDA PROJECT\storage_fallback\model_predictions_fallback.json`
- **Colab Deliverable**: `D:\hadoop-project\BDA PROJECT\Household_Electricity_Consumption_Analysis.ipynb`
- **PowerPoint Presentation (.pptx)**: `D:\hadoop-project\BDA PROJECT\Household_Electricity_Big_Data_Analytics_Presentation.pptx`
- **Interactive Presentation Deck (.html)**: `D:\hadoop-project\BDA PROJECT\presentation_preview.html`
- **Presentation Assets & Charts**: `D:\hadoop-project\BDA PROJECT\presentation_assets\`

---

## 7. Known Environment Limitations & Honesty Notes

1. **Apache Cassandra**: Cassandra cluster is not locally installed as a Windows service. The code connects to `127.0.0.1:9042` when an external Cassandra instance or Docker container (`docker run -d --name cassandra-bda -p 9042:9042 cassandra:latest`) is started. When offline, the pipeline automatically routes persistence to the clearly labelled `storage_fallback/` JSON repository. We never falsely simulate Cassandra using SQLite or CSV.
2. **Hadoop Windows Spaces**: Hadoop cmd scripts require commands to be invoked with Cwd set to `D:\hadoop-project` or with fully quoted paths to prevent argument parsing errors with directory spaces. All `.bat` launchers are configured accordingly.
