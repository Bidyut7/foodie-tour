# main.py
import os
import asyncio
import json
from julep import Client
from config import JULEP_API_KEY, OPENWEATHERMAP_API_KEY, YELP_API_KEY

async def run_foodie_tour_planner():
    os.environ["JULEP_API_KEY"] = JULEP_API_KEY
    client = Client(api_key=JULEP_API_KEY)

    os.environ["OPENWEATHERMAP_API_KEY"] = OPENWEATHERMAP_API_KEY
    os.environ["YELP_API_KEY"] = YELP_API_KEY

    print("Syncing Julep project from local YAML files...")
    print("Checking for FoodieTourAgent...")
    try:
        agent = await client.agents.get_by_name("FoodieTourAgent")
        print(f"Using existing agent: {agent.name} (ID: {agent.id})")
    except Exception:
        print("Agent not found. Please run 'julep sync' from your terminal first or ensure agent.yaml is correct.")
        print("Attempting to create Agent via SDK (less ideal for structured projects):")
        agent = await client.agents.create(
            name="FoodieTourAgent",
            about="An expert AI dedicated to crafting personalized foodie tours based on weather and local cuisine.",
            model="gpt-4o"
        )
        print(f"Agent '{agent.name}' created with ID: {agent.id}. Please run 'julep sync' next time.")

    print("Ensuring tools are configured with the agent...")
    try:
        await client.agents.tools.get_by_name(agent.id, "weather_tool")
        print("Weather tool exists.")
    except Exception:
        print("Weather tool not found for agent. Creating...")
        await client.agents.tools.create(
            agent_id=agent.id,
            name="weather_tool",
            type="integration",
            integration={
                "provider": "weather",
                "setup": {} 
            },
            description="Fetches current weather information for a given location."
        )

    try:
        await client.agents.tools.get_by_name(agent.id, "restaurant_search_tool")
        print("Restaurant search tool exists.")
    except Exception:
        print("Restaurant search tool not found for agent. Creating...")
        await client.agents.tools.create(
            agent_id=agent.id,
            name="restaurant_search_tool",
            type="api_call",
            api_call={
                "url": "https://api.yelp.com/v3/businesses/search",
                "method": "GET",
                "headers": {
                    "Authorization": f"Bearer {YELP_API_KEY}"
                },
                "query_params": {
                    "term": "{query}",
                    "location": "{location}",
                    "categories": "food",
                    "limit": 5,
                    "sort_by": "rating"
                }
            },
            description="Searches for restaurants using Yelp Fusion API."
        )

    print("Checking for MultiCityFoodieTourPlanner task...")
    try:
        task = await client.tasks.get_by_name("MultiCityFoodieTourPlanner")
        print(f"Using existing task: {task.name} (ID: {task.id})")
    except Exception:
        print("Task not found. Please run 'julep sync' from your terminal first or ensure task.yaml is correct.")
        print("Attempting to create Task via SDK (less ideal for structured projects):")
        import yaml
        with open("src/tasks/foodie_tour_task.yaml", "r") as f:
            task_definition = yaml.safe_load(f)
        task = await client.tasks.create(
            agent_id=agent.id,
            **task_definition
        )
        print(f"Task '{task.name}' created with ID: {task.id}. Please run 'julep sync' next time.")

    print("\n--- Starting Foodie Tour Planning ---")
    cities_to_tour = ["New York", "London", "Tokyo", "Paris"] 
    execution = await client.tasks.execute(
        task_id=task.id,
        inputs={"cities": cities_to_tour}
    )

    print(f"Task execution started. Execution ID: {execution.id}")
    print("Monitoring execution status... (This might take a while)")

    while execution.status not in ["completed", "failed"]:
        await asyncio.sleep(10)
        execution = await client.executions.get(execution.id)
        print(f"Current status: {execution.status} (Current step: {execution.current_step_name or 'N/A'})")

    if execution.status == "completed":
        print("\n--- Foodie Tour Generated Successfully! ---")
        final_report = execution.output.get("final_foodie_tour_report")
        if final_report:
            print("\n" + final_report)
        else:
            print("Final report output key not found in execution results.")
            print("Full execution output for debugging:")
            print(json.dumps(execution.output, indent=2))
    else:
        print(f"\n--- Foodie Tour Generation Failed! ---")
        print(f"Error: {execution.error_message}")
        print(f"Last successful step: {execution.current_step_name}")
        print("Full error details (if available):")
        print(json.dumps(execution.output, indent=2))

if __name__ == "__main__":
    asyncio.run(run_foodie_tour_planner())