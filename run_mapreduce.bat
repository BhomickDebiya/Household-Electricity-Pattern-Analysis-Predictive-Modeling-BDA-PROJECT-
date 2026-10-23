@echo off
setlocal enabledelayedexpansion

echo ======================================================================
echo    BIG DATA ANALYTICS LAB - AUTONOMOUS MAPREDUCE EXECUTION
echo    Project: Household Electricity Pattern Analysis
echo    Students: Bhomick Debiya (Roll 32), Shorya Chilate
echo ======================================================================

set "PROJECT_DIR=D:\hadoop-project\BDA PROJECT"
set "JAR_FILE=%PROJECT_DIR%\java_mapreduce\hourly_electricity.jar"
set "HDFS_INPUT=/bda_electricity/input/household_power_consumption.txt"
set "HDFS_OUTPUT=/bda_electricity/output/mr_hourly_results"
set "LOCAL_OUTPUT=%PROJECT_DIR%\mr_hourly_results"

cd /d "D:\hadoop-project"

echo [Step 1] Checking if HDFS is reachable...
call hdfs dfs -ls /bda_electricity/input >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] HDFS is not responding!
    echo Please make sure NameNode and DataNode are running.
    echo Run: D:\BDA\hadoop-3.2.4\sbin\start-dfs.cmd
    echo Retrying in 5 seconds...
    timeout /t 5 >nul
)

echo [Step 2] Ensuring raw dataset is in HDFS...
call hdfs dfs -test -e %HDFS_INPUT%
if %ERRORLEVEL% NEQ 0 (
    echo Dataset not found in HDFS. Uploading now...
    call hdfs dfs -mkdir -p /bda_electricity/input
    call hdfs dfs -put -f "%PROJECT_DIR%\household_power_consumption.txt" %HDFS_INPUT%
    echo Upload complete!
) else (
    echo Dataset already present in HDFS.
)

echo [Step 3] Checking MapReduce JAR...
if not exist "%JAR_FILE%" (
    echo JAR not found! Building now...
    call "%PROJECT_DIR%\java_mapreduce\build_jar.bat"
)

echo [Step 4] Running Hadoop MapReduce Job on HDFS...
echo Input:  %HDFS_INPUT%
echo Output: %HDFS_OUTPUT%
call hadoop jar "%JAR_FILE%" HourlyElectricityDriver %HDFS_INPUT% %HDFS_OUTPUT%

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Hadoop MapReduce execution failed!
    exit /b %ERRORLEVEL%
)

echo [SUCCESS] Hadoop MapReduce Job completed!
echo ======================================================================
echo [Step 5] Fetching results to local directory: %LOCAL_OUTPUT%
if exist "%LOCAL_OUTPUT%" rmdir /s /q "%LOCAL_OUTPUT%"
call hdfs dfs -get %HDFS_OUTPUT% "%LOCAL_OUTPUT%"

echo ======================================================================
echo MAPREDUCE AGGREGATION OUTPUT (24-Hour Electricity Profile):
echo Hour	Avg_Power_kW	Total_Records
echo ----------------------------------------------------------------------
type "%LOCAL_OUTPUT%\part-r-00000"
echo ======================================================================
cd /d "%PROJECT_DIR%"
pause
