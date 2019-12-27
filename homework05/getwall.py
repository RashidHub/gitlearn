import pandas as pd
import requests
import pymorphy2
import gensim
from nltk.corpus import stopwords
import pyLDAvis.gensim


def get_wall(
    owner_id: str = '',
    domain: str = '',
    offset: int = 0,
    count: int = 150,
    filter: str = 'owner',
    extended: int = 0,
    fields: str = '',
    v: str = '5.103'
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.
    @see: https://vk.com/dev/wall.get
    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.
    """
    code = ("return API.wall.get({" +
            f"'owner_id': '{owner_id}'," +
            f"'domain': '{domain}'," +
            f"'offset': {offset}," +
            f"'count': {count}," +
            f"'filter': '{filter}'," +
            f"'extended': {extended}," +
            f"'fields': '{fields}'," +
            f"'v': {v}," +
            "});")

    response = requests.post(
        url="https://api.vk.com/method/execute",
        data={
            "code": code,
            "access_token": #token,
            "v": '5.103'
        }
    )
    return pd.DataFrame(response.json()['response']['items'])


if __name__ == "__main__":

    morph = pymorphy2.MorphAnalyzer()

    wall = get_wall(domain='leftradicalmuslesplatinum')
    new_wall = get_wall(domain='typical_olimp')
    wall = wall.append(new_wall, ignore_index=True)
    new_wall = get_wall(domain='opyatmetel')
    wall = wall.append(new_wall, ignore_index=True)

    posts = []
    letters = set()

    for i in range(ord("a"), ord("z") + 1):
        letters.update(chr(i))
    for i in range(ord("а"), ord("я") + 1):
        letters.update(chr(i))
    letters.update("ё")

    stop_words = stopwords.words("russian")
    symbs = {'.', ',', ';', ':', '-', '—', '–', '"', "'", "`", "?", "!"}

    for i in range(len(wall)):
        stroka = wall['text'][i]
        stroka = str(stroka)
        output = []
        for word in stroka.split():
            word = morph.parse(word)[0]
            if ('NOUN' in word.tag):
                word = word.normal_form
                if word not in stop_words:
                    ok = 1
                    temp_word = ''
                    for letter in word:
                        if letter in letters:
                            temp_word += letter
                        elif (letter not in letters) and (letter not in symbs):
                            ok = 0
                    if ok == 1:
                        output.append(temp_word)
        posts.append(output)

    dictionary = gensim.corpora.Dictionary(posts)
    corpus = []
    for i in posts:
        corpus.append(dictionary.doc2bow(i))
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=dictionary,
                                           num_topics=3,
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=5,
                                           alpha='auto',
                                           per_word_topics=False)
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
    pyLDAvis.show(vis)
