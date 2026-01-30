from datetime import datetime, timezone
from enum import Enum

# enum class 
class ActionType(str, Enum):
    PUSH = "PUSH"
    PULL_REQUEST = "PULL_REQUEST"
    MERGE = "MERGE"

# github request class for saving in mongodb
class GithubRequest:

    # constructor
    def __init__(self, request_id: str, author: str, action: ActionType,
                 from_branch: str, to_branch: str, timestamp: datetime):
        self.request_id = request_id
        self.author = author
        self.action = action
        self.from_branch = from_branch
        self.to_branch = to_branch
        self.timestamp = timestamp or datetime.now(timezone.utc)

    # to_dict method
    def to_dict(self):
        return {
            "request_id": self.request_id,
            "author": self.author,
            "action": self.action.value,
            "from_branch": self.from_branch,
            "to_branch": self.to_branch,
            "timestamp": self.timestamp
        }
    