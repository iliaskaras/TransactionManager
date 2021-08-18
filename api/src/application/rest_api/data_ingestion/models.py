from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class DataIngestionPostRequestBody:
    filepath: str
    data_address: Optional[str] = "'Online Retail'!A1"
