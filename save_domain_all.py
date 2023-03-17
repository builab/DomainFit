import sys,os,time
from datetime import datetime
script_dir=os.path.dirname(os.path.realpath(__file__))
import subprocess

def print_usage ():
    print("usage: python save_domain_all.py inputDir outputDir")
    sys.exit()
print(len(sys.argv))
if len(sys.argv) != 3 :
    print_usage()
else:
    logs=[]
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

list = os.listdir(input_dir)
cmds=[]
for pdb in os.listdir(input_dir):
    if pdb.endswith("domains.pdb"):
        # Add them to the command list
        cmds.append(f'chimerax-daily --nogui --offscreen --cmd \"runscript {script_dir}/save_domain_single.py {input_dir} {output_dir} {pdb}" --exit')

print(cmds)

# Execute command list
#os.chdir(output_dir)
for cmd in cmds:
        print(f'start {cmd}', datetime.now())
        status = subprocess.call(cmd,shell=True)
#os.chdir(script_dir)
