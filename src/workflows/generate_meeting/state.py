from typing import TypedDict
class DataGenerationState(TypedDict):
    company_data: str	# init
    project_general: str	# init
    project_requirements: str		# init + need to be updated - this could be get from project state
    project_state : str 
    project_sprint_state : str 
    project_backlog : str
    project_sprint_backlog : str
    employee_profiles: str	# init
    meeting_history: str	# init + need to be updated -this could be get from project state
    meeting_purpose: str	# [optional] generated by first node
    meeting_type: str		# generated by 2nd node
    meeting_outline: str		# generated by 3rd node
    meeting_participants: str		# 
    meeting_length: str
    transcript: str