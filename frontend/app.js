var myApp = angular.module("myApp", ["ngRoute", "ngResource", "myApp.services"]);

var services = angular.module("myApp.services", ["ngResource"])
services
.factory('Search', function($resource) {
    return $resource('http://localhost:5000/search', {q: '@q'}, {
        query: { method: 'GET', isArray: false}
    });
})

.factory('Explorer', function($resource) {
    return $resource('http://localhost:5000/explore', {q: '@q'}, {
        query: { method: 'GET', isArray: false}
    });
});

myApp.config(function($routeProvider) {
    $routeProvider
    .when('/', {
        templateUrl: 'pages/main.html',
        controller: 'mainController'
    })
    .when('/visualize', {
        templateUrl: 'pages/visual.html',
        controller: 'visualController'
    })
});

myApp.filter('unsafe', function($sce) {
    return function(val) {
        return $sce.trustAsHtml(val);
    };
});

myApp.controller(
    'mainController',
    function ($scope, Search) {
        $scope.search = function() {
            q = $scope.searchString;
            if (q.length > 1) {
                $scope.response = Search.query({q: q});
            }
        };
    }
);

myApp.controller(
    'visualController',
    function ($scope, Explorer) {
        $scope.explore = function() {
            q = $scope.searchString;
            if (q.length > 1) {
                $scope.response = Explorer.query({q: q});
            }
        };
    }
);

