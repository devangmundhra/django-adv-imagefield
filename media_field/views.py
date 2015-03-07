from django.http import JsonResponse
import urllib2
from BeautifulSoup import BeautifulSoup
import re


def url_image_list(request):
    if request.method == 'GET':
        url = request.GET.get('url', None)
        response = {'status': 'error', 'urls': []}

        # Working only with http and https.
        # There is a check to using one of these protocols.
        # If a user defined URL without protocol prefix -- add it.
        # If a user defined another protocol, ValueError exception will be
        # raised below.
        if url:
            http = re.search(r'^http://', url)
            https = re.search(r'^https://', url)
            if not http and not https:
                url = 'http://' + url
        else:
            return JsonResponse(response)

        try:
            f = urllib2.urlopen(url, None, 10)
            mime_type = f.headers.gettype()

            # URL points directly to image
            if 'image' in mime_type:
                response['urls'] = [{'url': url}]
                response['status'] = 'ok'
            # URL points to human-readable text and source code
            elif mime_type == 'text/html' or mime_type == 'text/xml':
                url_content = f.read()
                soup = BeautifulSoup(url_content)
                imgs = soup.findAll('img')
                url_set = set([img['src'] for img in imgs])
                urls = [{'url': url_item} for url_item in url_set]
                response['urls'] = urls
                response['status'] = 'ok'
        except ValueError:
            response = {'status': 'error'}
        except urllib2.URLError:
            response = {'status': 'error'}
        return JsonResponse(response)
