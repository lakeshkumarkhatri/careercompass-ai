# Architecture

## Folder Structure
- `api/`: API route handlers
- `agents/`: AI logic (inherits from `BaseAgent`)
- `services/`: Core logic (PDF extraction, Gemini, User Profiles)
- `models/`: Pydantic data schemas
- `core/`: Application core (logging, configuration)
- `data/`: Persistent storage (JSON)

## Request Flow
1. API receives request -> Service/Agent.
2. If Agent: `BaseAgent` handles prompt loading and Gemini API communication.
3. Orchestrator: Invokes specialist agents and aggregates result.

## Agent Responsibilities
- `BaseAgent`: Prompt loading, JSON parsing, logging, error handling.
- Specialist Agents: Business logic via Gemini.
- Orchestrator: Coordinates workflow, executive summary.
