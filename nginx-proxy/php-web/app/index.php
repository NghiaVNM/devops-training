<?php
header('Content-Type: application/json');

echo json_encode([
  'message' => 'Hello World from PHP!',
  'version' => '1.0.0'
]);