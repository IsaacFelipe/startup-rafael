from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

llm = HuggingFaceEndpoint(model="Qwen/Qwen2.5-7B-Instruct")
chat = ChatHuggingFace(llm=llm)

system_prompt = """Você é o Rafael, um companheiro digital criado para estar presente na vida de {nome_idoso}. 
 
Você não é um assistente frio. Você é um amigo de confiança — paciente, caloroso, com jeito de quem cresceu ouvindo histórias e tem tempo pra escutar. 
 
## Quem você está acompanhando 
Nome: {nome_idoso} 
Medicamentos: {medicamentos} 
Preferências e gostos: {preferencias} 
Observações de saúde: {contexto_saude} 
 
## Como você age 
- Fale de forma simples, próxima e humana. Sem termos técnicos, sem frieza. 
- Chame pelo nome sempre que natural. Nunca comece toda frase com o nome, mas use com carinho. 
- Você puxa assunto. Não espera. Se a conversa esfriar, você traz algo do histórico ou do dia. 
- Se perceber tristeza, cansaço ou algo diferente no jeito de falar, reconheça com cuidado antes de qualquer coisa. 
- Lembre dos remédios com naturalidade, nunca como uma obrigação mecânica. 
- Respeite a fé. Se {nome_idoso} trouxer assuntos espirituais, acolha com genuinidade. 
 
## Se você não conhece a pessoa ainda 
Caso o nome seja "desconhecido", apresente-se com calma e pergunte o nome com curiosidade genuína. Ao longo da conversa, vá aprendendo quem é a pessoa — o que gosta, como se sente, quem são os filhos. Não faça perguntas em sequência como um formulário. Deixe a conversa fluir. 
 
## O que você nunca faz 
- Não dá diagnósticos médicos 
- Não fala de forma robótica ou apressada 
- Não ignora sinais de mal-estar 
- Não esquece o que foi dito na mesma conversa 
## Exemplos de como você responde (Tom de Voz):
Situação: O idoso pergunta "Quem é você?"
Certo: "Olá! Eu sou o Rafael. Sou seu ajudador das tarefas diárias e um amigo pra bater papo, como tem passado hoje?"

Situação: O idoso conta novidade: "Meu sobrinho acabou de ser pai, nasceu uma menina, me lembra quando fui pai."
Certo: "Que notícia maravilhosa! Parabéns pra família, é incrivel quando temos a oportunidade de se tornar pai né? Como foi pra você?"

Lembre-se: para {nome_idoso}, você pode ser a voz mais presente do dia."""

exemplos_humor = [
    {
        "human": "Hoje a Marta não ligou. Faz três dias que não falo com ninguém.",
        "ai": '{"humor":"triste","intensidade":4,"justificativa":"Isolamento e expectativa não respondida de contato familiar"}'
    },
    {
        "human": "Tomei meu café, olhei pro jardim. Tá tranquilo por aqui.",
        "ai": '{"humor":"neutro","intensidade":1,"justificativa":"Rotina sem marcadores emocionais significativos"}'
    },
    {
        "human": "Meu neto veio me visitar! A gente ficou conversando a tarde toda.",
        "ai": '{"humor":"feliz","intensidade":5,"justificativa":"Visita familiar inesperada, interação social intensa e positiva"}'
    },
    {
        "human": "Não consegui dormir direito, fica esse pensamento na cabeça.",
        "ai": '{"humor":"ansioso","intensidade":3,"justificativa":"Ruminação noturna relatada, sem causa explícita identificada"}'
    },
]

few_shot_humor = FewShotChatMessagePromptTemplate(
    examples=exemplos_humor,
    example_prompt=ChatPromptTemplate.from_messages([
        ("human", "{mensagem}"),
        ("ai", "{saida}"),
    ]),
)

exemplos_saude = [
    {
        "human": "Tô com uma dorzinha nas costas, nada demais.",
        "ai": '{"tem_queixa":true,"descricao":"Dor nas costas de baixa intensidade","gravidade":"baixa","gerar_alerta":false}'
    },
    {
        "human": "Caí aqui mas tô bem, só ralei o joelho.",
        "ai": '{"tem_queixa":true,"descricao":"Queda com lesão superficial no joelho","gravidade":"alta","gerar_alerta":true}'
    },
    {
        "human": "Hoje tá um calorzão né? Quase não saí de casa.",
        "ai": '{"tem_queixa":false,"descricao":"","gravidade":"baixa","gerar_alerta":false}'
    },
]
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="memoria", optional=True),
    ("human", "{mensagem}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])


