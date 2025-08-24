import os
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	SerperDevTool,
	BraveSearchTool
)



@CrewBase
class SmartCarBuyingAssistantCrew:
    """SmartCarBuyingAssistant crew"""

    
    @agent
    def car_buying_requirements_analyst(self) -> Agent:
        
        return Agent(
            config=self.agents_config["car_buying_requirements_analyst"],
            tools=[

            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
        )
    
    @agent
    def car_market_research_specialist(self) -> Agent:
        
        return Agent(
            config=self.agents_config["car_market_research_specialist"],
            tools=[
				SerperDevTool(),
				BraveSearchTool()
            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
        )
    
    @agent
    def interstate_car_purchase_legal_advisor(self) -> Agent:
        
        return Agent(
            config=self.agents_config["interstate_car_purchase_legal_advisor"],
            tools=[
				SerperDevTool()
            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
        )
    
    @agent
    def vehicle_valuation_expert(self) -> Agent:
        
        return Agent(
            config=self.agents_config["vehicle_valuation_expert"],
            tools=[
				SerperDevTool()
            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
        )
    
    @agent
    def car_purchase_negotiation_strategist(self) -> Agent:
        
        return Agent(
            config=self.agents_config["car_purchase_negotiation_strategist"],
            tools=[
				SerperDevTool()
            ],
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
            tools=[
				SerperDevTool()
            ],
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
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
