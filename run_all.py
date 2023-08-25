import subprocess
import pandas as pd
from pathlib import Path
import os

pqn = "pqn.n3"
log = "logs/sepsis.n3"

dirname = "queries"
dir = os.fsencode(dirname)
for file in os.listdir(dir):
    filename = os.fsdecode(file)
    filepath = os.path.join(dirname, filename)

    process_1 = subprocess.run([ 'eye', pqn, log, '--query', filepath ])
    print(process_1)
    print(process_1.args)
    print(process_1.returncode)
    print(process_1.stdout)
    print(process_1.stderr)