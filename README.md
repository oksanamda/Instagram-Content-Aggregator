# Aвтоматический агрегатор данных с Инстаграм.

Получение данных с помощью Scrapy, используя браузер Scrapy API.
Данные представляют собой картинку+текст. Плюс прослойка с ElasticSearch и нейронной сетью, которая будет распознавать содержание картинки и краткую суть текстов, пары персонаж - отношение + Клиент поиска постов и графа общих трендов отношения к людям (в русской зоне, с архитектурой на Истио).

# Что требовалось реализовать?
* Сбор данных с Instagram по ключевому слову (хэштегу). Данные должны содержать в себе информацию о постах, содержащих это слово - картинку, описани. Для дальнейшей работы так же необходимы количество комментариев и комментарии.
* Прикрепление нейронной сети, которая будет распознавать содержание картинки.
* Прикрепление нейронной сети, которая будет распознавать краткую суть текстовю
* Прослойка ElasticSearch. 
* Веб-сервис, позволяющий пользователю использовать приложение.
* Сентимент-анализ комментариев под каждым постом по выбранному слову для получения пар персонаж-отношение. 
* Построение графика, отражающего отношения. 
* Распределение частей проекта по контейнером. 
* Создание архитектуры на Истио. 

# Результаты. 
Проект выполнен. Однако, на данный момент отключена нейронная сеть, которая распознаёт краткую суть текстов под постами по причине того, что не запуск требует слишком серьезных технических характеристик, которых, к сожалению, не имеет ни один участник проекта (предполагалось использование нейронной сети из библиотеки Hugging Face для text summarisation). 

