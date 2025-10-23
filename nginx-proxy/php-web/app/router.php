<?php
$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($uri === '/healthz') {
    include 'healthz.php';
    return true;
    exit;
}

if ($uri === '/' || $uri === '/index.php') {
    include 'index.php';
    return true;
    exit;
}

if (file_exists(__DIR__ . $uri)) {
    return false;
}

http_response_code(404);
header('Content-Type: application/json');
echo json_encode(['error' => 'Not Found']);
return true;