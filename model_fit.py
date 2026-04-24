import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score

df = pd.read_csv('data01.csv')

columns_to_drop = ['photos', 'title', 'addressTitle', 'ownerName', 'hasPrice', 'isOnMap']
df = df.drop(columns=columns_to_drop, errors='ignore')

df['is_first_floor'] = df['is_first_floor'].astype(int)
df['is_last_floor'] = df['is_last_floor'].astype(int)
df['complexId'] = df['complexId'].fillna(0)
df['complexId'] = df['complexId'].astype(int).astype(str)
df['complexId'] = df['complexId'].replace('0', 'No_complex')
df['complexId'] = df['complexId'].astype('category')

df = df.dropna(subset=['price'])

lower_bound = df['price'].quantile(0.02)
upper_bound = df['price'].quantile(0.98)

print(f"Фильтрация цен: от {lower_bound:,.0f} до {upper_bound:,.0f} тенге")

df = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]

y = df['price']
ids = df['id']
X = df.drop(columns=['price', 'id'])

X_train, X_test, y_train, y_test, id_train, id_test = train_test_split(
    X, y, ids, test_size=0.2, random_state=42
)

model = xgb.XGBRegressor(
    n_estimators=10000,
    learning_rate=0.05,
    max_depth=6,
    enable_categorical=True,
    early_stopping_rounds=50,
    eval_metric='rmse',
    random_state=42
)

model.fit(
    X_train, np.log1p(y_train),
    eval_set=[(X_test, np.log1p(y_test))],
    verbose=200
)

predictions = np.expm1(model.predict(X_test))

mae = mean_absolute_error(y_test, predictions)
mape = mean_absolute_percentage_error(y_test, predictions) * 100
r2 = r2_score(y_test, predictions) * 100
accuracy = 100 - mape

print(f"mae: {mae:,.0f}".replace(',', ' '))
print(f"mape: {mape:.4f}%")
print(f"R²: {r2:.4f}%")

results_df = pd.DataFrame({
    'ID_квартиры': id_test,
    'Реальная_цена': y_test,
    'Предсказанная_цена': predictions
})

results_df['Разница'] = abs(results_df['Реальная_цена'] - results_df['Предсказанная_цена'])
results_df['Ошибка_%'] = (results_df['Разница'] / results_df['Реальная_цена']) * 100

print(results_df.head(20).to_string(formatters={
    'Реальная_цена': '{:,.0f}'.format,
    'Предсказанная_цена': '{:,.0f}'.format,
    'Разница': '{:,.0f}'.format,
    'Ошибка_%': '{:.1f}%'.format
}).replace(',', ' '))

model.save_model('model.json')