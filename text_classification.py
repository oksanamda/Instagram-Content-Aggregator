from transformers import pipeline

classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

candidate_labels = ['путешествие', 'готовка', 'танцы', 'еда', 'друзья', 'животные', 'кошка',
                    'собака', 'семья', 'праздник', 'учеба', 'образование', 'школа', 'университет', 'дети',
                    'отдых', 'работа', 'погода', 'зима', 'лето', 'весна', 'осень', 'каникулы', 'отпуск',
                    'солнце', 'праздник', 'новый год', 'день рождения', 'подарки', 'техника', 'любовь', 'отношения']

sequence_to_classify = "однажды я смогу увидеть весь мир"

res = classifier(sequence_to_classify, candidate_labels)
res_label = list(res.values())[1][0]
