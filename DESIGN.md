# Design

## Job Queue Processing

The application uses the database as a job queue. Jobs are created with a `pending` status and are processed by separate worker processes.

Multiple workers can run at the same time. To ensure that the same job is not picked up by multiple workers, the worker uses a database row-level lock with `FOR UPDATE SKIP LOCKED`.

When a worker picks a job:

```text
pending -> processing -> completed/failed
                       
```

The selected job is locked while it is being claimed, and other workers skip the locked row and look for the next available pending job.

This allows multiple workers to process different jobs concurrently while ensuring that a pending job is claimed by only one worker at a time.

The worker continuously checks the queue for pending jobs and processes them in job ID order. If no pending job is available, it waits before checking again.

## Worker Processes

Workers run separately from the FastAPI application. Multiple worker processes can be started based on the available CPU capacity.

Each worker uses the same database queue, so jobs are automatically distributed between the worker processes without two workers processing the same pending job at the same time.
