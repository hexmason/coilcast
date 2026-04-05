import datetime
from uuid import UUID, uuid4
from typing import Annotated
from sqlalchemy import String, func
from sqlalchemy.orm import mapped_column

uuid_pk = Annotated[
                UUID,
                mapped_column(default=uuid4,
                              primary_key=True,
                              index=True)]

str_column = Annotated[
                str,
                mapped_column(String(255),
                              default="",
                              nullable=False)]

str_column_indexed = Annotated[
                str,
                mapped_column(String(255),
                              default="",
                              nullable=False,
                              index=True)]

int_column = Annotated[
                int,
                mapped_column(default=0,
                              nullable=False)]

float_column = Annotated[
                float,
                mapped_column(default=0.0,
                              nullable=False)]

bool_column = Annotated[
                bool,
                mapped_column(default=False,
                              nullable=False)]

created_at = Annotated[
                datetime.datetime,
                mapped_column(server_default=func.now())]

updated_at = Annotated[
                datetime.datetime,
                mapped_column(server_default=func.now(),
                              onupdate=func.now())]
