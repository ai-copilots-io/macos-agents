# python 3.13 samples

```python

#!/usr/bin/env python3
"""MacOS Agents - A multi-agent system for executing tasks on macOS."""

from typing import Any, Self, Never, assert_type
from dataclasses import dataclass
from functools import cache
import asyncio
import sys


# PEP 695 type alias definition
type CommandResult = dict[str, Any]
type AgentID = str


class CommandError(Exception):
    """Base exception for command execution errors."""
    pass


# PEP 695 generic type alias
type EventHandler[T] = callable[[T], None]


@dataclass(frozen=True)  # Make dataclass hashable for caching
class Agent:
    """Base class for all MacOS agents."""
    
    id: AgentID
    name: str
    
    async def execute(self, command: str) -> CommandResult:
        """Execute a command on the system."""
        # PEP 702 f-string shorthand
        print(f"{self.name=} executing {command=}")
        
        try:
            result = await self._run_command(command)
            return {"status": "success", "result": result}
        except Exception as e:
            # Fixed for Python 3.13 compatibility
            return {"status": "error", "errors": [str(e)]}
    
    async def _run_command(self, command: str) -> str:
        """Run the actual command implementation."""
        # Placeholder for actual implementation
        return f"Executed: {command}"


class SystemAgent(Agent):
    """Agent for system-level operations."""
    
    def __init__(self) -> None:
        # Use object.__setattr__ for frozen dataclass
        object.__setattr__(self, "id", "system")
        object.__setattr__(self, "name", "System Agent")


# Static method with cache
@cache
def get_system_info() -> dict[str, str]:
    """Get system information."""
    return {
        "os": "macOS",
        "version": "14.0",
        "python": sys.version
    }


# Demonstration of match statement
async def process_result(result: CommandResult) -> None:
    """Process a command result."""
    match result:
        case {"status": "success", "result": value}:
            print(f"Success: {value}")
        case {"status": "error", "errors": errors}:
            print(f"Failed with {len(errors)} errors:")
            for error in errors:
                print(f"  - {error}")
        case _:
            print("Unknown result format")


async def main() -> None:
    """Main entry point for the application."""
    agent = SystemAgent()
    
    # Type checking demonstration
    assert_type(agent.id, AgentID)
    
    # Run a simple command
    result = await agent.execute("ls -la")
    await process_result(result)
    
    # Show system info
    sys_info = get_system_info()
    print("\nSystem Information:")
    for key, value in sys_info.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())
```