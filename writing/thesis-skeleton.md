# Thesis Skeleton: AI-Powered Multi-Agent System for Meeting Transcript Processing

## Introduction

In an era of rapid technological advancement, artificial intelligence (AI) has emerged as a transformative force across industries, reshaping how we work, communicate, and make decisions. This thesis presents a novel AI-powered system for analyzing meeting transcripts, a solution that sits at the intersection of recent advancements in AI, changes in work practices, and the growing need for efficient information processing in business environments. By leveraging state-of-the-art language models and carefully designed workflows, this system aims to revolutionize how organizations extract value from their digital meetings, turning unstructured conversations into actionable insights.

### The AI Revolution and Its Catalysts

The field of AI has experienced unprecedented growth in recent years, marked by a clear distinction between traditional AI approaches and the emergence of generative AI. While traditional AI has long been employed in tasks such as data analysis, pattern recognition, and decision support systems, generative AI has opened new frontiers in content creation, language understanding, and problem-solving.

This "AI boom" has been fueled by several key factors:
1. The exponential increase in available data for training AI models
2. Significant advancements in computing power, particularly in specialized hardware
3. Innovations in model architectures, especially the development of transformer models
4. The creation of sophisticated frameworks that facilitate AI development and deployment

These catalysts have converged to enable the development of Large Language Models (LLMs), AI systems capable of understanding and generating human-like text with unprecedented accuracy and fluency. LLMs represent a quantum leap in natural language processing, demonstrating remarkable capabilities in comprehending context, inferring meaning, and even performing complex reasoning tasks.

### The Digital Meeting Revolution

Parallel to these technological advancements, the global business landscape has undergone a significant transformation in how work is conducted. The COVID-19 pandemic acted as a catalyst, forcing organizations worldwide to rapidly adopt remote work practices. As the initial crisis has subsided, many businesses have transitioned to hybrid or fully remote work models, solidifying the central role of digital collaboration tools in modern work life.

This shift has led to an explosion in the number of digital meetings, with platforms like Microsoft Teams, Zoom, and Google Meet becoming integral to daily operations. While these tools have enabled continued collaboration in a distributed work environment, they have also created new challenges. Organizations now grapple with efficiently managing, documenting, and extracting value from the vast amount of information exchanged in these digital meetings.

### Technological Enablers

Two key technological advancements have set the stage for addressing these challenges:

1. **Speech-to-Text Technology**: Recent years have seen remarkable improvements in the accuracy of speech recognition systems. Platforms like Microsoft Teams now offer highly reliable automatic transcription services, providing a solid foundation for further analysis.

2. **Large Language Models**: The development of LLMs has revolutionized natural language understanding and generation. These models, trained on vast amounts of text data using enormous computational resources, have demonstrated an unprecedented ability to comprehend and work with human language.

### AI Systems and Workflows for Business Applications

The availability of these powerful AI tools has led to the development of various frameworks for creating AI-driven systems, such as AutoGen and CrewAI. While these frameworks offer flexibility and power, they often introduce complexity that can be challenging to manage in business environments where reliability and consistency are paramount.

This thesis proposes an alternative approach: the use of controlled workflows with specific, well-defined prompts for each step. This method provides the robustness and predictability required in business applications while still leveraging the power of advanced language models.

### Proposed Solution: AI-Powered Meeting Transcript Analysis System

Building on these technological foundations and guided by the needs of modern businesses, this thesis presents a novel system for analyzing meeting transcripts and generating actionable insights. The system is specifically designed to align with agile software development practices, particularly the Scrum framework, which is widely adopted in the software industry.

By focusing on common Scrum meeting types such as daily stand-ups, sprint planning, and sprint retrospectives, the system addresses the most frequent and critical touchpoints in agile project management. This approach not only provides a clear scope for the research but also ensures that the solution is immediately applicable to a large number of software development teams. The system's modular design allows for easy adaptation to other meeting types and company-specific needs in the future.

This system stands to benefit various stakeholders within an organization:
- **Employees** receive personalized, concise summaries of meetings, ensuring they never miss critical information relevant to their roles.
- **Managers** gain enhanced oversight of project progress and team dynamics, facilitating more informed decision-making.
- **Scrum Masters** can more efficiently track action items, sprint progress, and team performance, enhancing their ability to facilitate the Scrum process.

