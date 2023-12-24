import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder


# Veri setini yükle
veriseti = pd.read_csv("dataset_Facebook.csv", sep=";")

label_encoder = LabelEncoder()
veriseti['Type'] = label_encoder.fit_transform(veriseti['Type'])

veriseti.fillna(0, inplace=True)

# Bağımsız ve bağımlı değişkenleri seç
X = veriseti[["Category","Type", "Page total likes", "Post Month", "Post Hour", "Post Weekday", "Paid"]]
Y = veriseti["Total Interactions"].values

# Verileri normalize et
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)


scaler = StandardScaler()
X_non_categorical = X[["Page total likes", "Post Month", "Post Hour", "Post Weekday", "Paid"]]
X_non_categorical_scaled = scaler.fit_transform(X_non_categorical)
X.loc[:, ["Page total likes", "Post Month", "Post Hour", "Post Weekday", "Paid"]] = X_non_categorical_scaled
X[["Page total likes", "Post Month", "Post Hour", "Post Weekday", "Paid"]] = X_non_categorical_scaled

# Veriyi eğitim ve test setine bölelim
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Gradyan İnişi için gerekli fonksiyonları tanımlayalım

def calculate_cost(X, Y, weights):
    m = len(Y)
    predictions = np.dot(X, weights)
    cost = (1 / (2 * m)) * np.sum(np.square(predictions - Y))
    return cost

def gradient_descent(X, Y, weights, learning_rate, epochs):
    m = len(Y)
    cost_history = []

    for epoch in range(epochs):
        predictions = np.dot(X, weights)
        errors = predictions - Y
        gradient = (1 / m) * np.dot(X.T, errors)
        weights = weights - learning_rate * gradient

        cost = calculate_cost(X, Y, weights)
        cost_history.append(cost)

    return weights, cost_history

# İlk ağırlık katsayılarını tanımla
initial_weights = np.zeros(X_train.shape[1])

# Gradyan İnişi ile modeli eğit
learning_rate = 0.001
epochs = 2000
trained_weights, cost_history = gradient_descent(X_train, Y_train, initial_weights, learning_rate, epochs)

# Eğitim ve test verileri için Toplam Kare Hatayı (Sum Squared Error) hesapla
train_error = calculate_cost(X_train, Y_train, trained_weights)
test_error = calculate_cost(X_test, Y_test, trained_weights)

# Toplam Kare Hata (Sum Squared Error) grafiğini çiz
plt.plot(range(1, epochs+1), cost_history, color='blue')
plt.title('Toplam Kare Hata - Gradyan İnişi')
plt.xlabel('Epochs')
plt.ylabel('Cost')
plt.show()
# Eğitim ve test hatalarını çiz
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.scatter(Y_train,np.dot(X_train, trained_weights), color='blue')
plt.title('Eğitim Seti: Gerçek Değerler vs. Tahminler')
plt.xlabel('Gerçek Değerler')
plt.ylabel('Tahminler')

plt.subplot(1, 2, 2)
plt.scatter(Y_test,np.dot(X_test, trained_weights), color='red')
plt.title('Test Seti: Gerçek Değerler vs. Tahminler')
plt.xlabel('Gerçek Değerler')
plt.ylabel('Tahminler')

plt.tight_layout()
plt.show()

def calculate_percentage_error(Y, predictions):

    return (100 / np.sum(np.square(Y))) * np.sum(np.square(predictions - Y))
    

train_percentage_error = calculate_percentage_error(Y_train, np.dot(X_train, trained_weights))
test_percentage_error = calculate_percentage_error(Y_test, np.dot(X_test, trained_weights))


print("Eğitim Hatası (Percentage Error):", train_percentage_error)
print("Test Hatası (Percentage Error):", test_percentage_error)

# Sonuçları yazdır
print("Eğitim Hatası (MSE):", train_error)
print("Test Hatası (MSE):", test_error)
print("Eğitilmiş Ağırlık Katsayıları:", trained_weights)

