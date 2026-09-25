#!/usr/bin/env bash
# hyp033_pod.sh -- runs ON the RunPod pod. Stage 1: Julia exports (SIM-061 pipeline). Stage 2: C-HAAR
# networks. Stage 3: gates + grid, parallel over networks. Everything lands in /workspace/hyp033/networks.
# Env: SEEDS6 (default 8), SEEDS8 (default 4), SEEDS_GAP (8), MAXITER (2500), NJOBS (grid parallelism),
#      JULIA_PAR (parallel optimizations), POD_ID.
set -uo pipefail
cd /workspace/hyp033
export RUNPOD_POD_ID="${POD_ID:-unknown}"
NPROC="${NPROC_OVERRIDE:-$(nproc)}"   # the container reports the HOST core count; we own vcpuCount
NJOBS="${NJOBS:-3}"
JULIA_PAR="${JULIA_PAR:-8}"
SEEDS6="${SEEDS6:-8}"; SEEDS8="${SEEDS8:-4}"; SEEDS_GAP="${SEEDS_GAP:-8}"; MAXITER="${MAXITER:-2500}"
NET=/workspace/hyp033/networks
mkdir -p "$NET" logs
stamp(){ date -u +%FT%TZ; }
echo "[$(stamp)] pod $RUNPOD_POD_ID nproc=$NPROC njobs=$NJOBS julia_par=$JULIA_PAR seeds6=$SEEDS6 seeds8=$SEEDS8 seeds_gap=$SEEDS_GAP maxiter=$MAXITER" | tee -a logs/pod.log

# ---------------------------------------------------------------- stage 1: Julia (MERAKit, pinned Manifest)
if [ ! -f stage1.done ]; then
  export PATH=/workspace/hyp033/julia-1.8.5/bin:$PATH
  export JULIA_DEPOT_PATH=/workspace/hyp033/depot
  export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
  cd MERAKit.jl
  julia --project=. instantiate.jl > ../logs/instantiate.log 2>&1 || { echo "[$(stamp)] INSTANTIATE FAILED"; tail -20 ../logs/instantiate.log; touch ../all.done; exit 1; }
  echo "[$(stamp)] julia instantiated" | tee -a ../logs/pod.log
  # one optimization per process; per-seed invocations so they run in parallel
  {
    for s in $(seq 1 $SEEDS6);    do echo "3 3 $s $s $MAXITER 1.0 $NET"; done
    for s in $(seq 1 $SEEDS_GAP); do echo "3 3 $s $s $MAXITER 1.5 $NET"; done
    for s in $(seq 1 $SEEDS8);    do echo "4 4 $s $s $MAXITER 1.0 $NET"; done
  } > ../logs/julia_jobs.txt
  xargs -P "$JULIA_PAR" -L 1 bash -c 'julia --project=. qw_hyp033_export.jl $0 $1 $2 $3 $4 $5 $6 > ../logs/julia_$0$1_h$5_s$2.log 2>&1' < ../logs/julia_jobs.txt
  cd ..
  grep -h "seed" logs/julia_*.log | tee -a logs/pod.log
  touch stage1.done
  echo "[$(stamp)] stage 1 done: $(ls -d $NET/chi* | wc -l) optimized networks" | tee -a logs/pod.log
fi

# ---------------------------------------------------------------- stage 2: C-HAAR
if [ ! -f stage2.done ]; then
  python3 hyp033_haar.py "$NET" 6 1 "$SEEDS6" >> logs/pod.log 2>&1
  touch stage2.done
fi

# ---------------------------------------------------------------- stage 3: gates + grid
THREADS=$(( NPROC / NJOBS )); [ "$THREADS" -lt 1 ] && THREADS=1
export OMP_NUM_THREADS=$THREADS OPENBLAS_NUM_THREADS=$THREADS MKL_NUM_THREADS=$THREADS
# go/no-go on the first primary network's gates before anything else is started
if [ ! -f gate0.done ]; then
  D0=$(ls -d $NET/chi6_h1.00_seed1)
  python3 hyp033_grid.py --network "$D0" --gates --m 0 --edge left --out "$D0/gates_first.json" > logs/gate0.log 2>&1
  if ! grep -q "| PASS" logs/gate0.log; then echo "[$(stamp)] FIRST-NETWORK GATES FAILED -- stopping"; cat logs/gate0.log; exit 2; fi
  touch gate0.done
  echo "[$(stamp)] first-network gates PASS: $(grep gates: logs/gate0.log)" | tee -a logs/pod.log
fi
{
  for d in $NET/chi6_h1.00_seed*; do echo "$d --gates"; done
  for d in $NET/haar_chi6_seed*;  do echo "$d --gates"; done
  for d in $NET/chi6_h1.50_seed*; do echo "$d --gates"; done
  for d in $NET/chi8_h1.00_seed*; do echo "$d --gates --chi8"; done
} > logs/grid_jobs.txt
echo "[$(stamp)] stage 3: $(wc -l < logs/grid_jobs.txt) grid jobs, $NJOBS parallel x $THREADS threads" | tee -a logs/pod.log
xargs -P "$NJOBS" -L 1 bash -c 'd=$0; python3 hyp033_grid.py --network "$d" "$@" > "$d/grid.log" 2>&1; rc=$?; echo "[$(date -u +%FT%TZ)] finished $d rc=$rc" >> logs/pod.log' < logs/grid_jobs.txt
touch stage3.done
echo "[$(stamp)] ALL DONE" | tee -a logs/pod.log
