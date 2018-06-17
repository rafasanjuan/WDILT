'use strict';

var wdiltApp = angular.module('wdiltApp', ['ngMaterial', 'ngMessages', 'ngCookies']);


// Theme provider angular material configuration.
wdiltApp.config(['$mdThemingProvider', function($mdThemingProvider) {
  
  $mdThemingProvider.theme('input')
    .primaryPalette('blue')
    .accentPalette('pink')
    .dark();
  }
]);

wdiltApp.config(['$mdThemingProvider', function($mdThemingProvider) {
  
  $mdThemingProvider.theme('default')
    .primaryPalette('blue')
    .accentPalette('teal');
  }
]);


// App controller.
wdiltApp.controller('WdiltController', function CalendarController($scope, $cookies, $http, $mdToast, $mdDialog) {

  /****************************************************************************/
  // Local variables.
  /****************************************************************************/

  // Chips
  $scope.tags = [
    "English",
    "Business"
  ]

  $scope.selectedItem = null;
  $scope.searchText = null;

  /****************************************************************************/
  // API calls.
  /****************************************************************************/
  
  $scope.logIn = function (username, password, signup) {
    $http({
      method: 'GET',
      url: 'http://localhost/WDILT/api/user/login.php?username=' + username + '&password=' + password
    }).then(function successCallback(response) {
      $scope.atoken = response.data.token;
      $cookies.put('atoken', response.data.token);
      $cookies.put('username', username);
      if (!signup) {
        $scope.showToast("Login success");
      }
    }, function errorCallback(response) {
      $scope.showToast("Login failure");
    });
  };

  $scope.signUp = function (username, password) {
    $http({
      method: 'POST',
      data: { 
        'username' : username, 
        'password' : password,
      },
      url: 'http://localhost/WDILT/api/user/?username=' + username + '&password=' + password
    }).then(function successCallback(response) {
      $scope.atoken = response.data.token;
      $cookies.put('atoken', response.data.token);
      $cookies.put('username', username);
      $scope.showToast("SignUp success");
      $scope.logIn(username,password,true);
    }, function errorCallback(response) {
      $scope.showToast("SignUp failure");
    });
  };

  /****************************************************************************/
  // Initialization.
  /****************************************************************************/
  

  /****************************************************************************/
  // Click events.
  /****************************************************************************/

  $scope.signOutClicked = function() {
    $cookies.remove("atoken");
    $cookies.remove("username");
  }

  /****************************************************************************/
  // Other functions.
  /****************************************************************************/

  $scope.requireLogin = function() {
    var token = $cookies.get('atoken');

    // If the authentification token is not stored in a cookie, we ask for auth.
    if (!token)
    {
      return true;
    }
    
    $scope.atoken = token; 
    //alert("Cookie value " + $scope.atoken);
    return false;
  }

  $scope.getUsername = function() {
    return $cookies.get('username');
  }
  
  $scope.showToast = function(message) {
    $mdToast.show(
      $mdToast.simple()
        .textContent(message)
        .hideDelay(3000)
        .position("top right")
    );
  };
  
  /****************************************************************************/
  // Other controllers
  /****************************************************************************/
  
  // methods for dialog box
  function DialogController($scope, $mdDialog) {
    $scope.cancelDialog = function() {
      $mdDialog.cancel();
    };
  }

  $scope.selectedTags = [];

  var originatorEv;
  $scope.openMenu = function($mdMenu, ev) {
    originatorEv = ev;
    $mdMenu.open(ev);
  };
});