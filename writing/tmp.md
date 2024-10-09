this video so with the rise of large
language models so-called agentic
workflows and Frameworks became really
popular and as a result we saw a lot of
them pop up so for example we have
autogen we have crew Ai and also Lang
chain has a way to build agents and you
have a lot more and the problem with all
of these all of those Frameworks is that
most of them are probably way too
complex for what you're trying to do and
not robust enough for what you're trying
to do so let me
explain all of these tools in all of
these Frameworks are really most of them
are built around the core idea of
chaining agents together in a way where
they can reason and figure out the next
step within some kind of workflow so
here if you look at the definition by
Lang chain the core idea of an agent is
to use a language model so an LM to
choose a sequence uh of actions to tae
in a chain so a language model is used
as a reasoning engine to determine which
action to take crew AI follows a similar
approach where you can very easily
design agents you can give them tasks
and I believe there's also this allowed
delegation parameter that you can fill
in so agents have Back stories roles
goals and depending on the overall
system they can decide the next PATH to
take and the result of that is really
cool and creative in a way that every
time you run this you can get different
outcomes you can get new stories you can
build really cool processes for this but
the problem what I found is that most
most of the processes in the real world
right now that you want to automate for
a business for example does not require
that much room for
creativity actually mostly it's the
other way around you want to take a
process that is very clearly defined and
if it's not defined you want to you want
to Define that and then figure out the
sequence of steps the sequence of
actions to automate that workflow and
then whenever you need AI to solve a
particular step within that chain of
problems that is where a large language
model comes in so
model comes in so





----
# Diagram 

\documentclass{standalone}
\usepackage{tikz}
\usetikzlibrary{shapes,arrows,positioning,calc,backgrounds,fit,shapes.multipart,decorations.pathreplacing}

\begin{document}
\begin{tikzpicture}[
    node distance = 2cm and 2.5cm,
    box/.style = {draw, rectangle, rounded corners, minimum width=4cm, minimum height=1.5cm, text centered, align=center, fill=blue!10, font=\small},
    input/.style = {draw, ellipse, fill=green!20, minimum width=3.5cm, minimum height=1.5cm, align=center, font=\footnotesize},
    decision/.style = {draw, diamond, aspect=2, fill=yellow!20, align=center, font=\footnotesize, minimum width=3cm, minimum height=2cm},
    arrow/.style = {thick,->,>=stealth,draw=blue!50},
    label/.style = {text width=2.5cm, align=center, font=\small\itshape},
    note/.style = {draw, rectangle, rounded corners, fill=orange!20, align=left, text width=3.2cm, font=\footnotesize},
    group/.style={draw=gray!50, dashed, rounded corners, inner sep=1.2cm},
    grouptext/.style={font=\small\bfseries, fill=white, inner sep=2pt}
]

% Input data
\node[input] (input_data) {Company data \\ Employee profiles \\ Project Requirements};
\node[input, below=0.8cm of input_data] (project_state) {Project State\\ Meeting History};

% Main workflow
\node[box, shift={(3.0cm,-1.2cm)}] (transcript) at (input_data.east) {Transcript Generation};
\node[box, right=of transcript] (notetaker) {Note Taker};
\node[decision, right=of notetaker] (human) {Human Verification};
\node[box, right=of human] (updatestate) {Update State};

% Meeting type decision
\node[decision, right=of updatestate] (meeting_type) {Meeting Type};

% Specific workflows
\node[box, right=2.4cm of meeting_type] (daily) {Daily Meeting};
\node[box, below=1cm of daily] (sprint) {Sprint Planning};
\node[box, below=1cm of sprint] (retro) {Retrospective};

% Outputs
\node[note, right=1.2cm of daily] (daily_output) {Output:\\ - Tickets\\ - Personalized Summary};
\node[note, right=1.2cm of sprint] (sprint_output) {Output:\\ - Complete Summary\\ - Personalized Summary\\ - Epics, Stories, Tasks};
\node[note, right=1.2cm of retro] (retro_output) {Output:\\ - Sprint Feedback\\ - Improvement Suggestions};

% Arrows
\draw[arrow] (transcript) -- (notetaker);
\draw[arrow] (notetaker) -- (human);
\draw[arrow] (human) -- node[above, font=\footnotesize] {Approved} (updatestate);
\draw[arrow] (updatestate) -- (meeting_type);
\draw[arrow] (meeting_type) -- ++(2.8,0) |- (daily);
\draw[arrow] (meeting_type) -- ++(2.8,0) |- (sprint);
\draw[arrow] (meeting_type) -- ++(2.8,0) |- (retro);

% Feedback loop
\draw[arrow] (updatestate) |- node[left, text width=2cm, align=left, font=\footnotesize] {Update project state} ([yshift=-3cm]transcript.south) -| (project_state);

% Connecting outputs
\draw[arrow] (daily) -- (daily_output);
\draw[arrow] (sprint) -- (sprint_output);
\draw[arrow] (retro) -- (retro_output);

% Group boxes
\begin{pgfonlayer}{background}
    \node[group, fit={($(notetaker.north west)+(-0.5,0.5)$) ($(updatestate.south east)+(0.5,-0.5)$)}, label={[anchor=north west]north west:\textbf{Processing \& Verification}}] (process_group) {};
    \node[group, fit={($(meeting_type.north west)+(-0.5,0.5)$) ($(daily_output.north east)+(0.5,0)$) ($(retro_output.south east)+(0.5,-0.5)$)}, label={[anchor=north west]north west:\textbf{Meeting Workflows}}] (workflow_group) {};
\end{pgfonlayer}

% Data flow visualization
\draw[decorate,decoration={brace,amplitude=10pt,raise=4pt},thick]
  ($(input_data)+(2.2,1.1)$) -- ($(project_state)+(2.2,-1.1)$) 
  node [right=-5pt, text width=3cm,align=center] {\footnotesize Input context};

% Add some explanatory text
\node[text width=4cm, align=left, font=\footnotesize, below=0.2cm of workflow_group] 
    {Each meeting type generates specific outputs tailored to its purpose.};

\end{tikzpicture}
\end{document}

