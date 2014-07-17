var learnApp = angular.module('learn', []);

learnApp.controller('LearnController', function($scope, $http){
    $scope.main_topic = "";
    $scope.current_name = "";
    $scope.description = {};
    $scope.distractors = [];
    $scope.answers = [];
    $scope.testTopics = [];
    $scope.testResults = [];
    $scope.writeups = [];
    $scope.main_writeup = {};
    $scope.showIntro = true;
    $scope.showInfo = false;
    $scope.showQuiz = false;
    $scope.quizData = {};
    $scope.searchTerm = {};

    //might want to add live wikipedia suggestion if possible

    $scope.search = function(){
        $http.get('/learn/'+encodeURI($scope.searchTerm.term)+'/quiz')
            .success(function(data){
                if(!data.success){
                    $scope.errors = data.errors;
                    //need disambiguation handling
                }
                else{
                    $scope.main_topic = data.name;
                    $scope.testTopics = data.prereqs;
                    $scope.getQuiz();
                }
            });
    };

    $scope.submitQuiz = function(){
        if($scope.quizData.correct != "correct"){
            $scope.testResults.push({name: $scope.current_name, correct: true});
        }
        $scope.getQuiz();
    };

    $scope.getQuiz = function(){
        if($scope.testTopics.length !== 0){
            var term = $scope.testTopics.shift();
            $http.get('/learn/'+encodeURI(term)+'/quiz')
                .success(function(data){
                    if(!data.success){
                        $scope.errors = data.errors;
                    }
                    else{
                        $scope.current_name = data.name;
                        $scope.description.snippet = data.description;
                        $scope.distractors = data.distractors;
                        for(var i = 0; i < $scope.distractors.length; i++){
                            $scope.distractors[i].correct = $scope.distractors[i].pagetitle;
                            $scope.distractors[i].rand = Math.floor(Math.random() * 1000);
                        }
                        $scope.description.correct = "correct";
                        $scope.description.rand = Math.floor(Math.random() * 1000);
                        $scope.answers = $scope.distractors;
                        $scope.answers[$scope.answers.length] = $scope.description;
                        $scope.showIntro = false;
                        $scope.showInfo = false;
                        $scope.showQuiz = true;
                    }
                });
        }
        else{
            $scope.getInfo();
        }
    };

    $scope.getInfo = function(){
        for(var i = 0; i < $scope.testResults.length; i++){
            if($scope.testResults[i].correct){
                $scope.infoRequest($scope.testResults[i].name);
            }
        }
        $http.get('/learn/'+encodeURI($scope.current_name)+'/info')
            .success(function(data){
                if(!data.success){
                    $scope.errors = data.errors;
                }
                else{
                    $scope.main_writeup = data.writeup;
                }
            });
        $scope.showQuiz = false;
        $scope.showInfo = true;
    };

    $scope.infoRequest = function(topic_name){
        $http.get('/learn/'+encodeURI(topic_name)+'/info')
            .success(function(data){
                if(!data.success){
                    $scope.errors = data.errors;
                }
                else{
                    $scope.writeups.push(data.writeup);
                }
            });
    };
});
