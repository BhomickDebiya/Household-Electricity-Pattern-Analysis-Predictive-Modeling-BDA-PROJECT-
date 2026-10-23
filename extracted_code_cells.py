# ===== CELL 3 =====
# Step 1: Install PySpark if running in Google Colab
try:
    import pyspark
except ImportError:
    !pip install pyspark -q

# Step 3: Import standard libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 4: Import PySpark components
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.functions import (
    col, to_timestamp, concat_ws, hour, month, year,
    date_format, when, avg, min, max, stddev, count, round as spark_round
)

print("Environment setup and imports completed successfully.")


# ===== CELL 5 =====
# Initialize SparkSession
spark = SparkSession.builder \
    .appName("Household_Electricity_Consumption_Analysis") \
    .master("local[*]") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

# Suppress informational log messages
spark.sparkContext.setLogLevel("ERROR")

print("SparkSession initialized:")
print(f" - Spark Version : {spark.version}")
print(f" - Application   : {spark.sparkContext.appName}")
print(f" - Master URL    : {spark.sparkContext.master}")


# ===== CELL 7 =====
# Define exact schema for the dataset
schema = StructType([
    StructField("Date", StringType(), True),
    StructField("Time", StringType(), True),
    StructField("Global_active_power", DoubleType(), True),
    StructField("Global_reactive_power", DoubleType(), True),
    StructField("Voltage", DoubleType(), True),
    StructField("Global_intensity", DoubleType(), True),
    StructField("Sub_metering_1", DoubleType(), True),
    StructField("Sub_metering_2", DoubleType(), True),
    StructField("Sub_metering_3", DoubleType(), True)
])

# Load data into PySpark DataFrame
raw_df = spark.read.csv(
    "household_power_consumption.txt",
    sep=";",
    header=True,
    nullValue="?",
    schema=schema
)

print(f"Total Raw Records Loaded: {raw_df.count():,}")


# ===== CELL 9 =====
# Inspect DataFrame schema
raw_df.printSchema()

# Preview first 5 rows
raw_df.show(5, truncate=False)

# Compute basic descriptive statistics
raw_df.select(
    "Global_active_power",
    "Global_reactive_power",
    "Voltage",
    "Global_intensity"
).describe().show()


# ===== CELL 11 =====
# Count records containing null values in Global_active_power
null_count = raw_df.filter(col("Global_active_power").isNull()).count()
print(f"Records with missing values: {null_count:,}")

# Drop rows with null values
df_clean = raw_df.dropna()

# Verify row count after cleaning
clean_count = df_clean.count()
print(f"Clean records remaining    : {clean_count:,}")
print(f"Data retention rate        : {(clean_count / raw_df.count()) * 100:.2f}%")


# ===== CELL 13 =====
# Combine Date and Time into a single Timestamp and extract features
df_featured = df_clean.withColumn(
    "Timestamp",
    to_timestamp(concat_ws(" ", col("Date"), col("Time")), "d/M/yyyy HH:mm:ss")
).withColumn(
    "Hour", hour("Timestamp")
).withColumn(
    "DayOfWeek", date_format("Timestamp", "E")
).withColumn(
    "Month", month("Timestamp")
).withColumn(
    "Year", year("Timestamp")
).withColumn(
    "IsWeekend",
    when(col("DayOfWeek").isin("Sat", "Sun"), "Weekend").otherwise("Weekday")
)

# Cache DataFrame in memory for fast query execution
df_featured = df_featured.cache()
df_featured.count()  # Trigger action to materialize cache

# Display preview of engineered columns
df_featured.select(
    "Timestamp", "Hour", "DayOfWeek", "Month", "IsWeekend", "Global_active_power"
).show(5, truncate=False)


# ===== CELL 15 =====
# Overall power consumption metrics
overall_stats = df_featured.select(
    spark_round(avg("Global_active_power"), 3).alias("Mean_Active_Power_kW"),
    spark_round(min("Global_active_power"), 3).alias("Min_Active_Power_kW"),
    spark_round(max("Global_active_power"), 3).alias("Max_Active_Power_kW"),
    spark_round(stddev("Global_active_power"), 3).alias("Std_Active_Power_kW"),
    spark_round(avg("Voltage"), 2).alias("Avg_Voltage_V"),
    spark_round(avg("Global_intensity"), 2).alias("Avg_Current_A")
)
overall_stats.show()

