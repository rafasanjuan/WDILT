<?php
/**
 * Handles the database connection.
 */
class Database{
 
  // Database credentials
  private $credentials;
  private $host = "localhost";
  private $db_name = "api_db";
  private $username = "root";
  private $password = "";
  public $conn;
 
  /**
   * If not instanciated before, it connects to the database and stores then 
   * connection, if previusly connected, it just sends the stored database conection.
   * @return PDO Connection to the database.
   */
  public function getConnection(){
 
    $this->conn = null;
    $credentials = parse_ini_file("credentials.ini");

    try {
      $this->conn = new PDO("mysql:host=" . $this->host . 
        ";dbname=" . $this->db_name, $this->username, $this->password);
      $this->conn->exec("set names utf8");
    } catch( PDOException $exception ) {
              echo "Connection error: " . $exception->getMessage();
    }
  
    return $this->conn;
  }
}