### Data Generation for System Development and Testing

An important aspect of this research was the need to generate synthetic meeting data for system development and testing. Despite attempts to obtain real-world meeting transcripts, the confidential nature of most business communications made this unfeasible. To overcome this challenge, I developed a sophisticated data generation process that simulates realistic meeting scenarios within the context of an agile software development project.

This simulated dataset includes:
- A fictitious software development team with defined roles and responsibilities
- A series of Scrum meetings (daily stand-ups, sprint planning, retrospectives) over multiple sprints
- Realistic project progression, including the completion of tasks, emergence of challenges, and team dynamics

The data generation process not only provided the necessary input for system development but also offered valuable insights into the complexities of capturing and representing the nuanced interactions that occur in real-world agile teams. This approach ensures that while the system is trained and tested on synthetic data, it is well-prepared to handle the intricacies of actual workplace communications.

Figure 1 provides an overview of the system architecture:

![Description of SVG](figures/main_pipeline.svg)

Key features of the proposed system include:
- A modular architecture composed of interconnected workflows, each represented by a blue cylinder in the diagram. Each workflow consists of a sequence of steps executed in a specific order to perform a distinct function within the system.
- Clear delineation of system inputs and outputs for each workflow, allowing for easy tracking of data flow and processing stages.
- A "Human in the loop" component, illustrated in the diagram, which enables human intervention and guidance at any point in the process. This feature ensures that the system can be fine-tuned and directed towards optimal results, combining the efficiency of AI with human expertise and judgment.

### Thesis Structure and Objectives

The subsequent chapters will delve into the technical details of the system, including:
- A comprehensive review of relevant literature and technologies
- Detailed explanation of the system architecture and individual components
- Discussion of the challenges encountered during development and the solutions devised
- Presentation and analysis of system performance and user impact studies
- Exploration of future directions and potential broader applications of the technology

By addressing the growing challenge of information overload in the age of digital meetings, this research contributes to the ongoing dialogue about the role of AI in shaping the future of work. It demonstrates how thoughtfully designed AI systems can enhance human capabilities, improve organizational efficiency, and unlock new value from the wealth of information exchanged in our daily professional interactions.

Before proceeding to the subsequent sections, readers are strongly encouraged to explore the preliminary results and example outputs available in the project's Git repository. These materials provide tangible demonstrations of the system's capabilities and will enhance understanding of the concepts discussed in the following chapters.


## 2. Technical Background and Related Work

### 2.1 Evolution of Natural Language Processing (NLP)
- Early NLP approaches (e.g., rule-based systems, statistical methods)
- Introduction to neural network-based NLP
- The transformer architecture and its impact on NLP

### 2.2 Large Language Models (LLMs)
- Architecture and training of LLMs
- Key models and their capabilities (e.g., GPT-3, BERT, T5)
- Inference methods and computational requirements
- Challenges and limitations of LLMs (e.g., hallucinations, context window)

### 2.3 Retrieval-Augmented Generation (RAG)
- Concept and importance of RAG in LLM applications
- Techniques for efficient information retrieval
- Integration of external knowledge with LLM outputs

### 2.4 Multi-Agent AI Systems
- Theoretical foundations of multi-agent systems
- Applications in task decomposition and problem-solving
- Coordination and communication between agents

### 2.5 Agentic Workflows in Natural Language Processing
- Definition and components of agentic workflows
- Key paradigms: reflection, tool use, planning, and collaboration
- Examples of agentic workflows in NLP tasks

### 2.6 Meeting Summarization Techniques
- Overview of existing approaches to meeting summarization
- Extractive vs. abstractive summarization methods
- Challenges in meeting transcript processing (e.g., speaker diarization, topic segmentation)

### 2.7 Personalization in AI-generated Content
- Techniques for tailoring AI outputs to individual users
- Challenges in maintaining coherence while personalizing content
- Ethical considerations in AI personalization

### 2.8 Visual Information Generation from Text
- Methods for automatic diagram and chart generation
- Integration of visual elements in text summarization
- Tools and libraries for programmatic visualization (e.g., Mermaid)

### 2.9 Frameworks for LLM-based Applications
- Overview of LangChain and LangGraph
- Comparison with other frameworks for LLM application development
- Best practices in designing LLM-powered applications
