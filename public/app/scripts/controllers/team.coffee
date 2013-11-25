'use strict'

angular.module('apiExplorerApp')
  .controller 'TeamController', ($scope) ->
    $scope.teamGroup = [
      { 
        name    : 'Carlos Henrique'
        job     : 'Developer at DClick Web & Mobile Solutions (trainee)'
        github  : 'https://github.com/carloshpds' 
        linkedin: 'http://www.linkedin.com/profile/view?id=143700778&trk=nav_responsive_tab_profile_pic'
        img     : 'http://en.gravatar.com/userimage/48673773/404bc9a97d6861c0e70b17e7624ebc83.jpg?size=200'
      }
      {
        name    : 'Lucas Gabriel'
        job     : 'Developer at DClick Web & Mobile Solutions (trainee)'
        github  : 'https://github.com/lucasgmartins'
        linkedin: 'http://www.linkedin.com/profile/view?id=182681877&locale=pt_BR&trk=tyah&trkInfo=tas%3Alucas%2Cidx%3A1-1-1'
        img     : 'https://2.gravatar.com/avatar/48169a7ddea49b5e5746efbe684a83d2?d=https%3A%2F%2Fidenticons.github.com%2Fc7f1cb4cc81d10811df17fba9bacc6a4.png&r=x&s=400'
      }
      # {
      #   name    : 'Alessandro Camillo'
      #   job     : ''
      #   github  : 'https://github.com/lucasgmartins'
      #   linkedin: '#'
      #   img     : 'https://fbcdn-sphotos-a-a.akamaihd.net/hphotos-ak-prn1/60788_389365344471749_924557228_n.jpg'
      # }
      # {
      #   name    : 'Daniel Yokoyama'
      #   job     : 'Software Architect at RADI - Restaurant Application Development International LLC'
      #   github  : 'https://github.com/moreirayokoyama'
      #   linkedin: 'http://www.linkedin.com/profile/view?id=75965086&locale=pt_BR&trk=tyah&trkInfo=tas%3ADani%2Cidx%3A1-3-3'
      #   img     : 'http://m.c.lnkd.licdn.com/mpr/mpr/shrink_200_200/p/4/000/14b/022/354d837.jpg'
      # }
    ]
