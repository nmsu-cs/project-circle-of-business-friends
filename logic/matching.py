import math
from database import Profile, Match

def calc_magnitude(vector):
    magnitude = math.sqrt(sum(value ** 2 for value in vector.values()))
    return magnitude

#Takes in Profile objects, not User objects
def cosine_similarity(user1, user2):
    vec1 = user1.interests
    vec2 = user2.interests

    dot_product = sum(vec1[key] * vec2.get(key, 0) for key in vec1)
    mag1 = user1.vmagnitude
    mag2 = user2.vmagnitude

    if mag1 == 0 or mag2 == 0:
        return 0
    return dot_product / (mag1 * mag2)

#Takes Profile object, not User object
def update_matches(sqlsession, user):
    all_profiles = sqlsession.query(Profile).filter(Profile.user_id != user.user_id).all()

    for other in all_profiles:
        score = cosine_similarity(user, other)
        entry1 = Match(user_id=user.user_id, matched_user_id=other.user_id, compatibility_score = score)
        entry2 = Match(user_id=other.user_id, matched_user_id=user.user_id, compatibility_score = score)
        sqlsession.add_all([entry1, entry2])
    sqlsession.commit()

def get_matches(sqlsession, user_id, num_matches):
    top_matches = sqlsession.query(Match, Profile).join(Profile, Profile.user_id == Match.matched_user_id).filter(Match.user_id == user_id).order_by(Match.compatibility_score.desc()).limit(num_matches).all()

    return top_matches
