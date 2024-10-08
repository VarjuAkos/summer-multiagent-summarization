from workflows.generate_meeting.prompts import MEETING_PURPOSE_GENERATOR_PROMPT, MEETING_TPYE_SELECTOR, TOPIC_OUTLINER_PROMPT,MEETING_LENGTH_ESTIMATOR, PARTICIPANT_DEFINER_PROMPT, TRANSCRIPT_GENERATOR_PROMPT , UPDATE_MEETING_HISTORY_PROMPT
from workflows.generate_meeting.state import DataGenerationState
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from  dotenv import load_dotenv
import os
import json

load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
#model = ChatAnthropic(model="claude-3-haiku-20240307", anthropic_api_key=anthropic_api_key)
model = ChatAnthropic(model="claude-3-5-sonnet-20240620", anthropic_api_key=anthropic_api_key, max_tokens= 8192)


def meeting_purpose_node(state: DataGenerationState) -> DataGenerationState:
    formatted_prompt = MEETING_PURPOSE_GENERATOR_PROMPT.format(
		company_data = state.get("company_data"),
		employee_profiles = state.get("employee_profiles"),
		project_general = state.get("project_general"),
		project_requirements = state.get("project_requirements"),
		project_state = state.get("project_state"),
		project_sprint_state = state.get("project_sprint_state"),
		project_backlog = state.get("project_backlog"),
		project_sprint_backlog = state.get("project_sprint_backlog"),
		meeting_history = state.get("meeting_history"),
    )
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content="Generate a meeting purpose based on the provided information.")
	]
    response = model.invoke(messages)
    state["meeting_purpose"] = response.content
    print(state["meeting_purpose"])
    return state

def meeting_type_node(state: DataGenerationState) -> DataGenerationState:
    formatted_prompt = MEETING_TPYE_SELECTOR.format(
		meeting_purpose = state.get("meeting_purpose")
	)
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content="Generate a meeting type based on the provided information.")
    ]
    response = model.invoke(messages)
    state["meeting_type"] = response.content
    print(state["meeting_type"])
    return state


def topic_outliner_node(state: DataGenerationState) -> DataGenerationState:
    formatted_prompt = TOPIC_OUTLINER_PROMPT.format(
        meeting_type = state.get("meeting_type"),
        meeting_purpose = state.get("meeting_purpose"), 
		company_data = state.get("company_data"),
		employee_profiles = state.get("employee_profiles"),
		project_general = state.get("project_general"),
		project_state = state.get("project_state"),
		project_sprint_state = state.get("project_sprint_state"),
        project_backlog = state.get("project_backlog"),
        project_sprint_backlog = state.get("project_sprint_backlog"),
	)
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content="Generate the meeting topics and outline based on the provided information.")
    ]
    response = model.invoke(messages)
    state["meeting_outline"] = response.content
    print(state["meeting_outline"])
    return state


def meeting_length_estimator_node(state: DataGenerationState) -> DataGenerationState:
    formatted_prompt = MEETING_LENGTH_ESTIMATOR.format(
        meeting_type = state.get("meeting_type"),
		meeting_purpose = state.get("meeting_purpose"),
		meeting_outline = state.get("meeting_outline"),
	)
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content="Generate the meeting length based on the provided information.")
    ]
    response = model.invoke(messages)
    state["meeting_length"] = response.content
    print(state["meeting_length"])
    return state


def participant_definer_node(state: DataGenerationState) -> DataGenerationState:
    formatted_prompt = PARTICIPANT_DEFINER_PROMPT.format(
        meeting_type = state.get("meeting_type"),
		meeting_purpose = state.get("meeting_purpose"),
		meeting_outline = state.get("meeting_outline"),
		employee_profiles = state.get("employee_profiles"),
	)
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content="List the participants who need to be present at the meeting based on the provided information.")
    ]
    response = model.invoke(messages)
    state["meeting_participants"] = response.content
    print(state["meeting_participants"])
    return state


def generate_transcript_node(state: DataGenerationState) -> DataGenerationState:
    formatted_prompt = TRANSCRIPT_GENERATOR_PROMPT.format(
		company_data = state.get("company_data"),
		project_general = state.get("project_general"),
		employee_profiles = state.get("employee_profiles"),
		project_state = state.get("project_state"),
		project_sprint_state = state.get("project_sprint_state"),
		project_backlog = state.get("project_backlog"),
		project_sprint_backlog = state.get("project_sprint_backlog"),
		meeting_history = state.get("meeting_history"),
		meeting_type = state.get("meeting_type"),
		meeting_purpose = state.get("meeting_purpose"),
		meeting_outline = state.get("meeting_outline"),
		meeting_participants = state.get("meeting_participants"),
		meeting_length = state.get("meeting_length"),
	)
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content="Generate the transcript based on the provided information.")
    ]
    
    full_transcript = ""
    more_turns_needed = True
    turn_count = 0
    max_turns = 5
    
    while more_turns_needed and turn_count < max_turns:
        response = model.invoke(messages)
        turn_transcript = response.content
        
        full_transcript += turn_transcript
        
        if "FINISHED" in turn_transcript:
            more_turns_needed = False
        else:
            messages.append(AIMessage(content=turn_transcript))
            messages.append(HumanMessage(content="Continue the transcript from where you left off."))
        
        
        turn_count += 1
        print(turn_count)

    state["transcript"] = full_transcript
    print(state["transcript"])
    return state

def update_meeting_history_node(state: DataGenerationState) -> DataGenerationState:
    formatted_prompt = UPDATE_MEETING_HISTORY_PROMPT.format(
        meeting_type = state.get("meeting_type"),
		meeting_purpose = state.get("meeting_purpose"),
		meeting_outline = state.get("meeting_outline"),
	)
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content="Update the meeting history with the provided information. Your response has to be a valid JSON object.")
    ]
    response = model.invoke(messages)
    print(response.content)
    # Parse the response content as JSON
    new_meeting_entry = json.loads(response.content)

    # Get the current meeting history
    current_history = state.get("meeting_history", [])
    print(current_history)
    # Ensure current_history is a list
    if not isinstance(current_history, list):
        current_history = [current_history] if current_history else []
    
    # Check if an entry for this date already exists
    existing_entry = next((entry for entry in current_history if entry.get('date') == new_meeting_entry['date']), None)
    
    if existing_entry:
        # Update the existing entry
        existing_entry.update(new_meeting_entry)
    else:
        # Add the new entry to the front of the list
        current_history.insert(0, new_meeting_entry)
    
    # Remove any empty dictionaries
    current_history = [entry for entry in current_history if entry]
    
    # Update the state with the new meeting history
    state["meeting_history"] = current_history
    
    return state