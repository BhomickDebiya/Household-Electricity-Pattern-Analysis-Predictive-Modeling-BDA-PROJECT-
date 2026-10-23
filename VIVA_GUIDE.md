# Big Data Analytics Lab — Viva Defense Guide
### **Household Electricity Pattern Analysis & Predictive Modeling**
**Students:** Bhomick Debiya (Roll 32), Shorya Chilate  
**Course:** Big Data Analytics Lab (V-Semester, CSE AI & Data Science)

---

## 1. Core Architectural Questions

### Q1: Why use both Hadoop MapReduce AND Apache Spark in this project?
- **Answer**:
  - **Hadoop MapReduce** is an immutable, disk-based, batch processing framework. It is resilient, has a very low memory footprint, and excels at long-running batch aggregations that exceed physical cluster RAM. In our project, MapReduce serves as the reliable batch aggregation engine to compute exact 24-hour baseline active power averages.
  - **Apache Spark** is an in-memory distributed engine that executes operations via Directed Acyclic Graphs (DAGs) and in-memory Resilient Distributed Datasets (RDDs / DataFrames). It is up to 100x faster for multi-pass iterative jobs, complex feature engineering, correlation analysis, and machine learning pipelines.
  - Using both allows **Cross-Engine Verification**: we prove that both engines arrive at the exact same hourly aggregates (**delta = 0.000000 kW**), validating data processing integrity.

---

### Q2: What is HDFS, and what are the roles of NameNode and DataNode?
- **Answer**:
  - **HDFS (Hadoop Distributed File System)** is a distributed file system designed to run on commodity hardware with high fault tolerance and streaming data access patterns.
  - **NameNode (Master)**: Maintains the filesystem directory tree, namespace, file metadata, access permissions, and maps data blocks to DataNodes in memory. It does not store actual data.
  - **DataNode (Worker)**: Stores the actual physical 128 MB blocks on local disk, performs block creation, deletion, and replication upon NameNode instruction, and sends periodic Heartbeats (every 3 seconds) and Block Reports.

---

### Q3: Explain the MapReduce Execution Lifecycle in this project.
- **Answer**:
  1. **Input Split & Record Reader**: The 132.9 MB file in HDFS is split into splits. The `LineRecordReader` emits `(ByteOffset, LineText)`.
  2. **Map Phase (`HourlyElectricityMapper`)**:
     - Splits each line by semicolon (`;`).
     - Filters out header and rows with missing readings (`?`).
     - Extracts the hour (00-23) from the timestamp string.
     - Emits key-value pairs: `Key = Text(Hour)`, `Value = DoubleWritable(Global_active_power)`.
  3. **Shuffle & Sort Phase**:
     - Hadoop framework automatically partitions the mapper output by key using `HashPartitioner`.
     - Intermediate pairs are sorted and transferred across the network to reducers so all values for the same hour arrive at the same reducer.
  4. **Reduce Phase (`HourlyElectricityReducer`)**:
     - Iterates over the list of power values for each hour.
     - Calculates $\text{Average Power} = \frac{\sum \text{Power}}{\text{Count}}$.
     - Emits `(Hour, Average_Power_kW \t Count)`.
  5. **Output**: Stored in HDFS at `/bda_electricity/output/mr_hourly_results/part-r-00000`.

---

### Q4: Why can't we use a simple Combiner to calculate Average directly?
- **Answer**:
  - Mathematical reason: **Average is not an associative or commutative algebraic operation** ($\text{Avg}(A, B, C) \neq \text{Avg}(\text{Avg}(A, B), C)$).
  - If a Combiner averaged intermediate values, small mapper splits would be weighted equally with large splits, causing mathematical distortion.
  - To use a combiner for averaging, the intermediate value must be a tuple `(sum, count)`, not the raw average.

---

### Q5: What is Apache Cassandra, and why was it included in the architecture?
- **Answer**:
  - **Apache Cassandra** is a highly scalable, distributed NoSQL column-family database built on a masterless peer-to-peer ring architecture with no single point of failure.
  - Neither HDFS (append-only batch storage) nor Spark (processing engine) is suitable for low-latency single-row point lookups or concurrent real-time web serving.
  - In our architecture, Cassandra stores pre-computed hourly/daily aggregated summaries and real-time inference audit logs for sub-millisecond retrieval by the Gradio web dashboard.

---

### Q6: How does Cassandra ensure fault tolerance without a Master (unlike HDFS NameNode)?
- **Answer**:
  - Cassandra uses a **Peer-to-Peer Ring** topology based on consistent hashing (Murmur3Partitioner).
  - Data is replicated across multiple nodes using the **Gossip Protocol** to discover node health.
  - Tunable consistency levels (ONE, QUORUM, ALL) allow fine-tuning between latency and strong consistency ($R + W > N$).

---

### Q7: Explain the Machine Learning Prediction Model and Metrics.
- **Answer**:
  - **Algorithm**: `RandomForestRegressor` (`n_estimators=50`, `max_depth=10`).
  - **Target**: `Global_active_power` (kW).
  - **Features**: `Hour` (0-23), `Month` (1-12), `DayOfWeek` (One-hot encoded).
  - **Data Leakage Prevention**: We excluded simultaneous electrical variables (`Global_intensity`, `Voltage`, `Sub_metering`) because they are consequences of active power, not future inputs available at prediction time.
  - **Metrics**:
    - **MAE**: 0.6051 kW (average absolute error in load prediction).
    - **RMSE**: 0.8793 kW (penalizes large outlier mistakes).
    - **Baseline Model RMSE**: 1.0572 kW.
    - **Improvement over Baseline**: **16.83% error reduction**.
    - **R² Score**: 0.3082 on fine-grained minute-level variance.

---

## 2. Key Analytical Insights to Mention to the Examiner

1. **Evening Peak Window (19:00 - 21:00 hrs)**:
   - Consumption peaks at **~1.899 kW**. Driven by household evening activities: lighting, cooking, dishwashing, and television.
2. **Night Base Load (02:00 - 05:00 hrs)**:
   - Consumption drops to its minimum at **~0.443 kW**. This is the non-discretionary "vampire" load: refrigerators, clocks, and idle appliances.
3. **Appliance Energy Consumption Breakdown**:
   - **Climate Control (Sub_metering_3)** accounts for **72.7%** of sub-metered power.
   - **Laundry Room (Sub_metering_2)** accounts for **14.6%**.
   - **Kitchen (Sub_metering_1)** accounts for **12.6%**.
4. **Current vs Active Power Correlation**:
   - Pearson correlation is **+0.999**, verifying Ohm's law ($P = V \times I \times \cos \phi$).
5. **Voltage Inversion**:
   - Voltage shows an inverse correlation (**-0.40**) with power draws, reflecting transmission grid loading voltage drops during peak hours.

---

## 3. High-Priority Commands to Remember

```bash
# 1. Check active Java/Hadoop processes:
jps

# 2. View HDFS root and project files:
hdfs dfs -ls /bda_electricity/input
hdfs dfs -cat /bda_electricity/output/mr_hourly_results/part-r-00000

# 3. Check HDFS health & blocks:
hdfs fsck /bda_electricity/input -files -blocks

# 4. Run the MapReduce job:
hadoop jar hourly_electricity.jar HourlyElectricityDriver /bda_electricity/input/household_power_consumption.txt /bda_electricity/output/mr_hourly_results

# 5. Launch Spark pipeline:
python run_spark_pipeline.py

# 6. Launch Gradio web UI:
python app.py
```
