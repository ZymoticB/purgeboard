'use strict';

purgeboard.factory('AllFactionsDaily', function($resource) {
	return $resource('/faction/kills/day/:day', {day: '@day'});
});

purgeboard.factory('AllFactionsTotal', function($resource) {
	return $resource('/faction/kills/total');
});
