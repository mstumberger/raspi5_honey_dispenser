import concurrent.futures


class GPIOExecutor:
    """This class delegates the event handling to the EventHandler class."""

    def __init__(self, delegate):
        # The delegate is passed as a parameter (can be set or changed dynamically)
        self.delegate = delegate
        # Thread pool executor with 2 threads
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def trigger_event(self, event):
        # Delegate the handling of the event asynchronously using a thread pool
        print(f"Event triggered: {event}, delegating to handler in a separate thread...")
        self.executor.submit(self.delegate.handle_event, event)

    def shutdown(self):
        """Shut down the thread pool executor gracefully."""
        self.executor.shutdown(wait=True)
