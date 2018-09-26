# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 16:25:46 2018

@author: asimon
"""

class PrintFile(object):
    def __init__(self, filename, inv_start_patt):
        file_as_list = []
        self.filename = filename
        with open(self.filename, 'r') as f:
            for line in f:
                file_as_list.append(line)
            f.close()
        self.file_length = len(file_as_list)
        
# TODO check on new page flag along with header to mark files
        
for l in pf:
    if l[15:20] in invs_dict:
        invs_dict[l[15:20]][l[1:7]+l[25:30]] = l
    else:
        invs_dict[l[15:20]] = {
            l[1:7]: l
        }