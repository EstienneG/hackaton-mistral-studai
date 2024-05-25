# -*- coding: utf-8 -*-
"""generateSummaryFromDocuments - Copie.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1no5Dx7_JIRgw2A0XfDj92VmSjHzPy6sX

<h2>Demo from a pdf. Replace pdf_content[0] in the first call of the writer to make it functionnal</h2>

# Imports, init modèle de langue et du parser
"""

from langchain_mistralai import ChatMistralAI
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser


def generate_summary_from_document(input: str) -> str:

    llm = ChatMistralAI(api_key = "ImsUHfFLA6OjlX6mARbnM1YcDOy7ujsq")

    output_parser = StrOutputParser()

    writer_prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are the redactor. Given a chapter of a book, you are able to write a small course in less than 300 words, that is very ludic and interesting about the topic of the corresponding document.
        You need to adapt the informations that you teach based on 3 levels of difficulty:
        - Newbie
        - Intermediate
        - Advanced
        """
        ),
        ("user", "{input}"),
        ])

    # Notice that we need to align the `memory_key`
    memory = ConversationBufferMemory(memory_key="writer_history")

    writer_conversation = LLMChain(
        llm=llm,
        prompt=writer_prompt,
        verbose=True,
        memory=memory
    )

    first_summary = writer_conversation.run('You are going to summarize for a Newbie. Here is the information : ' + input)

    """<h2>Definition of the difficulty critic and answer of the writer</h2>"""

    difficulty_critic_prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are the critic. You are part of a course redaction team experts that creates very ludic and interesting courses based on real books to make them more readable and interactive. Your role in this group is to evaluate the course written by the redactor so that it respects the level of difficulty asked by the user.
        Ther 3 levels of difficulty:
        - Newbie
        - Intermediate
        - Advanced

        You will critic the course given by the redactor evaluate if it respects the difficulty level and explain why.
        """
        ),
        ("user", "{input}"),
        ])


    difficulty_critic_chain = difficulty_critic_prompt | llm | output_parser
    difficulty_critic_output = difficulty_critic_chain.invoke(first_summary)

    summary_difficulty_critiqued = writer_conversation.run(difficulty_critic_output)


    style_critic_prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are the critic. You are part of a course redaction team experts that creates very ludic and interesting courses based on real books to make them more readable and interactive. Your role in this group is to evaluate the course written by the redactor so that it is ludic and interesting.
        You will critic the course given by the redactor, evaluate if it is ludic and interesting and explain why.
        """
        ),
        ("user", "{input}"),
        ])


    style_critic_chain = style_critic_prompt | llm | output_parser
    style_critic_output = style_critic_chain.invoke(summary_difficulty_critiqued)

    summary_style_critiqued = writer_conversation.run(style_critic_output)

    return summary_style_critiqued