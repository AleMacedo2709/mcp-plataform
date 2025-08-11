from .celery_app import app
import os, httpx, json, traceback
from celery import current_task
from packages.shared_ingestion.analyzer import analyze_file

PERSISTENCE = os.getenv('PERSISTENCE_BASE_URL', 'http://mcp-persistence:8000')

@app.task(bind=True)
def ingest_analyze(self, file_path: str, analysis_type: str = 'analyze_project_document_cnmp', owner: str | None = None, filename: str | None = None):
    task_id = self.request.id or current_task.request.id
    async def _patch(status: str, result=None):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                await client.patch(f"{PERSISTENCE}/tasks/{task_id}", json={
                    'status': status,
                    'result': result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)
                }, headers={'x-user': owner or 'unknown@local'})
        except Exception:
            pass

    try:
        # started
        import asyncio
        asyncio.run(_patch('started', None))
        # analyze
        result = asyncio.run(analyze_file(file_path))
        status = 'success' if isinstance(result, dict) and not result.get('error') else 'failed'
        asyncio.run(_patch(status, result))
        return {'status': status}
    except Exception as e:
        err = {'error': str(e), 'trace': traceback.format_exc()}
        import asyncio
        asyncio.run(_patch('failed', err))
        return err
