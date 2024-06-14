import json
import argparse
import random
#Reads a JSON file and returns a JSON dictionnary.
def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
    
#Method to display the menu for the user
def display_menu():
    print("\n1. Display Global Statistics")
    print("2. Display Base Station Statistics")
    print("\t2.1. Statistics for a random station")
    print("\t2.2. Choose a station by Id")
    print("3. Check Coverage")
    print("4. Exit\n")


#Function that calculates all the global statistics and prints it to the user console.
def calculate_global_statistics(data):
    base_stations = data['baseStations'] #Get the list of Base Stations
    num_base_stations = len(base_stations) #Calculate the number of base stations
    antennas = [ant for bs in base_stations for ant in bs['ants']]
    num_antennas = len(antennas) #Calculate the number of antennas
    
    antennas_per_bs = [len(bs['ants']) for bs in base_stations]
    max_antennas_per_bs = max(antennas_per_bs) # Get the maximum number of antennas per base station
    min_antennas_per_bs = min(antennas_per_bs)
    avg_antennas_per_bs = sum(antennas_per_bs) / num_base_stations
    
    all_points = set()
    points_covered_once = set()
    points_covered_multiple = set()
    
    #Loop through each antenna and check if the point is covered once or multiple times and store the coordiantes in their appropriate sets.
    for ant in antennas:
        points = set(tuple(pt)[:2] for pt in ant['pts'])
        all_points.update(points)
        for point in points:
            if point in points_covered_once:
                points_covered_multiple.add(point)
                points_covered_once.remove(point)
            elif point not in points_covered_multiple:
                points_covered_once.add(point)
    
    #Get the MIN/MAX latitude and longitude in order to calculate the Total Squares(Points) covered by our antennas
    min_lat = data['min_lat']
    max_lat = data['max_lat']
    min_lon = data['min_lon']
    max_lon = data['max_lon']
    step = data['step']
    
    #Getting the number of latitude and longitude points we have. We then multiply them to get the number of all points.
    lat_points = round((max_lat - min_lat) / step) + 1
    lon_points = round((max_lon - min_lon) / step) + 1
    total_possible_points = lat_points * lon_points
    num_points_covered_once = len(points_covered_once)
    num_points_covered_multiple = len(points_covered_multiple)
    num_points_not_covered = total_possible_points - num_points_covered_once - num_points_covered_multiple
    
    #Loop through antennas to find the maximum/average number covering one point
    max_antennas_covering_point = max(len([ant for ant in antennas if point in set(tuple(pt)[:2] for pt in ant['pts'])]) for point in all_points)
    avg_antennas_covering_point = sum(len([ant for ant in antennas if point in set(tuple(pt)[:2] for pt in ant['pts'])]) for point in all_points) / len(all_points)
    
    #Points covered/total nb of points in order to get the percentage of points covered.
    coverage_percentage = (num_points_covered_once + num_points_covered_multiple) / total_possible_points * 100
    
    antenna_covering_max_points = max(antennas, key=lambda ant: len(ant['pts']))
    bs_id_max_points = [bs['id'] for bs in base_stations if antenna_covering_max_points in bs['ants']][0]
    
    #Print the results to the user
    print(f"Total number of base stations = {num_base_stations}")
    print(f"Total number of antennas = {num_antennas}")
    print(f"Max, min, and average of antennas per BS = {max_antennas_per_bs}, {min_antennas_per_bs}, {avg_antennas_per_bs:.2f}")
    print(f"Total number of points covered by exactly one antenna = {num_points_covered_once}")
    print(f"Total number of points covered by more than one antenna = {num_points_covered_multiple}")
    print(f"Total number of points not covered by any antenna = {num_points_not_covered}")
    print(f"Maximum number of antennas that cover one point = {max_antennas_covering_point}")
    print(f"Average number of antennas covering a point = {avg_antennas_covering_point:.2f}")
    print(f"Percentage of the covered area = {coverage_percentage:.2f}%")
    print(f"ID of the base station and antenna covering the maximum number of points = base station {bs_id_max_points}, antenna {antenna_covering_max_points['id']}")


