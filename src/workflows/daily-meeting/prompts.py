GENERAL_INFO_EXTRACTOR_PROMPT = """
You are an AI assistant helping to extract general information from a daily scrum meeting note. Your task is to summarize the key points that are relevant to all team members.


Here's the daily scrum meeting note:
####
{note}
####

Please extract and summarize the following information:
1. Overall sprint progress
2. Main challenges or blockers
3. Key decisions made
4. Any updates that affect the entire team

Provide this information in a concise, bullet-point format.
IMPORTANT: Answer only with the general information. No more. 
You must not say here is the summary ... just the information.
Note that your task is not to make a summary but to find information that effect everyone.
"""

PERSONAL_TASK_EXTRACTOR_PROMPT = """
You are an AI assistant helping to extract personal tasks and progress for a specific team member from a daily scrum meeting note.

Here's the daily scrum meeting note:
####
{note}
####

Here's the profile of the team member:
####
{employee_profile}
####

Here's the curret state of the project: 
Note that this document already contains information about the current meeting that have just happened. It is up to date.
####
{project_sprint_state}
####

Here's the current state of the backlog:
Note that this document does not contains information about the current meeting. It representes a previous state.
####
{project_backlog}
####

Please extract the following information for this team member:
1. Their reported progress since the last meeting
2. Their current tasks or focus areas
3. Any blockers or challenges they're facing
4. Their next steps or goals

Provide this information in a concise, bullet-point format.
"""



DIAGRAM_GENERATOR_PROMPT = """
You are an AI assistant tasked with generating a Mermaid diagram based on a team member's tasks and progress.

Here's the daily scrum meeting note:
####
{note}
####


Here's the information about the team member's tasks and progress:
####
{personal_tasks}
####

Please create a Mermaid diagram that visualizes this information. The diagram should show:
1. Completed tasks
2. In-progress tasks
3. Upcoming tasks
4. Any dependencies between tasks

Provide only the Mermaid diagram code, without any explanation or additional text.
"""



REPORT_COMPILER_PROMPT = """
You are an AI assistant tasked with compiling a personalized daily scrum report for a team member.

Here's the general project information:
####
{general_info}
####

Here's the team member's personal task information:
####
{personal_tasks}
####

Here's a rendered Mermaid diagram representing the team member's tasks:
![Task Diagram]({diagram})

Please compile a personalized report for this team member. The report should include:
1. A brief overview of the sprint progress
2. The team member's personal progress and next steps
3. Any relevant challenges or blockers
4. The rendered Mermaid diagram (include it using the Markdown image syntax)

Format the report in Markdown, including appropriate headers and sections.
"""



MOTIVATIONAL_MESSAGE_PROMPT = """
You are an AI assistant tasked with generating a short, personalized motivational message or fun fact for a team member.

Here's the team member's profile:
####
{employee_profile}
####

Please generate a short, uplifting message or interesting fun fact related to the team member's interests, role, or recent achievements. The message should be positive and encouraging.

Provide only the message, without any additional explanation.
"""