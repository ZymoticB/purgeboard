'use strict';

Number.prototype.pad = function(size) {
	if(typeof(size) !== "number"){size = 2;}
	var s = String(this);
	while (s.length < size) s = "0" + s;
	return s;
};

purgeboard.controller('AllCharsHandler', 
	function AllCharsHandler($scope, AllCharsDaily, AllCharsTotal) {
		$scope.total = AllCharsTotal.query();
		var today = new Date();
		var year = today.getUTCFullYear();
		var month = today.getUTCMonth() + 1; //why the fuck would you return 0-11 ...
		var day = today.getUTCDate() - 1;
		$scope.yesterday = year+month.pad(2)+day.pad(2);
		$scope.current_day_stats = AllCharsDaily.query({day: $scope.yesterday});
		$scope.update_stats = function() {
			$scope.current_day_stats = AllCharsDaily.query({day: $scope.yesterday});
		};
	}
);
