import json
from datetime import datetime
from flask_restplus import Namespace, Resource

from . import session
from .utils import create_soup_object, get_max_page_in_category
from .models import Website, Category, Job, JobListing

api = Namespace('dev_bg', description='Scraping dev.bg')


# Website endpoints
@api.route('/')
class GetAllWebsites(Resource):
    @api.doc('get_all_websites')
    def get(self):
        '''Get all of the website's we have data for'''

        results = [site[0] for site in Website.query.with_entities(Website.url).all()]
        return results


@api.route('/<path:url>')
@api.param('url', 'The website we want to save')
class SaveWebsite(Resource):
    @api.doc('save_website_html')
    def post(self, url):
        '''Save the website's data in our DB'''

        soup = create_soup_object(data=url, from_type='url')

        # Query the DB first to see if we already have an entry for our URL
        existing_row = Website.query.filter(Website.url == url).first()

        # If we don't, create a new one
        if not existing_row:
            row = Website(url=url, data=str(soup), last_updated=datetime.utcnow())
            session.add(row)
            session.commit()
        # if we do, check if the data has changed since then and update it
        else:
            existing_data = existing_row.data

            if not existing_data == str(soup):
                existing_row.data = str(soup)
                existing_row.last_updated = datetime.utcnow()
                session.commit()

        return True


# Categories endpoints
@api.route('/extract_categories/<path:url>')
@api.param('url', 'The website we want to extract the categories from')
class WebsiteCategories(Resource):
    @api.doc('save_categories')
    def post(self, url):
        '''Save the website's categories in our DB'''

        # Query the DB for the website data
        website_row = Website.query.filter(Website.url == url).first()

        if website_row:
            soup = create_soup_object(data=website_row.data, from_type='html')

            all_categories = soup.find_all('a', class_='category-name')
            category_names = list()
            categories_to_add = list()

            for cat in all_categories:
                # Take the child element and get the text
                category_names.append(cat.next_element.strip())

            existing_categories = Category.query.\
                filter(Category.category_name.in_(category_names)).\
                filter(Category.website_id == website_row.id).all()

            # First we must filter out the existing categories to prevent duplicates, IF we have data for this website
            # Otherwise, we will just add the categories
            if existing_categories:
                for cat in all_categories:
                    cat_exists = False

                    for existing_cat in existing_categories:
                        cat_name = cat.next_element.strip()

                        # if the category exists, we will set the boolean to false and skip adding it
                        if cat_name == existing_cat.category_name:
                            cat_exists = True
                            break

                    if not cat_exists:
                        categories_to_add.append(cat)
            else:
                categories_to_add = all_categories

            for cat in categories_to_add:
                # Take the child element and get the text
                category_name = cat.next_element.strip()

                category_url = cat.get('href')
                website_id = website_row.id

                new_category_row = Category(website_id=website_id,
                                            category_name=category_name,
                                            category_url=category_url)
                session.add(new_category_row)
                session.commit()
        return True

    @api.doc('get categories')
    def get(self, url):
        '''Get a list of our saved categories for the website'''

        # Query the DB for the website data
        website_row = Website.query.filter(Website.url == url).first()
        all_categories = list()

        if website_row:
            website_categories = Category.query.filter(Category.website_id == website_row.id).all()

            if website_categories:
                for cat in website_categories:
                    all_categories.append(cat.category_name)

        return all_categories


@api.route('/extract_listings_first_page/<path:url>/category/<path:category>')
@api.param('url', 'The website we want to extract the categories from')
@api.param('category', 'The category')
class WebsiteCategoryListingsFirstPage(Resource):
    @api.doc('get_category_listings_first_page')
    def get(self, url, category):
        '''Get all listings for the given category, first page only'''

        # Get the website id first
        website_id = Website.query.with_entities(Website.id).filter(Website.url == url).first()[0]

        # Get the category url next
        category_row = Category.query.\
            filter(Category.website_id == website_id).\
            filter(Category.category_name == category).first()

        category_url = category_row.category_url

        # Create the soup object
        soup = create_soup_object(data=category_url, from_type='url')

        all_listings = soup.find_all('div', class_='inner-right')

        listing_results = list()
        for listing in all_listings:
            title = listing.find('h6', class_='job-title')
            listing_results.append(title.text.strip())

        return listing_results


