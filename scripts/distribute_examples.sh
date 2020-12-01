# Distribute a fixed number of examples to each experiment subfolder

n=1;

# num of directories
max=50;
# Total balanced DS size (pos and neg will be half each rounded down)
N=22500;
# Total training DS size (<= N)
NT=10000;

N=`expr "$N" / 2`;
NT=`expr "$NT" / 2`;

while [ "$n" -le "$max" ]; do
  echo "generating DS for experiment $n"
  shuf -n "$N" "all/pos.csv" > "experiments/run_$n/pos.csv";
  shuf -n "$N" "all/neg.csv" > "experiments/run_$n/neg.csv";
  # seperate testing data
  head -n `expr "$N" - "$NT"` "experiments/run_$n/pos.csv" > "experiments/run_$n/pos_train.csv"
  tail -n "$NT" "experiments/run_$n/pos.csv" > "experiments/run_$n/pos_test.csv"
  head -n `expr "$N" - "$NT"` "experiments/run_$n/neg.csv" > "experiments/run_$n/neg_train.csv"
  tail -n "$NT" "experiments/run_$n/neg.csv" > "experiments/run_$n/neg_test.csv"

  n=`expr "$n" + 1`;
done