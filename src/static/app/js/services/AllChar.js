'use strict';

purgeboard.factory('AllCharsDaily', function($resource) {
	return $resource('/char/kills/day/:day', {day: '@day'});
});

purgeboard.factory('AllCharsTotal', function($resource) {
	return $resource('/char/kills/total');
});
