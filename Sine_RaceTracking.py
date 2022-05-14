"""This script will extract points and lap data from the supplied CSV and populate a
shapefile with each lap as a seperate polyline. It also provides some basic speed
statistics. O&A additons elements of tracking the top speed and printing it for each lap,
and a race total, in the console. Tried to write it into an additional field for each lap
in the shapefile, but ran out of time before I could fully figure it out. 

Created by: Patrick Sine, December 2021"""

#import arcpy & csv modules, allow overwrite of files, and set workspace.
import arcpy
import csv
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"C:\Users\Patrick\PSU\GEOG485\Lesson4"
#Variables for paths, spatial ref, also create a blank shapefile then add new field
spatialRef = arcpy.SpatialReference(4326) #Factory code for WGS 1984
outPath = arcpy.env.workspace
raceFC = r"WakefieldLaps.shp"
arcpy.CreateFeatureclass_management(outPath, raceFC, "POLYLINE", "","","", spatialRef)
arcpy.AddField_management(raceFC, "LapNo", "SHORT") #*
#path to csv, and variable/list/dictionary creation for use in loops                           
raceCSV = r"C:\Users\Patrick\PSU\GEOG485\Lesson4\WakefieldParkRaceway_20160421.csv"
lapNo = 0
raceDictionary = {}
lapList = []
speedList = []
lapSpeedList = []

try: #Error handeling with try/except
    with open(raceCSV, "r") as raceGPS: #opening CSV with reader
        csvReader = csv.reader(raceGPS)
        header = next(csvReader) #reading header
        print (header) #Code check and user interface message
        latIndex = header.index("Latitude") #index value in header for latitude
        lonIndex = header.index("Longitude") #index value in header for longitude
        lapIndex = header.index("Lap") #index value in header for lap number
        speedIndex = header.index("Speed (KM/H)") #index value in header for speed
       #Start reading through the rows of the CSV
        for row in csvReader:
            if row[0].startswith("#"): # "Starts with a #" i.e. inbetween laps
                  lapNo = lapNo + 1 #*Increment lap counter 
                  lapTopSpeed = max(lapSpeedList) #find highest value in speed list
                  lapSpeedList = [] # Reset list for next lap
                  with arcpy.da.InsertCursor(raceFC, ("SHAPE@", "LapNo")) as cursor: #inserting ployline and lap number
                      for item in raceDictionary:
                          cursor.insertRow((lapList, item))
                          raceDictionary = {} #Reset for next lap
                      del cursor #Delete cursor for good parctice's sake
                  print ("Done lap " + str(lapNo) + ", top speed of " + str(lapTopSpeed) + " kph.") #Code check and user interface message
                  next #Move on to next row
            else: #If it doesn't "start with a #"...
                if row[0].isnumeric: #*If it's numeric i.e. race data...
                    lat = row[latIndex] #Assign a variable with the latitude
                    lon = row[lonIndex] #Assign a variable with the longitude
                    lap = row[lapIndex] #Assign a variable with the lap number
                    coordPair = (lon,lat) #*Glad to catch this early on via Pro, but why is this not ordered lat then lon????
                    speed = float(row[speedIndex]) #Assign a variable with the speed 
                    speedList.append(speed) #Add the speed to the cumulative speedList
                    lapSpeedList.append(speed) #Add the speed to the lap's speedList
                    lapList.append(coordPair) #Add the lat/lon pair to the lap's coordinate list
                    if lap in raceDictionary: #If the current lap number is a key in the race dictionary...
                        raceDictionary[lap] = lapList  #Add in the most recent coordinates
                    elif lap not in raceDictionary: #*If the current lap is not a key found in the dictionary...
                        newLap = [coordPair] #Begin single item list of the current point
                        raceDictionary[lap] = newLap #Add it to the race dictionary with a new key of the current lap number
                        lapList = [] #Reset the lap coordinate list for next time  
    topSpeed = max(speedList) #Find the top speed of the whole race    
    print ("\nDone shapefile, "+ str(lapNo) + " laps created in " + str(raceFC)) #Code Checking/user interface message
    print (str(topSpeed) + " kph was your top speed for the day!") #Code Checking/user interface message
            
                
except: #Error handeling 
    print ("Error, try again.")