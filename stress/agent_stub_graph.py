import time
import uuid

from langgraph.graph import StateGraph
from typing_extensions import TypedDict


from langchain_core.messages import ToolMessage


class AgentState(TypedDict):
    tool_calls: list[ToolMessage]
    done: bool


class StubAgentGraph(StateGraph):
    def __init__(
        self,
        agent_id: int,
        ttl: int,
        mem_mb: int,
        event_logger=None,
        handoff_tool=None,
    ):
        super().__init__(state_schema=AgentState)
        self._agent_name = f"agent-{agent_id}"
        self.agent_id = agent_id
        self.ttl = ttl
        self.mem_mb = mem_mb
        self.event_logger = event_logger
        self.handoff_tool = handoff_tool
        self.state = {"done": False, "tool_calls": []}

        # Define the graph
        self.add_node("run", self.run)
        self.set_entry_point("run")
        self.set_finish_point("run")

    @property
    def name(self):
        return self._agent_name

    def run(self, state: dict):
        """LangGraph node for agent execution"""
        print(f"Agent {self.agent_id} running: {state=}")
        if self.event_logger:
            self.event_logger(
                {
                    "event": "agent_start",
                    "agent_id": self.agent_id,
                    "ttl": self.ttl,
                    "memory": self.mem_mb,
                    "time_sec": time.time(),
                }
            )

        # Consume memory (dummy)
        dummy = bytearray(self.mem_mb * 1024 * 1024)  # noqa

        # Simulate TTL
        time.sleep(self.ttl)

        if self.handoff_tool:
            tool_call = {
                "name": self.handoff_tool.name,
                "args": {},
                "type": "tool_call",
                "id": str(uuid.uuid4()),
            }
            self.state["tool_calls"] = [tool_call]
            return {"tool_calls": [tool_call]}

        if self.event_logger:
            self.event_logger(
                {
                    "event": "agent_stop",
                    "agent_id": self.agent_id,
                    "ttl": self.ttl,
                    "memory": self.mem_mb,
                    "time_sec": time.time(),
                }
            )

        state["done"] = True
        self.state = state
        return {"done": True}

    def get_graph(self):
        return self

    def __call__(self, state, **kwargs):
        return self.compile().invoke(state, **kwargs)

    def compile(self, **kwargs):
        """Compile the graph with default settings if none provided"""
        return super().compile(
            **{
                "checkpointer": None,
                "interrupt_before": None,
                "interrupt_after": None,
                **kwargs,
            }
        )
