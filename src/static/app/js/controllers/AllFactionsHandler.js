'use strict';

Number.prototype.pad = function(size) {
	if(typeof(size) !== "number"){size = 2;}
	var s = String(this);
	while (s.length < size) s = "0" + s;
	return s;
}

purgeboard.controller('AllFactionsHandler', 
	function AllFactionsHandler($scope, AllFactionsDaily, AllFactionsTotal){
		$scope.total = AllFactionsTotal.query();
		var today = new Date();
		var year = today.getUTCFullYear();
		var month = today.getUTCMonth() + 1; //why the fuck would you return 0-11 ...
		var day = today.getUTCDate();
		var yesterday = year+month.pad(2)+day.pad(2);
		$scope.yesterday = AllFactionsDaily.query({day: yesterday});
	}
);
