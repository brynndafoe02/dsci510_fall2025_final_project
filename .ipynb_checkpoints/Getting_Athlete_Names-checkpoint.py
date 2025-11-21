import os
import csv

def getting_athlete_names():

    root = "."
    
    men_names = set()
    women_names = set()
    
    for folder in os.listdir(root):
        folder_path = os.path.join(root, folder)
        if os.path.isdir(folder_path):
            if folder.startswith("M_"):
                for file_name in os.listdir(folder_path):
                    if file_name.endswith(".csv"):
                        csv_path = os.path.join(folder_path, file_name)
                        with open(file=csv_path, mode="r") as f:
                            read_csv = csv.DictReader(f)
                            count = 0
                            for row in read_csv:
                                if count >= 30:
                                    break
                                name = row.get(" Name", "").strip()
                                if name:
                                    men_names.add(name)
                                count+=1
                            
            elif folder.startswith("W_"):
                for file_name in os.listdir(folder_path):
                    if file_name.endswith(".csv"):
                        csv_path = os.path.join(folder_path, file_name)
                        with open(file=csv_path, mode="r") as f:
                            read_csv = csv.DictReader(f)
                            count = 0
                            for row in read_csv:
                                if count >= 30:
                                    break
                                name = row.get(" Name", "").strip()
                                if name:
                                    women_names.add(name)
                                count+=1
            else:
                continue
    
    with open(file="Men_Names.csv", mode="w") as f:
        column_name = "Name\n"
        f.write(column_name)
        for name in men_names:
            f.write(f"{name}\n")
    
    with open(file="Women_Names.csv", mode="w") as f:
        column_name = "Name\n"
        f.write(column_name)
        for name in women_names:
            f.write(f"{name}\n")