import random
from models.observation import Observation

class APIEnv:

    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty
        self.reset_state()

    def reset_state(self):
        self.state = {
            "pending_tasks": ["auth", "payment", "notify"],
            "completed_tasks": [],
            "failures": 0,
            "step_count": 0,
            "last_error": None,
            "api_status": {
                "auth_api": "healthy",
                "payment_api": "unstable" if self.difficulty != "easy" else "healthy",
                "notify_api": "healthy"
            }
        }

    async def reset(self):
        self.reset_state()
        return self._get_obs()

    async def step(self, action):
        self.state["step_count"] += 1
        # handle dict input
        if isinstance(action, dict):
            action = action.get("action", "")

        # clean action string
        action = action.strip().lower()

        if action == "call_auth_api":
            reward = self._handle_success("auth", 0.2)

        elif action == "call_payment_api":
            if "auth" not in self.state["completed_tasks"]:
                self.state["last_error"] = "auth_required"
                reward = -0.3
            else:
                reward = self._handle_payment()

        elif action == "call_notify_api":
            if "payment" not in self.state["completed_tasks"]:
                self.state["last_error"] = "payment_required"
                reward = -0.1
            else:
                reward = self._handle_success("notify", 0.2)

        elif action == "retry":
            if self.state["last_error"]:
                reward = 0.2
                self.state["last_error"] = None
            else:
                reward = -0.1

        elif action == "abort":
            return self._terminate(-0.5)

        else:
            reward = -0.2
            self.state["last_error"] = "invalid_action"

        done = len(self.state["completed_tasks"]) == 3

        return {
            "observation": self._get_obs(),
            "reward": reward,
            "done": done,
            "info": {}
        }

    def _handle_success(self, task, reward):
        if task not in self.state["completed_tasks"]:
            self.state["completed_tasks"].append(task)
            self.state["pending_tasks"].remove(task)
            self.state["last_error"] = None
            return reward
        else:
            self.state["last_error"] = "already_completed"
            return -0.1
        return 0  # IMPORTANT: no penalty for repeat

    def _handle_payment(self):
        fail_prob = 0.0 if self.difficulty == "easy" else 0.6

        if random.random() < fail_prob:
            self.state["failures"] += 1
            self.state["last_error"] = "payment_failed"
            return -0.2

        return self._handle_success("payment", 0.4)

    def _terminate(self, reward):
        return {
            "observation": self._get_obs(),
            "reward": reward,
            "done": True,
            "info": {}
        }

    def _get_obs(self):
        return Observation(**self.state).dict()
    
    async def close(self):
        return
