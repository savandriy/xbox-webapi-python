from enum import Enum
from typing import List, Optional
from xbox.webapi.common.models import CamelCaseModel

class PresenceLevel(str, Enum):
    USER = "user"
    DEVICE = "device"
    TITLE = "title"
    ALL = "all"


class LastSeen(CamelCaseModel):
    device_type: Optional[str]
    title_id: Optional[str]
    title_name: Optional[str]
    timestamp: Optional[str]
    
class ActivityRecord(CamelCaseModel):
    richPresence: Optional[str]
    media: Optional[str]

class TitleRecord(CamelCaseModel):
    id: Optional[str]
    name: Optional[str]
    activity: Optional[ActivityRecord]
    lastModified: Optional[str]
    placement: Optional[str]
    state: Optional[str]

class DeviceRecord(CamelCaseModel):
    titles: Optional[List[TitleRecord]]
    type: Optional[str]
        

class PresenceItem(CamelCaseModel):
    xuid: str
    state: str
    last_seen: Optional[LastSeen]
    devices: Optional[List[DeviceRecord]]
    

class PresenceBatchResponse(CamelCaseModel):
    __root__: List[PresenceItem]
