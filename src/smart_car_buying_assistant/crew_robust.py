import os
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class SmartCarBuyingAssistantCrewRobust:
    """Robust SmartCarBuyingAssistant crew that handles missing API keys gracefully"""

    def _get_tools_for_agent(self, agent_name):
        """Get tools for an agent, with fallbacks for missing API keys"""
        tools = []
        
        # Check if search API keys are available
        serper_key = os.getenv('SERPER_API_KEY')
        brave_key = os.getenv('BRAVE_API_KEY')
        
        if serper_key and brave_key:
            # Both keys available - use full search capabilities
            try:
                from crewai_tools import SerperDevTool, BraveSearchTool
                if agent_name in ['car_market_research_specialist']:
                    tools = [SerperDevTool(), BraveSearchTool()]
                elif agent_name in ['interstate_car_purchase_legal_advisor', 'vehicle_valuation_expert', 'car_purchase_negotiation_strategist']:
                    tools = [SerperDevTool()]
                print(f"✅ Using full search tools for {agent_name}")
            except ImportError:
                print(f"⚠️  Search tools not available for {agent_name}")
        elif brave_key:
            # Only Brave key available
            try:
                from crewai_tools import BraveSearchTool
                if agent_name in ['car_market_research_specialist']:
                    tools = [BraveSearchTool()]
                print(f"✅ Using Brave search for {agent_name}")
            except ImportError:
                print(f"⚠️  Brave search tool not available for {agent_name}")
        else:
            # No search keys available - use no tools
            print(f"⚠️  No search API keys available for {agent_name}, using knowledge-based responses")
        
        return tools

    @agent
    def car_buying_requirements_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["car_buying_requirements_analyst"],
            tools=[],  # No tools needed for requirements analysis
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
        )
    
    @agent
    def car_market_research_specialist(self) -> Agent:
        tools = self._get_tools_for_agent('car_market_research_specialist')
        return Agent(
            config=self.agents_config["car_market_research_specialist"],
            tools=tools,
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
        )
    
    @agent
    def interstate_car_purchase_legal_advisor(self) -> Agent:
        tools = self._get_tools_for_agent('interstate_car_purchase_legal_advisor')
        return Agent(
            config=self.agents_config["interstate_car_purchase_legal_advisor"],
            tools=tools,
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
        )
    
    @agent
    def vehicle_valuation_expert(self) -> Agent:
        tools = self._get_tools_for_agent('vehicle_valuation_expert')
        return Agent(
            config=self.agents_config["vehicle_valuation_expert"],
            tools=tools,
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
        )
    
    @agent
    def car_purchase_negotiation_strategist(self) -> Agent:
        tools = self._get_tools_for_agent('car_purchase_negotiation_strategist')
        return Agent(
            config=self.agents_config["car_purchase_negotiation_strategist"],
            tools=tools,
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
        )
    
    @agent
    def vehicle_inspection_coordinator(self) -> Agent:
        return Agent(
            config=self.agents_config["vehicle_inspection_coordinator"],
            tools=[],  # No tools needed for inspection planning
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
        )

    @task
    def collect_car_buying_requirements(self) -> Task:
        return Task(
            config=self.tasks_config["collect_car_buying_requirements"],
        )
    
    @task
    def research_vehicle_market(self) -> Task:
        return Task(
            config=self.tasks_config["research_vehicle_market"],
        )
    
    @task
    def analyze_legal_requirements(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_legal_requirements"],
        )
    
    @task
    def evaluate_vehicle_values(self) -> Task:
        return Task(
            config=self.tasks_config["evaluate_vehicle_values"],
        )
    
    @task
    def develop_negotiation_strategies(self) -> Task:
        return Task(
            config=self.tasks_config["develop_negotiation_strategies"],
        )
    
    @task
    def create_inspection_plan(self) -> Task:
        return Task(
            config=self.tasks_config["create_inspection_plan"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SmartCarBuyingAssistant crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
