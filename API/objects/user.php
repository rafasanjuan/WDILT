<?php
class User {
 
    // database connection and table name
    private $conn;
    private $table_name = "users";
 
    // object properties
    public $username;
    public $password;
 
    // constructor with $db as database connection
    public function __construct($db){
        $this->conn = $db;
    }

  function login() {
    $query = "SELECT * FROM " . $this->table_name . " WHERE username='"
            . $this->username . "'";

    $stmt = $this->conn->prepare($query);

    $stmt->execute();
    $num = $stmt->rowCount();

    if ( $num > 0 ) 
    {
      $userdata = $stmt->fetch(PDO::FETCH_LAZY);
      
      return password_verify($this->password, $userdata["password"]);
    }
    return false;
  }

  function read() {
    
    // select all query
    $query = "SELECT username FROM " . $this->table_name;
    
    // prepare query statement
    $stmt = $this->conn->prepare($query);
    
    // execute query
    $stmt->execute();

    return $stmt;
  }
  
  function readUsername() {
    
    // select all query
    $query = "SELECT username  FROM " . $this->table_name . " WHERE username='"
      . $this->username . "'";
    
    // prepare query statement
    $stmt = $this->conn->prepare($query);
    
    // execute query
    $stmt->execute();
    $num = $stmt->rowCount();
    
    // If an user got found return true;
    if ( $num > 0 ) 
    {
      return true;
    }
    return false;
  }

  // Read events from a date.
  function create() {
    $query = "INSERT INTO
        " . $this->table_name . " (`username`, `password`)
      VALUES (
        '" . $this->username . "', 
        '" . $this->password ."'
        )";

    $stmt = $this->conn->prepare($query);

    if ( $stmt->execute() ) {
      return true;
    }
    return false;
  }

  // Deletes an user from the database.
  function delete() {
    $query = "DELETE FROM " . $this->table_name . " WHERE username = ?";

    $stmt = $this->conn->prepare($query);

    $this->username = htmlspecialchars(strip_tags($this->username));

    $stmt->bindParam(1, $this->username);

    if($stmt->execute()){
        return true;
    }

    return false;
  }
}
