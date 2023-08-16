from scheduler import run_continuous_lazy
import sys
print(sys.argv)
run_continuous_lazy(sys.argv[1] + ' ' + sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6])
