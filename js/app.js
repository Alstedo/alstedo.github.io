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

// Define the `HistoryController` controller on the `App` module
App.controller('HistoryController', function ResultsController($scope, $http) {

  $scope.display = function(team) {
    console.log(team);
    team.previousRosterStr = team.previousRoster.join(', ');
    $scope.displayedTeam = team;
  }

  $scope.compare = function(a, b) {
    // return a['stats']['average'] - b['stats']['average'];
    var cmp, isSorted;

    cmp = b['stats']['first'] - a['stats']['first'];
    isSorted = (cmp !== 0);
    if ( isSorted )
      return cmp;

    cmp = b['stats']['second'] - a['stats']['second'];
    isSorted = (cmp !== 0);
    if ( isSorted )
      return cmp;

    cmp = b['stats']['third'] - a['stats']['third'];
    isSorted = (cmp !== 0);
    if ( isSorted )
      return cmp;

    return a['stats']['average'] - b['stats']['average'];
  }

  $http.get('../data/weights.json')
    .then(function(response) {
        $scope.weights = response.data;
    });

  $http.get('../data/tournaments.json')
    .then(function(response) {
        var tournaments = response.data;

        var teams = Object.keys(tournaments.teams).map(function (key) { return tournaments.teams[key]; });
        var count = 0;

        for ( var key in teams )
        {
          var team = teams[key];

          teams[key]['nameShort'] = teams[key]['name'].slice(0, 15);

          var weeks = teams[key]['weeks'];

          var numWeeks = Object.keys(weeks).length;
          if ( numWeeks === 0 )
            continue;

          teams[key]['stats'] = {
            'average': 0,
            'topThrees': 0,
            'first': 0,
            'second': 0,
            'third': 0,
            'numWeeks': numWeeks
          }

          var sum = 0;
          for ( var k in weeks )
          {
            standing = parseInt(weeks[k]);

            if ( standing === 1 )
              teams[key]['stats']['first'] += 1;
            if ( standing === 2 )
              teams[key]['stats']['second'] += 1;
            if ( standing === 3 )
              teams[key]['stats']['third'] += 1;

            sum += standing;
          }
          teams[key]['stats']['topThrees'] =
            teams[key]['stats']['first'] +
            teams[key]['stats']['second'] +
            teams[key]['stats']['third'];


          var average = sum / numWeeks;
          teams[key]['stats']['average'] = average.toFixed(2);

          count += 1;
        }

        teams.sort($scope.compare)

        $scope.numWeeks = tournaments.weeks.length;
        $scope.numTeams = count;
        $scope.teams = teams;
        $scope.display($scope.teams[0]);
        $scope.list(teams);
    });

});


// Define the `PostsController` controller on the `PostsApp` module
App.controller('PostsController', function PostsController($scope, $http, $window) {

  $http.get('../data/posts.json')
    .then(function(response) {
        $scope.posts = response.data.posts;

        $scope.posts.sort(function(a, b) {
          var aDate = new Date(a.date);
          var bDate = new Date(b.date);
          return aDate < bDate ? 1 : -1;
        });

        $scope.posts.map(function(value) {
          var date = new Date(value.date);

          var locale = 'en';
          var options = {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
          }
          value.prettyDate = date.toLocaleString(locale, options);

          options = {
            hour: 'numeric',
            timeZoneName: 'short'
          }
          value.prettyTime = date.toLocaleString(locale, options);
          return value;
        });

        var currentDate = new Date();
        $scope.posts.map(function(value) {
          var date = new Date(value.date);
          value.open = currentDate < date;
          value.openPretty = value.open ? "Yes" : "No";
          return value;
        });

        $scope.eu = $scope.posts.filter(function(value) { return value.category === "EU"; });
        $scope.na = $scope.posts.filter(function(value) { return value.category === "NA"; });

        var future;

        future = $scope.eu.filter(function(value) { return value.open; });
        $scope.euNext = future.length === 0 ? $scope.eu[0] : future[future.length-1];
        $scope.euRedirect = function() {
          console.log($scope.euNext.url)
          $window.location.href = $scope.euNext.url;
        }

        future = $scope.na.filter(function(value) { return value.open; });
        $scope.naNext = future.length === 0 ? $scope.na[0] : future[future.length-1];
        $scope.naRedirect = function() {
          console.log($scope.naNext.url)
          $window.location.href = $scope.naNext.url;
        }

        var element = document.getElementById("eu-redirect");
        if (element !== null) {
          angular.element().ready(function() {
            $scope.euRedirect();
          });
        }


        var element = document.getElementById("na-redirect");
        if (element !== null) {
          angular.element(element).ready(function() {
            $scope.naRedirect();
          });
        }
    });

});
