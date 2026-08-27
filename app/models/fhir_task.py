import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    DRAFT = "draft"
    REQUESTED = "requested"
