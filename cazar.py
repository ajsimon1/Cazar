# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 16:25:46 2018

@author: asimon
"""
import re

class PrintFile(object):
    '''
        sample sequence of events to produce parsed dict of print file
        1. from cazar import PrintFile
        2. f = PrintFile(base_dir + filename)
        3. f.set_regxpattern('Last Page', '59')
        data = f.parse_file(2, 123, 133)
    '''
    def __init__(self, filename, read_type='full'):
        self.filename = filename
        self.read_type = read_type
        
        with open(self.filename, 'r') as f:
            if read_type == 'split':
                self.contents = list(f)
            elif read_type == 'full':
                self.contents = f.read()
            f.close()
        self.file_length = len(self.contents)
        self.parsed_dict = {}
    
    def get_length(self):
        return self.file_length
    
    def get_contents(self):
        return self.contents
    
    def get_parsed_dict(self):
        return self.parsed_dict
    
    def get_specific_doc(self, doc_key):
        return self.parsed_dict[str(doc_key)]
    
    def build_generator(self):
        # iterate over each line of the file on demand
        # note, once a generator is exhausted the method must be called again
        cont = self.get_contents()
        for i in cont:
            yield i

    def set_regx_pattern(self, doc_end_pattern, doc_line_count, end_pattern=True):
        # regex pattern return variables amount lines = doc_line_count
        # including and before doc_end_pattern
        if end_pattern:
            self.regx_pattern = re.compile(r'((.*\n){{{0}}}{1}.*\n)'.format(str(doc_line_count), str(doc_end_pattern)))
        else:
            self.regx_pattern = re.compile(r'{1}((.*\n){{{0}}})'.format(str(doc_line_count), str(doc_end_pattern)))
        print('Instance inv_pattern set as "{}"'.format(self.regx_pattern))

    def parse_file(self, doc_num_line, doc_num_strt, doc_num_end):
        # parses file based on pattern set in class property
        doc_dict = {}
        contents = self.contents
        patt = self.regx_pattern
        result = re.findall(patt, contents)
        for doc in result:
            split_doc = doc[0].split('\n')
            # updating numbers provided to counter zero based index
            # sets provided line, strt, end #s as key of dict for each doc
            doc_dict[split_doc[doc_num_line - 1][doc_num_strt - 1:doc_num_end - 1]] = split_doc
        self.parsed_dict = doc_dict
        return doc_dict
    
    def prt_all_from_pos(self, line_num, strt_pos, end_pos):
        # prints all values from parsed_dic to screen using provided line #
        # and start / end positions
        for k, v in self.parsed_dict.items():
            print('{0}: {1}'.format(k, v[int(line_num)-1][int(strt_pos)-1:int(end_pos)-1]))
    
    # TODO find a way to check for multi pages and accomodate

