#Scalpyr - Get SeatGeek API info fast in pure Python

#Install
As of now, you can just clone the git repo and run setup.py.

```shell
git clone git://github.com/yolesaber/scalpyr.git
cd scalpyr
python setup.py install
```

#Start scalping!
```python
from scalpyr import Scalpyr
seatgeek = Scalpyr()
request_args = {"venue.city": "NY"}
events = seatgeek.get_events(request_args)
...
```

#TODO
+ Add functionality to access tickets
+ Add module to pip

Author: Michael Anzuoni [tangents.co](http://tangents.co)
