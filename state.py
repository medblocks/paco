from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(ai_prefix="Paco", human_prefix="Patient")
memory.chat_memory.add_ai_message(
    "Hello, I'm Paco, your medical knowledge assistant. How can I assist you today with your prescriptions?"
)

memory.chat_memory.add_user_message

state_store = {
    "transcript": "",
    "doctor_summary": "",
    "patient_instruction_memory": memory,
    "patient_mode": False,
    "patient_recording": False
}
