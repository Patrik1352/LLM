from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


class RAGSystem:
    def __init__(self, db):
        """
        Инициализирует систему RAG, загружая базу данных векторов.
        
        Аргументы:
            db: Экземпляр базы данных векторов.
        """
        self.db = db
    
    def search_database(self, query, k=5):
        """
        Выполняет поиск в базе данных по запросу.
        
        Аргументы:
            query: Текстовый запрос для поиска.
            k: Количество возвращаемых релевантных элементов.
            
        Возвращает:
            Список словарей с результатами поиска.
        """
        return self.db.search(query, k=k)
    
    def _prepare_messages(self, query, context_items):
        """
        Формирует сообщения для отправки в ChatGPT.
        
        Аргументы:
            query: Вопрос пользователя.
            context_items: Список словарей с контекстом из базы данных.
            
        Возвращает:
            Список сообщений для отправки модели.
        """
        messages = []
        context_texts = []
        context_tables = []
        context_images = []
        
        # Собираем данные из контекста
        for item in context_items:
            if 'text' in item:
                context_texts.append(item['text'])
            if 'tables' in item and item['tables']:
                context_tables.extend(item['tables'])
            if 'images' in item and item['images']:
                context_images.extend(item['images'])
        
        # Добавляем изображения в сообщения
        for image in context_images:
            image_message = {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image}"},
            }
            messages.append(image_message)
        
        # Формируем текстовое сообщение
        text_content = f"Вопрос пользователя: {query}\n\n"
        
        if context_texts:
            text_content += "Текстовый контекст:\n" + "\n\n".join(context_texts) + "\n\n"
        
        if context_tables:
            text_content += "Таблицы:\n" + "\n\n".join(context_tables) + "\n\n"
        
        text_message = {
            "type": "text",
            "text": text_content,
        }
        messages.append(text_message)
        
        return [HumanMessage(content=messages)]
    
    def query_ai(self, query, k=5):
        """
        Выполняет запрос к ИИ с учетом контекста из базы данных.
        
        Аргументы:
            query: Вопрос пользователя.
            k: Количество релевантных элементов для поиска.
            
        Возвращает:
            Ответ от ChatGPT.
        """
        # Поиск в базе данных
        results = self.search_database(query, k=k)
        
        # Подготовка сообщений
        messages = self._prepare_messages(query, results)
        
        # Настройка модели и промпта
        model = ChatOpenAI(temperature=1, model='gpt-4o')
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Ты врач-помощник для людей больных ревматоидным артритом. Помогай, отвечая на вопросы. Также тебе будет представлен контекст из последних научных статей. Используй их для ответа. Также не забывай в конце ответа добавить, что ты AI-помощник, и всегда нужна консультация с врачом"),
            ("human", "{messages}")
        ])
        
        # Выполнение запроса
        chain = prompt | model
        return chain.invoke({'messages': messages}).content