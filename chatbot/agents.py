import os
from typing import TypedDict, Dict, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, MessagesState
from datetime import datetime
from django.conf import settings

class SupervisorState(MessagesState):
    """State for the multi-agent system"""
    next_agent: str
    research_data: str
    analysis: str
    final_report: str
    task_complete: bool
    current_task: str

class MultiAgentSystem:
    def __init__(self):
        # Initialize the LLM Model with correct Groq model
        self.llm = ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model_name="llama3-8b-8192"  # Use correct Groq model name
        )

    def supervisor_agent(self, state: SupervisorState) -> Dict:
        """Supervisor decides which agent should work next"""

        # Extract task from messages if not in state
        if not state.get("current_task"):
            messages = state.get("messages", [])
            if messages:
                # Get the latest human message as the task
                for msg in reversed(messages):
                    if isinstance(msg, HumanMessage):
                        current_task = msg.content
                        break
                else:
                    current_task = "No specific task provided"
            else:
                current_task = "No task specified"
        else:
            current_task = state["current_task"]

        # Check current state
        has_research = bool(state.get("research_data"))
        has_analysis = bool(state.get("analysis"))
        has_report = bool(state.get("final_report"))
        task_complete = state.get("task_complete", False)

        # Decision logic
        if task_complete or has_report:
            next_agent = "end"
            supervisor_message = "🎯 Supervisor: Task completed successfully!"
        elif not has_research:
            next_agent = "researcher"
            supervisor_message = f"🎯 Supervisor: Starting research phase for: {current_task}"
        elif not has_analysis:
            next_agent = "analyst"
            supervisor_message = "🎯 Supervisor: Moving to analysis phase"
        elif not has_report:
            next_agent = "writer"
            supervisor_message = "🎯 Supervisor: Creating final report"
        else:
            next_agent = "end"
            supervisor_message = "🎯 Supervisor: All phases complete"

        return {
            "messages": [AIMessage(content=supervisor_message)],
            "next_agent": next_agent,
            "current_task": current_task
        }

    def researcher_agent(self, state: SupervisorState) -> Dict:
        """Researcher uses Groq to gather information"""

        task = state.get("current_task", "research topic")

        # Create research prompt
        research_prompt = f"""As a research specialist, provide comprehensive information about: {task}

        Include:
        1. Key facts and background
        2. Current trends or developments
        3. Important statistics or data points
        4. Notable examples or case studies

        Be concise but thorough."""

        # Get research from LLM
        try:
            research_response = self.llm.invoke([HumanMessage(content=research_prompt)])
            research_data = research_response.content
        except Exception as e:
            research_data = f"Research error: {str(e)}"

        # Create agent message
        agent_message = f"🔍 Researcher: I've completed the research on '{task}'.\n\nKey findings:\n{research_data[:500]}..."

        return {
            "messages": [AIMessage(content=agent_message)],
            "research_data": research_data,
            "next_agent": "supervisor"
        }

    def analyst_agent(self, state: SupervisorState) -> Dict:
        """Analyst uses Groq to analyze the research"""

        research_data = state.get("research_data", "")
        task = state.get("current_task", "")

        # Create analysis prompt
        analysis_prompt = f"""As a data analyst, analyze this research data and provide insights:

    Research Data:
    {research_data}

    Provide:
    1. Key insights and patterns
    2. Strategic implications
    3. Risks and opportunities
    4. Recommendations

    Focus on actionable insights related to: {task}"""

        # Get analysis from LLM
        try:
            analysis_response = self.llm.invoke([HumanMessage(content=analysis_prompt)])
            analysis = analysis_response.content
        except Exception as e:
            analysis = f"Analysis error: {str(e)}"

        # Create agent message
        agent_message = f"📊 Analyst: I've completed the analysis.\n\nTop insights:\n{analysis[:400]}..."

        return {
            "messages": [AIMessage(content=agent_message)],
            "analysis": analysis,
            "next_agent": "supervisor"
        }

    def writer_agent(self, state: SupervisorState) -> Dict:
        """Writer uses Groq to create final report"""

        research_data = state.get("research_data", "")
        analysis = state.get("analysis", "")
        task = state.get("current_task", "")

        # Create writing prompt
        writing_prompt = f"""As a professional writer, create an executive report based on:

    Task: {task}

    Research Findings:
    {research_data[:1000]}

    Analysis:
    {analysis[:1000]}

    Create a well-structured report with:
    1. Executive Summary
    2. Key Findings
    3. Analysis & Insights
    4. Recommendations
    5. Conclusion

    Keep it professional and concise."""

        # Get report from LLM
        try:
            report_response = self.llm.invoke([HumanMessage(content=writing_prompt)])
            report = report_response.content
        except Exception as e:
            report = f"Report generation error: {str(e)}"

        # Create final formatted report
        final_report = f"""
📄 FINAL REPORT
{'='*50}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Topic: {task}
{'='*50}

{report}

{'='*50}
Report compiled by Multi-Agent AI System powered by Groq
"""

        return {
            "messages": [AIMessage(content=f"✍️ Writer: Report complete! See below for the full document.")],
            "final_report": final_report,
            "next_agent": "supervisor",
            "task_complete": True
        }

    def router(self, state: SupervisorState) -> Literal["supervisor", "researcher", "analyst", "writer", "__end__"]:
        """Routes to next agent based on state"""

        next_agent = state.get("next_agent", "supervisor")

        if next_agent == "end" or state.get("task_complete", False):
            return "__end__"

        if next_agent in ["supervisor", "researcher", "analyst", "writer"]:
            return next_agent

        return "supervisor"

    def create_workflow(self):
        """Create and compile the workflow"""
        # Create workflow
        workflow = StateGraph(SupervisorState)

        # Add nodes
        workflow.add_node("supervisor", self.supervisor_agent)
        workflow.add_node("researcher", self.researcher_agent)
        workflow.add_node("analyst", self.analyst_agent)
        workflow.add_node("writer", self.writer_agent)

        # Set entry point
        workflow.set_entry_point("supervisor")

        # Add routing
        for node in ["supervisor", "researcher", "analyst", "writer"]:
            workflow.add_conditional_edges(
                node,
                self.router,
                {
                    "supervisor": "supervisor",
                    "researcher": "researcher",
                    "analyst": "analyst",
                    "writer": "writer",
                    "__end__": "__end__"
                }
            )

        # Compile the graph
        return workflow.compile()

    def execute_workflow(self, task: str):
        """Execute the multi-agent workflow"""
        graph = self.create_workflow()

        response = graph.invoke({
            "messages": [HumanMessage(content=task)],
            "current_task": task,
            "next_agent": "supervisor",
            "research_data": "",
            "analysis": "",
            "final_report": "",
            "task_complete": False
        })

        return response