
<?php

$db = new PDO('sqlite:database/pi_database.db');

$result = $db->query('SELECT * FROM images');

$data = array();

$result->setFetchMode(PDO::FETCH_ASSOC);

while ($row = $result->fetch()) {

extract($row);

$data[] = array($id, $dateTime, $path_to_image, $latitude, $longitude, $altitude);
}

$data = json_encode($data);

echo($data);

?>

