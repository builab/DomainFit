from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import os, sys
import subprocess
script_dir=os.path.dirname(os.path.realpath(__file__))


# Syntax
def print_usage ():
    print("usage: visaulize_noRes.py <log_fit_revised>" )

# Ensures that there are 5 arguments
if len(sys.argv) < 1:
    print_usage()
else:
    input_csv = sys.argv[1]


df = pd.read_csv(input_csv, sep='\s*,\s*')
# df.info()
df.dropna()
# print(df["NoRes"])

d = df["NoRes"].to_numpy()

(mu, sigma) = norm.fit(d)

print(mu)
print(sigma)


# An "interface" to matplotlib.axes.Axes.hist() method
n, bins, patches = plt.hist(x=d, bins=range(min(d), max(d) + 5, 5), color='#0504aa',
                            alpha=0.7, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('noRes')
plt.ylabel('Count (noDomains)')
plt.title('CU428_Complete')
# plt.text(23, 45, r'$\mu=15, b=3$')
maxfreq = n.max()
# Set a clean upper y-axis limit.
y = norm.pdf( bins, mu, sigma)
y = y*n.sum()*10
# plt.plot(bins, y, 'r--', linewidth=2)
plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)

plt.show()