import bottle


@bottle.get('/xkcd')
def get_xkcd(self):
    return '''
        <form action="/api/xkcd" method="post">
            Query: <input name="query" type="text" />
            <input value="Submit" type="submit" />
        </form>
    '''


@bottle.get('/api/xkcd/<query>')
def route_xkcd(self, query):
    return bottle.template('</p>Query was {{query}}</p>', query=query)


@bottle.get('/api/xkcd')
@bottle.post('/api/xkcd')
def do_xkcd(self):
    try:
        if bottle.request.json:
            query = bottle.request.json['query']
        else:
            query = bottle.request.forms['query']
        return bottle.template('</p>Query was {{query}}</p>', query=query)
    except KeyError:
        bottle.abort(500, 'Request did not contain a query.')


bottle.run(host='localhost', port='8080', debug=True)
