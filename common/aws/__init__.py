from typing import Any
from boto3 import Session

def create_session() -> Session:
    return Session()

def create_client(session: Session, service_name: str, region_name: str) -> Any:
    return session.client(service_name, region_name)