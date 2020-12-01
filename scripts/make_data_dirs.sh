n=1;
max=50;
while [ "$n" -le "$max" ]; do
  mkdir "run_$n"
  n=`expr "$n" + 1`;
done
