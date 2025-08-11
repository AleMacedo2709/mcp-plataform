import json, logging, sys, time, os

def configure_json_logging(service: str):
    logger = logging.getLogger()
    logger.setLevel(os.getenv("LOG_LEVEL","INFO"))
    handler = logging.StreamHandler(sys.stdout)
    formatter = JsonLogFormatter(service)
    handler.setFormatter(formatter)
    logger.handlers = [handler]

class JsonLogFormatter(logging.Formatter):
    def __init__(self, service: str):
        super().__init__()
        self.service = service
    def format(self, record):
        base = {
            "ts": int(time.time()*1000),
            "level": record.levelname,
            "service": self.service,
            "msg": record.getMessage(),
            "logger": record.name
        }
        if record.exc_info:
            base["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(base, ensure_ascii=False)
