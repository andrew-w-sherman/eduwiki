var prereqApp = angular.module('prereq', []);

prereqApp.controller('PrereqController', function($scope, $http){

    $scope.submit = function(){
        // sends back array of dicts with name and isGood
        $http.post('/studies/prereq/'+$rootScope.title, $rootScope.reqForm.reqs)
            .success(function(data){
                $rootScope.name = data.name;
                $rootScope.reqForm.reqs = data.reqs;
            });
    };


});

prereqApp.run(function($rootScope, $http){
    $http.get('/prereq/start')
        .success(function(data){
            $rootScope.reqForm = {};
            $rootScope.name = data.name;
            $rootScope.reqForm.reqs = data.reqs;
        });
});
