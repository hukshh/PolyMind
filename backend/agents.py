import os
from crewai import Agent, Task, Crew, Process

class PolyMindCrew:
    def __init__(self, context_str: str = ""):
        self.llm = "groq/llama-3.3-70b-versatile"
        self.context = context_str

    def run(self, query: str):
        # 1. Researcher: Precision Retrieval
        researcher = Agent(
            role='Retrieval Specialist',
            goal=f'Find raw facts from the context for: {query}',
            backstory='You find specific quotes and facts with [Page X] citations. No summarizing.',
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        # 2. Fulfiller: Exact Response
        fulfiller = Agent(
            role='Fulfillment Expert',
            goal=f'Give a direct answer to: {query}',
            backstory="""You fulfill the user's request using the research provided.
            NO PART 1/2/3 headers. No 'Summary' headers.
            If MCQ is asked, give only MCQ.
            Always use [Page X] for facts.
            Tone: Professional and clinical.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        r_task = Task(
            description=f"Find facts for: {query} in {self.context}",
            expected_output="Raw factual nodes with page numbers.",
            agent=researcher
        )

        f_task = Task(
            description=f"Answer the question: {query}. Fulfill the specific format requested. NO TEMPLATES.",
            expected_output="A direct and perfectly formatted response to the query.",
            agent=fulfiller,
            context=[r_task]
        )

        crew = Crew(
            agents=[researcher, fulfiller],
            tasks=[r_task, f_task],
            process=Process.sequential,
            verbose=True
        )

        return str(crew.kickoff())
