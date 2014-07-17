var prereqApp = angular.module('prereq', []);

buildApp.controller('PrereqController', function($scope, $http){
    $scope.reqForm = {};

    $scope.submit = function(){
        $http.post('/studies/prereq/'+$rootScope.title, $scope.reqForm)
            .success(function(data){
                $rootScope.title = data.title;
                $rootScope.reqs = data.reqs;
            });
    };


});

prereqApp.run(function($rootScope, $http){
    $http.get('/studies/prereq/start')
        .success(function(data){
            $rootScope.title = data.title;
            $rootScope.reqs = data.reqs;
        });
});
