import bottle
import re

from relevantxkcd.database import session_scope, Comic

URL = 'http://xkcd.com/'

PATTERNS = [
    r'\b%s\b',
    r'\b%s',
    r'%s',
]


class ApiController:
    @staticmethod
    @bottle.get('/xkcd')
    def get_query():
        return '''
<form action="/api/xkcd" method="post">
    Query: <input name="query" type="text" />
    <input value="Submit" type="submit" />
</form>
        '''

    @staticmethod
    @bottle.get('/api/xkcd/<query>')
    def query_subject(query):
        result_urls = None
        with session_scope() as session:
            results = session.query(Comic.num, Comic.safe_title).filter(Comic.safe_title.like('%{:s}%'.format(query))).all()
            print('Results:', len(results))
            new_results = []
            while len(new_results) == 0:
                for pattern in PATTERNS:
                    for result in results:
                        if re.findall(pattern % (query,), result.safe_title, re.IGNORECASE):
                            if result not in new_results:
                                new_results.append(result)
            for result in new_results:
                result_urls = (result_urls or '') + r'<p><a href="{url}{num}">{title}</a></p>'.format(title=result.safe_title, url=URL, num=result.num)
        return bottle.template('</p>Query was {{query}}</p><p>Search results: </p>{{!url}}', query=query, url=result_urls)

    @staticmethod
    @bottle.get('/api/xkcd')
    @bottle.post('/api/xkcd')
    def handle_query():
        try:
            if bottle.request.json:
                query = bottle.request.json['query']
            else:
                query = bottle.request.forms['query']
            return ApiController.query_subject(query)
        except KeyError:
            bottle.abort(500, 'Request did not contain a query.')
