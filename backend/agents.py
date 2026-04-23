import os
from crewai import Agent, Task, Crew, Process

class PolyMindCrew:
    def __init__(self, context: str = ""):
        self.llm = "groq/llama-3.3-70b-versatile"
        self.context = context

    def run(self, query: str):
        # 1. Fact Extraction Specialist: Precision Retrieval
        researcher = Agent(
            role='Fact Extraction Specialist',
            goal=f'Extract unique, factual nodes from the provided context for: {query}',
            backstory="""You are an expert at scanning documents for specific data points.
            Extract every relevant fact, quote, or data node that helps answer the query.
            Include the source [Page X] for every node.
            Do not summarize or add your own opinion. Just the raw factual data.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        # 2. Senior Research Analyst: Synthesis & Final Response
        fulfiller = Agent(
            role='Senior Research Analyst',
            goal=f'Synthesize the research into a coherent, unique response for: {query}',
            backstory="""You are a senior analyst known for clarity and precision. 
            Your job is to take raw research notes and transform them into a polished final answer.
            
            STRICT RULES:
            1. NEVER repeat the same fact or citation twice.
            2. If multiple sources say the same thing, group them together (e.g., 'X and Y are mentioned on [Page 13, Page 15]').
            3. If asked for a summary, provide a thematic overview, not a list of fragments.
            4. If asked for MCQs, ensure each question covers a DIFFERENT concept. Format them elegantly:
               - Use bold for the Question.
               - Use bullet points for the options (A, B, C, D).
               - Use a blockquote or bold text for the Answer.
               - Separate each MCQ with a horizontal rule (---).
            5. Always use [Page X] for facts.
            6. Tone: Professional, clinical, and direct.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        r_task = Task(
            description=f"Analyze the following context and extract unique facts for the query: '{query}'. \n\nCONTEXT:\n{self.context}",
            expected_output="A list of unique factual nodes with page citations. No repetition.",
            agent=researcher
        )

        f_task = Task(
            description=f"Using the extracted facts, provide a direct answer to: '{query}'. Ensure the response is synthesized and avoids any redundant information.",
            expected_output="A synthesized, professional, and cited response. NO REPETITION.",
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

