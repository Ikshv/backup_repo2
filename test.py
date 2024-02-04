from spacetime import Dataframe
from threading import Thread
import queue
import signal

# Import your PCC types here
from utils.pcc_models import Register

def application_logic(df):
    # Example: Add a new Register instance
    new_register = Register("crawler_1", True)
    df.add_one(Register, new_register)
    print("Added a new Register instance")

    # Commit changes to synchronize with other nodes or the server
    df.commit()
    print("Changes committed")

    # Example: Query all Register instances
    all_registers = df.read_all(Register)
    for reg in all_registers:
        print(f"Crawler ID: {reg.crawler_id}, Load Balancer: {reg.load_balancer}, Fresh: {reg.fresh}, Invalid: {reg.invalid}")
    print("Queried all Register instances")

def worker_logic(task_queue, df):
    while True:
        task = task_queue.get()
        if task is None:
            break
        print(f"Worker processing task: {task}")
        # Modify to perform tasks that potentially involve the DataFrame
        application_logic(df)
        print(f"Worker completed task: {task}")

def main_logic():
    task_queue = queue.Queue()

    # Initialize Spacetime Dataframe with actual PCC types
    df = Dataframe(appname="MyApp", types=[Register], server_port=0, autoresolve=True)
    print("Initialized Spacetime Dataframe")

    # Start worker threads
    workers = [Thread(target=worker_logic, args=(task_queue, df)) for _ in range(4)]
    for worker in workers:
        worker.start()
    print("Started worker threads")

    try:
        # Add a simple task or directly call application logic for demonstration
        task_queue.put('start')  # Placeholder task
        print("Added a task to the queue")

        # Wait for all workers to finish
        for worker in workers:
            worker.join()
        print("All workers have finished")
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("Terminating workers...")

        # Signal workers to stop
        for _ in workers:
            task_queue.put(None)

        # Wait for all workers to finish
        for worker in workers:
            worker.join()

        print("All workers have terminated.")

if __name__ == "__main__":
    main_logic()
