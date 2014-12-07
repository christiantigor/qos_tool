'use strict';

angular.module('qostoolApp', [
  'ngCookies',
  'ngResource',
  'ngSanitize',
  'ngRoute',
  'd3',
  'c3',
  'ui.bootstrap',
  'leaflet-directive',
  'ngTable',
  'firebase'
])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .when('/login',{
        templateUrl: 'views/login.html',
        controller: 'MainCtrl'
      })
      .when('/analytics',{
        templateUrl: 'views/analytics.html',
        controller: 'AnalyticsCtrl'		
      })
      .otherwise({
        redirectTo: '/'
      });
  });
  
//setup dependency injection
angular.module('d3',[]);
angular.module('c3',['d3']);
