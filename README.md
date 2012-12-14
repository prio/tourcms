# tourcms

A simple wrapper for connecting to [TourCMS Marketplace API](http://www.tourcms.com/support/api/mp/). This wrapper mirrors the TourCMS PHP library.

[![Build Status](https://secure.travis-ci.org/prio/tourcms.png)](http://travis-ci.org/prio/tourcms)

## Install

    pip install tourcms
    
## Usage

Using the library is as simple as creating a **TourCMS::Connection** object:

    conn = TourCMS::Connection.new(marketplace_id, private_key, result_type)
    
Your Marketplace ID and Private Key can be found in the TourCMS Partner Portal. The result type can be one of **hash** or **raw** where **raw** will return the raw XML from the API and **hash** will return a Ruby Hash of the result.

### Working with your connection in Raw mode

```python
    # Instantiate the connection
    import os
    from tourcms import Connection

    conn = Connection(0, os.getenv('TOURCMS_PRIVATE_KEY'))

    # Check we're working
    conn.api_rate_limit_status(channel_id)
    => "<?xml version="1.0" encoding="utf-8" ?><response><request>GET /api/rate_limit_status.xml</request>
        <error>OK</error><remaining_hits>1999</remaining_hits><hourly_limit>2000</hourly_limit></response>"

    # List the channels we have access to
    conn.list_channels
    => ""<?xml version="1.0" encoding="utf-8" ?><response><request>GET /p/channels/list.xml</request>
        <error>OK</error><channel>(...)</channel><channel>(...)</channel><channel>(...)</channel></response>"
    
    # Show a particular channel
    conn.show_channel(1234567)
    => ""<?xml version="1.0" encoding="utf-8" ?><response><request>GET /p/channels/list.xml</request>
        <error>OK</error><channel>(...)</channel></response>"
```

### Working with your connection in Dictionary mode
    Requires xmltodict to be installed

        pip install xmltodict
        
```python
    # Instantiate the connection
    conn = Connection(0, os.getenv('TOURCMS_PRIVATE_KEY'), "dict")

    # Check we're working
    conn.api_rate_limit_status(channel_id)
    => OrderedDict([(u'request', u'GET /api/rate_limit_status.xml?'), (u'error', u'OK'), (u'remaining_hits', u'1999'), (u'hourly_limit', u'2000')])
    obj["hourly_limit"]
    => 2000   
```

### Passing parameters

Many TourCMS methods accept parameters. Most methods take a dictionary of parameters like so:

    obj = conn.search_tours({"country": "GB", "lang": "en"})

## List of functions in TourCMS::Connection

*   api\_rate\_limit\_status
*   list\_channels
*   show\_channel
*   search\_tours
*   search\_hotels\_range
*   search\_hotels\_specific
*   list\_tours
*   list\_tour\_images
*   show\_tour
*   show\_tour\_departures
*   show\_tour\_freesale

## Dependencies

None. xmltodict optional. Tested with Python 2.7.

## Copyright

Copyright (c) 2012 Jonathan Harrington. See LICENSE.txt for further details.
