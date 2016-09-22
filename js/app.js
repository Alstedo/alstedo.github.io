// Define the `App` module
var App = angular.module('App', []);

App.config([
  '$interpolateProvider', function($interpolateProvider) {
    return $interpolateProvider.startSymbol('{(').endSymbol(')}');
  }
]);

// http://stackoverflow.com/questions/11873570/angularjs-for-loop-with-numbers-ranges
App.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);

    for (var i = 0; i < total; i++) {
      input.push(i);
    }

    return input;
  };
});

var topFourCompare = function(a, b) {
  var value = 0;

  value = b['stats']['topFours'] - a['stats']['topFours'];
  if (value != 0)
    return value;

  value = b['stats']['firstCount'] - a['stats']['firstCount'];
  if (value != 0)
    return value;

  value = b['stats']['secondCount'] - a['stats']['secondCount'];
  if (value != 0)
    return value;

  value = b['stats']['thirdCount'] - a['stats']['thirdCount'];
  if (value != 0)
    return value;

  value = b['stats']['fourthCount'] - a['stats']['fourthCount'];
  if (value != 0)
    return value;

  return value;
}

var keyCompare = function(key) {
  return function(a, b) { return b['stats'][key] - a['stats'][key]; };
}

var averageCompare = function(a, b) {
  return a['stats']['average'] - b['stats']['average'];
}

// Define the `ResultsController` controller on the `App` module
App.controller('ResultsController', function ResultsController($scope, $http) {
  $scope._sort = function(key, range=32) {
    var compare;
    if ( key === 'topFour' )
      compare = topFourCompare;
    else if ( key === 'average' )
      compare = averageCompare;
    else
      compare = keyCompare(key);

    var filteredTeams = $scope.teams;
    filteredTeams.sort(compare);
    filteredTeams = filteredTeams.slice(0, range);
    $scope.filteredTeams = filteredTeams;
  }

  $http.get('../data/results.json')
    .then(function(response) {
        var results = response.data;

        teams = results.teams;
        for ( var i = 0; i < teams.length; i++ )
        {
          var weeks = teams[i]['weeks'];

          var numWeeks = Object.keys(weeks).length;
          if ( numWeeks == 0 )
            continue;

          teams[i]['stats'] = {
            'average': 0,
            'topFours': 0,
            'firstCount': 0,
            'secondCount': 0,
            'thirdCount': 0,
            'fourthCount': 0,
            'numWeeks': numWeeks
          }

          var sum = 0;
          for ( key in weeks )
          {
            standing = weeks[key];

            sum += standing;
            if ( standing == 1 )
              teams[i]['stats']['firstCount'] += 1
            if ( standing == 2 )
              teams[i]['stats']['secondCount'] += 1
            if ( standing == 3 )
              teams[i]['stats']['thirdCount'] += 1
            if ( standing == 4 )
              teams[i]['stats']['fourthCount'] += 1
            if ( standing >= 1 && standing <= 4 )
              teams[i]['stats']['topFours'] += 1
          }

          var average = sum / numWeeks;
          teams[i]['stats']['average'] = average.toFixed(2);
        }

        $scope.numWeeks = results.numWeeks;
        $scope.numTeams = results.numTeams;
        $scope.teams = teams;
        $scope._sort('topFours')
    });



});
