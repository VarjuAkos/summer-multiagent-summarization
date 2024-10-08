from workflows.update_state.prompts import MEETING_NOTE_ANALYZER_PROMPT, PROJECT_STATE_UPDATER_PROMPT, BACKLOG_MANAGER_PROMPT, SPRINT_STATE_UPDATER_PROMPT, SPRINT_BACKLOG_UPDATER_PROMPT
from workflows.update_state.state import ProjectUpdateState
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from  dotenv import load_dotenv
import os
import json


load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
#model = ChatAnthropic(model="claude-3-haiku-20240307", anthropic_api_key=anthropic_api_key)
model = ChatAnthropic(model="claude-3-5-sonnet-20240620", anthropic_api_key=anthropic_api_key, max_tokens= 8192)




def meeting_note_analyzer_node(state: ProjectUpdateState) -> ProjectUpdateState:
        formatted_prompt = MEETING_NOTE_ANALYZER_PROMPT.format(
            company_data=state["company_data"],
            project_general=state["project_general"],
            project_requirements=state["project_requirements"],
            employee_profiles=state["employee_profiles"],
            meeting_history=state["meeting_history"],
            meeting_type=state["meeting_type"],
            meeting_note=state["meeting_note"]
        )
        messages = [
            SystemMessage(content=formatted_prompt),
            HumanMessage(content="Analyze the meeting note and extract key information.")
        ]
        response = model.invoke(messages)
        state["meeting_analysis"] = response.content
        return state

def project_state_updater_node(state: ProjectUpdateState) -> ProjectUpdateState:
        formatted_prompt = PROJECT_STATE_UPDATER_PROMPT.format(
            company_data=state["company_data"],
            project_general=state["project_general"],
            project_requirements=state["project_requirements"],
            employee_profiles=state["employee_profiles"],
            meeting_history=state["meeting_history"],
            current_project_state=state["project_state"],
            meeting_note=state["meeting_note"],
            meeting_analysis=state["meeting_analysis"]
        )
        messages = [
            SystemMessage(content=formatted_prompt),
            HumanMessage(content="Update the project state based on the meeting analysis.")
        ]
        response = model.invoke(messages)
        state["updated_project_state"] = response.content
        return state    
def backlog_manager_node(state: ProjectUpdateState) -> ProjectUpdateState:
    try:
        # Remove the {id} placeholder from the BACKLOG_MANAGER_PROMPT
        cleaned_prompt = BACKLOG_MANAGER_PROMPT.replace('{id}', 'id')
        
        formatted_prompt = cleaned_prompt.format(
            company_data=state.get("company_data", ""),
            project_general=state.get("project_general", ""),
            project_requirements=state.get("project_requirements", ""),
            employee_profiles=state.get("employee_profiles", ""),
            meeting_history=state.get("meeting_history", ""),
            current_project_backlog=state.get("project_backlog", ""),
            meeting_note=state.get("meeting_note", ""),
            meeting_analysis=state.get("meeting_analysis", ""),
        )
        messages = [
            SystemMessage(content=formatted_prompt),
            HumanMessage(content="Update the project backlog based on the provided information. ANSWER IN JSON FORMAT, AND ONLY WITH THE JSON")
        ]
        response = model.invoke(messages)
        
        # Attempt to parse the JSON response
        try:
            updated_backlog = json.loads(response.content)
            state["updated_project_backlog"] = json.dumps(updated_backlog, indent=2)
        except json.JSONDecodeError as json_error:
            print(f"Error parsing JSON response: {json_error}")
            print("Raw response content:")
            print(response.content)
            state["updated_project_backlog"] = "Error: Invalid JSON response"
        
        return state
    except Exception as e:
        print(f"Error in backlog_manager_node: {type(e).__name__}: {str(e)}")
        print("Current state keys:")
        for key in state.keys():
            print(f"- {key}")
        
        return state

def sprint_state_updater_node(state: ProjectUpdateState) -> ProjectUpdateState:
    formatted_prompt = SPRINT_STATE_UPDATER_PROMPT.format(
        company_data=state["company_data"],
        project_general=state["project_general"],
        project_requirements=state["project_requirements"],
        employee_profiles=state["employee_profiles"],
        meeting_history=state["meeting_history"],
        current_sprint_state=state["sprint_state"],
        meeting_analysis=json.dumps(state["meeting_analysis"])
    )
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content="Update the sprint state based on the meeting analysis. Provide your response as a markdown-formatted string.")
    ]
    response = model.invoke(messages)
    
    state["updated_sprint_state"] = response.content
    return state

def sprint_backlog_updater_node(state: ProjectUpdateState) -> ProjectUpdateState:
    formatted_prompt = SPRINT_BACKLOG_UPDATER_PROMPT.format(
        company_data=state["company_data"],
        project_general=state["project_general"],
        project_requirements=state["project_requirements"],
        employee_profiles=state["employee_profiles"],
        meeting_history=state["meeting_history"],
        current_sprint_backlog=state["sprint_backlog"],
        updated_sprint_state=state["updated_sprint_state"],
        meeting_analysis=json.dumps(state["meeting_analysis"])
    )
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content="Update the sprint backlog based on the meeting analysis and updated sprint state. Provide your response as a JSON object.")
    ]
    response = model.invoke(messages)
    print(response.content)
    state["updated_sprint_backlog"] = response.content
    
    return state