#Function to calculate the statsitcs of a specific base station.
def calculate_base_station_statistics(data, station_id=None):
    
    #If the user does not specify an ID. We choose a random base station
    if station_id is None:
        station_id = random.choice([bs['id'] for bs in data['baseStations']])
    try:
        base_station = next(bs for bs in data['baseStations'] if bs['id'] == station_id) ##Search all basestations and return the basestation that has the same id as the user input.
    except: 
        print("Invalid ID! Please try again!")
        return
    
    if(base_station == None):
        print("Invalid ID! Please try again!")
        return
    antennas = base_station['ants']
    num_antennas = len(antennas)
    
    points_covered_once = set()
    points_covered_multiple = set()
    all_points = set()
    
    #Loop through each antenna
    for ant in antennas:
        points = set(tuple(pt)[:2] for pt in ant['pts'])
        all_points.update(points)
        for point in points:
            if point in points_covered_once: #If the point covered is already in the points_covered_once set then this points has been covered multiple times so we move it to points_covered_multiple set.
                points_covered_multiple.add(point)
                points_covered_once.remove(point)
            elif point not in points_covered_multiple:
                points_covered_once.add(point)
    
    
    # Get the MIN/MAX latitude and longitude in order to calculate the Total Squares(Points) covered by our antennas
    min_lat = data['min_lat']
    max_lat = data['max_lat']
    min_lon = data['min_lon']
    max_lon = data['max_lon']
    step = data['step']
    #Getting the total number of latitude and longitued points then multiplying one another to get total number of points
    lat_points = round((max_lat - min_lat) / step) + 1
    lon_points = round((max_lon - min_lon) / step) + 1
    total_possible_points = lat_points * lon_points
    num_points_covered_once = len(points_covered_once)
    num_points_covered_multiple = len(points_covered_multiple)
    num_points_not_covered = total_possible_points - num_points_covered_once - num_points_covered_multiple
    num_points_covered_once = len(points_covered_once)
    num_points_covered_multiple = len(points_covered_multiple)
    num_points_not_covered = len(all_points) - num_points_covered_once - num_points_covered_multiple
    
    #Loop through the antennas to find the max/average number of antennas covering one point
    max_antennas_covering_point = max(len([ant for ant in antennas if point in set(tuple(pt)[:2] for pt in ant['pts'])]) for point in all_points)
    avg_antennas_covering_point = sum(len([ant for ant in antennas if point in set(tuple(pt)[:2] for pt in ant['pts'])]) for point in all_points) / len(all_points)
    
    #Calculate the percentage of points covered by the antennas
    coverage_percentage = (num_points_covered_once + num_points_covered_multiple) / total_possible_points * 100
    
    #Get the ID of the antenna covering the maximum amount of points
    antenna_covering_max_points = max(antennas, key=lambda ant: len(ant['pts']))
    
    #Print results
    print(f"Base station {station_id} statistics:")
    print(f"Total number of antennas = {num_antennas}")
    print(f"Total number of points covered by exactly one antenna = {num_points_covered_once}")
    print(f"Total number of points covered by more than one antenna = {num_points_covered_multiple}")
    print(f"Total number of points not covered by any antenna = {num_points_not_covered}")
    print(f"Maximum number of antennas that cover one point = {max_antennas_covering_point}")
    print(f"Average number of antennas covering a point = {avg_antennas_covering_point:.2f}")
    print(f"Percentage of the covered area = {coverage_percentage:.2f}%")
    print(f"ID of the antenna covering the maximum number of points = {antenna_covering_max_points['id']}")


#Function that takes in coordiantes and determines whether any antennas cover it. If no antennas does, we display the nearest antennas to the user.
def check_coverage(data, lat, lon):
    base_stations = data['baseStations']
    all_points = set()
    points_with_antenna_info = {}
    
    #Loop through each base station
    for bs in base_stations:
        #Loop through each antenna in the base station
        for ant in bs['ants']:
            for pt in ant['pts']:
                point = (pt[0], pt[1])
                all_points.add(point)
                if point not in points_with_antenna_info:
                    points_with_antenna_info[point] = []
                points_with_antenna_info[point].append((bs['id'], ant['id'], pt[2]))
    
    point = (lat, lon)
    #Check if coordinates provided are covered by an antenna
    if point in points_with_antenna_info:
        print(f"The point ({lat}, {lon}) is covered by the following antennas:")
        for info in points_with_antenna_info[point]:
            print(f"Base station {info[0]}, Antenna {info[1]}, Received power {info[2]}")
    else:
        #If not, get the nearest point to the coordinates provided by the user
        nearest_point = min(all_points, key=lambda p: (p[0] - lat)**2 + (p[1] - lon)**2) #Compare between the coordinates entered and antennas, the minimum is the closest.
        nearest_info = points_with_antenna_info[nearest_point][0] #Get the nearest point information
        print(f"The point ({lat}, {lon}) is not explicitly covered. Nearest antenna information:")
        print(f"Base station {nearest_info[0]}, Antenna {nearest_info[1]}, Received power {nearest_info[2]}")

def main():
    #Parse through the arguments passed in the command line to get the path of our json file
    parser = argparse.ArgumentParser(description="Cellular Network Coverage")
    parser.add_argument('file', type=str, help='JSON file with coverage data')
    args = parser.parse_args()
    try:
        data = read_json(args.file)
    except:
        print("Could not open JSON file!")

    while True:
        #Display the menu for the user to choose.
        display_menu()
        try:
            choice = input("Enter your choice: ")
        except:
            print("Invalid entry! Please make sure to enter a number!")
        if choice == '1':
            calculate_global_statistics(data)
        elif choice == '2':
            print(f"Please choose one of the sub-menus of choice {choice}\n")
        elif choice == '2.1':
            # make a random choice from the IDs we have in baseStations.
            station_id = random.choice([bs['id'] for bs in data['baseStations']])
            calculate_base_station_statistics(data, station_id)
        elif choice == '2.2':
            try:
                station_id = int(input("Enter base station ID: "))
                calculate_base_station_statistics(data, station_id)
            except:
                print("Invalid entry! Please make sure to enter a number")
        elif choice == '3':
            try:
                lat = float(input("Enter latitude: "))
                lon = float(input("Enter longitude: "))
                check_coverage(data, lat, lon)
            except:
                print("Invalid Entry! Please enter the correct coordinates")
            
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == '__main__':
    main()
