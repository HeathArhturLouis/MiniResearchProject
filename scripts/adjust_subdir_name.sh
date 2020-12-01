n=1;
max=50;
while [ "$n" -le "$max" ]; do
  mkdir "run_$n/test"
  mkdir "run_$n/train"
  cp "run_$n/pos_test.csv" "run_$n/test/pos.csv"
  cp "run_$n/neg_test.csv" "run_$n/test/neg.csv"
  cp "run_$n/pos_train.csv" "run_$n/train/pos.csv"
  cp "run_$n/neg_train.csv" "run_$n/train/neg.csv"
  n=`expr "$n" + 1`;
done