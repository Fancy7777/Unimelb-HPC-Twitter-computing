##################
#Student Name: Derui Wagn
#Student ID: 679552
#Subject: Cluster and Cloud computing
##################
import json, time
from mpi4py import MPI
import numpy as np
from collections import OrderedDict


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# load melbgrid data
with open('melbGrid.json') as data_file:
    melGrid_data = json.load(data_file)

# save the melgrid information into melGrid list
melGrid = []
for index in range(len(melGrid_data.get("features"))):
    melGrid.append(melGrid_data.get("features")[index].get("properties"))


# return the section id of this location
def location(y, x):
    for item in melGrid:
        if item.get("xmin") <= x <= item.get("xmax") and item.get("ymin") <= y <= item.get("ymax"):
            return item.get("id")
    return "not_found"


# return a dictionary of counting section of the dataset
def count_each_section(tweet_coordinates):
    result = OrderedDict()
    for coordinate in tweet_coordinates:
        section = location(coordinate[0], coordinate[1])
        result[section] = result.get(section, 0) + 1
    del result["not_found"]
    sorted_result = OrderedDict(sorted(result.items(), key = lambda x:x[1], reverse = True))
    return sorted_result

#filter the location. save labour
def filter_location(x,y):
    if (( y> 145.45) or (y < 144.7)) and ((x < -38.1) or (x > -37.5)):
        return False
    elif (y > 145.3) and (x > -37.8):
        return False
    elif (y < 145.15) and (x < -37.95):
        return False
    else:
        return True

def load_send_data():
    # load smalltwitter data. loads line by line
    if rank == 0:  
        twitter_data = []
        with open('bigTwitter.json') as data_file:
            for line in data_file:
                if line[0] == '{':
                    line = line[:-1]
                    if line[-1] == ',':
                        #get the coordinates 
                        coordinate =json.loads(line[:-1]).get('json').get('geo').get("coordinates")
                        if filter_location(coordinate[0],coordinate[1]):
                            twitter_data.append(coordinate)
                    else:
                        twitter_data.append(json.loads(line).get('json').get('geo').get("coordinates"))
        # split the data into several  parts
        data = np.array_split(twitter_data, size)    
    else:
        data = None
    ##scatter the processed data to other rank

    data = comm.scatter(data, root=0)
    return data




def gather_process_data(data):
    #for each other rank. run the fuctions to count the data parralle
    for r in range(size):
        if rank == r:
            newData = count_each_section(data)
    #gather data from other ranks
    new_Data = comm.allgather(newData)

    #combine all the data in one set
    if len(new_Data) > 1:
        finalData = new_Data[0]
        for index in range(1, len(new_Data)):
            for key, value in new_Data[index].items():
                if key in finalData.keys():
                    finalData[key] = finalData.get(key, 0) + value
                else:
                    finalData[key] = value
    else:
        finalData = newData
    return finalData

def print_result(finalData):
    #go back to rank 0 and print all the result
    if rank == 0:
        print("Order (rank) the Grid boxes based on the total number of "
               "tweets made in each box and return the total count of tweets in each box: ")
        for item in finalData.items():
            print(str(item[0]) + ": " + str(item[1]) + " tweets")

        # Row number rank
        row_rank = OrderedDict()
        for item in finalData.items():
            if item[0] in ("A1", "A2", "A3", "A4"):
                row_rank["A-Row"] = row_rank.get("A-Row", 0) + item[1]
            elif item[0] in ("B1", "B2", "B3", "B4"):
                row_rank["B-Row"] = row_rank.get("B-Row", 0) + item[1]
            elif item[0] in ("C1", "C2", "C3", "C4", "C5"):
                row_rank["C-Row"] = row_rank.get("C-Row", 0) + item[1]
            elif item[0] in ("D3", "D4", "D5"):
                row_rank["D-Row"] = row_rank.get("D-Row", 0) + item[1]

        print("\n")
        row_rank_sort = OrderedDict(sorted(row_rank.items(), key = lambda x:x[1], reverse = True))
        print("Order (rank) the rows based on the total number of tweets in each row:")
        for item in row_rank_sort.items():
            print(item[0] + ": " + str(item[1]))
        
        # column number rank
        column_rank = OrderedDict()
        for item in finalData.items():
            if item[0] in ("A1", "B1", "C1"):
                column_rank["Column 1"] = column_rank.get("Column 1", 0) + item[1]
            elif item[0] in ("A2", "B2", "C2"):
                column_rank["Column 2"] = column_rank.get("Column 2", 0) + item[1]
            elif item[0] in ("A3", "B3", "C3", "D3"):
                column_rank["Column 3"] = column_rank.get("Column 3", 0) + item[1]
            elif item[0] in ("A4", "B4", "C4"):
                column_rank["Column 4"] = column_rank.get("Column 4", 0) + item[1]
            elif item[0] in ("C5", "D5"):
                column_rank["Column 5"] = column_rank.get("Column 5", 0) + item[1]

        print("\n")
        #print column_rank
        column_rank_sort = OrderedDict(sorted(column_rank.items(), key = lambda x:x[1], reverse = True))
        print("Order (rank) the columns based on the total number of tweets in each column:")
        for item in column_rank_sort.items():
            print(item[0] + ": " + str(item[1]))
    else:
        pass

def main():
    data = load_send_data()
    finalData = gather_process_data(data)
    print_result(finalData)


if __name__ == '__main__':
    main()