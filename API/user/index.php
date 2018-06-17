<?php
/**
 * Handle requests for signing up and logging.
 */
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Max-Age: 3600");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

include_once '../config/database.php';
include_once '../objects/user.php';

$requestMethod = $_SERVER['REQUEST_METHOD'];

if ($requestMethod === 'GET') 
{
  $database = new Database();
  $db = $database->getConnection();
  
  $user = new user($db);

  // If received username ("api/user/<username>") then checks that user.
  if (isset($_GET['username']))
  {
    $user->username = $_GET['username'];

    if ( $user->readUsername() )
    {
      echo '{';
        echo '"message": "User exists."';
      echo '}';
    }
    else
    {
      http_response_code(404);
      echo '{';
        echo '"message": "User not registered."';
      echo '}';
    }
  }
}
else if ($requestMethod === 'POST') 
{
  $database = new Database();
  $conn = $database->getConnection();

  $user = new User($conn);

  $data = json_decode(file_get_contents("php://input"));

  $user->username = isset($_GET['username']) ? $_GET['username'] : http_response_code(400);
  $user->password = isset($_GET['password']) ? password_hash($_GET['password'], PASSWORD_DEFAULT) : http_response_code(400);

  if ( $user->create() ) {
    echo '{';
      echo '"message": "User succesfully created."';
    echo '}';
  } else {
  echo '{';
    echo '"message": "Unable to signup user."';
  echo '}';
  }
}
