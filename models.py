from typing import Optional
from pydantic import BaseModel, HttpUrl

class FundData(BaseModel):
    """
    Schema for validating the scraped mutual fund factual data.
    Ensures that the basic necessary information exists before it's vectorized.
    """
    url: HttpUrl
    fund_name: Optional[str] = None
    expense_ratio: Optional[float] = None
    exit_load: Optional[str] = None
    nav: Optional[float] = None
    aum: Optional[str] = None
    fund_manager: Optional[str] = None
    raw_text_content: str

    class Config:
        # Allows extra fields if needed, but strictly types the ones defined above
        extra = "allow"
