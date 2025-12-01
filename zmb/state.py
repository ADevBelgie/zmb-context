import json
import os
import logging

STATE_FILE = 'zmb_state.json'

class State:
    def __init__(self):
        self.logger = logging.getLogger('ZMB_STATE')
        self.data = self._load_state()

    def _load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                self.logger.error("Failed to decode state file. Resetting.")
                return self._default_state()
        else:
            return self._default_state()

    def _default_state(self):
        return {
            "phase": "Bootstrapping",
            "active_tasks": [],
            "completed_tasks": [],
            "history": []
        }

    def save(self):
        with open(STATE_FILE, 'w') as f:
            json.dump(self.data, f, indent=4)

    def update_phase(self, phase):
        self.data['phase'] = phase
        self.save()

    def add_task(self, task):
        self.data['active_tasks'].append(task)
        self.save()

    def complete_task(self, task):
        if task in self.data['active_tasks']:
            self.data['active_tasks'].remove(task)
            self.data['completed_tasks'].append(task)
            self.save()
