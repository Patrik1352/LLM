import os
from database import VectorDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage



class VideoSearcher:
    def __init__(self, db, video_base_path='/content/drive/MyDrive/Итоговый проект/data/video'):
        self.db = db
        self.video_base_path = video_base_path

    def get_video_info(self, query):
        result = self.db.search(query, k=1)[0]
        file_name = result['file_name'].replace('.txt', '.mp4')
        video_path = os.path.join(self.video_base_path, file_name)
        summary = result.get('summarization', '')
        return video_path, summary

    def polite_response(self, query, summary):
        model = ChatOpenAI(temperature=1, model='gpt-4o')
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Ты врач-помощник для людей больных ревматоидным артритом. На основе краткого описания видео и запроса пользователя, сформулируй ответ, что найдено подходящее видео. Добавь, что всегда стоит проконсультироваться с врачом."),
            ("human", "Запрос пользователя: {query}\nОписание видео: {summary}\nОтветь вежливо и кратко.")
        ])
        chain = prompt | model
        return chain.invoke({'query': query, 'summary': summary}).content

    def search_video(self, query):
        video_path, summary = self.get_video_info(query)
        response = self.polite_response(query, summary)
        return video_path, response