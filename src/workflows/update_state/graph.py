import os
import sys
from langgraph.graph import StateGraph, END
from workflows.base_graph import Graph
from workflows.update_state.state import ProjectUpdateState
from workflows.update_state.node_functions import meeting_note_analyzer_node, project_state_updater_node, backlog_manager_node, sprint_state_updater_node, sprint_backlog_updater_node
from utils.functions import (
    load_markdown_to_str,
    export_transcript,
    export_state,
    load_from_json,
    load_latest_sprint_backlog,
    export_meeting_history,
    manage_sprint_folders,
    load_latest_json,
    export_markdown,
    export_json,
    get_latest_sprint_folder
)


from langgraph.graph import StateGraph, END
class UpdateProjectState(Graph):
    def __init__(self):
        self.workflow = None

    def create_graph(self):
        workflow = StateGraph(ProjectUpdateState)

        workflow.add_node("meeting_note_analyzer", meeting_note_analyzer_node)
        workflow.add_node("project_state_updater", project_state_updater_node)
        workflow.add_node("backlog_manager", backlog_manager_node)
        workflow.add_node("sprint_state_updater", sprint_state_updater_node)
        workflow.add_node("sprint_backlog_updater", sprint_backlog_updater_node)

        workflow.add_edge("meeting_note_analyzer", "project_state_updater")
        workflow.add_edge("project_state_updater", "backlog_manager")
        workflow.add_edge("backlog_manager", "sprint_state_updater")
        workflow.add_edge("sprint_state_updater", "sprint_backlog_updater")
        workflow.add_edge("sprint_backlog_updater", END)

        workflow.set_entry_point("meeting_note_analyzer")

        self.workflow = workflow.compile()

    def run_graph(self, project_folder: str, meeting_note: str, meeting_type: str) -> ProjectUpdateState:
        if self.workflow is None:
            raise ValueError("Graph has not been created. Call create_graph() first.")
        previous_state = load_latest_json(folder_path = os.path.join(project_folder,"state-logs"))

        state = initialize_project_update_state(
            project_folder=project_folder,
            previous_state=previous_state
        )

        updated_state = self.workflow.invoke(state)

        self.export_updated_state(updated_state, project_folder)

        return updated_state
    
    def export_updated_state(self, state: ProjectUpdateState, project_folder: str):
        current_sprint = get_latest_sprint_folder(project_folder)
        export_markdown(state["updated_project_state"], os.path.join(project_folder, "project-state.md"))
        export_json(state["updated_project_backlog"], os.path.join(project_folder, "project-backlog.json"))
        export_markdown(state["updated_sprint_state"], os.path.join(project_folder, current_sprint, "sprint-state.md"))
        export_json(state["updated_sprint_backlog"], os.path.join(project_folder, current_sprint, "sprint-backlog.json"))

def initialize_project_update_state(project_folder: str, previous_state: ProjectUpdateState) -> ProjectUpdateState:
    return ProjectUpdateState(
        meeting_note=previous_state["note_final"],
        meeting_type=previous_state["meeting_type"],
        company_data=previous_state["company_data"],
        project_general=previous_state["project_general"],
        project_requirements=previous_state["project_requirements"],
        employee_profiles=previous_state["employee_profiles"],
        meeting_history=previous_state["meeting_history"],
        project_state=previous_state["project_state"],
        project_backlog=previous_state["project_backlog"],
        sprint_state=previous_state["sprint_state"],
        sprint_backlog=previous_state["sprint_backlog"],
        meeting_analysis="",
        updated_project_state="",
        updated_project_backlog="",
        updated_sprint_state="",
        updated_sprint_backlog=""
    )