#!/bin/bash

# Hadoop Streaming JAR
HADOOP_STREAMING_JAR="./hadoop-streaming-3.1.4.jar"

# HDFS input paths
TRIPS="/Input/Trips.txt"
TAXIS="/Input/Taxis.txt"

# HDFS output paths
OUTPUT_FINAL="/Output/Task3"
OUTPUT_TEMP1="/Output/Task3-temp1"
OUTPUT_TEMP2="/Output/Task3-temp2"

# Upload input files if they don't exist
hdfs dfs -mkdir -p /Input
hdfs dfs -test -e $TRIPS || hdfs dfs -put -f Trips.txt /Input/
hdfs dfs -test -e $TAXIS || hdfs dfs -put -f Taxis.txt /Input/

# Clean old outputs
hdfs dfs -rm -r -f $OUTPUT_TEMP1 $OUTPUT_TEMP2 $OUTPUT_FINAL

# -------------------
# JOB 1: Join Trips with Taxis (3 reducers)
# -------------------
hadoop jar $HADOOP_STREAMING_JAR \
  -D mapred.reduce.tasks=3 \
  -files Task3-mapper.py,Task3-reducer.py \
  -mapper "python3 Task3-mapper.py job1" \
  -reducer "python3 Task3-reducer.py job1" \
  -input $TRIPS -input $TAXIS \
  -output $OUTPUT_TEMP1

# -------------------
# JOB 2: Count Trips per Company (3 reducers)
# -------------------
hadoop jar $HADOOP_STREAMING_JAR \
  -D mapred.reduce.tasks=3 \
  -files Task3-mapper.py,Task3-reducer.py \
  -mapper "python3 Task3-mapper.py job2" \
  -reducer "python3 Task3-reducer.py job2" \
  -input $OUTPUT_TEMP1 \
  -output $OUTPUT_TEMP2

# -------------------
# JOB 3: Sort total trips ascending (3 reducers, Option A)
# -------------------
hadoop jar $HADOOP_STREAMING_JAR \
  -D mapred.reduce.tasks=3 \
  -D stream.map.output.field.separator=$'\t' \
  -D map.output.key.field.separator=$'\t' \
  -D stream.num.map.output.key.fields=2 \
  -D mapred.text.key.comparator.options=-k1,1n \
  -files Task3-mapper.py,Task3-reducer.py \
  -mapper "python3 Task3-mapper.py job3" \
  -reducer "python3 Task3-reducer.py job3" \
  -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
  -input $OUTPUT_TEMP2 \
  -output $OUTPUT_FINAL

echo "Task3 complete. Final results are in HDFS directory: $OUTPUT_FINAL"
