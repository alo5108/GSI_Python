import arcpy
arcpy.env.overwriteOutput = True

print "********************************************************************************************************************************"                                                                                                                     
print "*Call function createLiDARCircuit, 4 parameters (circuit, PriOH, output, input)                                                *"
print "********************************************************************************************************************************"  
print "Example createLiDARCircuit('214', r'C:\GIS\PriOH.shp,r'C:\Temp\Data.gdb\LiDAR_Circuit,C:\Temp\GDI_pointfile) --> will return all spans for circuit 214"
print " "
print "Variable --> PriOH is the client provided GIS file,  for example:"
print "    r'C:\GIS\PriOH.shp --> Needs to be changed to the location of the local ShapeFile representive of the GIS data"
print "Variable --> output is the polyline file that will be populated (connect the dots) between the LiDAR poles,  for example:"
print "    r'C:\Temp\Data.gdb\LiDAR_Circuit --> Needs to be changed to location of the output featureClass"
print "Variable --> input is the point file representitive of the LiDAR derived pole locations.  ***Note: It is expected to have the"
print "    attribute fields named XCOORD and YCOORD popluted.  A field called NAME is expected to hold the pole ID"


def isDuplicate(input_LiDAR):

    arr = []
    arrDUP = []


    rows = arcpy.SearchCursor(input_LiDAR)

    
        
    for row in rows:
        if row.name in arr:
            #print "DUP - " + str(row.name)
            arrDUP.append(row.name)
        arr.append(row.name)

    print "These poles are duplicates in the database:"
    print   u', '.join(arrDUP)


def createLiDARCircuit(circuit, eGIS_PriOH, outputFC, inputFC):

    print "You chose circuit " + str(circuit)

    #check for duplicate poleIDs - 1st STEP

    arr = []
    arrDUP = []


    rows = arcpy.SearchCursor(inputFC)

    
        
    for row in rows:
        if row.name in arr:
            #print "DUP - " + str(row.name)
            arrDUP.append(row.name)
        arr.append(row.name)

    print  u', '.join(arrDUP)

    
    #Where is the Circuit INFO?  --> Actual featureClass Line information with
    #upstream and downstream data?



    #set variable here :
    #circuitFC = r'C:\GIS\SDGE\Circuits_2017_08_17.shp'
    circuitFC = eGIS_PriOH

    # A list that will hold each of the Polyline objects
    
    features = []


    #Add an array to input the globalIDs that are being added to the LiDAR output featureClass
    arrGlobalID = []


    i = 0  # for testing to break out of loop

    #Locationpolyline added after LiDAR coords determined
    #fc2 = r'C:\Temp\Data.gdb\LiDAR_Circuit'
    fc2 = outputFC


    #set query of specified circuit ID (FEEDERID?)
    rows = arcpy.SearchCursor(circuitFC, "FEEDERID = '" + circuit + "'")
    
    #print "This is a linear feature which contain span, each has an upstream and downstream pole:"
    for row in rows:
        i = i + 1
        #print i
        
        #Capture UpStream variable
        upStr = row.UPSTREAMSTRUCTUREID
 
        #Capture DownStream variable
        DownStr = row.DOWNSTREAMSTRUCTUREID
        #print row.DOWNSTREAM

        #LiDARFC = r'C:\GIS\SDGE\FiRM\Pole_Bottoms_11132017.gdb\LiDAR_Structures_060717'
        LiDARFC = inputFC

        LiDARRowsUp = arcpy.SearchCursor(LiDARFC, "NAME= '" + upStr + "'")
        
        #If a matching LiDAR pole exists for the uptream pole of this segment
        # get that upstream poles X and Y coords, then get the Downstream X,Y
        # WHAT IF Upstream pole has LiDAR not downstream??
        for row2 in LiDARRowsUp:

            xU = 0
            xD = 0
            
            xU = (row2.XCOORD)
            yU = (row2.YCOORD)

            LiDARRowsDown = arcpy.SearchCursor(LiDARFC, "NAME = '" + DownStr + "'")
            
            for row2 in LiDARRowsDown:
                xD = (row2.XCOORD)
                yD = (row2.YCOORD)

            #Check that downstream x,y populated if not break out
            if xD == 0:
                #print 'OUT!'
                break

            #At this point, UpStr DownStr X, Y coords should exist, draw!

            cursor = arcpy.da.InsertCursor(fc2, ("SHAPE@","globalid","upStr","downStr","xU","yU","xD","yD"))

            #for line in lines:
            
            coordList=[]

            coordList.append([float(xU),float(yU)])
            coordList.append([float(xD),float(yD)])

            polyline = arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in coordList]))
            cursor.insertRow((polyline,row.GLOBALID,upStr,DownStr,xU,yU,xD,yD))
            arrGlobalID.append(row.GLOBALID)

    rows = arcpy.SearchCursor(circuitFC, "FEEDERID = '" + circuit + "'")

    #make array to hold missing span GlobalIDs
    dupGIDs = []
    for row in rows:
        if row.GlobalID in arrGlobalID:
            continue
        else:
            print "You are missing Span " + row.UPSTREAMSTRUCTUREID + " to - "  + row.DOWNSTREAMSTRUCTUREID
            dupGIDs.append(row.GlobalID)

    
    print  u', '.join(dupGIDs)   
    

        
            
           
            

            

        
        
