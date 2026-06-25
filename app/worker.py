from redis import Redis
from rq import Worker, Queue
import app.tasks

redis_conn = Redis(
    host="redis",
    port=6379
)

queue = Queue("default", connection=redis_conn)

worker = Worker(
    [queue],
    connection=redis_conn
)

if __name__ == "__main__":
    worker.work()