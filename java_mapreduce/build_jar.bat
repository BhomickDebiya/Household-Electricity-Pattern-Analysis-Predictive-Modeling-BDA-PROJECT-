@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo [1/3] Setting up environment for Java MapReduce
echo ===================================================
set "JAVA_BIN=D:\BDA\java\bin"
set "HADOOP_BIN=D:\BDA\hadoop-3.2.4\bin"
set "PROJECT_DIR=D:\hadoop-project\BDA PROJECT\java_mapreduce"
set "CLASSES_DIR=%PROJECT_DIR%\classes"
set "JAR_FILE=%PROJECT_DIR%\hourly_electricity.jar"

if not exist "%CLASSES_DIR%" mkdir "%CLASSES_DIR%"

echo Cleaning old class files...
del /q "%CLASSES_DIR%\*.class" 2>nul
del /q "%JAR_FILE%" 2>nul

echo ===================================================
echo [2/3] Getting Hadoop classpath and Compiling...
echo ===================================================
cd /d "D:\hadoop-project"
for /f "delims=" %%i in ('hadoop classpath') do set "HADOOP_CP=%%i"

cd /d "%PROJECT_DIR%"
"%JAVA_BIN%\javac.exe" -cp "%HADOOP_CP%" -d "%CLASSES_DIR%" HourlyElectricityMapper.java HourlyElectricityReducer.java HourlyElectricityDriver.java

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Compilation failed!
    exit /b %ERRORLEVEL%
)

echo [SUCCESS] Compilation succeeded!
echo ===================================================
echo [3/3] Creating JAR package...
echo ===================================================
cd /d "%CLASSES_DIR%"
"%JAVA_BIN%\jar.exe" -cvf "%JAR_FILE%" *.class

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] JAR creation failed!
    exit /b %ERRORLEVEL%
)

echo [SUCCESS] JAR created at: %JAR_FILE%
cd /d "D:\hadoop-project"
