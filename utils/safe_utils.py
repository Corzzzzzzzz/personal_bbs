from urllib.parse import urlparse, urljoin
from flask import request, url_for

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    text_url = urlparse(urljoin(request.host_url, target))
    return text_url.scheme in ('http', 'https') and ref_url.netloc == text_url.netloc
