import time
from fastapi import HTTPException

# Simple per-user token bucket: 10 requests/min per user for AI-eval endpoints
RATE = 10
WINDOW = 60  # seconds
_buckets = {}  # user_id -> [timestamps]

def ensure_rate(user_id: int):
    now = time.time()
    q = _buckets.setdefault(user_id, [])
    # drop old
    while q and now - q[0] > WINDOW:
        q.pop(0)
    if len(q) >= RATE:
        raise HTTPException(status_code=429, detail="Rate limit exceeded (10 requests/min)")
    q.append(now)