# Compute average daily energy consumption in kWh
# Active power is measured in kW every minute -> Energy per minute = Power * (1/60) kWh
daily_energy_df = df_featured.groupBy("Date").agg(
    spark_round(avg("Global_active_power") * 24, 2).alias("Daily_kWh")
)

daily_energy_avg = daily_energy_df.agg(
    spark_round(avg("Daily_kWh"), 2).alias("Avg_Daily_Household_kWh")
)
daily_energy_avg.show()


# ===== CELL 17 =====
# Compute average consumption for each hour (0 - 23)
hourly_df = df_featured.groupBy("Hour").agg(
    spark_round(avg("Global_active_power"), 3).alias("Avg_Active_Power_kW"),
    spark_round(avg("Global_intensity"), 2).alias("Avg_Current_A")
).orderBy("Hour")

hourly_df.show(24)

# Identify peak and off-peak hours
peak_row = hourly_df.orderBy(col("Avg_Active_Power_kW").desc()).first()
offpeak_row = hourly_df.orderBy(col("Avg_Active_Power_kW").asc()).first()

print(f"Peak Consumption Hour : {peak_row['Hour']}:00 hrs ({peak_row['Avg_Active_Power_kW']} kW)")
print(f"Off-Peak Minimum Hour : {offpeak_row['Hour']}:00 hrs ({offpeak_row['Avg_Active_Power_kW']} kW)")


# ===== CELL 19 =====
# Average power consumption by day of week
daily_df = df_featured.groupBy("DayOfWeek").agg(
    spark_round(avg("Global_active_power"), 3).alias("Avg_Active_Power_kW"),
    spark_round(avg("Voltage"), 2).alias("Avg_Voltage")
).orderBy(
    when(col("DayOfWeek") == "Mon", 1)
    .when(col("DayOfWeek") == "Tue", 2)
    .when(col("DayOfWeek") == "Wed", 3)
    .when(col("DayOfWeek") == "Thu", 4)
    .when(col("DayOfWeek") == "Fri", 5)
    .when(col("DayOfWeek") == "Sat", 6)
    .when(col("DayOfWeek") == "Sun", 7)
)

daily_df.show()


# ===== CELL 21 =====
# Average power consumption by month
monthly_df = df_featured.groupBy("Month").agg(
    spark_round(avg("Global_active_power"), 3).alias("Avg_Active_Power_kW"),
    spark_round(avg("Sub_metering_3"), 2).alias("Avg_Climate_Sub3_Wh")
).orderBy("Month")

monthly_df.show(12)


# ===== CELL 23 =====
# Overall Weekday vs Weekend comparison
weekend_df = df_featured.groupBy("IsWeekend").agg(
    spark_round(avg("Global_active_power"), 3).alias("Avg_Active_Power_kW"),
    spark_round(avg("Global_intensity"), 2).alias("Avg_Current_A"),
    count("*").alias("Total_Minutes")
)
weekend_df.show()

# Hourly profile grouped by Weekday vs Weekend
hourly_ww_df = df_featured.groupBy("Hour", "IsWeekend").agg(
    spark_round(avg("Global_active_power"), 3).alias("Avg_Active_Power_kW")
).orderBy("Hour", "IsWeekend")

hourly_ww_df.show(10)


# ===== CELL 25 =====
# Calculate average energy per minute for each sub-metering zone (in Wh)
submetering_summary = df_featured.agg(
    spark_round(avg("Sub_metering_1"), 2).alias("Sub1_Kitchen_Wh"),
    spark_round(avg("Sub_metering_2"), 2).alias("Sub2_Laundry_Wh"),
    spark_round(avg("Sub_metering_3"), 2).alias("Sub3_Climate_Wh")
)
submetering_summary.show()

