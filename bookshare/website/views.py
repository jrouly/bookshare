from website.models import Listing,Seller
from website.forms import ListingForm
from django.http import Http404
from django.conf import settings
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils import timezone
from datetime import datetime,timedelta
from django.contrib.auth.decorators import login_required

import pyisbn
import requests

# pulls worldcat metadata from ISBNs
def ISBNMetadata(standardISBN):
    url = "http://xisbn.worldcat.org/webservices/xid/isbn/" + standardISBN + "?method=getMetadata&format=json&fl=title,year,author,ed"
    metadata = request.get(url)
    # format into a dictionary
    dejson = metadata.json()
    metadataDict = dejson['list'][0]
    return metadataDict

# gamification
def totalSold(seller):
    soldList = Listing.objects.filter(seller__user__username=seller)
    totalSold = 0
    for book in soldList:
        if book.finalPrice:
            totalSold += book.finalPrice
    return totalSold

# validation of new listing forms
    # <3 test cases

# relevant comments
def relevantComments(seller):
    sellerListings = Listing.objects.filter(seller__user__username=seller).order_by("-date_created")
    # all listings that seller has commented on (preferably ordered in reverse)
    # put those lists together
    # return that list
    return False

# saved searches
    # need to implement haystack stuff first

# seller's rating
def ratingsAverage(seller):
    sellerRating = Seller.objects.filter(user__username=seller)
    ratingNumber = 0
    ratingTotal = 0
    ratingAverage = 0
    for rating in sellerRating:
        ratingNumber += 1
        ratingTotal += rating
    ratingAverage = ratingTotal/ratingNumber
    return ratingNumber


############# VIEWS #######################



# home page
# Maybe don't login_require this, and allow anonymous users to browse a
# list of currently potsed books? idk.
@login_required
def index(request):

#    # front page of the site shows the 12 most recent listings
#    products = Book.objects.all().order_by("-uploaded")
#    paginator = Paginator(products, 12)
#
#    # can we get a first page please?
#    try:
#        page = int(request.GET.get("page", '1'))
#    except ValueError: page = 1
#
#    # how many pages do we have?
#    try:
#        products = paginator.page(page)
#    except (InvalidPage, EmptyPage):
#        blogs = paginator.page(paginator.num_pages)
    
    # need to figure out what needs to be displayed/accessed

    # ability to create and display saved searches
    # pull all comments from listings user has posted on and their listings
    # make pagination work
    # NEED TO HAVE THE SEARCH WORK--- YAY HAYSTACK
    return render(request, 'index.html', {

    },
    )

# User profile page
@login_required
def profile(request, slug):

    # verify that the user exists
    seller = get_object_or_404(Seller, user__username=slug)
    listings = Listing.objects.filter(seller__user__username=slug)

    return render(request, 'profile.html', {
        'seller' : seller,
        'listings': listings,
        'total_sold' : totalSold( slug ),
    },
    )

# User listings page
#@login_required
#def user_listings(request, slug):
#
#    # verify that the user exists
#    seller = get_object_or_404(Seller, user__username=slug)
#    listings = Listing.objects.filter(seller__user__username=slug)
#
#    return render(request, 'user_listings.html', {
#        'seller' : seller,
#        'listings': listings,
#    },
#    )

# Listing page
@login_required
def listing(request, slug, book_slug):

    seller = get_object_or_404(Seller,user__username=slug)
    listing = get_object_or_404(Listing,pk=book_slug)

    # if the listing is over a week old, it's old
    old_threshold = timezone.now() - timedelta(weeks=3)

    # make a thumbnail of the image
#    from PIL import Image
#    size = (100, 100)
#    image = Image.open( listing.photo )
#    image.thumbnail(size, Image.ANTIALIAS)
#    background = Image.new('RGBA', size, (255, 255, 255, 0))
#    background.paste( image,
#        ((size[0] - image.size[0]) / 2, (size[1] - image.size[1]) / 2))

    if listing.seller != seller:
        raise Http404("Seller does not match listing.")

    if not listing.active:
        raise Http404("Listing inactive.")

    return render(request, 'listing.html', {
        'listing' : listing,
        'media' : settings.MEDIA_URL,
        'old' : listing.date_created < old_threshold,
#        'thumbnail' : background,
    },
    )

@login_required
def create_listing(request):

    if request.method == 'POST':
        listing_form = ListingForm(request.POST, request.FILES, request=request)
        if listing_form.is_valid():
            listing = listing_form.save(commit=False)
            listing.seller = request.user.seller
            listing.slug = listing.title + listing.author
            listing.save()

            #listing.save()
            return redirect( 'listing', listing.seller.user.username, listing.pk )
    else:
        listing_form = ListingForm(request=request)

    return render(request, 'create_listing.html', {
        'form' : listing_form,
    },
    )

def close_listing(request, book_slug):
    user = request.user
    listing = Listing.objects.get(pk=book_slug)

    if listing.seller.user == user:
        listing.active = False
        listing.save()

    return redirect('profile', request.user.username)

@login_required
def search(request):
    # merely forms
    return render(request, 'search.html', {
    
    },
    )

def about(request):
    # merely forms
    return render(request, 'about.html', {
    },
    )

def contact(request):
    # merely forms
    return render(request, 'contact.html', {
    },
    )

def privacy(request):
    # merely forms
    return render(request, 'privacy.html', {
    },
    )
