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

    $scope.explorerLinksTargets       = ['text/html']
    $scope.explorerImagesTargets      = [
      'image/bmp' 
      'image/cgm' 
      'image/vnd.djvu' 
      'image/gif' 
      'image/x-icon' 
      'image/ief' 
      'image/jp2' 
      'image/jpeg' 
      'image/x-macpaint'
      'image/x-portable-bitmap'
      'image/pict'
      'image/png'
      'image/x-portable-anymap'
    ]
    $scope.explorerTextFilesTargets   = []
    $scope.explorerDocumentsTargets   = ['documento/crawler']
    $scope.explorerVideosTargets      = [
      'video/crawler'
      'video/x-msvideo' 
      'video/x-dv' 
      'video/x-m4v' 
      'video/quicktime' 
      'video/x-sgi-movie' 
      'video/mp4' 
      'video/mpeg'
      'video/vnd.mpegurl' 
    ]
    $scope.explorerSongsTargets       = []

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
      do $scope.timeSrc.close

    ## Logical Methods
    #=====================================
    $scope.addItems = (json) =>
      for data in json
        hasType = false

        hasType = $scope.getLink(data)

        if not hasType then $scope.getImage(data) else continue
        if not hasType then $scope.getVideo(data) else continue

    $scope.getLink = (json) =>
      $scope.getSomething json, $scope.explorerLinksTargets, $scope.explorerLinks

    $scope.getImage = (json) =>
      $scope.getSomething json, $scope.explorerImagesTargets, $scope.explorerImages

    $scope.getVideo = (json) =>
      $scope.getSomething json, $scope.explorerVideosTargets, $scope.explorerVideos

    $scope.getSomething = (json, selfTargets, attribute ) =>
      for target in selfTargets
        if target is json.data.type
          url = if _.isArray(json.data.url) then json.data.url[0] else json.data.url
          attribute.push(url)
          return true
    
    $scope.loadUrl = ()->
      if not _.isEmpty( $scope.DOMELements.$urlInput.val())
        $scope.illustration = false

        $scope.DOMELements.$formUrl.slideUp 'fast', =>
          $scope.DOMELements.$loading.slideDown 'slow', =>
            
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
                  $scope.errorMessage = 'Status code: ' + status + ', Message: ' + data
                  $scope.DOMELements.$errorAlert.fadeIn 'slow'
                  $scope.DOMELements.$loading.slideUp   'slow'
                  $scope.DOMELements.$core.fadeOut      'slow'
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



  