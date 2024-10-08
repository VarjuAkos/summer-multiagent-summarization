{
  "backlog": [
    {
      "id": "US001",
      "title": "User Registration",
      "description": "As a new user, I want to create an account so that I can start tracking my health data.",
      "status": "Not Started",
      "priority": "High",
      "estimated_effort": "8 story points",
      "assigned_to": "Alex Rodriguez",
      "tags": [
        "feature",
        "authentication"
      ],
      "dependencies": []
    },
    {
      "id": "US002",
      "title": "User Login",
      "description": "As a registered user, I want to log in to my account to access my health data.",
      "status": "Not Started",
      "priority": "High",
      "estimated_effort": "5 story points",
      "assigned_to": "Alex Rodriguez",
      "tags": [
        "feature",
        "authentication"
      ],
      "dependencies": [
        "US001"
      ]
    },
    {
      "id": "US003",
      "title": "User Profile Management",
      "description": "As a user, I want to view and edit my profile information to keep my data up to date.",
      "status": "Not Started",
      "priority": "Medium",
      "estimated_effort": "5 story points",
      "assigned_to": "Emily Watson",
      "tags": [
        "feature",
        "frontend"
      ],
      "dependencies": [
        "US001"
      ]
    },
    {
      "id": "US004",
      "title": "Basic Activity Tracking",
      "description": "As a user, I want to manually log my daily activities to track my health progress.",
      "status": "Not Started",
      "priority": "High",
      "estimated_effort": "8 story points",
      "assigned_to": "Michael Kim",
      "tags": [
        "feature",
        "backend"
      ],
      "dependencies": [
        "US001"
      ]
    },
    {
      "id": "US005",
      "title": "Basic Health Metrics Dashboard",
      "description": "As a user, I want to view a dashboard of my basic health metrics to understand my overall health status.",
      "status": "Not Started",
      "priority": "High",
      "estimated_effort": "13 story points",
      "assigned_to": "Emily Watson",
      "tags": [
        "feature",
        "frontend"
      ],
      "dependencies": [
        "US004"
      ]
    },
    {
      "id": "US006",
      "title": "Simplified Nutrition Logging",
      "description": "As a user, I want to log my daily food intake to track my nutrition.",
      "status": "Not Started",
      "priority": "Medium",
      "estimated_effort": "8 story points",
      "assigned_to": "Michael Kim",
      "tags": [
        "feature",
        "backend"
      ],
      "dependencies": [
        "US001"
      ]
    },
    {
      "id": "T001",
      "title": "Set up project structure",
      "description": "Set up initial project structure, create repositories, configure ESLint and Prettier",
      "status": "In Progress",
      "priority": "High",
      "estimated_effort": "3 story points",
      "assigned_to": "Alex Rodriguez",
      "tags": [
        "technical",
        "setup"
      ],
      "dependencies": []
    },
    {
      "id": "T002",
      "title": "Configure frontend environment",
      "description": "Set up frontend environment with React, TypeScript, and Tailwind CSS",
      "status": "Not Started",
      "priority": "High",
      "estimated_effort": "3 story points",
      "assigned_to": "Emily Watson",
      "tags": [
        "technical",
        "setup",
        "frontend"
      ],
      "dependencies": [
        "T001"
      ]
    },
    {
      "id": "T003",
      "title": "Set up backend structure",
      "description": "Set up backend structure and initial database schema",
      "status": "Not Started",
      "priority": "High",
      "estimated_effort": "5 story points",
      "assigned_to": "Michael Kim",
      "tags": [
        "technical",
        "setup",
        "backend"
      ],
      "dependencies": [
        "T001"
      ]
    },
    {
      "id": "T004",
      "title": "Configure CI/CD pipeline",
      "description": "Set up CI/CD pipeline with Jenkins and configure Docker environments",
      "status": "Not Started",
      "priority": "High",
      "estimated_effort": "5 story points",
      "assigned_to": "Olivia Martinez",
      "tags": [
        "technical",
        "devops"
      ],
      "dependencies": [
        "T001"
      ]
    },
    {
      "id": "T005",
      "title": "Create design system",
      "description": "Create shared Figma project, start building component library and design guidelines",
      "status": "Not Started",
      "priority": "High",
      "estimated_effort": "8 story points",
      "assigned_to": "Liam Foster",
      "tags": [
        "design",
        "ui/ux"
      ],
      "dependencies": []
    },
    {
      "id": "T006",
      "title": "Set up project documentation",
      "description": "Set up Confluence space for project documentation",
      "status": "Not Started",
      "priority": "Medium",
      "estimated_effort": "2 story points",
      "assigned_to": "Sarah Chen",
      "tags": [
        "documentation"
      ],
      "dependencies": []
    },
    {
      "id": "T007",
      "title": "Research security standards",
      "description": "Research security standards and compliance requirements (e.g., HIPAA) for health data",
      "status": "Not Started",
      "priority": "High",
      "estimated_effort": "5 story points",
      "assigned_to": "Olivia Martinez",
      "tags": [
        "research",
        "security"
      ],
      "dependencies": []
    }
  ]
}