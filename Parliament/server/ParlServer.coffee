Requests = new Meteor.Collection 'requests'
Queries = new Meteor.Collection 'queries'
Responses = new Meteor.Collection 'responses'

Meteor.methods
  addQuery: (topic, queries, tags, comment, text, html) ->
    # check topic, String
    # check queries, [String]
    # check tags, [String]
    # check comment, String
    # check text, String
    # check html, String

    if Meteor.userId()
      requestId = Requests.insert
        topic: topic
        tags: tags
        comment: comment
        text: text
        html: html
        created: new Date
        createdBy:
          _id: Meteor.userId()
          name: Meteor.user().profile.name
          image: Meteor.user().services.google.picture

      newQuery = (qu) ->
        Queries.insert
          topic: topic
          query: qu
          tags: tags
          text: text
          request: requestId
          created: new Date
          createdBy:
            _id: Meteor.userId()
            name: Meteor.user().profile.name
            image: Meteor.user().services.google.picture

      queryIds = (newQuery query for query in queries)

      Requests.update requestId,
        $set:
          queries: queryIds

  queryRespond: (queryId, response) ->
    if Meteor.userId()
      responseId = Responses.insert
        query: queryId
        response: response
        votes: 0
        created: new Date
        createdBy:
          _id: Meteor.userId()
          name: Meteor.user().profile.name
          image: Meteor.user().services.google.picture

      Queries.update queryId,
        $push:
          responses: responseId

  upvote: (responseId) ->
    if Meteor.userId()
      Responses.update responseId,
        $inc:
          votes: 1

  downvote: (responseId) ->
    if Meteor.userId()
      Responses.update responseId,
        $inc:
          votes: -1



Meteor.publish 'latest', ->
  Queries.find {},
    sort: [['created', 'desc'], 'query']
    limit: 20

Meteor.publish 'tagged', (tag) ->
  return Queries.find {tags: tag},
    sort: [['created', 'desc'], 'query']

Meteor.publish 'responses', (queryId) ->
  return Responses.find {query: queryId},
    sort: [['votes', 'desc'], ['created', 'desc']]

Meteor.publish 'query', (id) -> Queries.find id

Meteor.publish 'request', (id) -> Requests.find id

Meteor.publish 'requestQueries', (requestId) ->
  Queries.find
    request: requestId

Meteor.publish 'queryRequest', (queryId) ->
  Requests.find
    queries: queryId

Meteor.publish 'requestResponses', (requestId) ->
  request = Requests.findOne requestId
  queriesCursor = Queries.find
    _id:
      $in: request.queries
  queries = queriesCursor.fetch()
  responseIds = []
  for query in queries
    responseIds = responseIds.concat query.responses
  return Responses.find
    _id:
      $in: responseIds

Meteor.publish 'userSelf', ->
  return Meteor.user()
