#!/usr/bin/env python
# coding: utf-8

# In[1]:


import PyPDF2
import pandas as pd
import glob
import sys


# In[2]:


dir_path = sys.argv[1]
file_paths = [x for x in glob.glob(dir_path+"*.pdf")]


# In[3]:


## scrape data from PDFS given in dir_path
for file_path in file_paths[-1::-1]:
    
    out_name = file_path.split("\\")[-1][:-4]
    pdfFileObject = open(file_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    p_count = pdfReader.numPages
    content = []
    for i in range(p_count):
        page = pdfReader.getPage(i)
        full = page.extractText().split("\n")
        for f in full:
            content.append(f)
            count = -1

    cur_topic = ""
    cols = """Total_Applied Total_Offered Total_Percent_Offered Total_Enrolled Total_Percent_Enrolled 
    Female_Applied Female_Offered Female_Percent_Offered Female_Enrolled Female_Percent_Enrolled 
    Minority_Applied Minority_Offered Minority_Percent_Offered Minority_Enrolled Minority_Percent_Enrolled 
    Intl_Applied Intl_Offered Intl_Percent_Offered Intl_Enrolled Intl_Percent_Enrolled""".split()

    overall_d = {}

    for c in content:
        # keeps track of the overall index of the data
        count += 1
        topics = "Arts and Sciences,School of,College of,Environments,Programs,Information School".split(",")
        for topic in topics:
            # this adds cur_topic to the overall_d, with a dictionary of empty values and cols as keys
            if topic in c and "Marine" not in c and "Evans" not in c and "Bothell" not in c and c != "School of":
                d = {}
                if c == "Arts and Sciences - Social Sci":
                    c = "Arts and Sciences - Social Sciences"
                for col in cols:
                    d[col] = 0

                # standardize format of school name
                c = c.replace(",", " -")

                cur_topic = c
                overall_d[cur_topic] = d
        if "SubTotal" in c:

            # the following ensures we don't update subtotal 
            # for anything invalid cur_topic #
            some = 0 
            try:
                temp = overall_d[cur_topic]
                for value in temp.values():
                    some += value

                if some == 0:

                    # then add stats to overall dict
                    stats = content[count+1:count+21]
                    for i in range(len(stats)):
                        temp[cols[i]] = float(stats[i].replace(",","")) # commas mess up floats
                    overall_d[cur_topic] = temp
            except KeyError as e:
                print(e)


                
## Build and save CSV files of data
    df = pd.DataFrame()
    df = pd.DataFrame(columns=cols)

    for school in overall_d.keys():
        data = overall_d[school]
        vals = list(data.values())
        temp = pd.DataFrame([vals], columns=cols)
        df = df.append(temp)

    # make sure you don't have index of 0's
    df = df.reset_index(drop=True)

    df["UW School"] = list(overall_d.keys())

    # get the right ordering
    cols.insert(0, "UW School")

    df = df[cols]
    df2 = df[df['Total_Applied'] != 0]
    df2 = df2.sort_values(by='UW School')
    df2 = df2.reset_index(drop=True)
    df2.to_csv(dir_path+out_name+".csv", index=False)
   

