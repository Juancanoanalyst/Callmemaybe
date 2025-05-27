# 📊 Análisis de Datos de Telecomunicaciones 📞

## 🚀 Proyecto Overview

Este proyecto se enfoca en el análisis exhaustivo de datos de telecomunicaciones para extraer insights valiosos y fundamentar la toma de decisiones estratégicas. A través de la manipulación y el análisis de los datos, buscamos optimizar operaciones, identificar áreas de mejora y potenciar el rendimiento general de los servicios de telecomunicaciones.

---

## 📂 Contenido del Proyecto

### Jupyter notebook
-  Análisis exploratorio de datos (EDA)
-  Limpieza y transformación de datos
-  Visualización de métricas clave
-  Interpretación de resultados

### Python 
- `myfunctions.py`:  Script de Python que define las funciones reutilizables para el análisis de datos, incluyendo:
    -  `cambiar_tipo(df)`:  Cambia el tipo de datos de las columnas.
    - `nulos_analisis(df)`:  Analiza los valores nulos.
    - `duplicados_analisis(df)`:  Analiza los duplicados.
    - `analisis_clientes(df)`:  Realiza un análisis de los clientes.
    - `analisis_operadores(df)`:  Realiza un análisis de los operadores.
    - `calcular_ineficacia(df)`:  Calcula el índice de ineficacia de los operadores.
    - `eliminar_operadores(df, operadores_a_eliminar)`:  Elimina los operadores especificados del DataFrame.
    - `convertir_a_excel(df, nombre_archivo)`:  Convierte un DataFrame a un archivo Excel.

### Datasets
  - Directorio que contiene los datasets de entrada (`telecom_dataset_us.csv`, `telecom_clients_us.csv`) 
  - Dataset de salida limpio (`telecom_dataset_us_clean.xlsx`).

---

## 📊 Gráfica principal 

### **Distribucion de operadores ineficacez**
   > 📌 Estas gráfica muestra cómo en que espectro de la grafica se encuentran los operadores que se van a eliminar.


<p align="center">
  <img src="distribucion_operadores.png" alt="Distribucion operadores ineficacez" width="85%" >
</p>

