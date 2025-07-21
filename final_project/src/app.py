import random
from database import VectorDatabase
from pdf_search import RAGSystem
from video_search import VideoSearcher
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Заглушка для определения типа запроса (видео или нет)
def is_video_query(qwery: str) -> bool:
    model = ChatOpenAI(temperature=1, model='gpt-4o')

    prompt = ChatPromptTemplate([("system", "Ты полезный ассистент. Формат вывода True или False"),
                             ("human", '''Тебе передается запрос пользователя. Тебе нужно определить есть ли в запросе:
запрос на предоставление видео (пришли видео, скинь видео, запись и тп).
Если такой запрос есть, то отправь True. Если нет, то отправь False
Вот запрос:
{qwery}
Не пиши ничего лишнего. Отвечай сразу True или False''')])

    chain = prompt | model

    return chain.invoke({'qwery':qwery}).content

class App:
    def __init__(self, api_key, 
    video_db_path ="/content/drive/MyDrive/Итоговый проект/data/openai_embeddings_db/video_bd", 
    pdf_db_path = "/content/drive/MyDrive/Итоговый проект/data/openai_embeddings_db/openai_embeddings_db"):
        pdf_db = VectorDatabase(api_key = api_key)
        pdf_db.load(pdf_db_path)
        self.rag = RAGSystem(pdf_db)

        video_db = VectorDatabase(api_key = api_key)
        video_db.load(video_db_path)
        self.video_searcher = VideoSearcher(video_db)
        

    def process_query(self, query: str):
        if eval(is_video_query(query)):
            video_path, polite_answer = self.video_searcher.search_video(query)
            return {
                'type': 'video',
                'video_path': video_path,
                'answer': polite_answer
            }
        else:
            answer = self.rag.query_ai(query)
            return {
                'type': 'text',
                'answer': answer
            } 