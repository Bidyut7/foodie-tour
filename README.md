# Foodie Tour Planner with Julep.ai

This project leverages Julep.ai to create delightful one-day "foodie tours" for a list of specified cities. It dynamically fetches weather information, identifies iconic local dishes, finds top-rated restaurants, and crafts engaging narratives for breakfast, lunch, and dinner, factoring in weather conditions.

## Directory Structure
├── README.md                 # Documentation and usage instructions
├── julep.yaml                # Project configuration and entrypoint
├── julep-lock.json (generated)# Lock file tracking server state (ignored by Git)
├── config.py (ignored)       # Stores API keys (ignored by Git)
├── venv/ (ignored)           # Python virtual environment
├── main.py                   # Python script to orchestrate Julep workflow
└── src/                      # Source directory for Julep definitions
├── agents/               # Agent definitions
│   └── agent.yaml
├── tasks/                # Task definitions
│   └── foodie_tour_task.yaml
└── tools/                # Tool definitions
├── weather_tool.yaml
└── yelp_restaurant_search_tool.yaml

## Features

-   **Weather-Aware Planning:** Checks current weather to suggest indoor or outdoor dining.
-   **Local Dish Discovery:** Identifies 3 iconic local dishes for each city.
-   **Top Restaurant Finder:** Locates highly-rated restaurants serving these iconic dishes.
-   **Delightful Itinerary Generation:** Crafts engaging narratives for breakfast, lunch, and dinner, incorporating weather and specific dining recommendations.
-   **Multi-City Support:** Processes a list of cities to generate comprehensive tour plans.

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/foodie-tour-julep-structured.git](https://github.com/YOUR_USERNAME/foodie-tour-julep-structured.git)
    cd foodie-tour-julep-structured
    ```

2.  **Install Prerequisites:**
    * **Node.js & npm:** If not installed: `brew install node`
    * **Julep CLI:** `npm install -g julep-ai`
    * **Python 3:** Ensure Python 3.9+ is installed: `brew install python` (if needed)

3.  **Create and Activate Python Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install Python Dependencies:**
    ```bash
    pip install julep-ai pyyaml
    ```

5.  **Obtain API Keys:**
    * **Julep.ai API Key:** Sign up at [julep.ai](https://julep.ai) and get your key from the dashboard.
    * **OpenWeatherMap API Key:** Sign up at [openweathermap.org](https://openweathermap.org) and get your key.
    * **Yelp Fusion API Key:** Sign up at [yelp.com/developers](https://www.yelp.com/developers) and create an app to get your key.

6.  **Configure `config.py`:**
    Create a file named `config.py` in the root of the project (`foodie-tour-julep-structured/`).
    Add your API keys to this file:

    ```python
    # config.py
    JULEP_API_KEY = "YOUR_JULEP_API_KEY"
    OPENWEATHERMAP_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
    YELP_API_KEY = "YOUR_YELP_API_KEY"
    ```
    **Important:** Replace `"YOUR_API_KEY"` placeholders with your actual keys. This file is ignored by Git for security.

## Usage

1.  **Sync Julep Project Definitions:**
    First, you need to sync your local Julep YAML definitions with the Julep platform. This creates/updates your agent, tasks, and tools on the Julep server.
    Ensure your virtual environment is active (`(venv)` in your terminal prompt) and run:

    ```bash
    julep sync
    ```
    * You might be prompted to log in to Julep if this is your first time using the CLI.
    * A `julep-lock.json` file will be created in your root, tracking the synced state (it's in `.gitignore`).

2.  **Run the Foodie Tour Planner:**
    Once synced, execute the main Python script:

    ```bash
    python main.py
    ```
    The script will print progress updates and the final foodie tour itineraries in your terminal.

## Debugging and Monitoring

* **Julep.ai Dashboard:** For detailed execution logs, step-by-step inputs/outputs, and error tracing, visit your Julep.ai dashboard. Navigate to "Executions" to see your task runs.
* **Terminal Output:** The `main.py` script provides real-time status updates and prints the final generated report.
* **Prompt Engineering:** If the generated content (e.g., dish suggestions, narratives) isn't satisfactory, refine the prompts in `src/tasks/foodie_tour_task.yaml`.

---