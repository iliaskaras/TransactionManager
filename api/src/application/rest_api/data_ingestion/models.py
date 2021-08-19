from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class DataIngestionPostRequestBody:
    filepath: str
    excel_sheet_name: Optional[str] = "'Online Retail'!A1"

