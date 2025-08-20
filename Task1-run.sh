#!/bin/bash

# Set Hadoop Streaming JAR path
HADOOP_STREAMING_JAR="./hadoop-streaming-3.1.4.jar"

# Input and Output paths on HDFS
INPUT_PATH="/Input/Trips.txt"
OUTPUT_PATH="/Output/Task1"

# Local input file path
LOCAL_INPUT_FILE="./Trips.txt"

# Step 1: Upload input file to HDFS
hdfs dfs -mkdir -p /Input
hdfs dfs -put -f "$LOCAL_INPUT_FILE" /Input/

# Step 2: Remove previous output directory if it exists
hdfs dfs -rm -r -f "$OUTPUT_PATH"

# Step 3: Run Hadoop Streaming job
hadoop jar "$HADOOP_STREAMING_JAR" \
    -D mapred.reduce.tasks=3 \
    -files ./mapper.py,./reducer.py \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input "$INPUT_PATH" \
    -output "$OUTPUT_PATH"

# Step 4: Show job output
echo "=== MapReduce Output ==="
hdfs dfs -cat "$OUTPUT_PATH"/part-*
