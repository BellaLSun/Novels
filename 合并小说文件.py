import pandas as pd
import os
import os.path


'''
It generates the file names in a directory tree by walking the tree either
top-down or bottom-up.

For each directory in the tree rooted at directory top (including top itself), 
it yields a 3-tuple (dirpath, dirnames, filenames).
'''

def MergeTxt(filepath,outfile):
    k = open(filepath+outfile, 'a+')
    for parent, dirnames, filenames in os.walk(filepath):
        for filepath in filenames:
            # txtpath是所有文件夹的路径
            txtPath = os.path.join(parent, filepath)
            f = open(txtPath)
            k.write(f.read()+"\n")

    k.close()

if __name__ == '__main__':
    filepath="./Novel"
    outfile="全职高手.txt"
    MergeTxt(filepath,outfile)
