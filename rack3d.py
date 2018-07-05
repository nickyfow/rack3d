#!/usr/bin/env python3
import mysql.connector

# location id of the datacenter
locationId=1
# output files
objFile="/tmp/dc.obj"
mtlFile="/tmp/dc.mtl"
#database settings
con = mysql.connector.connect(host="",database="",user="",password="")

obj = open(objFile, 'w')
mtl = open(mtlFile, 'w')
cur1 = con.cursor()
cur2 = con.cursor()
cur3 = con.cursor()
cur4 = con.cursor()
vert=0
face=0
rowCount=0
rackCount=0
# get all rows
query1 = "SELECT r.name AS rowName, r.id AS rowId FROM Object AS r INNER JOIN EntityLink AS e ON r.id = e.child_entity_id WHERE e.parent_entity_id = \""+str(locationId)+"\" ORDER BY r.name"
cur1.execute(query1)
result1 = cur1.fetchall()
for (rowName, rowId) in result1:
    # for each row, get all racks
    query2 = "SELECT rack.name AS rackName, rack.id AS rackId FROM Object AS rack INNER JOIN EntityLink AS e ON rack.id = e.child_entity_id WHERE e.parent_entity_id ="+str(rowId) 
    cur2.execute(query2)
    result2 = cur2.fetchall()
    for (rackName, rackId) in result2:
        # for each rack, get all the objects
        query3 = "SELECT DISTINCT o.name AS objName, o.id AS objId, o.objtype_id AS objType FROM Object AS o INNER JOIN RackSpace AS r ON o.id = r.object_id WHERE (o.objtype_id=4 OR objtype_id=8 OR objtype_id=9) AND r.rack_id="+str(rackId)
        cur3.execute(query3)
        result3 = cur3.fetchall()
        for (objName, objId, objType) in result3:
            # for each object, get unit and depth
            query4 = "SELECT unit_no AS unit, atom FROM RackSpace WHERE object_id = "+str(objId)
            cur4.execute(query4)
            result4 = cur4.fetchall()
            maxUnit=0
            minUnit=50
            maxDepth=0
            minDepth=4
            for (unit,atom) in result4:
                if ( unit < minUnit ):
                    minUnit = unit
                if ( unit > maxUnit ):
                    maxUnit = unit  
                if ( atom == "front" ):
                    depth=0
                if ( atom == "interior" ):
                    depth=1
                if ( atom == "rear" ):
                    depth=2
                if ( depth < minDepth ):
                    minDepth = depth
                if ( depth > maxDepth ):
                    maxDepth = depth
            # calculate x,y,z in meters
            if ( rowCount % 2 == 0 ):
                xMin = ( rowCount * 2.4 ) + 1.2 - ( maxDepth * 0.4 ) - 0.4
                xMax = ( rowCount * 2.4 ) + 1.2 - ( minDepth * 0.4 )
            else:
                xMin = ( rowCount * 2.4 ) + ( minDepth * 0.4 )
                xMax = ( rowCount * 2.4 ) + ( maxDepth * 0.4 ) + 0.4
            yMin = ( rackCount * 0.6 ) + 0.01
            yMax = ( rackCount * 0.6 ) + 0.59
            zMin = ( minUnit * 0.05 )
            zMax = ( maxUnit * 0.05 ) + 0.045
            # generate rgb values by object type
            blue=0.5
            green=0.5
            red=0.5
            if ( objType == 4 ):
                blue=0.75
                green=0.75
                red=1.0
            if ( objType == 8 ):
                blue=0.75
                green=1.0
                red=0.75
            if ( objType == 9 ):
                blue=1.0
                green=0.75
                red=0.75
            # rotate -90 on x axis to compensate for blender import script
            temp = yMin
            yMin = zMin
            zMin = yMax*-1
            yMax = zMax
            zMax = temp*-1
            # export to obj file
            obj.write("o {}\n".format(objName))
            obj.write("v {} {} {}\n".format(xMin,yMin,zMin))
            obj.write("v {} {} {}\n".format(xMin,yMax,zMin))
            obj.write("v {} {} {}\n".format(xMax,yMax,zMin))
            obj.write("v {} {} {}\n".format(xMax,yMin,zMin))
            obj.write("v {} {} {}\n".format(xMin,yMin,zMax))
            obj.write("v {} {} {}\n".format(xMin,yMax,zMax))
            obj.write("v {} {} {}\n".format(xMax,yMax,zMax))
            obj.write("v {} {} {}\n".format(xMax,yMin,zMax))
            obj.write("vn 0.0 0.0 -1.0\n")
            obj.write("vn 0.0 0.0 1.0\n")
            obj.write("vn 0.0 1.0 0.0\n")
            obj.write("vn 1.0 0.0 0.0\n")
            obj.write("vn 0.0 -1.0 0.0\n")
            obj.write("vn -1.0 0.0 0.0\n")
            obj.write("usemtl {}\n".format(objName))
            obj.write("s off\n")
            obj.write("f {}//{} {}//{} {}//{} {}//{}\n".format( (vert+1), (face+1), (vert+2), (face+1), (vert+3), (face+1), (vert+4), (face+1)))
            obj.write("f {}//{} {}//{} {}//{} {}//{}\n".format( (vert+5), (face+2), (vert+8), (face+2), (vert+7), (face+2), (vert+6), (face+2)))
            obj.write("f {}//{} {}//{} {}//{} {}//{}\n".format( (vert+2), (face+3), (vert+6), (face+3), (vert+7), (face+3), (vert+3), (face+3)))
            obj.write("f {}//{} {}//{} {}//{} {}//{}\n".format( (vert+3), (face+4), (vert+7), (face+4), (vert+8), (face+4), (vert+4), (face+4)))
            obj.write("f {}//{} {}//{} {}//{} {}//{}\n".format( (vert+4), (face+5), (vert+8), (face+5), (vert+5), (face+5), (vert+1), (face+5)))
            obj.write("f {}//{} {}//{} {}//{} {}//{}\n".format( (vert+1), (face+6), (vert+5), (face+6), (vert+6), (face+6), (vert+2), (face+6)))
            obj.write("\n")
            vert = vert + 8
            face = face + 6
            # export to material file
            mtl.write("newmtl {}\n".format(objName))
            mtl.write("Ns 96.078431\n")
            mtl.write("Ka 1.000000 1.000000 1.000000\n");
            mtl.write("Kd {} {} {}\n".format(red,green,blue))
            mtl.write("Ks 0.500000 0.500000 0.500000\n");
            mtl.write("Ke 0.000000 0.000000 0.000000\n");
            mtl.write("Ni 1.000000\n");
            mtl.write("d 1.000000\n");
            mtl.write("illum 2\n");
            mtl.write("\n");
        rackCount=rackCount+1      
    rowCount=rowCount+1
    rackCount = 0
obj.close()
mtl.close()

