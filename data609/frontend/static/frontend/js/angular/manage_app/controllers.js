angular.module('manageApp.controllers', []).controller(
        'ManageCtrl', ['$scope', '$http', 'manageManager', function($scope, $http, manageManager) {
    $scope.ready = false;
    $scope.show_add_node_form = false;
    $scope.user_profile = {
        "nodes": {}
    };
    $scope.get_profile = function(){
        manageManager.get('/api/profiles/?format=json', function(data) {
            $scope.user_profile.nodes.nodes_num = data[0].max_nodes;
            $scope.user_profile.nodes.current_nodes_num = data[0].num_of_nodes;
            $scope.user_profile.adding_nodes_is_available =
                ($scope.user_profile.nodes.nodes_num-$scope.user_profile.nodes.current_nodes_num)>0;
        });
    }
    $scope.node_to_add = {
        name: "",
        username: "",
        password: ""
    };
    $scope.add_node = function(){
        var node_data = {};
        $http.post("/api/nodes/", data=node_data).success(function(){
            $scope.refresh_nodes();
        })
    };
    $scope.refresh_nodes = function(){
        manageManager.get('/api/nodes/?format=json', function(data) {
            $scope.nodes = data;
        });
    }
    $scope.refresh_nodes();
    $scope.get_profile();

}]);