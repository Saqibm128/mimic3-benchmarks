from __future__ import print_function

import os
import argparse
import pandas as pd
import numpy as np

def is_subject_folder(x):
    for c in x:
        if (c < '0' or c > '9'):
            return False
    return True


def main():
    #Set up some variables for verbose logging
    bad_pairs = set()
    missing_events = [];
    
    n_events = 0
    emptyhadm = 0
    noicustay = 0
    recovered = 0
    couldnotrecover = 0
    icustaymissinginstays = 0
    nohadminstay = 0
    
    parser = argparse.ArgumentParser()
    parser.add_argument('subjects_root_path', type=str,
                        help='Directory containing subject sub-directories.')
    args = parser.parse_args()
    print(args)
    
    subfolders = os.listdir(args.subjects_root_path)
    subjects = list(filter(is_subject_folder, subfolders))
    
    # get mapping for subject
    maps = {}
    for (index, subject) in enumerate(subjects):
        staysDF = pd.DataFrame.from_csv(os.path.join(args.subjects_root_path, subject, "stays.csv"))
        staysDF.columns = staysDF.columns.str.upper()
        staysDF.dropna(axis=0, how="any", subset=["HADM_ID"])
        if (index % 100 == 0):
            print("processed %d / %d" % (index+1, len(subjects)), "         \r")
            print("")   
        ##if for some reason no events file was written
        if os.path.isfile(os.path.join(args.subjects_root_path, subject, "events.csv")): 
            eventsDF = pd.DataFrame.from_csv(os.path.join(args.subjects_root_path, subject, "events.csv"))
            eventsDF = eventsDF.dropna(axis=0, how="any", subset=["HADM_ID", "ICUSTAY_ID"])
            print eventsDF.index
            print eventsDF.columns
            joined = eventsDF.join(staysDF, on=["HADM_ID"], how="left", rsuffix="_r")
            joined.to_csv(os.path.join(args.subjects_root_path, subject, "events2.csv"))
    
    #print bad_pairs
    print('n_events', n_events,
        'emptyhadm', emptyhadm,
        'noicustay', noicustay, 
        'recovered', recovered ,
        'couldnotrecover', couldnotrecover ,
        'icustaymissinginstays', icustaymissinginstays ,
        'nohadminstay', nohadminstay,
        'noevents', missing_events )
        
if __name__=="__main__":
    main()
