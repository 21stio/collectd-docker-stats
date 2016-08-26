import threading
import json
import time


class ContainerStatsStream(threading.Thread):

    def __init__(self, dockerClient, container_name):
        threading.Thread.__init__(self)
        self.daemon = True
        self.stop = False

        self.running = True
        self._container_name = container_name
        self._dockerClient = dockerClient
        self._stream = None
        self._stats = None

        self.start()

    def run(self):
        failures = 0
        while self.running:
            try:
                if not self._stream:
                    self._stream = self._dockerClient.stats(self._container_name)
                self._stats = self._stream.next()

                failures = 0
            except Exception:
                failures += 1
                if failures > 10:
                    self.running = False

                self._stream = None

                time.sleep(1)

    def get_stats(self):
        sleep = 0.1
        slept = 0
        while self._stats is None and slept < 3:
            slept += sleep
            time.sleep(sleep)

        if self._stats:
            return json.loads(self._stats)

        return {}
