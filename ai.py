from langchain.chat_models import ChatOpenAI
from langchain import ConversationChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
# from socketcallback import SocketIOCallback
from langchain.chains import LLMChain
import os

llm = ChatOpenAI(model='gpt-4', temperature=0.5, streaming=True)

doctor_helper_template = PromptTemplate(input_variables=["transcript"],
                                        template="""
You need to convert the following into Hindi
Transcript: {transcript}
""")

patient_instructions_template = PromptTemplate(input_variables=["summary"],
                                               template="""
{summary}
""")

doctor_helper = LLMChain(llm=llm, prompt=doctor_helper_template)
patient_instructor = LLMChain(llm=llm, prompt=patient_instructions_template)


# result = doctor_helper.run({"transcript": "I have fever since 3 days"}, callbacks=[StreamingStdOutCallbackHandler()])
# print(result)