# Extract numeric values and compute relative shares
sub1_val = submetering_summary.first()["Sub1_Kitchen_Wh"]
sub2_val = submetering_summary.first()["Sub2_Laundry_Wh"]
sub3_val = submetering_summary.first()["Sub3_Climate_Wh"]
total_sub = sub1_val + sub2_val + sub3_val

print(f"Sub-metering 1 (Kitchen)         : {sub1_val} Wh ({(sub1_val / total_sub) * 100:.1f}%)")
print(f"Sub-metering 2 (Laundry Room)    : {sub2_val} Wh ({(sub2_val / total_sub) * 100:.1f}%)")
print(f"Sub-metering 3 (Climate Control) : {sub3_val} Wh ({(sub3_val / total_sub) * 100:.1f}%)")


# ===== CELL 27 =====
# Evaluate linear correlation with Global_active_power
target_cols = [
    "Global_reactive_power",
    "Voltage",
    "Global_intensity",
    "Sub_metering_1",
    "Sub_metering_2",
    "Sub_metering_3"
]

print("Pearson Correlation with Global_active_power:")
print("-" * 50)
for col_name in target_cols:
    corr_score = df_featured.stat.corr("Global_active_power", col_name)
    print(f"Global_active_power vs {col_name:22s} : {corr_score:+.4f}")


# ===== CELL 29 =====
# Convert aggregated PySpark results to Pandas DataFrames
pdf_hourly = hourly_df.toPandas()
pdf_monthly = monthly_df.toPandas()
pdf_hourly_ww = hourly_ww_df.toPandas()

# -----------------------------------------------------------
# Figure 1: Hourly and Monthly Profiles
# -----------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(16, 5))

