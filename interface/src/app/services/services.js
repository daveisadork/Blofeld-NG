angular.module( 'ngBlofeld.services', [
        'ngResource'
])

.factory('Artists', function ($resource) {
    return $resource('http://localhost:8000/api/artists');
})

.factory('Albums', function ($resource) {
    return $resource('http://localhost:8000/api/artist/:artist\/albums');
})

.factory('Album', function ($resource) {
    return $resource('http://localhost:8000/api/album/:album');
})

.factory('Songs', function ($resource) {
    return $resource('http://localhost:8000/api/artist/:artist\/album/:album\/songs');
})

;
