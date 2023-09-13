from pydantic import BaseModel, validator
from typing import Optional
import re

class Job(BaseModel):
    domain: str
    status: Optional[str] = None
    retry: Optional[int] = 0

    @validator("domain")
    def check_domain(cls, v):
        if not is_subdomain(v):
            raise ValueError("domain is not a subdomain")
        return v

def is_subdomain(s):
    pattern = r"(?!-)[A-Za-z0-9-]{1,63}(?<!-)\." \
              r"(?!-)[A-Za-z0-9-]{1,63}(?<!-)\." \
              r"[A-Za-z]{2,6}"
    return re.fullmatch(pattern, s) is not None