@api.route('/extract_all_listings/<path:url>/category/<path:category>')
@api.param('category', 'The category')
@api.param('url', 'The website we want to extract the categories from')
class WebsiteCategoryListingsAllPages(Resource):
    @api.doc('get_all_category_listings')
    def get(self, url, category):
        '''Get all listings for the given category'''

        # Get the website id first
        website_id = Website.query.with_entities(Website.id).filter(Website.url == url).first()[0]

        # Get the category url next
        category_row = Category.query.\
            filter(Category.website_id == website_id).\
            filter(Category.category_name == category).first()

        category_url = category_row.category_url

        # Create the soup object for the first page
        soup = create_soup_object(data=category_url, from_type='url')
        max_page = get_max_page_in_category(soup)

        max_page = 3  # Hardcoding this so we don't wait ages for the endpoint to finish

        # Iterate through all the pages and get the listings
        listing_results = list()
        for i in range(1, max_page+1):

            # We already have the soup object for the first page, only need to re-create it when we switch page
            if i == 1:
                pass
            else:
                new_page = f'{category_url}/page/{i}/'
                soup = create_soup_object(new_page, from_type='url')

            all_listings = soup.find_all('div', class_='inner-right')

            for listing in all_listings:
                title = listing.find('h6', class_='job-title')
                listing_results.append(title.text.strip())

        return listing_results


@api.route('/jobs_in_category/<path:url>')
@api.param('url', 'The website we want to extract the categories from')
class WebsiteCategoryJobs(Resource):
    @api.doc('save_all_category_jobs')
    def post(self, url):
        '''Save all jobs for each category'''

        # Create the soup object
        soup = create_soup_object(data=url, from_type='url')

        existing_categories = Category.query.all()

        all_categories = soup.find_all('div', class_='category-block')

        for cat in all_categories:
            category_name = cat.find_all('a', class_='category-name')[0].next_element.strip()

            # Get the category ID from the name
            category_id = None
            for existing_cat in existing_categories:
                if existing_cat.category_name == category_name:
                    category_id = existing_cat.id
                    break

            if category_id:
                jobs_in_category = cat.find_all('div', class_='child-term')

                for job in jobs_in_category:
                    a_tag = job.find('a')

                    job_url = a_tag.get('href')

                    div_element = a_tag.find('div', class_='term-icon')
                    job_name = div_element.next_element.strip()

                    new_job = Job(category_id=category_id,
                                  job_name=job_name,
                                  job_url=job_url)
                    session.add(new_job)
                    session.commit()

        return True


@api.route('/jobs_in_category')
class GetWebsiteJobs(Resource):
    @api.doc('get_all_jobs')
    def get(self):
        '''Get all jobs'''

        results = list()

        all_jobs = Job.query.all()
        for job in all_jobs:
            job_data = {
                'job_id': job.id,
                'job_name': job.job_name,
                'job_url': job.job_url
            }
            results.append(job_data)

        return results


@api.route('/jobs_in_category/<path:category>')
@api.param('category', 'The category')
class GetWebsiteCategoryJobs(Resource):
    @api.doc('get_all_jobs_for_category')
    def get(self, category):
        '''Get jobs for a specific category'''

        category_id = Category.query.with_entities(Category.id).filter(Category.category_name == category).first()[0]

        all_jobs_for_category = Job.query.filter(Job.category_id == category_id).all()
        results = list()
        for job in all_jobs_for_category:
            job_data = {
                'job_id': job.id,
                'job_name': job.job_name,
                'job_url': job.job_url
            }
            results.append(job_data)

        return results


@api.route('/listings')
class WebsiteCategoryJobs(Resource):
    @api.doc('save_all_listings_for_jobs')
    def post(self):
        '''Save all listings for each job'''

        all_jobs = Job.query.all()

        for job in all_jobs:
            soup = create_soup_object(job.job_url, from_type='url')

            all_listings = soup.find_all('div', class_='inner-right')

            for listing in all_listings:
                title_tag = listing.find('h6', class_='job-title')
                listing_name = title_tag.text.strip()

                listing_url = listing.find('a', class_='overlay-link').get('href')

                date_created = ''
                date_tag = listing.find('span', class_='date')
                if date_tag:
                    date_created = date_tag.text.strip()

                location = ''
                location_tag = listing.find('span', class_='badge')
                if location_tag:
                    location = location_tag.text.strip()

                listing_data = {
                    'date_created': date_created,
                    'location': location
                }

                new_listing = JobListing(job_id=job.id,
                                         listing_name=listing_name,
                                         listing_url=listing_url,
                                         listing_data=json.dumps(listing_data, ensure_ascii=False))

                session.add(new_listing)
                session.commit()

        return True

    @api.doc('get_all_listings_for_jobs')
    def get(self):
        '''Get all listings for jobs'''

        results = list()

        all_listings = JobListing.query.all()
        for listing in all_listings:
            listing_data = {
                'listing_name': listing.listing_name,
                'listing_url': listing.listing_url,
                'listing_data': listing.listing_data
            }
            results.append(listing_data)

        return results
