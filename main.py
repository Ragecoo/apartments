import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

df = pd.read_csv('data01.csv')

columns_to_drop = ['photos', 'title', 'addressTitle', 'ownerName']
df = df.drop(columns=columns_to_drop, errors='ignore')
df = df.drop(columns=['hasPrice', 'isOnMap'], errors='ignore')
df['is_first_floor'] = df['is_first_floor'].astype(int)
df['is_last_floor'] = df['is_last_floor'].astype(int)
df['complexId'] = df['complexId'].fillna(0)
df['complexId'] = df['complexId'].astype(int).astype(str)
df['complexId'] = df['complexId'].replace('0', 'No_complex')

df = df.dropna(subset=['price'])

df = df[(df['price'] >= 3_000_000) & (df['price'] <= 150_000_000)]

y = df['price']
ids = df['id']

X = df.drop(columns=['price', 'id'])
cat_features = ['complexId']

X_train, X_test, y_train, y_test, id_train, id_test = train_test_split(
    X, y, ids, test_size=0.2, random_state=42
)

model = CatBoostRegressor(
    iterations=10000,
    learning_rate=0.05,
    depth=6,
    loss_function='RMSE',
    verbose=200,
    cat_features=cat_features
)

model.fit(
    X_train, np.log1p(y_train),
    eval_set=(X_test, np.log1p(y_test)),
    early_stopping_rounds=50
)

predictions = np.expm1(model.predict(X_test))

mae = mean_absolute_error(y_test, predictions)
print(f"\nСредняя ошибка модели: {mae:,.0f} тенге")

results_df = pd.DataFrame({
    'ID_квартиры': id_test,
    'Реальная_цена': y_test,
    'Предсказанная_цена': predictions
})

results_df['Разница'] = abs(results_df['Реальная_цена'] - results_df['Предсказанная_цена'])

print("\nПримеры предсказаний на тестовых данных:")
print(results_df.head(10).to_string(formatters={
    'Реальная_цена': '{:,.0f}'.format,
    'Предсказанная_цена': '{:,.0f}'.format,
    'Разница': '{:,.0f}'.format
}).replace(',', ' '))

model.save_model('model.cbm')