'use strict';

purgeboard.factory('AllCorpsDaily', function($resource) {
	return $resource('/corp/kills/day/:day', {day: '@day'});
})

purgeboard.factory('AllCorpsTotal', function($resource) {
	return $resource('/corp/kills/total');
});
