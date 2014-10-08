// Declare app level module which depends on filters, and services
'use strict';
var manageModule = angular.module('manageApp', ['manageApp.directives', 'manageApp.controllers', 'manageApp.services']);
manageModule.config(['$interpolateProvider', '$httpProvider', function($interpolateProvider, $httpProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'; 
}]);
