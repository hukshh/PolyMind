from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
import os

class PolyMindCrew:
    def __init__(self, context: str):
        self.llm = ChatGroq(
            model_name="llama3-70b-8192", 
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.7
        )
        self.context = context

    def setup_agents(self):
        self.researcher = Agent(
            role='Researcher',
            goal='Extract precise information from the provided context.',
            backstory='You are an expert at scanning documents and finding specific details to answer complex questions.',
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        self.summarizer = Agent(
            role='Summarizer',
            goal='Condense information into a clear, concise, and smart answer.',
            backstory='You specialize in taking complex research notes and turning them into executive summaries.',
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        self.critic = Agent(
            role='Critic',
            goal='Identify gaps, hallucinations, or inconsistencies in the answer.',
            backstory='You have a sharp eye for detail and ensure all claims are backed by the provided research.',
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        self.recommender = Agent(
            role='Recommender',
            goal='Suggest 2-3 related sections or topics from the document for further exploration.',
            backstory='You are great at connecting dots and suggesting what the user should read next.',
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def run(self, query: str):
        self.setup_agents()

        research_task = Task(
            description=f"Using the context below, find all relevant information to answer the question: {query}\n\nContext: {self.context}",
            agent=self.researcher,
            expected_output="Detailed notes covering all aspects of the query based ONLY on the context."
        )

        summary_task = Task(
            description="Summarize the research notes into a smart, cited answer. Mention source citations (Page/URL) where possible.",
            agent=self.summarizer,
            context=[research_task],
            expected_output="A polished answer with inline citations."
        )

        critique_task = Task(
            description="Review the summary for accuracy and gaps. If something is missing or seems like a hallucination, point it out.",
            agent=self.critic,
            context=[summary_task],
            expected_output="A review report or a confirmation that the answer is accurate."
        )

        recommendation_task = Task(
            description="Based on the query and research, suggest 2-3 related sections or concepts the user might find interesting.",
            agent=self.recommender,
            context=[research_task],
            expected_output="A list of 2-3 recommendations."
        )

        crew = Crew(
            agents=[self.researcher, self.summarizer, self.critic, self.recommender],
            tasks=[research_task, summary_task, critique_task, recommendation_task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return result
