# hackaton-mistral-studai

## What is it
StudAI is a revolutionary educational platform designed to make learning more efficient and effective. Leveraging the power of Retrieval-Augmented Generation (RAG) and the advanced Mistral Large Language Model (LLM), studAI transforms the way students interact with their study materials.

## What it does
studAI is an educational platform that enhances learning through AI technology. Here's a streamlined look at its features:

### Upload and Parse:

- Upload Documents: Students upload lectures, presentations, or research papers.
- AI Parsing: The system identifies and segments the document into chapters.

### Chapter and Level Selection:

- Select Chapter: Users choose the specific section they want to study.
- Select Level: Users choose their level of understanding of the chapter, influencing the difficulty of the generated exercices.

### Summarization:

- Get Summaries: studAI provides concise summaries of the chosen chapters, highlighting key points.

### Interactive Exercises:

- Fill-in-the-Blanks: The platform generates fill-in-the-blank exercises.
- Quizzes: It also creates multiple-choice quizzes based on the material.
### Instant Feedback:

- Automatic Correction: Students receive immediate corrections

## How we built it
### Summarization

We used a multi-agent system to refine a course chapter summary. Difficulty Level Agent:

Assesses whether the summary matches the expected complexity for the intended audience. Ensures the content is accessible yet challenging enough to meet course standards. Style and Ludic Critique Agent:

Focuses on making the summary engaging and playful. Enhances readability and enjoyment through a more interactive and entertaining style.

### Interactive Exercises

We set up a system that uses AI agents to create and critique educational exercises from book chapters. Here's the architecture :

Exercise Writer: This agent crafts fill-in-the-gaps exercises with exactly six gaps, tailored to different difficulty levels (Newbie, Intermediate, Advanced).

Critic Agent: Another agent evaluates these exercises based on their difficulty and how well they relate to the chapter content. It provides feedback aimed at improving the clarity and educational value of the exercises.

# Set Up
