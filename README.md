# Análisis de Datos de Telecomunicaciones

Este proyecto realiza un análisis de datos de telecomunicaciones para obtener información valiosa y tomar decisiones informadas. Utiliza Python con las bibliotecas Pandas, NumPy, SciPy, Scikit-learn, Seaborn, Matplotlib, Plotly, Power BI, Excel, Dash, Streamlit, PostgreSQL y BigQuery.

## Descripción

El proyecto incluye las siguientes funcionalidades principales:

* **Limpieza y Transformación de Datos:**
    * Cambio de tipo de datos de las columnas.
    * Análisis y manejo de valores nulos.
    * Análisis de duplicados.
* **Análisis de Datos:**
    * Análisis de clientes.
    * Análisis de operadores.
    * Cálculo del índice de ineficacia de los operadores.
* **Generación de Reportes:**
    * Identificación de operadores a deshabilitar.
    * Generación de un dataset limpio en formato Excel.

## Archivos del Proyecto

* `jupyter.ipynb`:  El notebook de Jupyter que contiene el flujo de trabajo principal del análisis de datos.
* `myfunctions.py`:  Script de Python que define las funciones reutilizables para el análisis de datos, incluyendo:
    * `cambiar_tipo(df)`:  Cambia el tipo de datos de las columnas.
    * `nulos_analisis(df)`:  Analiza los valores nulos.
    * `duplicados_analisis(df)`:  Analiza los duplicados.
    * `analisis_clientes(df)`:  Realiza un análisis de los clientes.
    * `analisis_operadores(df)`:  Realiza un análisis de los operadores.
    * `calcular_ineficacia(df)`:  Calcula el índice de ineficacia de los operadores.
    * `eliminar_operadores(df, operadores_a_eliminar)`:  Elimina los operadores especificados del DataFrame.
    * `convertir_a_excel(df, nombre_archivo)`:  Convierte un DataFrame a un archivo Excel.
* `datasets/`:  Directorio que contiene los datasets de entrada (`telecom_dataset_us.csv`, `telecom_clients_us.csv`) y el dataset de salida limpio (`telecom_dataset_us_clean.xlsx`).

## Requisitos

Asegúrate de tener instaladas las siguientes bibliotecas de Python:

```bash
pip install pandas numpy scipy scikit-learn seaborn matplotlib plotly openpyxl dash streamlit psycopg2 google-cloud-bigquery