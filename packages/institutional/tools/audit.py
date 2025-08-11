import os, httpx, json, hashlib, time

AUDIT_WEBHOOK_URL = os.getenv("AUDIT_WEBHOOK_URL")

async def send_audit(event: str, payload: dict):
    if not AUDIT_WEBHOOK_URL:
        return
    data = {
        "ts": int(time.time()*1000),
        "event": event,
        "payload": payload
    }
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(AUDIT_WEBHOOK_URL, json=data)
    except Exception:
        pass
