from scheduler import run_continuous_lazy
import sys
print(sys.argv)
run_continuous_lazy(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4])