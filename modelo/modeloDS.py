import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score

# Leemos el .CSV
data = pd.read_csv("./datos/dataset_phishing.csv")

#drop columns
columnas_eliminar = ["random_domain", "domain_age", "dns_record", "page_rank", "nb_redirection", "nb_external_redirection", "nb_hyperlinks", "ratio_intHyperlinks", "ratio_extHyperlinks", "ratio_extRedirection", "ratio_extErrors", "external_favicon", "links_in_tags", "ratio_intMedia", "domain_with_copyright", "domain_registration_length", "google_index"]
data_final = data.drop(columnas_eliminar, axis=1)
data_final["status"] = data_final.status.map({"legitimate": 0, "phishing":1})
mapeo = ["legitimate", "phishing"]

# Separamos los conjuntos
Y = np.array(data_final["status"])
data_final.drop(["url", "status"], inplace=True, axis=1)
X = np.array(data_final)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

# Creamos el Random Forest
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Entrenamos
rf_classifier.fit(X_train, Y_train)

# Predecimos
y_pred = rf_classifier.predict(X_test)

# Metricas
precision = precision_score(Y_test, y_pred)
recall = recall_score(Y_test, y_pred)
f1 = f1_score(Y_test, y_pred)
print("Metricas del modelo:\n")
print("Precisión:","%.2f" % (precision*100),"%")
print("Recall:", "%.2f" % (recall*100),"%")
print("F1 score:", f1)

#nuevos_parametros = [28, 19, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 3, 3, 0, 11, 11, 0, 7.0, 7.0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 1, 0, 100.0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0]
# Convertir el vector de parámetros a un array de numpy
#new_data = np.array([nuevos_parametros])

# Realizar la predicción utilizando el modelo entrenado
#prediccion = rf_classifier.predict(new_data.reshape(1, -1))
#print(prediccion[0])