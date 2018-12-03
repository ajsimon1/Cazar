import os
import sys
import pandas as pd

from xml.etree import ElementTree as et

cwd = os.getcwd()
filepath = 'C:\\Users\\asimon\\Desktop\\Practice-' \
            'Training\\p21_template_out3.xml'

def parse_wfd_xml(filepath):
    tree = et.parse(filepath)
    root = tree.getroot()
    data, page = root.findall('.//LineDataInput/LDILayout/Nodes/Node/Node')
    data_dict = {}
    page_dict = {}
    for i in data.findall('./Node/Node/Content'):
        data_dict[i.find('Name').text] = i.find('Guid').text
        df_data = pd.DataFrame.from_dict(data_dict,
                                        orient='index',
                                        columns=['guid'])
    for i in page.findall('./Node/Node/Node/Content'):
        try:
            page_dict[i.find('DataVariable').text] = [i.find('Name').text,
                                                i.find('Size').get('X'),
                                                i.find('Size').get('Y'),
                                                i.find('Offset').get('X'),
                                                i.find('Offset').get('X')]
        except AttributeError:
            pass
        df_page = pd.DataFrame.from_dict(page_dict,
                                        orient='index',
                                        columns=['name',
                                                 'size_x',
                                                 'size_y',
                                                 'offest_x',
                                                 'offest_y'])
    # df_combined = df_data.join(df_page, on='guid')
    # possible drop NaNs?
    return df_data.join(df_page, on='guid')
if __name__ == '__main__':

    df = parse_wfd_xml(filepath)
    writer = pd.ExcelWriter('wfd_output.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
