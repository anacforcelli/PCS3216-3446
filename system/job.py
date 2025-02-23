import time
import enum
import logging

logger = logging.getLogger(__name__)

JobState = enum.Enum('JobState', 'SUBMIT WAIT_RESOURCES READY RUNNING WAIT_IO DONE')
JobPriority = enum.IntEnum('JobPriority', 'LOW NORMAL HIGH CRITICAL')

class Job:
    def __init__(self, _id, execution_time, priority=JobPriority.NORMAL, io=(False, 0, 0)):
        self.id = _id
        self.total_cycles = execution_time
        self.priority = priority

        self.arrive_time = 0
        self.start_time = 0
        self.current_cycle = 0
        self._state = JobState.SUBMIT

        self.io = io

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, st):
        if self._state != JobState.DONE:
            self._state = st

    def __str__(self):
        return str(self.id)

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __eq__(self, other):
        return self.id == other.id

    def cycle(self):
        self.current_cycle += 1
        logger.info(f'Job {self.id} rodando ({self.current_cycle}/{self.total_cycles} ciclos).')
        if self.current_cycle == self.total_cycles:
            self.state = JobState.DONE
