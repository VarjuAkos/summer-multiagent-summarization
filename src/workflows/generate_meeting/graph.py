import os
import sys

src_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, src_dir)

from langgraph.graph import StateGraph, END
from workflows.base_graph import Graph
from workflows.generate_meeting.state import DataGenerationState
from workflows.generate_meeting.node_functions import meeting_purpose_node, meeting_type_node, topic_outliner_node, meeting_length_estimator_node, participant_definer_node, generate_transcript_node, update_meeting_history_node
from utils.functions import (
    load_markdown_to_str,
    export_transcript,
    export_state,
    load_from_json,
    load_latest_sprint_backlog,
    export_meeting_history,
    manage_sprint_folders,
    load_json
)
import json
import os   

class GenerateMeeting(Graph):
    def __init__(self):
        self.workflow = None

    def create_graph(self):
        workflow = StateGraph(DataGenerationState)

        workflow.add_node("meeting_purpose_node", meeting_purpose_node)
        workflow.add_node("meeting_type_node", meeting_type_node)
        workflow.add_node("topic_outliner_node", topic_outliner_node)
        workflow.add_node("meeting_length_estimator_node", meeting_length_estimator_node)
        workflow.add_node("participant_definer_node", participant_definer_node)
        workflow.add_node("generate_transcript_node", generate_transcript_node)
        workflow.add_node("update_meeting_history_node", update_meeting_history_node)

        workflow.add_edge("meeting_purpose_node", "meeting_type_node")
        workflow.add_edge("meeting_type_node", "topic_outliner_node")
        workflow.add_edge("topic_outliner_node", "meeting_length_estimator_node")
        workflow.add_edge("meeting_length_estimator_node", "participant_definer_node")
        workflow.add_edge("participant_definer_node", "generate_transcript_node")
        workflow.add_edge("generate_transcript_node", "update_meeting_history_node")
        workflow.add_edge("update_meeting_history_node", END)

        workflow.set_entry_point("meeting_purpose_node")

        self.workflow = workflow.compile()
    
    def run_graph(self, project_folder) -> DataGenerationState:
        # TODO : make folder management and file handling

        if self.workflow is None:
            raise ValueError("Graph has not been created. Call create_graph() first.")
        
        state = initialize_data_generation_state(
            company_data=load_markdown_to_str(file_path=os.path.join(project_folder, "company-general.md")), # check
            project_general=load_markdown_to_str(file_path=os.path.join(project_folder, "project-general.md")), # check
            project_requirements=load_markdown_to_str(file_path=os.path.join(project_folder, "project-requirements.md")), # check
            employee_profiles =load_markdown_to_str(file_path=os.path.join(project_folder, "employee-profiles.md")), # check

            
            project_state=load_markdown_to_str(file_path=os.path.join(project_folder, "project-state.md")), # TODO
            project_backlog=load_from_json(file_path=os.path.join(project_folder, "project-backlog.json")), # TODO
            
            project_sprint_state=load_latest_sprint_backlog(base_path=project_folder), # TODO
            project_sprint_backlog=load_latest_sprint_backlog(base_path=project_folder), # TODO
            
            meeting_history =load_from_json(file_path=os.path.join(project_folder, "meeting-history.json")) # TODO
	    )

        state = self.workflow.invoke(state)

        return state
    
    def export_files(self, state: DataGenerationState, project_folder: str):
        export_transcript(state=state, folder_path=os.path.join(project_folder, "transcripts/"))
        export_state(state=state, folder_path=os.path.join(project_folder, "state-logs/"), filename="generate_transcript")
        export_meeting_history(state=state, output_file=os.path.join(project_folder, "meeting-history.json"))
        manage_sprint_folders(state=state, project_folder=project_folder)


def initialize_data_generation_state(company_data: str, project_general: str, project_requirements: str, project_state : str, project_sprint_state: str, project_backlog :str, project_sprint_backlog :str, employee_profiles: str, meeting_history: str ) -> DataGenerationState:
    return DataGenerationState(
    	company_data=company_data,
        project_general = project_general,
    	project_requirements = project_requirements,
        employee_profiles=employee_profiles,

		project_state= project_state,	
        project_backlog = project_backlog,
        	
    	project_sprint_state= project_sprint_state,	
        project_sprint_backlog = project_sprint_backlog,
    	
        meeting_history = meeting_history,	
    	meeting_purpose="",	
    	meeting_type="",		
    	meeting_outline= "",		
    	meeting_participants="",		 
    	meeting_length= "",
    	transcript="",
    )


if __name__ == "__main__":
    #python -m workflows.generate_meeting.graph
    #from src 
    summer_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    project_folder = os.path.join(summer_dir, 'data_', 'project1')

    print(f"Project folder path: {project_folder}")

    if os.path.exists(project_folder):
        print("Project folder exists")
        graph = GenerateMeeting()
        graph.create_graph()
        try:
            # Run the graph without saving the state
            #state = graph.run_graph(project_folder=project_folder)
            state = load_json(file_path=os.path.join(project_folder, "extra/state_log_1.json"))
            print(state["meeting_type"])    
            graph.export_files(state=state, project_folder=project_folder)
        except Exception as e:
            print(f"An error occurred while running the graph: {str(e)}")
    else:
        print(f"Project folder not found: {project_folder}")