import pandas as pd
from surprise import Dataset, Reader
from surprise import SVD
from surprise.model_selection import train_test_split
from surprise import accuracy

RATING_MIN, RATING_MAX = 1, 5

# utf-8-sig strips the byte-order mark at the start of file.csv
dataset = pd.read_csv("file.csv", encoding="utf-8-sig")

# Validate ratings: drop rows with missing values and clip ratings into the 1-5 scale
before = len(dataset)
dataset = dataset.dropna(subset=['user', 'item', 'rating'])
dataset['rating'] = pd.to_numeric(dataset['rating'], errors='coerce')
dataset = dataset.dropna(subset=['rating'])
out_of_range = ((dataset['rating'] < RATING_MIN) | (dataset['rating'] > RATING_MAX)).sum()
dataset['rating'] = dataset['rating'].clip(RATING_MIN, RATING_MAX)
print(f'Loaded {before} ratings; dropped {before - len(dataset)} invalid rows; '
      f'clipped {out_of_range} ratings into the {RATING_MIN}-{RATING_MAX} range.')

reader = Reader(rating_scale=(RATING_MIN, RATING_MAX))
data = Dataset.load_from_df(dataset[['user', 'item', 'rating']], reader)

trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

algo = SVD(random_state=42)
algo.fit(trainset)
predictions = algo.test(testset)

rmse = accuracy.rmse(predictions)
print(f'RMSE: {rmse}')

# User ids in file.csv are lowercase ('user1'); match case-insensitively
requested_user = 'User1'
known_users = {u.lower(): u for u in dataset['user'].unique()}
user_id = known_users.get(requested_user.lower())
if user_id is None:
    raise SystemExit(f'Unknown user {requested_user!r}; ids look like {next(iter(known_users.values()))!r}.')

items_to_recommend = []

all_items = dataset['item'].unique()
already_rated = set(dataset.loc[dataset['user'] == user_id, 'item'])

user_ratings = {}
for item in all_items:
    if item in already_rated:
        continue  # only recommend items the user has not rated yet
    prediction = algo.predict(user_id, item)
    user_ratings[item] = prediction.est

recommended_items = sorted(user_ratings.items(), key=lambda x: x[1], reverse=True)[:3]

print(f'Recommended items for {user_id}:')
for item, rating in recommended_items:
    items_to_recommend.append(item)
    print(f'{item} (predicted rating: {rating:.2f})')
