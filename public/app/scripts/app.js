'use strict';

angular.module('apiExplorerApp', ['ngResource'])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/services', {
        templateUrl: 'views/services.html',
        controller : 'ServicesController'
      }).when('/team', {
        templateUrl: 'views/team.html',
        controller : 'TeamController'
      })
      .otherwise({
        redirectTo: '/services'
      });
  });
