#Scalpyr - Get SeatGeek API info fast in pure Python

#Install
As of now, you can just clone the git repo and run setup.py.

```shell
git clone git://github.com/yolesaber/scalpyr.git
cd scalpyr
python setup.py install
```

It'll be on pip soon...

#Start scalping!
```python
from scalpyr import scalpyr
seatgeek_info = Scalpyr()
request_args = {"venue.city": "NY"}
events = seatgeek_info.get_events(request_args)
...
```

#TODO
+ Add functionality to access tickets

Author: Michael Anzuoni [tangents.co](http://tangents.co)