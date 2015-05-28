/**
 * Each section of the site has its own module. It probably also has
 * submodules, though this boilerplate is too simple to demonstrate it. Within
 * `src/app/home`, however, could exist several additional folders representing
 * additional modules that would then be listed as dependencies of this one.
 * For example, a `note` section could have the submodules `note.create`,
 * `note.delete`, `note.edit`, etc.
 *
 * Regardless, so long as dependencies are managed correctly, the build process
 * will automatically take take of the rest.
 *
 * The dependencies block here is also where component dependencies should be
 * specified, as shown below.
 */
angular.module( 'ngBlofeld.home', [
  'ui.router',
  'ngBlofeld.services',
  'ngResource'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config( $stateProvider ) {
  $stateProvider.state( 'home', {
    url: '/home',
    views: {
      "main": {
        controller: 'HomeCtrl',
        templateUrl: 'home/home.tpl.html'
      }
    },
    data:{ pageTitle: 'Home' }
  });
})

/**
 * And of course we define a controller for our route.
 */
.controller( 'HomeCtrl', function HomeController( $scope, Artists, Albums, Songs ) {
    $scope.selected = {
        artist: 'All Artists',
        album: 'All Albums'
    };

    $scope.artists = Artists.query();
    $scope.albums = Albums.query($scope.selected);
    $scope.songs = Songs.query($scope.selected);

    $scope.selectArtist = function (artist) {
        $scope.selected.artist = artist;
        Albums.query($scope.selected).$promise.then(function (albums) {
            if (albums.indexOf($scope.selected.album) === -1) {
                $scope.selected.album = 'All Albums';
            }
            $scope.albums = albums;
            $scope.songs = Songs.query($scope.selected);
        });
    };

    $scope.selectAlbum = function (album) {
        $scope.selected.album = album;
        $scope.songs = Songs.query($scope.selected);
    };
})

;

