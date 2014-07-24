Requests = new Meteor.Collection 'requests'
Queries = new Meteor.Collection 'queries'
Responses = new Meteor.Collection 'responses'

Router.onBeforeAction 'loading'

Router.map ->
  this.route 'home',
    path: '/'
    waitOn: -> Meteor.subscribe 'latest'
    data:
      latest: Queries.find {}, {sort: [['created', 'desc'], 'query']}
  this.route 'create'
  this.route 'tag',
    path: '/tagged/:tag'
    waitOn: -> Meteor.subscribe 'tagged', decodeURI this.params.tag
    data: ->
      tag = this.params.tag
      return {
        tag: decodeURI tag
        queries: Queries.find {}, {sort: [['created', 'desc'], 'query']}
      }
  this.route 'query',
    path: '/queries/:_id'
    waitOn: ->
      Meteor.subscribe 'query', this.params._id
      Meteor.subscribe 'responses', this.params._id
      Meteor.subscribe 'queryRequest', this.params._id
    data: ->
      id = this.params._id
      dict =
        query: Queries.findOne id
        responses: Responses.find {}
        request: Requests.findOne {queries: id}
      return dict
  this.route 'request',
    path: '/requests/:_id'
    waitOn: ->
      Meteor.subscribe 'request', this.params._id
      Meteor.subscribe 'requestQueries', this.params._id
      Meteor.subscribe 'requestResponses', this.params._id
    data: ->
      id = this.params._id
      dict = Requests.findOne id
      return dict
  this.route 'me',
    path: '/me'
    waitOn: ->
      Meteor.subscribe 'userSelf'

Template.intro.events
  'click #create': ->
    Router.go 'create'

Template.create.events
  'click #submit': (event, template) ->
    jhtml = template.$('.pen')
    html = jhtml.html()
    queryArray = (query.innerText for query in jhtml.find('u').get())
    text = jhtml.text()
    topic = template.find('#topic').value
    comment = template.find('#comment').value
    tags = template.find('#tags').value.split(/\s*,\s*/)
    Meteor.call 'addQuery', topic, queryArray, tags, comment, text, html
    Router.go 'home'

Template.navbar.events
  'submit form#tagsearch': (event, template) ->
    term = template.find('#searchfield').value
    term = encodeURI(term)
    Router.go 'tag',
      tag: term
  'click a.userPage': (event, template) ->
    Router.go 'me'

Template.query.events
  'click button#add': (event, template) ->
    jhtml = template.$('.pen')
    html = jhtml.html()
    id = this.query._id
    # id = Queries.findOne({})._id
    Meteor.call 'queryRespond', id, html
    template.$('.pen').html('')
  'click button.up': (event, template) ->
    id = this._id
    Meteor.call 'upvote', id
  'click button.down': (event, template) ->
    id = this._id
    Meteor.call 'downvote', id

Template.request.events
  'click u': (event, template) ->
    name = event.currentTarget.innerText
    id = Queries.findOne({query: name})._id
    top = Responses.findOne {query: id},
      sort: [['votes', 'desc'], ['created', 'desc']]
    console.log this
    Session.set 'topResponse', top
    $('#explanation').modal 'show'
  'click button.close': (event, template) ->
    $('#explanation').modal 'hide'

Template.explanation.helpers
  topResponse: ->
    return Session.get 'topResponse'

Template.create.rendered = ->
  this._editor = new Pen('#editor')

Template.create.destroyed = ->
  this._editor.destroy

Template.query.rendered = ->
  this._editor = new Pen('#editor')

Template.query.destroyed = ->
  this._editor.destroy

Template.explanation.rendered = ->
  $('#explanation').modal
    show: false

Template.explanation.destroyed = ->
  $('#explanation').modal 'hide'
