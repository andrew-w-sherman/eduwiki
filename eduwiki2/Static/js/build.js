var buildApp = angular.module('build', []);

buildApp.controller('BuildController', function($scope, $http){
    $scope.tree = null;
    $scope.topic = null;
    $scope.user = null;
    $scope.reqs = null;
    $scope.review = null;
    $scope.showReqs = false;
    $scope.showTree = false;
    $scope.showReg = true;
    $scope.showReview = false;
    $scope.reviewDisabled = false;
    $scope.regData = {};
    $scope.revData = {};

    $scope.onRegister = function() {

    };

    $scope.flatTree = function() {
        return flattenTree($scope.tree, 0);
    };

    $scope.regSubmit = function() {
        //submit the post request for the registration, get back user info
        $http({
            method  :   'POST',
            url     :   '/register',
            data    :   $.param($scope.regData),
        })
            .success(function(data){
                if(!data.success){
                    //bind AJAX errors to scope and process them
                    $scope.errors = data.errors;
                    //process errors
                }
                else{
                    $scope.user = data.user; //or something, depending on how user stuff is done
                    //if it works, get the review data for the root topic
                    $http({
                        method  :   'GET',
                        url     :   '/'+$scope.regData.topic+'/review',
                        data    :   $.param($scope.user),
                    })
                    .success(function(data){
                        if(!data.success){
                            if(data.errors.disambig){
                                //disambiguation logic for starting topic
                            }
                            else{
                                //error handling
                                $scope.errors = data.errors;
                                //standard error display
                            }
                        }
                        else{
                            //on success, bind data to scope and show review pane
                            $scope.tree = {name: data.name};
                            $scope.topic = $scope.tree;
                            $scope.review = data.review;
                            $scope.showReg = false;
                            $scope.showTree = true;
                            $scope.showReview = true;
                        }
                    });
                }
            });
    };

    $scope.revSubmit = function(){
        //post request for the review data
        $http({
            method: 'POST',
            url: '/'+$scope.topic.name+'/review',
            data: $.param($scope.revData),
        })
        .success(function(data){
            if(!data.success){
                $scope.errors = data.errors;
                //error display
            }
            else{
                //once submitted, get prerequisites
                $http({
                    method: 'GET',
                    url: '/'+$scope.topic.name+'/prerequisites',
                    //maybe submit user in the future?
                })
                .success(function(data){
                    if(!data.success){
                        $scope.errors = data.errors;
                        //error display
                    }
                    else{
                        //show the prerequisite buttons and disable the form
                        $scope.reqs = data.reqs;
                        $scope.topic.children = data.reqs;
                        $scope.showReview = false;
                        $scope.reviewDisabled = true;
                        $scope.showReqs = true;
                    }
                });
            }
        });
    };

    $scope.reqSubmit = function(choice){ //see below about the choice thing but it's a decent placeholder
        $http({
            method: 'GET',
            url: '/'+$scope.reqs.choice+'/review', //this choice thing is weird idk
            data: $.param($scope.revData),
        })
        .success(function(data){
            if(!data.success){
                $scope.errors = data.errors;
                //error display
            }
            else{
                //on success, bind data to scope and make review pane active
                $scope.topic = $scope.topic.choice; //what's gonna happen if choice is from tree?
                $scope.review = data.review;
                $scope.showReg = false;
                $scope.showTree = true;
                $scope.showReview = true;
            }
        });
    };

    $scope.getNum = function(num) {
        coll = [];
        for(var i = 0; i < num; i++){
            coll.push(null);
        }
    };

});

//buildApp.directive('');

function flattenTree(tree, startlevel) {
    var list = [];
    list.push({level: startlevel, name: tree.topic, active: tree.active});
    if(children in list){
        for(var i = 0; i < list.children.length; i++){
            flattenTree(list.children[i], startlevel + 1);
        }
    }
}
