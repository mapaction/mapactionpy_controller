import os
import sys
import pandas as pd
import json


##
# 
def parse_directory(sourceDir, extList):
    sourceList = []
    for root, dirs, files in os.walk(sourceDir):
        for file in files:
            for ext in extList:
                if file.endswith(ext):
                    #print(os.path.join(root, file))
                    #sourceList.append([root, file])
                    sourceList.append(os.path.join(root, file))
    return sourceList

##
#
def process_json_report(json_source):
    # Load JSON into Dictionary Type object
    # Note the JSON headers don't follow order of the file
    with open(json_source) as json_data: 
        json_d = json.load(json_data)

    # Various structure definitions - obtain from the Metis codebase
    # To ensure final column order
    prod_details = [
            'classification',
            'productName',
            'result',
            'summary',
            ]

    correct_order = [
            'classification',
            'productName',
            'result',
            'added',            # Unpacked from results
            'dataSource',       # Unpacked from results
            'dateStamp',        # Unpacked from results
            'hash',             # Unpacked from results
            'layerName',        # Unpacked from results   
            'message',          # Unpacked from results   
            'summary',
            ]

    # Add to a Pandas Data frame - or process into seprate tables.
    df_start = pd.DataFrame.from_dict(json_d)
    df_ok = df_start[prod_details]
    df_ok = df_ok.drop_duplicates()
    #
    df_results = pd.DataFrame.from_dict(json_d['results'])
    #
    df_final = df_results
    # Append results values
    for col in df_ok.columns.values:
        df_final[col] = df_ok[col][0]
    # Reorder cols
    df_final = df_final[correct_order]
    return df_final


# 
def main(arvg=None):
    # Define location of folder with JSON report files.
    # To do - set up argument parsing...
    root = r'J:\04_MapAction\Projects\Metis\TaskManager'        
    json_dir = r'json_examples'                                
    json_dir = os.path.join(root, json_dir)                   
    # Get all reports as a list of file paths
    reports = parse_directory(json_dir, ['.json'])
    # Loop through the folder of JSON reports
    # Process each source json file in turn
    # Append to a list object for final aggregation
    all_product_output = []
    for json_source in reports:
        print("Processing {0}...".format(json_source))
        df_processed_json = process_json_report(json_source)
        all_product_output.append(df_processed_json)
        print('Finished processing.')
    # Merge all dfs into a single df
    df_all = pd.concat(all_product_output)
    # Export to csv
    df_all.to_csv('merged_reports.csv', index=False)
    print('End.')


if __name__ == '__main__':
    main()


