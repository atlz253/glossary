from . import API
from ..db import create_database

create_database()

app = API()
