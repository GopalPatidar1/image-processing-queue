import os
import asyncio
from multiprocessing import Process

from worker.main import worker

def run_worker():
    asyncio.run(worker())


if __name__ == "__main__":
    num_workers = max(1, os.cpu_count() // 2)
    workers = []
    for i in range(num_workers):
        process = Process(
            target=run_worker,
            name=f"worker-{i + 1}"
        )
        process.start()
        workers.append(process)

    for process in workers:
        process.join()