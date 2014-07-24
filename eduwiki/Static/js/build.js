var buildApp = angular.module('build', []);

buildApp.controller('BuildController', function($scope, $http){
    $scope.tree = {};
    $scope.topic = null;
    $scope.user = null;
    $scope.review = null;
    $scope.showReqs = false;
    $scope.showReg = true;
    $scope.showReview = false;
    $scope.reviewDisabled = "";
    $scope.regData = {};
    $scope.regTopic = {};
    $scope.revData = {};

    // debug review
    //$scope.showReqs = false;
    //$scope.showReg = false;
    //$scope.showReview = true;

    $scope.regSubmit = function() {
        //submit the post request for the registration, get back user info
        $http.post('/build/register', $scope.regData) //needs an extra bool for if disambig prone
            .success(function(data){
                if(!data.success){
                    //bind AJAX errors to scope and process them
                    $scope.errors = data.errors;
                    //process errors
                }
                else{
                    $scope.user = data.user; //or something, depending on how user stuff is done
                    //if it works, get the review data for the root topic
                    $http.get('/build/'+encodeURI($scope.regTopic.topic)+'/review',
                    {params: {user: encodeURI($scope.user)}})  //probably gonna need to use tokens instead
                    .success(function(data){
                        if(!data.success){
                            if(data.errors.disambig){
                                //disambiguation logic for starting topic
                            }
                            else{
                                //error handling
                                $scope.errors = data.errors;
                                //standard error display
                                //need error for done already
                            }
                        }
                        else{
                            //on success, bind data to scope and show review pane
                            $scope.tree = {name: data.name, description: data.description, distractors: data.distractors, active: true};
                            $scope.topic = $scope.tree;
                            $scope.showReg = false;
                            $scope.showReview = true;
                        }
                    });
                }
            });
    };

    $scope.revSubmit = function(){
        //post request for the review data
        $scope.revData.distractors = [];
        for(var i = 0; i < $scope.topic.distractors.length; i++){
            $scope.revData.distractors.push({name: $scope.topic.distractors[i].pagetitle, isGood: $scope.topic.distractors[i].isGood});
        }
        $http.post('/build/'+encodeURI($scope.topic.name)+'/review', {user: $scope.user, review: $scope.revData})
            .success(function(data){
                if(!data.success){
                    $scope.errors = data.errors;
                    //error display
                    //need an error for done already (if (data.errors.done))
                }
                else{
                    //mark as done
                    $scope.topic.done = true;
                    //once submitted, get prerequisites
                    $http({
                        method: 'GET',
                        url: '/build/'+encodeURI($scope.topic.name)+'/prerequisites',
                        //maybe submit user in the future?
                    })
                    .success(function(data){
                        if(!data.success){
                            $scope.errors = data.errors;
                            //error display
                        }
                        else{
                            //show the prerequisite buttons and disable the form
                            for(var i=0; i < data.reqs.length; i++){
                                data.reqs[i].parent = $scope.topic;
                            }
                            $scope.topic.children = data.reqs;
                            $scope.reviewDisabled = "review-dark";
                            $scope.showReqs = true;
                        }
                    });
                }
            });
    };

    $scope.showReview = function(node) {
        $http({
            method: 'GET',
            url: '/build/'+encodeURI(node.name)+'/review',
            data: $scope.revData,
        })
        .success(function(data){
            if(!data.success){
                $scope.errors = data.errors;
                //error display
            }
            else{
                //on success, switch topic to that node and display review
                $scope.topic = node;
                $scope.showReqs = false;
                $scope.reviewDisabled = false;
                $scope.showReview = true;
            }
        });
    };
});
