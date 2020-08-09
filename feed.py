import streamlit as st
import streamlit.components.v1 as components

import inoreader
from inoreader import main
import itertools

from inoreader.consts import BASE_URL
from inoreader.article import Article
from urllib.parse import urljoin, quote_plus
def _get_stream_contents(self, stream_id, continuation='', n=1000):
    self.check_token()

    url = urljoin(BASE_URL, self.STREAM_CONTENTS_PATH + quote_plus(stream_id))
    params = {
        'n': n,            # default 20, max 1000
        'r': '',
        'c': continuation,
        'output': 'json'
    }
    response = self.parse_response(self.session.post(url, params=params, proxies=self.proxies))
    if 'continuation' in response:
        return response['items'], response['continuation']
    else:
        return response['items'], None
import requests

# https://github.com/jupyter/notebook/issues/2790
class Tweet(object):
    def __init__(self, s, embed_str=False):
        if not embed_str:
            # Use Twitter's oEmbed API
            # https://dev.twitter.com/web/embedded-tweets
            api = 'https://publish.twitter.com/oembed?url={}'.format(s)
            response = requests.get(api)
            self.text = response.json()["html"]
        else:
            self.text = s

    def _repr_html_(self):
        return self.text

def get_stream_contents(client, stream_id, c='', n=1000):
    while True:
        articles, c = _get_stream_contents(client, stream_id, c, n=n)
        for a in articles:
            yield Article.from_json(a)
        if c is None:
            break

@st.cache
def fetch_articles(stream_id=None, n=5):
    client = main.get_client()
    #f = client.fetch_articles(stream)
    f = get_stream_contents(client, stream_id, n=n)
    f = itertools.islice(f, n)
    xs = list(f)
    return xs

st.title('Feed')

feed_id = st.text_input('Feed ID', 'feed/http://planet.clojure.in/atom.xml')

xs = fetch_articles(feed_id)

st.button('Mark All as Read')
#components.iframe('https://www.instapaper.com/read/1281280152')
for x in xs:
  #components.html('<hr>')
  
  st.text('------\n%s' % x.feed_title)
  st.text(f'{x.title} || {x.feed_link}')
  components.html(x.content, scrolling=True)
  st.multiselect('labels', ['-1', '+1', 'orbit'], key=f"label:{x.id}") 
  st.text_input('Notes', '', key=f"note:{x.id}")


# interactive cljs
#my_component = components.declare_component("my_component", path="frontend/public")
#num_clicks = my_component(default=0)
#st.markdown("You've clicked %s times!" % int(num_clicks))