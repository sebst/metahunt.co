
from .apis import BETALIST

from .models import BetalistProduct


def gain_betalist():
    print ("gain_betalist")
    i=0
    while True:
        r = BETALIST.startups({'method':'GET', 'per_page':100, 'page':i})
        r = r['startups']
        if r==[]:
            break
        for startup in r:
            db = BetalistProduct(**startup)
            db.save()
        i+=1







import requests, json
from .models import *



PH_API_ROOT = "https://api.producthunt.com/v1/"

from django.conf import settings
PH_ACCESS_TOKEN = settings.PH_ACCESS_TOKEN



class ProductHuntAPI:
    etag = False
    posts = []
    

    def getPosts(self, day):
        #print ("getPosts")
        headers = {
            'Content-Type': 'application/json',
            'Accept'      : 'application/json',
            'Authorization':'Bearer '+PH_ACCESS_TOKEN,
            'Accept-Encoding': '' # To disable auto gzip decompression
        }

        url = PH_API_ROOT + "posts?day=%s"%(day)
        #print(url)
        r = requests.get(url, headers=headers)

        #if r.status_code == 304 and ProductHuntAPI.posts!= []:
        #    print("IF")
        #    #return ProductHuntAPI.posts

        #print(r.headers['x-rate-limit-reset'])

        return r.json()['posts']
        



    
    def getUsers(self, newer=0):
        headers = {
            'Content-Type': 'application/json',
            'Accept'      : 'application/json',
            'Authorization':'Bearer '+PH_ACCESS_TOKEN,
            'Accept-Encoding': '' # To disable auto gzip decompression
        }
        while True:
            url = PH_API_ROOT + "users?per_page=50&order=asc&newer=%s"%(newer)
            r = requests.get(url, headers=headers)
            users = r.json()['users']
            if len(users)<1:
                break
            for user in users:
                yield user
            newer = user['id']



def gain(day='2015-01-02', force_save=False):

    #print ("GAIN", day)
    
    api = ProductHuntAPI()
    #print ("1")
    products = api.getPosts(day)
    #print ("2")
    #print ("LEN", len(products))

    #print (day, products)

    added_products = []
    added_makers = []

    for product in products:
        #print(product['id'])
        #continue

        #print (product['id'])

        #if not force_save:
        #    if ProductHunt.objects.filter(ph_id=product['id']).exists():
        #        print (ProductHunt.objects.get(ph_id=product['id']), ":::::")
        #        continue

        product_json = json.dumps(product)
        """
        P = ProductHunt(
                ph_id = product['id'],
                name = product['name'],
                tagline = product['tagline'],
                day = product['day'],
                hunted_at = product['created_at'],
                ph_featured = product['featured'],
                comments_count = product['comments_count'],
                votes_count = product['votes_count'],
                discussion_url = product['discussion_url'],
                redirect_url = product['redirect_url'],
                screenshot_850px = product['screenshot_url']['850px'],
                slug = product['discussion_url'].replace('http://www.producthunt.com/posts/', '').replace('https://www.producthunt.com/posts/', ''),
                details = product_json
            )
        """

        try: 
            P = ProductHunt.objects.get(ph_id=product['id'])
        except Exception as e:
            P = ProductHunt()

        P.ph_id = product['id']
        P.name = product['name']
        P.tagline = product['tagline']
        P.day = product['day']
        P.hunted_at = product['created_at']
        P.ph_featured = product['featured']
        P.comments_count = product['comments_count']
        P.votes_count = product['votes_count']
        P.discussion_url = product['discussion_url']
        P.redirect_url = product['redirect_url']
        P.screenshot_850px = product['screenshot_url']['850px']
        P.slug = product['discussion_url'].replace('http://www.producthunt.com/posts/', '').replace('https://www.producthunt.com/posts/', '').replace('https://www.producthunt.com/tech/', '').replace('http://www.producthunt.com/tech/', '')
        P.details = product_json


        P._update_betalist_product()
        
        P.save()
        P._update_makers()
        #P._get_real_domain()

        #if P.pk==19666:
        #    print (P.name, P._real_domain)

        P.save()
        #print(P.name)


from django.db.models import Max
def gain_ph_users():
    newer = 0
    newer = 154700
    newer= 33100
    try:
        newer = ProductHuntMaker.objects.all().aggregate(Max('ph_id'))['ph_id__max']-1
    except:
        newer = 0
    print ("starting at", newer)
    api = ProductHuntAPI()
    for user in api.getUsers(newer):
        m= ProductHuntMaker(
            ph_id = user['id'],
            signed_up_at = user['created_at'],
            username = user['username']
            )
        m.save()
        print(user['username'])




