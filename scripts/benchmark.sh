#!/sur/bin/env bash
DORADO=/data/staging/dorado-0.4.3-linux-x64/bin/dorado
MODELS=("dna_r10.4.1_e8.2_400bps_fast@v4.2.0" "dna_r10.4.1_e8.2_400bps_hac@v4.2.0" "dna_r10.4.1_e8.2_400bps_sup@v4.2.0")
DATA=/data/staging/benchmarking/benchmarking
ITERATIONS=100

for model in "${MODELS[@]}";
do
  echo "Running $model for $ITERATIONS iterations"
  for ((i = 1; i <= ITERATIONS; i++)); do
    echo "Iteration $i"
    log_filename="${model}_iteration_${i}.log"
    $DORADO basecaller -x 'cuda:all' -v /data/staging/dorado-0.4.3-linux-x64/models/$model $DATA 2>> "$log_filename" > "${model}_iteration_${i}.bam"
    rm *.bam
  done
done