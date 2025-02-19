from enum import Enum

class ResourceAllocationStatus(str, Enum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"