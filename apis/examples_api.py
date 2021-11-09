import os
import flask
from flask_restplus import Namespace, Resource

from .utils import create_soup_object

api = Namespace('examples', description='BeautifulSoup Examples')


@api.route('/')
class HardcodedWebsite(Resource):
    @api.doc('get_hardcoded_website_html')
    def get(self):
        '''Get the hardcoded website's html'''

        soup = create_soup_object(data='https://dev.bg/', from_type='url').prettify()

        # print the prettified html to a file
        with open(os.path.join(os.getcwd(), 'example_files/dev_bg.html'), "w", encoding='utf-8') as text_file:
            text_file.write(str(soup))

        # return it to swagger as a string
        return flask.render_template_string(soup)


@api.route('/<path:url>')
@api.param('url', 'The website we want to get')
@api.response(404, 'Website not found')
class Website(Resource):
    @api.doc('get_website_html')
    def get(self, url):
        '''Fetch the html for a given website'''

        soup = create_soup_object(data=url, from_type='url')
        return flask.render_template_string(soup.prettify())


@api.route('/extract_a_tags/<path:url>')
@api.param('url', 'The website we want to work with')
@api.response(404, 'Website not found')
class Website(Resource):
    @api.doc('get_all_a_tags_from_website')
    def get(self, url):
        '''Get a list of all <a> tags in the given website'''

        soup = create_soup_object(data=url, from_type='url')
        return str(soup.find_all('a'))


@api.route('/extract_urls/<path:url>')
@api.param('url', 'The website we want to work with')
@api.response(404, 'Website not found')
class Website(Resource):
    @api.doc('get_all_urls_from_website')
    def get(self, url):
        '''Get a list of all the URLs from a website'''

        soup = create_soup_object(data=url, from_type='url')
        result = list()

        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href != '#':
                result.append(href)

        return result
