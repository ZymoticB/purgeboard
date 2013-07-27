'use strict';

var purgeboard = angular.module('purgeboard', ['ngResource']);

purgeboard.config(function($routeProvider) {
	$routeProvider.
		when('/', {
			controller: 'IndexController',
			templateUrl: 'views/index.html'
		}).
		when('/crossfire', {
			controller: 'CorpHandler',
			templateUrl: 'views/corp.html'
		}).
		when('/corps/', {
			controller: 'AllCorpsHandler',
			templateUrl: 'views/allcorps.html'
		}).
		when('/chars/', {
			controller: 'AllCharsHandler',
			templateUrl: 'views/allchars.html'
		}).
		when('/factions/', {
			controller: 'AllFactionsHandler',
			templateUrl: 'views/allfactions.html'
		}).
		otherwise({ redirectTo: '/' });
});