# Plot 1: 24-Hour Electricity Consumption Curve
axes[0].plot(pdf_hourly["Hour"], pdf_hourly["Avg_Active_Power_kW"], marker="o", color="#1f77b4", linewidth=2.5)
axes[0].set_title("24-Hour Electricity Consumption Curve", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Hour of Day (0-23)", fontsize=11)
axes[0].set_ylabel("Average Active Power (kW)", fontsize=11)
axes[0].set_xticks(range(0, 24, 2))
axes[0].grid(True, linestyle="--", alpha=0.6)
axes[0].axvspan(19, 21, color="red", alpha=0.15, label="Evening Peak (19:00 - 21:00)")
axes[0].legend(loc="upper left")

# Plot 2: Monthly Consumption Trend
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
axes[1].bar(pdf_monthly["Month"], pdf_monthly["Avg_Active_Power_kW"], color="#2ca02c", edgecolor="black", alpha=0.8)
axes[1].set_title("Monthly Electricity Consumption Trend", fontsize=13, fontweight="bold")
axes[1].set_xlabel("Month", fontsize=11)
axes[1].set_ylabel("Average Active Power (kW)", fontsize=11)
axes[1].set_xticks(range(1, 13))
axes[1].set_xticklabels(month_names)
axes[1].grid(True, linestyle="--", alpha=0.6, axis="y")

plt.tight_layout()
plt.show()

# -----------------------------------------------------------
# Figure 2: Weekday vs Weekend and Sub-Metering Breakdown
# -----------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(16, 5))

# Plot 3: Weekday vs Weekend Hourly Load Curves
wk_data = pdf_hourly_ww[pdf_hourly_ww["IsWeekend"] == "Weekday"]
we_data = pdf_hourly_ww[pdf_hourly_ww["IsWeekend"] == "Weekend"]

axes[0].plot(wk_data["Hour"], wk_data["Avg_Active_Power_kW"], marker="s", linewidth=2, label="Weekday", color="#1f77b4")
axes[0].plot(we_data["Hour"], we_data["Avg_Active_Power_kW"], marker="o", linewidth=2, label="Weekend", color="#ff7f0e")
axes[0].set_title("Hourly Load Profile: Weekday vs. Weekend", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Hour of Day (0-23)", fontsize=11)
axes[0].set_ylabel("Average Active Power (kW)", fontsize=11)
axes[0].set_xticks(range(0, 24, 2))
axes[0].legend(fontsize=11)
axes[0].grid(True, linestyle="--", alpha=0.6)

# Plot 4: Appliance Sub-metering Distribution (Donut Chart)
labels = [
    "Sub 1: Kitchen\n(Dishwasher / Oven)",
    "Sub 2: Laundry\n(Washer / Fridge)",
    "Sub 3: Climate\n(Water Heater / AC)"
]
sizes = [sub1_val, sub2_val, sub3_val]
colors = ["#ff9999", "#66b3ff", "#99ff99"]

axes[1].pie(
    sizes,
    labels=labels,
    colors=colors,
    autopct="%1.1f%%",
    startangle=140,
    textprops=dict(color="black", fontsize=10),
    wedgeprops=dict(width=0.45, edgecolor="white")
)
axes[1].set_title("Appliance Sub-Metering Energy Share", fontsize=13, fontweight="bold")

plt.tight_layout()
plt.show()

# -----------------------------------------------------------
# Figure 3: Correlation Matrix Heatmap
# -----------------------------------------------------------
numeric_fields = [
    "Global_active_power", "Global_reactive_power", "Voltage",
    "Global_intensity", "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"
]

corr_df = pd.DataFrame(index=numeric_fields, columns=numeric_fields, dtype=float)
for r in numeric_fields:
    for c in numeric_fields:
        corr_df.loc[r, c] = df_featured.stat.corr(r, c)

plt.figure(figsize=(8, 6))
sns.heatmap(corr_df, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, square=True, linewidths=0.5)
plt.title("Correlation Heatmap of Electrical Parameters", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.show()


# ===== CELL 31 =====
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, concat_ws, hour, month, year, date_format

# 1. Start a temporary Spark session to retrieve feature data
temp_spark = SparkSession.builder \
    .appName("Temp_ML_Extraction") \
    .master("local[*]") \
    .getOrCreate()
temp_spark.sparkContext.setLogLevel("ERROR")

# 2. Extract engineered features
raw_df = temp_spark.read.csv(
    "household_power_consumption.txt",
    sep=";",
    header=True,
    nullValue="?",
    schema=schema
).dropna()

df_featured_temp = raw_df.withColumn(
    "Timestamp",
    to_timestamp(concat_ws(" ", col("Date"), col("Time")), "d/M/yyyy HH:mm:ss")
).withColumn(
    "Hour", hour("Timestamp")
).withColumn(
    "DayOfWeek", date_format("Timestamp", "E")
).withColumn(
    "Month", month("Timestamp")
)

# Gather Pandas DataFrame
pdf_ml = df_featured_temp.select("Hour", "DayOfWeek", "Month", "Global_active_power").toPandas()
temp_spark.stop()

# 3. Clean and train ML model
pdf_ml = pd.get_dummies(pdf_ml, columns=["DayOfWeek"], drop_first=True)

# Convert bool arrays to int (0 or 1)
for col_name in pdf_ml.columns:
    if col_name.startswith("DayOfWeek_"):
        pdf_ml[col_name] = pdf_ml[col_name].astype(int)

X = pdf_ml.drop(columns=["Global_active_power"])
y = pdf_ml["Global_active_power"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("Model Evaluation Metrics:")
print(f"- Mean Squared Error (MSE) : {mse:.4f}")
print(f"- Root Mean Squared Error (RMSE) : {rmse:.4f} kW")
print(f"- R-squared (R2 Score)          : {r2:.4f}")

# ===== CELL 32 =====
# Visualize Feature Importance of our trained Random Forest Regressor
importances = rf_model.feature_importances_
feature_names = X.columns
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 5))
plt.title("Machine Learning Model: Feature Importances", fontsize=13, fontweight="bold")
plt.bar(range(X.shape[1]), importances[indices], color="#66b3ff", edgecolor="black", align="center")
plt.xticks(range(X.shape[1]), [feature_names[i] for i in indices], rotation=45)
plt.xlim([-1, X.shape[1]])
plt.ylabel("Relative Importance")
plt.tight_layout()
plt.show()

# ===== CELL 34 =====
# Install Gradio if not already installed
try:
    import gradio as gr
except ImportError:
    !pip install gradio -q
    import gradio as gr

import io
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

# Helper function to generate analytics plots for the dashboard
def generate_dashboard_plot(view_name):
    fig, ax = plt.subplots(figsize=(8, 5))

    if view_name == "Hourly Load Curve":
        ax.plot(pdf_hourly["Hour"], pdf_hourly["Avg_Active_Power_kW"], marker="o", color="#1f77b4", linewidth=2.5)
        ax.set_title("24-Hour Electricity Consumption Curve", fontsize=12, fontweight="bold")
        ax.set_xlabel("Hour of Day (0-23)")
        ax.set_ylabel("Average Active Power (kW)")
        ax.set_xticks(range(0, 24, 2))
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.axvspan(19, 21, color="red", alpha=0.15, label="Evening Peak (19:00 - 21:00)")
        ax.legend(loc="upper left")

    elif view_name == "Weekday vs. Weekend Pattern":
        wk_data = pdf_hourly_ww[pdf_hourly_ww["IsWeekend"] == "Weekday"]
        we_data = pdf_hourly_ww[pdf_hourly_ww["IsWeekend"] == "Weekend"]
        ax.plot(wk_data["Hour"], wk_data["Avg_Active_Power_kW"], marker="s", linewidth=2, label="Weekday", color="#1f77b4")
        ax.plot(we_data["Hour"], we_data["Avg_Active_Power_kW"], marker="o", linewidth=2, label="Weekend", color="#ff7f0e")
        ax.set_title("Hourly Load Profile: Weekday vs. Weekend", fontsize=12, fontweight="bold")
        ax.set_xlabel("Hour of Day (0-23)")
        ax.set_ylabel("Average Active Power (kW)")
        ax.set_xticks(range(0, 24, 2))
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.6)

    elif view_name == "Appliance Energy Shares":
        labels = [
            "Sub 1: Kitchen\n(Dishwasher / Oven)",
            "Sub 2: Laundry\n(Washer / Fridge)",
            "Sub 3: Climate\n(Water Heater / AC)"
        ]
        sizes = [sub1_val, sub2_val, sub3_val]
        colors = ["#ff9999", "#66b3ff", "#99ff99"]
        ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            startangle=140,
            wedgeprops=dict(width=0.45, edgecolor="white")
        )
        ax.set_title("Appliance Sub-Metering Energy Share", fontsize=12, fontweight="bold")

    elif view_name == "Correlation Heatmap":
        sns.heatmap(corr_df, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, square=True, linewidths=0.5, ax=ax)
        ax.set_title("Correlation Heatmap of Electrical Parameters", fontsize=12, fontweight="bold")

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

