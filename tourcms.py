import hmac
import hashlib
import datetime as dt
try: # Python 3
  import urllib.parse as urllib
except ImportError:
  import urllib
try: # Python 3
  import urllib.request as urllib2
except ImportError: 
    import urllib2
try:
  import xmltodict
except ImportError:
  pass
import time
import base64
import logging


__author__ = 'Jonathan Harrington'
__version__ = '0.3'
__license__ = 'BSD'


class Connection(object):
  def __init__(self, marketp_id, private_key, result_type = "raw", loglevel = logging.CRITICAL):
    try:
      int(marketp_id)
    except ValueError:
      raise TypeError("Marketplace ID must be an Integer")
    self.marketp_id = int(marketp_id)
    self.private_key = private_key
    self.result_type = result_type
    self.base_url = "https://api.tourcms.com"
    self.logger = logging.getLogger("tourcms")
    self.logger.addHandler(logging.StreamHandler())
    self.logger.setLevel(loglevel)
    
  def _generate_signature(self, path, verb, channel, outbound_time):
    string_to_sign = u"{0}/{1}/{2}/{3}{4}".format(channel, self.marketp_id, verb, outbound_time, path)
    self.logger.debug("string_to_sign is: {0}".format(string_to_sign))
    dig = hmac.new(self.private_key.encode('utf8'), string_to_sign.encode('utf8'), hashlib.sha256)
    b64 = base64.b64encode(dig.digest())
    return urllib.quote_plus(b64)

  def _response_to_native(self, response):
    try:
      return xmltodict.parse(response)['response']
    except KeyError:
      return xmltodict.parse(response)
    except NameError:
      self.logger.error("XMLtodict not available, install it by running\n\t$ pip install xmltodict\n")
      return response

  def _request(self, path, channel = 0, params = {}, verb = "GET"):
    url = self.base_url + path + "?" + urllib.urlencode(params)
    self.logger.debug("url is: {0}".format(url))
    req_time = dt.datetime.utcnow()
    signature = self._generate_signature(
      path + "?" + urllib.urlencode(params), verb, channel, int(time.mktime(req_time.timetuple()))
    )    
    headers = {
      "Content-type": "text/xml", 
      "charset": "utf-8", 
      "Date": req_time.strftime("%a, %d %b %Y %H:%M:%S GMT"), 
      "Authorization": "TourCMS {0}:{1}:{2}".format(channel, self.marketp_id, signature)
    }
    self.logger.debug("Headers are: {0}".format(", ".join(["{0} => {1}".format(k,v) 
                                                           for k,v in headers.items()])))
    req = urllib2.Request(url)
    for key, value in headers.items():
      req.add_header(key, value)
    response = urllib2.urlopen(req).read()
    return response if self.result_type == "raw" else self._response_to_native(response)

  def api_rate_limit_status(self, channel = 0):
    return self._request("/api/rate_limit_status.xml", channel)
  
  def list_channels(self):
    return self._request("/p/channels/list.xml")
  
  def show_channel(self, channel):
    return self._request("/c/channel/show.xml", channel)
  
  def search_tours(self, params = {}, channel = 0):
    if channel == 0:
      return self._request("/p/tours/search.xml", 0, params)
    else:
      return self._request("/c/tours/search.xml", channel, params)
  
  def search_hotels_range(self, params = {}, tour = "", channel = 0):
    params.update({"single_tour_id": tour})
    if channel == 0:
      return self._request("/p/hotels/search_range.xml", 0, params)
    else:
      return self._request("/c/hotels/search_range.xml", channel, params)
    
  def search_hotels_specific(self, params = {}, tour = "", channel = 0):
    params.update({"single_tour_id": tour})
    if channel == 0:
      return self._request("/p/hotels/search-avail.xml", 0, params)
    else:
      return self._request("/c/hotels/search-avail.xml", channel, params)
  
  def list_tours(self, channel = 0):
    if channel == 0:
      return self._request("/p/tours/list.xml")
    else:
      return self._request("/c/tours/list.xml", channel)
  
  def list_tour_images(self, channel = 0):
    if channel == 0:
      return self._request("/p/tours/images/list.xml")
    else:
      return self._request("/c/tours/images/list.xml", channel)
  
  def show_tour(self, tour, channel):
    return self._request("/c/tour/show.xml", channel, {"id": tour})
  
  def show_tour_departures(self, tour, channel):
    return self._request("/c/tour/datesprices/dep/show.xml", channel, {"id": tour})
  
  def show_tour_freesale(self, tour, channel):
    return self._request("/c/tour/datesprices/freesale/show.xml", channel, {"id": tour})

  def show_supplier(self, supplier, channel):
    return self._request("/c/supplier/show.xml", channel, {"supplier_id": supplier})


