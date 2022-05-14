"""
@author: Patrick
"""
from datetime import date
today = str(date.today())
yearToday = int(today[2:4])
import arcpy, csv
arcpy.env.qualifiedFieldNames = False
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"C:\Users\Patrick\PSU\GEOG485\FPro\BearHunt.gdb"
#counties = "PaCounty2021_06.shp"
counties = "PaCounties"
bearHarvestCSV = "PoconoBearHarvestSimple.csv"
print ("Consult the CSV, and type the field of the year to begin on. \nHint, it's: total_3")
startYear = "total_20"#input()
currentYear = int(startYear[6:])
#allYearsMap = "bearHarvest_AllYears.shp"
#thisYearsMap = ("bearHarvest_2K" + str(currentYear) + ".shp")
allYearsMap = "bearHarvest_AllYears"
thisYearsMap = ("bearHarvest_2K" + str(currentYear))
acreField = "AREA_Acres"
mileToAcre = "!AREA_SQ_MI!  *  640"
joinField = "FIPS_Co"
fipsList = []
huntList = []
thisYearDict = {}
#yearList = []
totalDict = {}
completeDict = {}
regionNO = 1
loopCount = 0
try: #Error handeling via try except
    #print( [h.name for h in arcpy.ListFields(bearHarvestCSV)])
    #print( [f.name for f in arcpy.ListFields(counties)])
    arcpy.management.CalculateField(counties, joinField, "!FIPS_COUNT!", "PYTHON3", '', "SHORT", "")
    arcpy.management.CalculateField(counties, acreField, mileToAcre, "PYTHON3", '', "LONG", "")
    joinedTable = arcpy.AddJoin_management(counties, "FIPS_Co", bearHarvestCSV, joinField, "KEEP_COMMON", "")
    arcpy.management.CopyFeatures(joinedTable, allYearsMap)
    print ([n.name for n in arcpy.ListFields(allYearsMap)])

    while currentYear < yearToday:  
        print ("Creating harvest map for year: " + str(currentYear) )
        with open(bearHarvestCSV, "r") as poconoBears: 
            csvReader = csv.reader(poconoBears)
            header = next(csvReader) 
            #print (header) #Code Checking 
            harvestIndex = header.index(startYear)
            countyIndex = header.index("Short County Name")
            #prnIndex = header.index("PRN")
            FIPS = header.index(joinField)
            for row in csvReader:
                    
                if row[0].startswith("PRN" + str(regionNO)):
                    #print ("yay, done region " + str(regionNO))
                    count = row[harvestIndex]
                    huntYR = header[harvestIndex]
                    county = row[countyIndex]
                    fips = row[FIPS]
                    fipsList.append(fips)
                    huntList.append(count)
                    totalDict[huntYR] = huntList
                    #yearList.append(count)
                    thisYearDict["FIPS" + fips + " " + county] = count
                    regionNO = regionNO + 1
                   
                elif row[0].startswith("#"):
                    validFIPS = fipsList
                    completeDict[huntYR] = thisYearDict
                    thisYearsMap = ("bearHarvest_2K" + str(currentYear))
                    arcpy.management.CopyFeatures(counties, thisYearsMap)
                    arcpy.management.AddField(thisYearsMap, startYear, "LONG", "", "", "")
                    #use update cursor to assign values to rows for each county's annual total (huntlist)
                    #calculateField Harvest/Acre
                    #print ("Done, now doing next year.")    
                    regionNO = 1
                    #validFIPS = fipsList
                    thisYearDict = {}
                    fipsList = []
                    huntList=[]
                    currentYear = currentYear + 1
                    startYear = (startYear[:6] + str(currentYear))
                    harvestIndex = harvestIndex - 1
                    loopCount = loopCount + 1
                
    else:
        print ("\nEverything complete: \n"+ str(loopCount) + " annual map(s) created, \n1 map created of all years combined. \n\nSee you next year.")
            
except:
    print("Error, consult your brain... or google.")