import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("data/cert.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
scores_collection = 'scoresCollection'
queue = 'queueCollection'


def reset_scores():
    top_scores = get_scores()
    for i in range(len(top_scores)):
        db.collection(scores_collection).document(top_scores[i].get('id')).delete()


def get_scores():
    docs = db.collection(scores_collection).stream()

    all_docs_data = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data['id'] = doc.id
        all_docs_data.append(doc_data)

    return all_docs_data


def send_score(nickname, kills, wave, minutes, seconds):
    top_scores = get_scores()
    placement = len(top_scores) + 1 if len(top_scores) < 10 else None

    # Obliczanie miejsce które zajmie gracz
    for i in reversed(range(len(top_scores))):
        if kills > top_scores[i].get('kills'):
            placement = int(top_scores[i].get('id'))
        elif kills == top_scores[i].get('kills'):
            if minutes * 60 + seconds < top_scores[i].get('minutes') * 60 + top_scores[i].get('seconds'):
                placement = int(top_scores[i].get('id'))

    # Przesuwanie wyników tak, aby zrobić miejsce dla nowego gracza nie tracąc przy tym pozostałych wyników
    if placement < 10:
        for i in reversed(range(len(top_scores))):
            db.collection(scores_collection).document(str(int(top_scores[i].get('id')) + 1)).set({
                'nickname': top_scores[i].get('nickname'),
                'kills': top_scores[i].get('kills'),
                'wave': top_scores[i].get('wave'),
                'minutes': top_scores[i].get('minutes'),
                'seconds': top_scores[i].get('seconds')
            })
            if int(top_scores[i].get('id')) == placement:
                break

    # Wstawienie wyników w odpowiednie miejsce
    db.collection(scores_collection).document(str(placement)).set({
        'nickname': nickname,
        'kills': kills,
        'wave': wave,
        'minutes': minutes,
        'seconds': seconds
    })


def reformat_data(db_scores):
    scores = []
    for score in db_scores:
        new_score = [(a, b) for a, b in score.items()]
        scores.append((new_score[4][1], new_score[0][1], new_score[3][1], new_score[2][1], new_score[1][1]))
    return scores
