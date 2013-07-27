'ue strict';

purgeboard.factory('CorpStats', function($resource) {
	return $resource('/crossfire/');
});
