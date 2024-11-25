import datetime
import sqlalchemy
from typing import Union
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import select, update, func, delete, cast

from utils.db.models import *
from utils.db.models import engine, async_session
