'use strict'

describe 'Controller: TechnologiesCtrl', () ->

  # load the controller's module
  beforeEach module 'publicApp'

  TechnologiesCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope = $rootScope.$new()
    TechnologiesCtrl = $controller 'TechnologiesCtrl', {
      $scope: scope
    }

  it 'should attach a list of awesomeThings to the scope', () ->
    expect(scope.awesomeThings.length).toBe 3
