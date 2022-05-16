## Gotipy

A simple Python wrapper for [Gotify](https://github.com/gotify/server)


## Requirements
- [python>=3.6](https://www.python.org/downloads/)
- [gotify/server](https://gotify.net/docs/install)


## Installation

```sh
pip install gotipy
```

## Usage

### Create a new application

```py
from gotipy import Gotify

g = Gotify(host_address='https://yourdomain.com')
g.create_app(admin_username='admin', admin_password='admin', app_name='demo', desc='My first app!')

# {'id': 1, 'token': 'xxxxxxxxxx', 'name': 'demo', 'description': 'My first app!', 'internal': False, 'image': 'static/defaultapp.png'}
```

### Push messages to an application

```py
from gotipy import Gotify

g = Gotify(host_address='https://yourdomain.com')
g.push(title='My message', message='Hello, World!', priority=9, token='xxxxxxxxxx')

# {'id': 1, 'appid': 1, 'message': 'Hello, World!', 'title': 'My message', 'priority': 9, 'date': '2022-05-16T05:25:29.367216435Z'}
```


### Notes:

- You can set `GOTIFY_HOST_ADDRESS` as an envionmnt variable instead of passing it to the class instance.
- If you want to use the same app in all your `push` calls, you can pass `fixed_token=...` to the class instance, or set `GOTIFY_APP_TOKEN` as an envionmnt variable intead of passing `token` to the `push` method.
- If you want to set a fixed priority for all your `push` calls, pass `fixed_priority` to the class instance.

