var learnApp = angular.module('learn', []);

learnApp.controller('LearnController', function($scope, $http){
    $scope.main_topic = "";
    $scope.current_name = "";
    $scope.definition = {};
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
                    $scope.main_topic = data.current_name;
                    $scope.testTopics = data.prereqs;
                    getQuiz();
                }
            });
    };

    $scope.submitQuiz = function(){
        if(quizData.correct != "correct"){
            $scope.testResults.push({name: $scope.current_name, correct: true});
        }
        getQuiz();
    };

    $scope.getQuiz = function(){
        if(testTopics.length !== 0){
            var term = $scope.testTopics.shift();
            $http.get('/learn/'+encodeURI(term)+'/quiz')
                .success(function(data){
                    if(!data.success){
                        $scope.errors = data.errors;
                    }
                    else{
                        $scope.current_name = data.name;
                        $scope.definition.snippet = data.definition;
                        $scope.distractors = data.distractors;
                        for(var i = 0; i < distractors.length; i++){
                            distractors[i].correct = "incorrect";
                            distractors[i].rand = Math.random();
                        }
                        $scope.definition.correct = "correct";
                        $scope.definition.rand = Math.random();
                        $scope.answers = $scope.distractors;
                        $scope.answers[$scope.answers.length] = $scope.definition;
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
        for(var i = 0; i < testResults.length; i++){
            if(testResults[i].correct){
                $scope.infoRequest(testResults[i].name);
            }
        }
        $http.get('/learn/'+encodeURI(current_name)+'/info')
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
