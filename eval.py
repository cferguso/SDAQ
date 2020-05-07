#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Charles.Ferguson
#
# Created:     05/05/2020
# Copyright:   (c) Charles.Ferguson 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def CreateNewTable(newTable, columnNames, columnInfo):
    # Create new table. Start with in-memory and then export to geodatabase table
    #
    # ColumnNames and columnInfo come from the Attribute query JSON string
    # MUKEY would normally be included in the list, but it should already exist in the output featureclass
    #
    try:
        # Dictionary: SQL Server to FGDB
        dType = dict()

        dType["int"] = "long"
        dType["smallint"] = "short"
        dType["bit"] = "short"
        dType["varbinary"] = "blob"
        dType["nvarchar"] = "text"
        dType["varchar"] = "text"
        dType["char"] = "text"
        dType["datetime"] = "date"
        dType["datetime2"] = "date"
        dType["smalldatetime"] = "date"
        dType["decimal"] = "double"
        dType["numeric"] = "double"
        dType["float"] = "double"

        # numeric type conversion depends upon the precision and scale
        dType["numeric"] = "float"  # 4 bytes
        dType["real"] = "double"  # 8 bytes

        # Iterate through list of field names and add them to the output table
        i = 0

        # ColumnInfo contains:
        # ColumnOrdinal, ColumnSize, NumericPrecision, NumericScale, ProviderType, IsLong, ProviderSpecificDataType, DataTypeName
        # PrintMsg(" \nFieldName, Length, Precision, Scale, Type", 1)

        joinFields = list()
        outputTbl = os.path.join("IN_MEMORY", os.path.basename(newTable))
        arcpy.CreateTable_management(os.path.dirname(outputTbl), os.path.basename(outputTbl))

        for i, fldName in enumerate(columnNames):
            vals = columnInfo[i].split(",")
            length = int(vals[1].split("=")[1])
            precision = int(vals[2].split("=")[1])
            scale = int(vals[3].split("=")[1])
            dataType = dType[vals[4].lower().split("=")[1]]

            if fldName.lower().endswith("key"):
                # Per SSURGO standards, key fields should be string. They come from Soil Data Access as long integer.
                dataType = 'text'
                length = 30

            arcpy.AddField_management(outputTbl, fldName, dataType, precision, scale, length)

        return outputTbl

    except:
        errorMsg()
    return False

def sdaCall(q):

    try:

        url = r'https://SDMDataAccess.sc.egov.usda.gov/Tabular/post.rest'


        # Create request using JSON, return data as JSON
        request = {}
        request["format"] = "JSON+COLUMNNAME+METADATA"
        request["query"] = q

        #json.dumps = serialize obj (request dictionary) to a JSON formatted str
        data = json.dumps(request)

        # Send request to SDA Tabular service using urllib2 library
        # because we are passing the "data" argument, this is a POST request, not a GET
        resp = requests.post(url, data)
        raw = (resp.text)


        # Convert the returned JSON string into a Python dictionary.
        qData = json.loads(raw)
        #qData = qData.decode('utf-8')
        print(qData)
        print(type(qData))

        # get rid of objects
        #del qResults, response, req

        # if dictionary key "Table" is found
        if "Table" in qData:

            return True, qData, resp

        else:
            cResponse = "muaggat failed for " + state
            return False, None, cResponse

    except socket.timeout as e:
        Msg = 'Soil Data Access timeout error'
        return False, None, Msg

    except socket.error as e:
        state + " = " + str(e)
        return False, None, Msg

    except HTTPError as e:
        Msg = state +  " = " + str(e)
        return False, None, Msg

    except urllib.error.URLError as e:
        state + " = " + str(e)
        return False, None, Msg

    except:
        #errorMsg()
        Msg = 'Unhandled error collecting SDA info'
        return False, None, Msg

import sys, os, requests, socket, json, urllib, arcpy
from requests import HTTPError

##get the query, url requires
url = 'https://raw.githubusercontent.com/cferguso/SDAQ/master/tax_order_stt_abbr.txt'
resp = requests.get(url)
raw = (resp.text)

# first line of query is the table name
firstL = raw.find("\n")
tblName = raw[2:firstL]


##clean up the placeholder parameters
raw = raw.replace("param1", "NE109")

##execute the SDA request
##cBool, cRes, cMsg = sdaCall(raw)
##
##if cBool:
##
##    ws = r'D:\Chad\GIS\scratch\scratch.gdb'
##
##    # dig into the results
##    sdaTbl = cRes.get('Table')
##    columnNames = sdaTbl.pop(0)
##    columnInfo = sdaTbl.pop(0)
##
##    # get the new, empty, in memory table with columsn ready from sda results
##    memTbl = CreateNewTable(tblName, columnNames=columnNames, columnInfo=columnInfo)
##
##    # stuff the results into the in mem table with the remaining data from sda
##    with arcpy.da.InsertCursor(memTbl, columnNames) as cursor:
##        for row in sdaTbl:
##            cursor.insertRow(row)
##
##    # finally, convert the in mem table to table on disk
##    arcpy.conversion.TableToTable(memTbl, ws, tblName)
##
##else:
##    print(cMsg)




