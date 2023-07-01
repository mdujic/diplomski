#!/bin/bash                                                                    
n=100  # number of times to run the command                                     
# array of commands to run
commands_to_run=("pytest rpq_evaluation/tests/test_diamond.py -s -vv")                                                                            
total_time=0                                                                   
for ((i=1; i<=n; i++))                                                         
do                                                                             
  start_time=$(date +%s.%N)  # get current time with nanoseconds               
  # for each command in commands_to_run, run the command
  for command_to_run in "${commands_to_run[@]}"
  do
    echo "Running command: $command_to_run"
    eval $command_to_run
  done

  end_time=$(date +%s.%N)  # get current time with nanoseconds                 
                                                                               
  # calculate time difference in seconds                                       
  time_taken=$(echo "$end_time - $start_time" | bc)                            
  total_time=$(echo "$total_time + $time_taken" | bc)                          
                                                                               
  echo "Time taken for run $i: $time_taken seconds"                            
done                                                                           
                                                                               
echo "Total time taken for $n runs: $total_time seconds" 
