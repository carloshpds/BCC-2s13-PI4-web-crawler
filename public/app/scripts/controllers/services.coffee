'use strict'

angular.module('apiExplorerApp')

  # ====================================================
  # Controller
  # ====================================================
  .controller 'ServicesController',  ($scope, FactoryRequest) =>

    # ====================================================
    # Attributes
    # ==================================================== 
    $scope.explorerLinks        = []
    $scope.explorerImages       = []
    $scope.explorerTextFiles    = []
    $scope.explorerDocuments    = []
    $scope.explorerVideos       = []
    $scope.explorerSongs        = []
    $scope.searchResultsLength  = 0

    $scope.errorMessage  = 'Some error has appeared'
    $scope.illustration  = true

    # ====================================================
    # Mock
    # ====================================================
    $scope.createMock = (maxValue) =>
      i = 0
      googleObject  =  text : 'google'  , href : 'http://www.google.com'
      gizmodoObject =  text : 'gizmodo' , href : 'http://gizmodo.uol.com.br'
      while i < maxValue
        if i % 2 is 0
          $scope.explorerLinks     .push googleObject
          $scope.explorerImages    .push googleObject
          $scope.explorerTextFiles .push googleObject
          $scope.explorerDocuments .push googleObject
          $scope.explorerVideos    .push googleObject
          $scope.explorerSongs     .push googleObject
        else
          $scope.explorerLinks     .push gizmodoObject
          $scope.explorerImages    .push gizmodoObject
          $scope.explorerTextFiles .push gizmodoObject
          $scope.explorerDocuments .push gizmodoObject
          $scope.explorerVideos    .push gizmodoObject
          $scope.explorerSongs     .push gizmodoObject
        i++




    # ====================================================
    # Methods
    # ==================================================== 
    
    ## General
    #=====================================
    $scope.initialize = =>
      # $scope.createMock 20
      do $scope.cacheDOMElements
      do $('.alert').alert

    $scope.cacheDOMElements = =>
      $scope.DOMELements =
        $errorAlert     : $('.alert.alert-danger')               .hide()
        $formUrl        : $('#form-url')                         
        $urlInput       : $('#url-input')
        $loading        : $('.progress.progress-striped.active') .hide()
        $tabsAndFilter  : $('#tabs-and-filter')                  .hide()
        $core           : $('#api-core')                         .hide()                       

    ## Server Sent Events
    #=====================================
    $scope.openServerEvents = =>
      if !!window.EventSource 
        $scope.timeSrc = new EventSource 'yieldResource'
        $scope.timeSrc.addEventListener 'time', (event) =>
          if event.data isnt "None"

            $scope.addItems(JSON.parse(event.data))
            $scope.searchResultsLength = $scope.changeSearchResultsLength()
            $scope.$apply()

            $scope.DOMELements.$tabsAndFilter.slideDown('slow')
            $scope.DOMELements.$core.fadeIn('slow')
          else
            do $scope.closeServerSentEvents
      else
        console.log 'something wrong happened'

    $scope.closeServerSentEvents = =>
      if $scope.timeSrc
        do $scope.timeSrc.close

    ## Logical Methods
    #=====================================
    $scope.addItems = (json) =>

      # Urls
      for url in json.urls
        $scope.explorerLinks.push url

      # Images
      for image in json.images
        $scope.explorerImages.push image

      # Videos
      for video in json.videos
        $scope.explorerVideos.push video

      # Documents
      for doc in json.documents
        $scope.explorerDocuments.push doc


        
    
    $scope.loadUrl = ()->
      if not _.isEmpty( $scope.DOMELements.$urlInput.val()) 
        $scope.illustration = false
        $scope.DOMELements.$formUrl.slideUp 'fast', =>
          $scope.DOMELements.$loading.slideDown 'slow', =>
          
            if $scope.url.substring(0,7) is "http://" 
              $scope.url = _.toArray($scope.url)
              $scope.url.splice(0,7)
              aux = $scope.url
              $scope.url = []
              for char in aux
                $scope.url += char

            do $scope.openServerEvents
            FactoryRequest.get($scope.url)
            .success( (data, status, headers, config) ->   
              $scope.DOMELements.$loading.slideUp 'slow', =>
                console.log ' ================ O server retornou 200 ==================='
            )
            .error(
              (data, status, headers, config)->
                do $scope.closeServerSentEvents
                $scope.DOMELements.$formUrl.slideUp 'slow', =>
                  $scope.errorMessage = 'Status code: ' + status
                  $scope.DOMELements.$errorAlert.fadeIn 'slow'
                  $scope.DOMELements.$loading.slideUp   'slow'
            )


    ## Aux Methods
    #=====================================
    $scope.changeSearchResultsLength = =>
      $scope.explorerLinks.length +  $scope.explorerImages.length + $scope.explorerTextFiles.length + $scope.explorerDocuments.length + $scope.explorerVideos.length + $scope.explorerSongs.length        
    

    $scope.doAnotherSearch = =>
      do $scope.closeServerSentEvents

      $scope.DOMELements.$errorAlert.slideUp    'slow'
      $scope.DOMELements.$tabsAndFilter.slideUp 'slow'
      $scope.DOMELements.$core.fadeOut          'slow'

      $scope.DOMELements.$formUrl.slideDown     'slow'
      $scope.illustration  = true

      do $scope.clearItems

    $scope.clearItems = =>
      $scope.explorerLinks        = []
      $scope.explorerImages       = []
      $scope.explorerTextFiles    = []
      $scope.explorerDocuments    = []
      $scope.explorerVideos       = []
      $scope.explorerSongs        = []

    $scope.downloadFile = =>
      document.location = 'data:Application/oct-stream,' + encodeURIComponent()


    # ====================================================
    # Runner
    # ====================================================
    do $scope.initialize
    
    

  # ====================================================
  # Factory
  # ====================================================
  .factory 'FactoryRequest', ($http) =>
    get: (site)->
      $http 
        url: 'start'
        method:'GET'
        params:
          site: site



  