import subprocess
import inspect, os

OUTPUT_PROCESS_IDS = ".pids"
CURRENT_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

pids = []

process = subprocess.Popen(["nohup", "python", os.path.join(CURRENT_PATH, "start.py")])
pids.append(process)
print "Start collector with id", process.pid

pidsFile = open(OUTPUT_PROCESS_IDS, "a")
s = ""

for p in pids:
	s += str(p.pid) + "\n"

pidsFile.write(s)
