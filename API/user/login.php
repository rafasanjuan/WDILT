<?php
/**
 * Using PHP-JWT (https://github.com/firebase/php-jwt) library to encode and
 * decode Json Web Tokens.
 * 
 * Requieres composer for installing the dependence.
 */
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Origin, Content-Type, X-Auth-Token');

include '../objects/user.php';
include '../config/database.php';

// We add composer autoload.
require '../vendor/autoload.php';

// And we specify we are using PHP-JWT
use \Firebase\JWT\JWT;

// CHECK IF THE CREDENTIALS ARE RIGHT (username, password)
$database = new Database();
$conn = $database->getConnection();
 
$user = new User($conn);

$user->username = isset($_GET['username']) ? $_GET['username'] : http_response_code(400);
$user->password = isset($_GET['password']) ? $_GET['password'] : http_response_code(400);

if ($user->login()) 
{
  $key = "example_key";

  $payload = array(
    "iss" => "localhost",
    "sub" => $user->username
  );
  
  $jwt = JWT::encode($payload, $key);

  $response = array(
    "token" =>  $jwt
    
  );
    
  print_r(json_encode($response));
}
else 
{
  // If user not found.
  echo '{';
    echo '"message": "User not found."';
  echo '}';
  http_response_code(404);
}