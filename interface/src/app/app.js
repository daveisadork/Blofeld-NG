angular.module( 'ngBlofeld', [
  'ngResource',
  'templates-app',
  'templates-common',
  'ngBlofeld.services',
  'ngBlofeld.home',
  'ngBlofeld.albums',
  'ngBlofeld.album',
  'ui.router'
])

.config( function myAppConfig ( $stateProvider, $urlRouterProvider ) {
  $urlRouterProvider.otherwise( '/albums' );
})

.run( function run () {
})

.controller( 'AppCtrl', function AppCtrl ( $scope, $location ) {
  $scope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams){
    if ( angular.isDefined( toState.data.pageTitle ) ) {
      $scope.pageTitle = toState.data.pageTitle + ' | Blofeld' ;
    }
  });
})

;

