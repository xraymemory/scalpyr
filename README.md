#Scalpyr - Get SeatGeek API info fast in pure Python

Scalpyr provides a thin wrapper around the SeatGeek api.

Current supported endpoints are
 - events
 - performers
 - venues
 - taxonomies
 - recommendations

Scalpyr also provides some convenience functions for retrieving ticket urls from SeatGeek. Note that this loads the
SeatGeek page and scrapes the urls so it may stop working at any moment.

#Install
Install from pip

```shell
pip install scalpyr
```

You can just clone the git repo and run setup.py.

```shell
git clone git://github.com/yolesaber/scalpyr.git
cd scalpyr
python setup.py install
```

#Using Scalpyr

Scalpyr can be passed a `dev_key` on instantiation, otherwise it will access SeatGeek anonymously.

#Get event info!
```python
from scalpyr import Scalpyr
seatgeek = Scalpyr()
request_args = {"venue.city": "NY"}
events = seatgeek.get_events(request_args)
...
```

#TODO
+ Add more examples

Author: Michael Anzuoni [tangents.co](http://tangents.co), and Cezar Jenkins @emperorcezar for [SpotHero](http://spothero.com)
