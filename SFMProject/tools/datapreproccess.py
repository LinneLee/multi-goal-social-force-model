import os
import re
import json

"""
preproccess Edinburgh Informatics Forum Pedestrian(Track) Database for socialforcemodel input
"""

def spacerepl(matchobj):
    if matchobj.group(0) == " ": return ", "

def stringToTrack(track_string):
    # [307 3 717]
    return [int(x) for x in track_string[1:-1].split(" ")]


file_name = r"G:\data\Edinburgh Informatics Forum Pedestrian Database\tracks.24Aug.txt"
# generate list for pedestrian into the forum 

json_data = {}
current_person_id = 0

with open(file=file_name) as f:
    for line in f:
        if line[:6] == "Proper":
            current_person_id += 1
            # line = re.sub("=", ":", line)
            # line = re.sub(" ", spacerepl, line)

            # Properties.{Identifier}= [ Number_of_Points_in_trajectory, Start_time, End_Time, Average_Size_of_Target,Average_Width, Average_height, Average_Histogram ];
            start_pos = re.search("=", line).span()[1] + 1
            pro = [float(x) if x!="" else None for x in line[start_pos:-3].split(" ")]
            # pro = [map(lambda x: float(x) if x!="" else None, line[15:-3].split(" "))]
            json_data[current_person_id] = {
                "Number_of_Points_in_Trajectory" : pro[0],
                "Start_Time" : pro[1],
                "End_Time" : pro[2],
                "Average_Size_of_Target" : pro[3],
                "Average_Width" : pro[4],
                "Average_Height" : pro[5],
                "Average_Histogram" : pro[6:]
            }
            # if current_person_id not in json_data.keys():
            #     json_data[current_person_id] = []
            # json_data[current_person_id].append({line})
            # print(json_data)

        if line[1:6] == "TRACK":
            # TRACK.{Identifier}= [[ centre_X(1) Centre_Y(1) Time(1)] ; [ centre_X(2) Centre_Y(2) Time(2)] ... and so on ... until ... [ centre_X(end) Centre_Y(end) Time(end) ]]
            start_pos = re.search("=", line).span()[1] + 1
            tracklet = [stringToTrack(x) if x!="" else None for x in line[start_pos:-3].split("; ")]
            add_json_data = {
                "Entry_Time": tracklet[0][2],
                "Entry_Position": tracklet[0][:-1],
                "Leave_Position": tracklet[-1][:-1],
                "Full_Tracklet": tracklet
            }
            
            json_data[current_person_id] = {**json_data[current_person_id], **add_json_data}
json_path = r"G:\data\Edinburgh Informatics Forum Pedestrian Database\tracks.24Aug.json"
with open(json_path, "w") as f:
    json.dump(json_data, f, indent=4)