import logging
import sys

stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [stdout_handler, ]

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger("BenchmarkingLogger")
