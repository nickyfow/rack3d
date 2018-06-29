<?php

function map_dc($location_id){
    global $dbxlink;
    $objectArray=array();
    $rowCount=0;
    $rackCount=0;
    # rows
    $query1 = "SELECT row.name, row.id FROM Object AS row INNER JOIN EntityLink AS e ON row.id = e.child_entity_id WHERE e.parent_entity_id = \"".$location_id."\" ORDER BY row.name";
    if ($result1 = $dbxlink->query($query1)) {
        while($row1 = $result1->fetch(PDO::FETCH_ASSOC)) {
            # racks
            $query2 = "SELECT rack.name, rack.id FROM Object AS rack INNER JOIN EntityLink AS e ON rack.id = e.child_entity_id WHERE e.parent_entity_id =".$row1['id'];
            if ($result2 = $dbxlink->query($query2)) {
                while($row2 = $result2->fetch(PDO::FETCH_ASSOC)) {
                    # objects
                    $query3 = "SELECT DISTINCT o.name, o.id, o.objtype_id FROM Object AS o INNER JOIN RackSpace AS r ON o.id = r.object_id WHERE (o.objtype_id=4 OR objtype_id=8 OR objtype_id=9) AND r.rack_id=".$row2['id'];
                    if ($result3 = $dbxlink->query($query3)) {
                        while($row3 = $result3->fetch(PDO::FETCH_ASSOC)) {
                            # object unit and depth
                            $query4 = "SELECT unit_no, atom FROM RackSpace WHERE object_id = ".$row3['id'];
                            if ($result4 = $dbxlink->query($query4)) {
                                $maxUnit=0;
                                $minUnit=50;
                                $maxDepth=0;
                                $minDepth=4;
                                while($row4 = $result4->fetch(PDO::FETCH_ASSOC)) {
                                    $unit = intval($row4['unit_no']);
                                    if ( $unit < $minUnit ){
                                        $minUnit = $unit;
                                    }
                                    if ( $unit > $maxUnit ){
                                        $maxUnit = $unit;
                                    }
                                    if ( $row4['atom'] == "front" ){
                                        $depth=0;
                                    }
                                    if ( $row4['atom'] == "interior" ){
                                        $depth=1;
                                    }
                                    if ( $row4['atom'] == "rear" ){
                                        $depth=2;
                                    }
                                    if ( $depth < $minDepth ){
                                        $minDepth = $depth;
                                    }
                                    if ( $depth > $maxDepth ){
                                        $maxDepth = $depth;
                                    }
                                }
                            }
                            // generate xyz values
                            if ( $rowCount % 2 == 0 ){
                                $xMin = ( $rowCount * 2400 ) + 1200 - ( $maxDepth * 400 ) - 400;
                                $xMax = ( $rowCount * 2400 ) + 1200 - ( $minDepth * 400 );
                            } else {
                                $xMin = ( $rowCount * 2400 ) + ( $minDepth * 400 );
                                $xMax = ( $rowCount * 2400 ) + ( $maxDepth * 400 ) + 400;
                            }
                            $yMin = ( $rackCount * 600 ) + 10;
                            $yMax = ( $rackCount * 600 ) + 590;
                            $zMin = ( $minUnit * 50 );
                            $zMax = ( $maxUnit * 50 ) + 45;
                            // flip y axis
                            $temp = $yMin;
                            $yMin = $yMax * -1;
                            $yMax = $temp * -1;
                            // add to array
                            $objectArray[] = array('name' => $row3['name'], 'id' => $row3['id'], 'objtype_id' => $row3['objtype_id'], 'xMin' => $xMin, 'xMax' => $xMax, 'yMin' => $yMin, 'yMax' => $yMax, 'zMin' => $zMin, 'zMax' => $zMax );
                        }
                    }
                    $rackCount++;
                }
                $rowCount++;
                $rackCount=0;
            }
        }
        // php 5.4 onward
        //return json_encode($objectArray, 'JSON_PRETTY_PRINT');
        return json_encode($objectArray);
    }
}

$location_id=1;
$script_mode = TRUE;
include("/var/www/html/racktables/inc/init.php");
header('Content-Type: application/json');
printf(map_dc($location_id));
?>
