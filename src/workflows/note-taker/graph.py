from typing import TypedDict
from .node_functions import note_taker_node, note_approvel_node, reflection_node, reflection_approvel_node, update_project_state
from langgraph.graph import StateGraph, END
from ..base_graph  import Graph
from ...utils.functions import load_markdown_to_str,export_transcript, export_state, load_txt_to_str

class NoteTakerState(TypedDict):
    company_data: str	
    project_general: str	
    project_requirements: str		
    project_sprint_state : str
    project_backlog : str
    employee_profiles: str	
    meeting_history: str	
    meeting_type: str		
    transcript: str
    note_taker_halucinate : bool
    reflection_haluconate : bool
    note_draft : str
    note_after_reflection : str
    note_final : str

class NoteTaker(Graph):
    def __init__(self):
        self.workflow = None

    def create_graph(self):
        workflow = StateGraph(NoteTakerState)

        # Define nodes
        workflow.add_node("note_taker", note_taker_node)
        workflow.add_node("note_approvel", note_approvel_node)
        workflow.add_node("reflection", reflection_node)
        workflow.add_node("reflection_approvel", reflection_approvel_node)
        workflow.add_node("update_project_state", update_project_state)
        
        # Define edges
        workflow.add_edge("note_taker", "note_approvel")
        workflow.add_conditional_edges(
            "note_approvel",
            lambda x: "reflection" if not x.get("note_taker_halucinate") else "note_taker",
            {
                "reflection": "reflection",
                "note_taker": "note_taker"
            }
        )
        workflow.add_edge("reflection", "reflection_approvel")
        workflow.add_conditional_edges(
            "reflection_approvel",
            lambda x: "reflection" if x.get("reflection_haluconate") else "update_project_state",
            {
                "reflection": "reflection",
                "update_project_state": "update_project_state"
            }
        )
        workflow.add_edge("update_project_state", END)


        # Set entry point
        workflow.set_entry_point("note_taker")
        self.workflow = workflow.compile()
    
    def run_graph(self, project_folder):
        # TODO : make folder management and file handling

        if self.workflow is None:
            raise ValueError("Graph has not been created. Call create_graph() first.")

        state = initialize_NoteTaker_state(
            company_data=load_markdown_to_str(file_path="../data/company-data/company-data.md"),
            project_general=load_markdown_to_str(file_path= "../data/company-data/current-project-general.md"),
            project_requirements=load_markdown_to_str(file_path="../data/company-data/current-project-requirements.md"),
            project_sprint_state=load_markdown_to_str(file_path="../data/company-data/current-project-sprint-state.md"),
            project_backlog=load_markdown_to_str(file_path="../data/company-data/current-project-backlog.md"),
            employee_profiles=load_markdown_to_str(file_path="../data/company-data/employee-profiles.md"),
            meeting_history=load_markdown_to_str(file_path="../data/company-data/current-meeting-history.md"),
            meeting_type="Sprint Planning",
            transcript=load_txt_to_str(file_path="../data/transcript-workflow/1.txt"),
        )
        state = self.workflow.invoke(state)
        export_transcript(state=state, folder_path="../data/transcript-workflows")
        export_state(state=state, folder_path="../data/logs")
        #update_meeting_history(state=state, file_path="../data/company-data/current-meeting-history.md")

def initialize_NoteTaker_state(company_data: str, project_general: str, project_requirements: str, project_sprint_state: str, project_backlog :str, employee_profiles: str, meeting_history: str, meeting_type: str, transcript : str ) -> NoteTakerState:
    return NoteTakerState(
    	company_data=company_data,
        project_general = project_general,
    	project_requirements = project_requirements,	
    	project_sprint_state= project_sprint_state,	
        project_backlog = project_backlog,
    	employee_profiles=employee_profiles,
        meeting_history = meeting_history,	
    	meeting_type=meeting_type,			
    	transcript=transcript,
        note_taker_halucinate = False,
        reflection_haluconate = False,
        note_draft = "",
        note_after_reflection = "",
        note_final = "",
    )