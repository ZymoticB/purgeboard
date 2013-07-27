'use strict';

purgeboard.controller('CorpHandler',
	function CorpHandler($scope, CorpStats) {
		$scope.corp = "crossfire"
		$scope.stats = CorpStats.get()
	}
);
