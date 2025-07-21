# 🤖 Домашние задания по трансформерам (Transformers Homework)

Этот репозиторий содержит решения пяти заданий, направленных на глубокое погружение в архитектуру и практическое применение трансформеров — от реализации с нуля до дообучения моделей на прикладные задачи.

---

## 📁 Содержание

- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://drive.google.com/file/d/16I3g702jThO-InOyiVDj-NTJZOLZe70x/view?usp=drive_link) [`Transformer`](./transformer.ipynb) — **Создание трансформера с нуля**
- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://drive.google.com/file/d/1HPiXifZlNX7MwrtT-_83XKgZCungn2qT/view?usp=drive_link) [`BERT_QA`](./bert_qa.ipynb) — **Решение задачи Question Answering**
- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://drive.google.com/file/d/1GFGIqh3FiFGLMl2FmKwy7mJEvOejZRJq/view?usp=drive_link) [`SFT_T5`](./SFT_T5.ipynb) — **Файнтюнинг модели T5 для генерации заголовков**
- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://drive.google.com/file/d/1bFOxFK8oGVVnxHGML-dUzxgWXByuz6nk/view?usp=drive_link) [`Guard_LLM`](./Guard_LLM.ipynb) — **Фильтрация опасного контента и изучение векторных баз данных**
- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://drive.google.com/file/d/1tpLFS2QWopXahQ5gULKyCZ7RA-6TyDyN/view?usp=drive_link) [`QLoRa`](./LoRa.ipynb) — **Дообучение Mistral методом LoRA и обработка PDF-документов**
- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://drive.google.com/file/d/14KdeNLJj6q87Vq5nKq3Yjy0558mGUTgG/view?usp=drive_link) [`vllm`](./vllm.ipynb) — **Оптимизация LLM с помощью vLLM: квантизация и speculative decoding**
---

## 🔧 `Transformer`: Реализация трансформера с нуля

> Основная цель — реализовать трансформер без использования `transformers`, включая:
- Механизм Multi-Head Attention
- Позиционное кодирование
- Feed-forward слой
- Encoder и Decoder блоки
- Финальную архитектуру Encoder-Decoder

🔍 Полезно для глубокого понимания архитектуры и механики трансформеров.

---

## 📚 `BERT_QA`: Fine-tuning BERT для Question Answering

> Решение задачи **вопрос-ответ** на датасете [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/):

- Используется модель `distilbert-base-cased` для поиска ответов.
- Реализована токенизация с учетом скользящих окон.
- Метрики: F1 и Exact Match.
- Используются библиотеки `transformers`, `datasets`, `evaluate`.

📌 Отличный пример практического применения моделей BERT-подобного типа.

---

## 📰 `SFT_T5`: Дообучение T5 на задачу суммаризации

> Цель — научить модель T5 генерировать заголовки по содержимому статей с портала Medium:

- Загружается кастомный датасет из CSV с текстами и заголовками.
- Используется модель `t5-base`.
- Выполняется предобработка данных и фильтрация.
- Настроена загрузка модели в Hugging Face Hub.
- Создан интерактивный интерфейс с `Streamlit` и опубликован в Hugging Face Spaces.

🚀 Хороший пример end-to-end пайплайна: от обучения до деплоя.

---

## 🛡️ `Guard_LLM`: Фильтрация опасного контента и векторные базы данных

> Основные задачи:
- Добавление запрещенных тем для модели Llama-Guard.
- Изучение работы модели против prompt injection.
- Исследование принципов работы векторных баз данных и методов индексации.

🔒 Важно для создания безопасных AI-ассистентов.

---

## 🍋 `QLoRa`: Дообучение Mistral методом LoRA и обработка PDF

> Ключевые аспекты:
- Тестирование предобученной модели в роли чат-бота магазина.
- Дообучение модели Mistral 7B методом LoRA.
- Изучение методов обработки PDF-документов (текст, изображения, таблицы).
- Практическое применение для парсинга документов.

📄 Полезно для работы с мультимодальными данными в RAG-системах.

## ⚡ `vLLM`: Оптимизация LLM с помощью vLLM

> Основные темы:
- Изучение методов квантизации (AWQ, GPTQ)
- Практическая реализация speculative decoding
- Работа с фреймворком vLLM для оптимизации инференса
- Сравнение производительности разных методов ускорения

🚀 Полезно для понимания оптимизации LLM в продакшн-среда

## 🏥 `MedicalAssistant`: Итоговый проект - AI-ассистент для пациентов с ревматоидным артритом

> Ключевые особенности проекта:
- 🤖 Telegram-бот для удобного взаимодействия с пациентами
- 📚 RAG-система на 31 PDF-документе медицинских рекомендаций
- 🎥 Мультимодальный поиск по 10 обучающим видео
- 🧠 GPT-4o для генерации ответов с медицинским контекстом
- 🔍 FAISS для эффективного векторного поиска
- ⚠️ Автоматическое предупреждение: "Я AI-помощник. Проконсультируйтесь с врачом."

Используемые технологии:
🦜🔗 LangChain + ChatOpenAI (gpt-4o)
🧠 FAISS для векторного поиска
📄 Unstructured для обработки PDF (текст, таблицы, изображения)
🎬 Whisper для транскрибации видео
🤖 python-telegram-bot
☁️ Хранение в Google Drive

---

## 🛠️ Используемые технологии

- `PyTorch`
- `Hugging Face Transformers`
- `Datasets`
- `NLTK`, `evaluate`, `Streamlit`
- `Google Colab` + `Google Drive`
- `Hugging Face Hub & Spaces`
- `PEFT` (LoRA)
- `Unstructured` (обработка PDF)
- `vLLM, AutoAWQ`
---

## 📌 Автор

Егор Быков

---

## 🧠 Лицензия

MIT — свободно используйте, улучшайте, дообучайте и делитесь своими результатами!
