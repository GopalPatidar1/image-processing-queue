import asyncio
from multiprocessing import Process

from worker.main import worker


def run_worker():
    asyncio.run(worker())


def start_workers(num_workers=3):
    workers = []

    for i in range(num_workers):
        process = Process(
            target=run_worker,
            name=f"test-worker-{i + 1}",
        )
        process.start()
        workers.append(process)

    return workers


def stop_workers(workers):
    for process in workers:
        process.terminate()

    for process in workers:
        process.join()