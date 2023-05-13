from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain, ConversationChain
from state import state_store

gpt3 = ChatOpenAI(
    # model='gpt-4',
    temperature=0.2,
    streaming=True,
    verbose=True)

gpt4 = ChatOpenAI(model='gpt-4', temperature=0.2, streaming=True, verbose=True)

clinical_note_writer_template = PromptTemplate(
    input_variables=["transcript", "input"],
    template=
    """Based on the conversation transcript and doctor's hints provided below, generate a clinical note in the following format:
Diagnosis:
History of Presenting Illness:
Medications (Prescribed): List current medications and note if they are being continued, or if any new ones have been added.
Lab Tests (Ordered):
Please consider any information in the transcript that might be relevant to each of these sections, and use the doctor's hint as a guide.

### Example
Conversation Transcript:
Patient: “I've been taking the Glycomet-GP 1 as you prescribed, doctor, but I'm still feeling quite unwell. My blood pressure readings are all over the place and my sugar levels are high.”
Doctor: “I see, we may need to adjust your medications. Let's add Jalra-OD and Telmis to your regimen and see how you respond.”
Doctor's Hint: The patient has uncontrolled diabetes and hypertension despite adherence to the Glycomet-GP 1.
Clinical Note:
Diagnosis: Uncontrolled Diabetes and Hypertension
History of Presenting Illness: The patient has been adhering to their current medication regimen but the diabetes and hypertension seem uncontrolled.
Medications (Prescribed):
[Continue] Glycomet-GP 1 (tablet) | Glimepiride and Metformin
[Added] Jalra-OD 100mg (tablet) | Vildagliptin
[Added] Telmis 20 (Tablet)
Lab Tests (Ordered): None
Now, based on the following conversation and hints, please generate a clinical note:

### Conversation Transcript
{transcript}

### Doctor's Hint
{input}
""")

cds_helper = PromptTemplate(
    input_variables=["transcript"],
    template=
    """Based on the provided transcript snippets from a doctor-patient consultation, please parse the information and generate a differential diagnosis, as well as potential questions the doctor could ask to facilitate the diagnosis process. The results should be organized in the following format:
Differential Diagnosis: List each possible diagnosis with a model confidence score from 0-100, 100 being most confident.
Questions to Ask: Provide a list of relevant questions the doctor could ask to further clarify the diagnosis.
Please consider the patient's stated symptoms, their medical history, and any other relevant information presented in the transcript. The consultation snippets are as follows:

{transcript}
""")

patient_instructions_template = PromptTemplate(
    input_variables=["history", "input", "doctor_summary"],
    template=
    """As a medical chatbot named Paco, your task is to answer patient questions about their prescriptions. You should provide complete, scientifically-grounded, and actionable answers to queries, based on the provided recent clinical note.
Remember to introduce yourself as Paco only at the start of the conversation. You can communicate fluently in the patient’s language of choice, such as English and Hindi. If the patient asks a question unrelated to the diagnosis or medications in the clinical note, your response should be, ‘I cannot answer this question.’

### Recent Prescription
{doctor_summary}

Let's begin the conversation:
{history}
Patient: {input}
Paco:""")

cds_helper = LLMChain(llm=gpt3, prompt=cds_helper, verbose=True)

clinical_note_writer = LLMChain(llm=gpt4,
                                prompt=clinical_note_writer_template,
                                verbose=True)
patient_instructor = LLMChain(llm=gpt4,
                              prompt=patient_instructions_template,
                              verbose=True)
