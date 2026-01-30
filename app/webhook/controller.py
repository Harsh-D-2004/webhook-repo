from datetime import datetime, timezone
from app.webhook.schema.request import GithubRequest, ActionType

# extract github request from webhook payload
def extract_github_request(webhook_payload: dict):

    if 'pull_request' in webhook_payload:
        return handle_pull_request_event(webhook_payload)

    elif 'ref' in webhook_payload and 'commits' in webhook_payload:
        return handle_push_event(webhook_payload)

    return None

# handle pull request event
def handle_pull_request_event(payload: dict):

    action = payload.get('action')
    pr = payload.get('pull_request', {})

    # handle merged state of pull request
    if action == 'closed' and pr.get('merged'):
        
        # extracting all required fields
        request_id = pr.get('merge_commit_sha')
        merged_by = pr.get('merged_by', {})
        author = merged_by.get('login')
        head = pr.get('head', {})
        base = pr.get('base', {})
        from_branch = head.get('ref')
        to_branch = base.get('ref')
        merged_at = pr.get('merged_at')
        timestamp = _parse_timestamp(merged_at)

        # creating github request object
        return GithubRequest(
            request_id=request_id,
            author=author,
            action=ActionType.MERGE,
            from_branch=from_branch,
            to_branch=to_branch,
            timestamp=timestamp
        )

    # handle opened state of pull request
    elif action == 'opened':

        # extracting all required fields
        head = pr.get('head', {})
        request_id = head.get('sha')
        user = pr.get('user', {})
        author = user.get('login')
        base = pr.get('base', {})
        from_branch = head.get('ref')
        to_branch = base.get('ref')
        created_at = pr.get('created_at')
        timestamp = _parse_timestamp(created_at)

        # creating github request object
        return GithubRequest(
            request_id=request_id,
            author=author,
            action=ActionType.PULL_REQUEST,
            from_branch=from_branch,
            to_branch=to_branch,
            timestamp=timestamp
        )

    return None

# handle push event
def handle_push_event(payload: dict):
    request_id = payload.get('after')

    if not request_id:
        request_id = ""

    # extracting all required fields
    pusher = payload.get('pusher', {})
    author = pusher.get('name')
    ref = payload.get('ref', '')
    branch = ref.replace('refs/heads/', '')
    head_commit = payload.get('head_commit', {})
    timestamp_str = head_commit.get('timestamp')
    timestamp = _parse_timestamp(timestamp_str)

    # creating github request object
    return GithubRequest(
        request_id=request_id,
        author=author,
        action=ActionType.PUSH,
        from_branch=branch,
        to_branch=branch,
        timestamp=timestamp
    )

# parse timestamp replacing Z with +00:00
def _parse_timestamp(timestamp_str: str):
    if not timestamp_str:
        return datetime.now(timezone.utc)

    timestamp_str = timestamp_str.replace('Z', '+00:00')

    return datetime.fromisoformat(timestamp_str)