# Dynamic findings based on the selected plot view
def get_graph_findings(view_name):
    if view_name == "Hourly Load Curve":
        return """
        ### 🔍 Hourly Load Curve - Key Findings:
        - **Evening Peak Window**: Consumption rises sharply starting at 17:00 and peaks between **19:00 and 21:00 hrs** (~2.14 kW).
        - **Base Load**: Consumption drops to its lowest level between **02:00 and 05:00 hrs** (~0.45 kW) when the household is asleep.
        """
    elif view_name == "Weekday vs. Weekend Pattern":
        return """
        ### 🔍 Weekday vs. Weekend - Key Findings:
        - **Weekend Overhead**: Weekend average active power usage is **19.2% higher** than weekdays overall.
        - **Afternoon Behavior**: Weekdays show a morning peak and an afternoon lull. On weekends, electricity consumption remains elevated consistently through the afternoon (10:00 to 18:00 hrs).
        """
    elif view_name == "Appliance Energy Shares":
        return """
        ### 🔍 Appliance Energy Shares - Key Findings:
        - **Climate Control Dominance**: Heating and air conditioning (**Sub_metering_3**) consumes **67.9%** of sub-metered energy.
        - **Laundry & Kitchen**: The laundry area account for **18.3%**, followed by kitchen appliances at **13.8%**.
        """
    elif view_name == "Correlation Heatmap":
        return """
        ### 🔍 Correlation Matrix - Key Findings:
        - **Current & Power**: Global Active Power and Global Current Intensity share an almost **perfect positive correlation (+0.999)**.
        - **Voltage Behavior**: Voltage has a negative correlation with power draws (**-0.385**), pointing to grid loading voltage drops.
        """
    return ""

