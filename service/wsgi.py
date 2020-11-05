#!/usr/bin/env python3

from api import create_app
from config import ProdConfig

app = create_app(ProdConfig)


