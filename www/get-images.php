
<?php

$db = new PDO('sqlite:database/pi_database.db');

$result = $db->query('SELECT * FROM images');

$data = array();

$result->setFetchMode(PDO::FETCH_ASSOC);

while ($row = $result->fetch()) {

  extract($row);

  $data[] = array(
                  "id" => $id,
                  "dateTime" => $dateTime,
                  "path_to_image" => $path_to_image,
                  "latitude" => $latitude,
                  "longitude" => $longitude,
                  "altitude" => $altitude
                  );
}

$data = json_encode($data);

echo($data);

?>