# Helper function to generate baseline stats
def get_stats():
    return """
    ### Key Dataset Statistics
    - **Total Records Analyzed**: 713,439
    - **Average Daily Household Energy**: 28.27 kWh
    - **Peak Consumption Hour**: 20:00 hrs (2.14 kW)
    - **Base Load Minimum Hour**: 04:00 hrs (0.45 kW)
    """

# ===== CELL 35 =====
import gradio as gr
import pandas as pd

def predict_electricity_load(hour_val, day_name, month_val):
    # Reconstruct the feature vector format expected by the model
    features_dict = {col: 0 for col in X.columns}
    features_dict["Hour"] = hour_val
    features_dict["Month"] = month_val

    # Set target day of week one-hot encoded variable to 1
    target_day_col = f"DayOfWeek_{day_name[:3]}"
    if target_day_col in features_dict:
        features_dict[target_day_col] = 1

    # Format as DataFrame row
    input_df = pd.DataFrame([features_dict])

    # Predict load
    predicted_val = rf_model.predict(input_df)[0]
    return f"### Estimated Household Load: {predicted_val:.3f} kW"

# Re-launch updated UI with tabs, accuracy details and interactive interpretations
with gr.Blocks(theme=gr.themes.Soft()) as advanced_demo:
    gr.Markdown("# ⚡ Advanced Household Electricity Analyzer")

    with gr.Tab("📊 Visual Analytics"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Settings")
                selector = gr.Dropdown(
                    choices=["Hourly Load Curve", "Weekday vs. Weekend Pattern", "Appliance Energy Shares", "Correlation Heatmap"],
                    value="Hourly Load Curve",
                    label="Select Analysis View"
                )
                stats_box = gr.Markdown(value=get_stats())

            with gr.Column(scale=2):
                output_image = gr.Image(type="pil", label="Chart Visual")
                interpretation_box = gr.Markdown(value=get_graph_findings("Hourly Load Curve"))

        # Update plot and interpretive text when selector changes
        selector.change(fn=generate_dashboard_plot, inputs=selector, outputs=output_image)
        selector.change(fn=get_graph_findings, inputs=selector, outputs=interpretation_box)
        advanced_demo.load(fn=generate_dashboard_plot, inputs=selector, outputs=output_image)

    with gr.Tab("🔮 Load Prediction AI"):
        gr.Markdown("### Real-time Energy Forecasting & Model Metrics")

        with gr.Row():
            with gr.Column(variant="panel"):
                gr.Markdown("### Model Accuracy & Quality")
                gr.Markdown(f"""
                - **Algorithm**: Random Forest Regressor
                - **R² Score (Accuracy Score)**: **{r2:.4f}** (~{r2*100:.1f}% variance explained)
                - **Root Mean Squared Error (RMSE)**: **{rmse:.4f} kW**
                - **Evaluation split**: 80% Train, 20% Test split
                """)

            with gr.Column():
                gr.Markdown("### Make Predictions")
                hour_slider = gr.Slider(minimum=0, maximum=23, step=1, value=12, label="Hour of Day (0-23)")
                day_dropdown = gr.Dropdown(
                    choices=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    value="Monday",
                    label="Day of the Week"
                )
                month_slider = gr.Slider(minimum=1, maximum=12, step=1, value=6, label="Month of Year (1-12)")
                predict_btn = gr.Button("Generate Forecast", variant="primary")

                prediction_output = gr.Markdown(value="### Expected Household Load: -- kW")

        predict_btn.click(
            fn=predict_electricity_load,
            inputs=[hour_slider, day_dropdown, month_slider],
            outputs=prediction_output
        )

# Launch advanced app
advanced_demo.launch(inline=True, share=True)

# ===== CELL 37 =====
# Stop SparkSession
spark.stop()
print("SparkSession stopped successfully.")


