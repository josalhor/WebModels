import os
import shutil

p='todo/migrations'

if os.path.isdir(p):
    shutil.rmtree(p)