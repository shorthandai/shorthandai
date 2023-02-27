## shorthandai

This package provides a Python SDK for working with the ShorthandAI platform.

### Installation
```sh
$ pip install shorthandai
```

### Usage
```py
from shorthandai import ShorthandAI

# Token can be passed by setting the environment variable `SHORTHANDAI_TOKEN`.
# token can be generated at https://apiv1.shorthand.ai/
SH = ShorthandAI()

# Alternately, pass in the token explicitly
token = 'sh-...' 
SH = ShorthandAI(token)

# Get values
print(SH.get("dev123"))

# Set values
print(SH.set("dev123", 4000))

import datetime
# Get historical
print(SH.geth("dev123", datetime.datetime(2022, 12, 31)))
```