from typing import TypedDict, Dict
from .node_functions import general_info_extractor_node, personal_task_extractor_node, diagram_generator_node, report_compiler_node, motivational_message_node
from langgraph.graph import StateGraph, END
from ..base_graph  import Graph
from ...utils.functions import load_markdown_to_str,export_transcript, export_state, load_employee_profiles


class DailyState(TypedDict):
    project_sprint_state: str
    project_backlog: str
    employee_profiles: Dict
    note: str
    general_info : str
    reports: Dict[str, str]  # Key: employee name, Value: report content
    diagrams: Dict[str, str]  # Key: employee name, Value: Mermaid diagram code
    personal_tasks : Dict [str,str]

class DailyMeeting(Graph):
    def __init__(self):
        self.workflow = None

    def create_graph(self):
        workflow = StateGraph(DailyState)

    
        # Define nodes
        workflow.add_node("general_info_extractor", general_info_extractor_node)
        workflow.add_node("personal_task_extractor", personal_task_extractor_node)
        workflow.add_node("diagram_generator", diagram_generator_node)
        workflow.add_node("report_compiler", report_compiler_node)
        workflow.add_node("motivational_message", motivational_message_node)
        
        # Define edges
        workflow.add_edge("general_info_extractor", "personal_task_extractor")
        workflow.add_edge("personal_task_extractor", "diagram_generator")
        workflow.add_edge("diagram_generator", "report_compiler")
        workflow.add_edge("report_compiler", "motivational_message")
        workflow.add_edge("motivational_message", END)
        
        # Set entry point
        workflow.set_entry_point("general_info_extractor")

        self.workflow = workflow

    def run_graph(self, project_folder) -> DailyState:
        # TODO : make folder management and file handling

        if self.workflow is None:
            raise ValueError("Graph has not been created. Call create_graph() first.")

        state = DailyState(
            project_sprint_state=load_markdown_to_str(file_path="../data/company-data/current-project-sprint-state.md"),
            project_backlog=load_markdown_to_str(file_path="../data/company-data/current-project-backlog.md"),
            employee_profiles=load_employee_profiles(file_path="../data/company-data/employee-profiles.json"),
            note=note,
            general_info= "",
            reports={},
            diagrams={},
            personal_tasks = {}
        )
    
        state = self.workflow.invoke(state)
        export_transcript(state=state, folder_path="../data/transcript-workflows")
        export_state(state=state, folder_path="../data/logs")
        return state

