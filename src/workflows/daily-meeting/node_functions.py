from prompts import GENERAL_INFO_EXTRACTOR_PROMPT, PERSONAL_TASK_EXTRACTOR_PROMPT, DIAGRAM_GENERATOR_PROMPT, REPORT_COMPILER_PROMPT, MOTIVATIONAL_MESSAGE_PROMPT
from graph import DailyState
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from  dotenv import load_dotenv
from utils.functions import render_mermaid_diagram, format_mermaid
import os

load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
#model = ChatAnthropic(model="claude-3-haiku-20240307", anthropic_api_key=anthropic_api_key)
model = ChatAnthropic(model="claude-3-5-sonnet-20240620", anthropic_api_key=anthropic_api_key, max_tokens=4096)


def general_info_extractor_node(state: DailyState) -> DailyState:
    formatted_prompt = GENERAL_INFO_EXTRACTOR_PROMPT.format(
        note=state["note"]
    )
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content="Extract the general information from the daily scrum note.")
    ]
    response = model.invoke(messages)
    state["general_info"] = response.content
    return state



def personal_task_extractor_node(state: DailyState) -> DailyState:
    for employee, profile in state["employee_profiles"].items():
        formatted_prompt = PERSONAL_TASK_EXTRACTOR_PROMPT.format(
            note=state["note"],
            employee_profile=profile,
            project_sprint_state = state.get("project_sprint_state"),
            project_backlog = state.get("project_backlog")


        )
        messages = [
            SystemMessage(content=formatted_prompt),
            HumanMessage(content=f"Extract personal tasks for {employee}.")
        ]
        response = model.invoke(messages)
        state["personal_tasks"][employee] = response.content
    return state


def diagram_generator_node(state: DailyState) -> DailyState:
    for employee, tasks in state["personal_tasks"].items():
        formatted_prompt = DIAGRAM_GENERATOR_PROMPT.format(
            note = state.get("note"),
			personal_tasks=tasks
        )
        messages = [
            SystemMessage(content=formatted_prompt),
            HumanMessage(content=f"Generate a Mermaid diagram for {employee}'s tasks.")
        ]
        response = model.invoke(messages)
        state["diagrams"][employee] = response.content
    return state




def report_compiler_node(state: DailyState) -> DailyState:
    for employee in state["employee_profiles"].keys():
        rendered_diagram = render_mermaid_diagram(format_mermaid(state["diagrams"][employee]))
        print(format_mermaid(state["diagrams"][employee]))
        print("ÁÁÁÁ", rendered_diagram)

        formatted_prompt = REPORT_COMPILER_PROMPT.format(
            general_info=state["general_info"],
            personal_tasks=state["personal_tasks"][employee],
            diagram=rendered_diagram
        )
        messages = [
            SystemMessage(content=formatted_prompt),
            HumanMessage(content=f"Compile a personalized report for {employee}.")
        ]
        response = model.invoke(messages)
        state["reports"][employee] = response.content
    return state


def motivational_message_node(state: DailyState) -> DailyState:
    for employee, profile in state["employee_profiles"].items():
        formatted_prompt = MOTIVATIONAL_MESSAGE_PROMPT.format(
            employee_profile=profile
        )
        messages = [
            SystemMessage(content=formatted_prompt),
            HumanMessage(content=f"Generate a motivational message for {employee}.")
        ]
        response = model.invoke(messages)
        state["reports"][employee] += f"\n\n{response.content}"
    return state