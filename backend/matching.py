import math
from datetime import datetime
from database import Profile, Match

#Computes interest similarity
def interest_similarity(vec1, vec2):
    def calc_magnitude(vector):
        magnitude = math.sqrt(sum(value ** 2 for value in vector.values()))
        return magnitude
    
    dot_product = sum(vec1[key] * vec2.get(key, 0) for key in vec1)
    mag1 = calc_magnitude(vec1)
    mag2 = calc_magnitude(vec2)

    if mag1 == 0 or mag2 == 0:
        return 0
    return dot_product / (mag1 * mag2)

#Computes major similarity
def major_similarity(major1, major2):
    college1graph = {
    'majorA': [('majorB', 0.9), ('majorC', 0.6)],
    'majorB': [('majorA', 0.9), ('majorC', 0.7)],
    'majorC': [('majorB', 0.7), ('majorA', 0.6)]
    }
    college2graph = {
    'majorD': [('majorE', 0.9), ('majorF', 0.6)],
    'majorE': [('majorA', 0.9), ('majorC', 0.7)],
    'majorF': [('majorB', 0.7), ('majorA', 0.6)]
    }
    
    colleges = [college1graph, college2graph]

    def get_college(major, colleges):
        for college in colleges:
            if major in college:
                return college
                
    maj1college = get_college(major1, colleges)
    maj2college = get_college(major2, colleges)

    score = 0
    if maj1college == maj2college:
        for m, s in maj1college[major1]:
            if m == major2:
                score = s
    else:
        score = 0.5

    if score is None:
        return 0
    else:
        return score
    
#Computes occupation similarity
def occupation_similarity(occ1, occ2):
    field1graph = {
    'occA': [('occB', 0.9), ('occC', 0.6)],
    'occB': [('occA', 0.9), ('occC', 0.7)],
    'occC': [('occB', 0.7), ('occA', 0.6)]
    }
    field2graph = {
    'occD': [('occE', 0.9), ('occF', 0.6)],
    'occE': [('occA', 0.9), ('occC', 0.7)],
    'occF': [('occB', 0.7), ('occA', 0.6)]
    }
    
    fields = [field1graph, field2graph]

    def get_field(occ, fields):
        for field in fields:
            if occ in field:
                return field
            
    occ1field = get_field(occ1, fields)
    occ2field = get_field(occ2, fields)

    score = 0

    if occ1field == occ2field:
        for o, s in occ1field[occ1]:
            if o == occ2:
                score = s
    else:
        score = 0.2

    if score is None:
        return 0
    else:
        return score
    
#Calculates education_similarity
def education_similarity(year1, year2):

    current_year = datetime.now().year
    year_map = {
        'Freshman': current_year-1,
        'Sophomore':current_year-2,
        'Junior':current_year-3,
        'Senior':current_year-4
    }

    min_year = min(year_map[year1], year_map[year2])
    max_year = max(year_map[year1], year_map[year2])

    def normalize(year, min_year, max_year):
        if max_year == min_year:
            return 1
        score = max_year - year
        normalized_score = (score - min_year) / (max_year - min_year)
        return normalized_score

    norm_year1 = normalize(year_map[year1], min_year, max_year)
    norm_year2 = normalize(year_map[year2], min_year, max_year)
    
    diff = abs(norm_year1 - norm_year2)
    
    similarity_score = 1 - diff
    
    return similarity_score

#Computes age similarity
def age_similarity(age1, age2, max_age_difference):
    score = 1 - abs(age1 - age2) / max_age_difference
    if score >= 0:
        return score
    else:
        return 0

#Computes gender similarity
def gender_similarity(gender1, gender2):
    return 1 if gender1 == gender2 else 0  

#get compatibility score between two users.
#NOTE: Pass in Profile objects, not User objects
max_age_difference = 10
def get_compatibility(user1, user2):
    interests_score = interest_similarity(user1.interests, user2.interests)
    major_score = major_similarity(user1.major, user2.major)
    occ_score = occupation_similarity(user1.career_interest, user2.career_interest)
    education_score = education_similarity(user1.education_level, user2.education_level)

    current_year = datetime.now().year
    age1 = current_year - user1.birthdate.year
    age2 = current_year - user2.birthdate.year
    age_score = age_similarity(age1, age2, max_age_difference)
    gender_score = gender_similarity(user1.gender, user2.gender)

    print(f"Interests:{interests_score}, Major:{major_score}, Occupation:{occ_score}, Education:{education_score},Age:{age_score}, Gender:{gender_score}")

    interests_w = 0.5
    major_w = 0.2
    occ_w = 0.1
    education_w = 0.1
    age_w = 0.05
    gender_w = 0.05

    total_score = interests_score * interests_w
    total_score += major_score * major_w
    total_score += occ_score * occ_w
    total_score += education_score * education_w
    total_score += age_score * age_w
    total_score += gender_score * gender_w

    return total_score

#Takes Profile object, not User object
#Generates the matches for a user, is called by profile_logic.py
def update_matches(sqlsession, user):
    all_profiles = sqlsession.query(Profile).filter(Profile.user_id != user.user_id).all()

    temp_query = sqlsession.query(Match.matched_user_id).filter_by(user_id=user.user_id).all()
    user_matches = [match[0] for match in temp_query]

    for other in all_profiles:
        score = get_compatibility(user, other)
        if other.user_id not in user_matches:
            entry1 = Match(user_id=user.user_id, matched_user_id=other.user_id, compatibility_score = score)
            entry2 = Match(user_id=other.user_id, matched_user_id=user.user_id, compatibility_score = score)
            sqlsession.add_all([entry1, entry2])
        else:
            match1 = sqlsession.query(Match).filter_by(user_id=user.user_id, matched_user_id=other.user_id).first()
            match2 = sqlsession.query(Match).filter_by(user_id=other.user_id, matched_user_id=user.user_id).first()
            if match1 and match2:    
                match1.compatibility_score = score
                match2.compatibility_score = score
    sqlsession.commit()

#Retrieves number of matches of a user
def get_matches(sqlsession, user_id, num_matches):
    #SQL query to join Match and Profile and order by compatibility score
    top_matches = sqlsession.query(Match, Profile).join(Profile, Profile.user_id == Match.matched_user_id).filter(Match.user_id == user_id).order_by(Match.compatibility_score.desc()).limit(num_matches).all()
    return top_matches

