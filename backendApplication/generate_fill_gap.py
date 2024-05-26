from langchain.memory import ConversationBufferMemory
from langchain import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI


def init_exercise_writer(llm:ChatMistralAI, revtrieved_chunks:str):
    # Define the template for the Exercise Writer
    system_message_fgap_choice = f"""
    You are the exercise creator. Your task is to generate a fill-in-the-gaps exercise based on a given chapter of a book, using no more than 100 words. The exercise should be relevant to the chapter's topic and designed to reinforce the reader's understanding of the material.

    You always put 6 gaps in your exercise

    You will create exercises based on the level of difficulty chosen by the user:
    - Newbie: for readers who are just starting to learn the subject. The correct answers should be clear and obvious, while the false answers should be easily distinguishable.
    - Intermediate: for readers who have some prior knowledge and experience with the subject. The correct answers should be more challenging, but still distinguishable from the false answers.
    - Advanced: for readers who are proficient in the subject and seeking a challenge. The correct answers should be subtly different from the false answers, requiring a deep understanding of the material.

    You Must always put 6 gaps inside your exercise at all costs. if you put more than 6 gaps or less than 6 gaps, your generation is considered as incorrect.

    All of your gaps need to be different from each other. Try to be the least repetitive as you can.

    The chapter you will be working with is provided below:
    ----
    {revtrieved_chunks}
    ----
    """ + """
    Your response will only be written as the following:            

    {{"exercise": {{
        "content" : "The fill-in-the-gaps exercise you have created. Each gap should be represented by a unique key, e.g. <gap_1>, <gap_2>",
        "answers" : {{
            "<gap_1>" : {{
                "correct" : "the correct answer for the first gap",
                "false" : "a false answer for the first gap"
                }},
            "<gap_2>" : {{
                "correct" : "the correct answer for the second gap",
                "false" : "a false answer for the second gap"
                }},
            ...
            }}
        }}
    }}     
    """

    human_message = "{difficulty}"

    exercise_template = ChatPromptTemplate.from_messages([("system", system_message_fgap_choice), ("human", human_message)])


    # Create a memory for the Exercise Writer
    exercise_memory = ConversationBufferMemory()

    # Create the Exercise Writer chain
    exercise_writer_chain = LLMChain(
        llm=llm,
        prompt=exercise_template,
        memory=exercise_memory
    )

    return exercise_writer_chain

def init_critic(llm:ChatMistralAI, revtrieved_chunks:str):
    # Define the template for Critic Agent
    system_message_critic = f"""
    You are the exercise critic. Your task is to evaluate the following exercise based on the difficulty level and the accuracy of the exercise with respect to the content of the chapter.

    Your response should include validation of the difficulty level and the accuracy of the exercise, along with suggestions for improvement if necessary.

    Based on the given input file, you will only give your advice. If you rewrite the content of the exercise, this will be considered as invalid.

    Your answer needs to be straight to the point

    This is the content of the chapter:
    ----
    {revtrieved_chunks}
    ----
    """ + """
    The exercise provided to you will always be in this format and needs to contains always 6 holes:          

    {{"exercise": {{
        "content" : "The fill-in-the-gaps exercise that will be given to you. Each gap should be represented by a unique key, e.g. <gap_1>, <gap_2>",
        "answers" : {{
            "<gap_1>" : {{
                "correct" : "the correct answer for the first gap",
                "false" : "a false answer for the first gap"
                }},
            "<gap_2>" : {{
                "correct" : "the correct answer for the second gap",
                "false" : "a false answer for the second gap"
                }},
            ...
            }}
        }}
    }}
    """

    human_message_critic = "{exercise}"

    critic_template = ChatPromptTemplate.from_messages([("system", system_message_critic), ("human", human_message_critic)])

    # Create the Critic Agent 1 chain
    critic_chain = LLMChain(
        llm=llm,
        prompt=critic_template
    )

    return critic_chain

def invoke_chain_of_agents(difficulty:str, writter:LLMChain, critic_chain:LLMChain):
    # Step 1: Generate the initial exercise
    exercise = writter.invoke({"difficulty": difficulty})

    # Step 2: Critic Agent 1 evaluates the exercise
    evaluation_1 = critic_chain.invoke({"exercise": exercise['text']})
    print("Evaluation by Critic 1:", evaluation_1['text'])

    # Integrate feedback from Critic 1 and regenerate the exercise
    improved_exercise = writter.invoke({"text": evaluation_1['text']})

    return improved_exercise

def generate_fill_gap(revtrieved_chunks:str, difficulty:str):
    llm = ChatMistralAI(api_key = "ImsUHfFLA6OjlX6mARbnM1YcDOy7ujsq", model = "open-mixtral-8x22b", temperature=0)
    writter = init_exercise_writer(llm, revtrieved_chunks)
    critic = init_critic(llm, revtrieved_chunks)

    return invoke_chain_of_agents(difficulty, writter, critic)
    

    