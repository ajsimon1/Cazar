# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 16:25:46 2018

@author: asimon
"""
# import os
import re
import xml.etree.ElementTree as et
import pandas as pd

# os.getcwd().split('\\')[0:4]
# '\\'.join(os.getcwd().split('\\')[0:4])

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
            doc_dict[str(split_doc[doc_num_line - 1][doc_num_strt - 1:doc_num_end - 1]).strip()] = split_doc
        self.parsed_dict = doc_dict
        return doc_dict
        
    
    def prt_all_from_pos(self, line_num, strt_pos, end_pos):
        # prints all values from parsed_dic to screen using provided line #
        # and start / end positions
        for k, v in self.parsed_dict.items():
            print('{0}: {1}'.format(k, v[int(line_num)-1][int(strt_pos)-1:int(end_pos)-1]))
    
    # TODO find a way to check for multi pages and accomodate
    
    # TODO create base class with standard methods, specific file classes then 
    # inherit off the base 
    
class XmlFile(object):
    # set doc_id var as init param
    def __init__(self, file_path, doc_keyword, doc_id):
        # doc_keyword param identifies element that marks separation of docs
        # within the xml
        self.file_path = file_path
        self.doc_keyword = doc_keyword
        self.doc_id = doc_id
        # parse xml
        self.tree = et.parse(file_path)
        # get root node of document
        self.root = self.tree.getroot()
        # return all sub elements
        self.elements_list = set([i.tag for i in self.root.findall('.//')])
        
    def get_doc_by_num(self, doc_num):
        a = self.root.findall('./{}'.format(self.doc_keyword))
        for i in a:
            try: 
                if i.find('.//{}'.format(self.doc_id)).text.strip() == doc_num:
                    return i
            except AttributeError as e:
                print('AE error: {}'.format(e))
                pass
                
        print('Document #: {} was not found'.format(doc_num))
        return
    
    def get_all_docs(self):
        return self.root.findall('./{}'.format(self.doc_keyword))
    
    def prnt_all_for_elem(self, elem):
        return [i.text for i in self.root.findall('.//{}'.format(elem))]
    
    def get_root(self):
        return self.root
    def get_tree(self):
        return self.tree
    
    def check_all_elem_agnst_value(self, elem, val, check_null=False):
        a_list = []
        for i in self.get_all_docs():
            try:
                if check_null:
                    if i.find('.//{}'.format(elem)).text.strip() != '{}'.format(val):
                        a_list.append(i.find('.//{}'.format(self.doc_id)).text.strip())
                else:
                    if i.find('.//{}'.format(elem)).text.strip() == '{}'.format(val):
                        a_list.append(i.find('.//{}'.format(self.doc_id)).text.strip())
            except AttributeError:
                pass
        return a_list
    
    def get_max_val(self, elem):
        elem_list = []
        for i in self.get_all_docs():
            for a in i.findall('.//{}'.format(elem)):
                try:
                    elem_list.append(a.text.strip())
                except AttributeError:
                    pass
        return max(elem_list, key=len, default=None)
    
    def get_all_max_vals(self):
        max_width_list = []
        print('Getting max vals for {} elements'.format(len(self.elements_list)))
        for item in self.elements_list:
            max_val = self.get_max_val(item)
            if max_val is not None:
                max_width_list.append((item, len(max_val), max_val))
            else:
                max_width_list.append((item, 'Empty', 0))
        return max_width_list
    
    def get_docid_if_elem_present(self, elem):
        result_list = []
        for i in self.get_all_docs():
            if bool(i.findall('.//{}'.format(elem))):
                result_list.append(i.find('.//{}'.format(self.doc_id)).text)
        return result_list
    
    def create_xml_file_for_doc(self, doc_num, filename):
        doc = self.get_doc_by_num(doc_num)
        create_xml_file_from_elem(doc, filename)
    
    def build_parent_map(self):
        # change s[0] to stmts
        parent_map = dict((c, p) for p in s[0].iter() for c in p)
        # this is going to miss parent/children relationships that are not
        # terminal, ie parent/children that are both nested nodes
        
def create_xml_file_from_elem(elem, filename, is_list=False):
    elem_tree = et.ElementTree(elem)
    root = et.Element('root')
    elem_tree._setroot(root)
    if is_list:
        for i in elem:
            root.append(i)
    else:
        root.append(elem)
    elem_tree.write(filename)
    return print('{} file created'.format(filename))
    '''
    steps to create xml for from list of doc #s
    - use get_doc_by_num for loop to grab all docs out of root
    - should be list of doc elements
    - create new element tree using ElementTree()
    - add root to new element tree 
    - root = et.Element('root') ; confirm with tree.gteroot()
    - loop through list of doc elements [root.append(i) for i in match_docs]
    - create_xml_file_from_elem func above
    
    '''
    
#TODO should be able to do something by nested for loops that check elements
# length and build dicts
        
# TODO add doc_id_num to contructor
        

class DelimFile(object):
    def __init__(self, filename, delim =',', ext='.xml'):
        self.delim = delim
        self.ext = ext
        df = pd.read_csv(filename, sep=delim)
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

