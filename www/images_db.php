<?php
$db = new SQLite3('./database/pi_database.db');
$results = $db->query('SELECT * FROM images');
while ($row = $results->fetchArray()) {
var_dump($row);
}
?>