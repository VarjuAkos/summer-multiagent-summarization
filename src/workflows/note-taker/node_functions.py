from prompts import NOTE_TAKER_PROMPT, NOTE_APPROVAL_PROMPT, REFLECTION_PROMPT, UPDATE_PROJECT_STATE
from graph import NoteTakerState
from utils import load_markdown_to_str, update_markdown_file
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from  dotenv import load_dotenv
import os

load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
#model = ChatAnthropic(model="claude-3-haiku-20240307", anthropic_api_key=anthropic_api_key)
model = ChatAnthropic(model="claude-3-5-sonnet-20240620", anthropic_api_key=anthropic_api_key, max_tokens= 8192)



def note_taker_node(state: NoteTakerState) -> NoteTakerState:
    formatted_prompt = NOTE_TAKER_PROMPT.format(
      company_data = state.get("company_data"),
      employee_profiles = state.get("employee_profiles"),
      project_general = state.get("project_general"),
      project_requirements = state.get("project_requirements"),
      project_sprint_state = state.get("project_sprint_state"),
      project_backlog = state.get("project_backlog"),
      meeting_history = state.get("meeting_history"),
      transcript = state.get("transcript"),
    )
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content="Generate a meeting note based on the provided information.")
	]
    response = model.invoke(messages)
    state["note_draft"] = response.content
    print(state["note_draft"])
    return state

def note_approvel_node(state: NoteTakerState) -> NoteTakerState:
    formatted_prompt = NOTE_APPROVAL_PROMPT.format(
      company_data = state.get("company_data"),
      employee_profiles = state.get("employee_profiles"),
      project_general = state.get("project_general"),
      project_requirements = state.get("project_requirements"),
      project_sprint_state = state.get("project_sprint_state"),
      project_backlog = state.get("project_backlog"),
      meeting_history = state.get("meeting_history"),
      transcript = state.get("transcript"),
      note_draft = state.get("note_draft")
    )
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content="Validate the node based on the provided information.")
	]
    response = model.invoke(messages)
    if "NOTE CONTAINS FALSE INFO" in response.content:
        state["note_taker_halucinate"] = True
        print(response.content)
    else:
        state["note_taker_halucinate"] = False
        print(response.content)
    return state



def reflection_node(state: NoteTakerState) -> NoteTakerState:
    formatted_prompt = REFLECTION_PROMPT.format(
      company_data = state.get("company_data"),
      employee_profiles = state.get("employee_profiles"),
      project_general = state.get("project_general"),
      project_requirements = state.get("project_requirements"),
      project_sprint_state = state.get("project_sprint_state"),
      project_backlog = state.get("project_backlog"),
      meeting_history = state.get("meeting_history"),
      transcript = state.get("transcript"),
      note_draft = state.get("note_draft")
    )
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content="Make the second version of the draft based on the provided information.")
    ]
    response = model.invoke(messages)

    state["note_after_reflection"] = response.content
    print(state["note_after_reflection"])
    return state


def reflection_approvel_node(state: NoteTakerState) -> NoteTakerState:
    formatted_prompt = NOTE_APPROVAL_PROMPT.format(
      company_data = state.get("company_data"),
      employee_profiles = state.get("employee_profiles"),
      project_general = state.get("project_general"),
      project_requirements = state.get("project_requirements"),
      project_sprint_state = state.get("project_sprint_state"),
      project_backlog = state.get("project_backlog"),
      meeting_history = state.get("meeting_history"),
      transcript = state.get("transcript"),
      note_draft = state.get("note_after_reflection")
    )
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content="Validate the note based on the provided information.")
	]
    response = model.invoke(messages)
    if "NOTE CONTAINS FALSE INFO" in response.content:
        state["note_taker_halucinate"] = True
        print(response.content)
    else:
        state["note_taker_halucinate"] = False
        state["note_final"] = state["note_after_reflection"]
        print(response.content)
    return state



def update_project_state(state: NoteTakerState) -> str:
    formatted_prompt = UPDATE_PROJECT_STATE.format(
        company_data = state.get("company_data"),
		employee_profiles = state.get("employee_profiles"),
		project_general = state.get("project_general"),
		project_requirements = state.get("project_requirements"),
		meeting_history = state.get("meeting_type"),
		note_final = state.get("note_final"),
		project_sprint_state = state.get("project_sprint_state"),
		template = load_markdown_to_str(file_path="../data/company-data/project-sprint-state-template.md"),
	)
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content="Update the state")
	]
    response = model.invoke(messages)
    update_markdown_file(file_path="../data/company-data/current-project-sprint-state.md", new_content=response.content)
    print(response.content)
    return state
	
