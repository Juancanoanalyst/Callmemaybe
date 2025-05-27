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
  <img src="images/distribucion_operadores.png" alt="Distribucion operadores ineficacez" width="85%" >
</p>

## 🧠 Resultados Clave

### 🤖 **Funcion identificacion operadores**

### Función: `identificar_operadores_a_deshabilitar`

"""  python
def identificar_operadores_a_deshabilitar(i_perdidas, i_espera, i_saliente=None, umbral_ineficacia=0.7):
    import pandas as pd
    from sklearn.preprocessing import MinMaxScaler
    import matplotlib.pyplot as plt
    import seaborn as sns

    """
    Calcula un índice de ineficacia y devuelve una lista de operadores que superan un umbral.

    Args:
        i_perdidas: DataFrame con columnas 'operador_id' y la métrica de conteo de llamadas perdidas('total_perdidas').
        i_espera : DataFrame con columnas 'operador_id' y la métrica de tiempo de espera promediada ('promedio_tiempo_espera').
        i_saliente : DataFrame con columnas 'operador_id' y la métrica de llamadas salientes que es un conteo ('total_salientes'). Hay casos donde no las hay se deja none por default
        umbral_ineficacia : Umbral para el índice de ineficacia. Los operadores con un índice mayor o igual a este umbral se consideran para deshabilitar.

    Returns:
        list: Lista de nombres de los operadores a deshabilitar.
    """

    scaler_perdidas = MinMaxScaler()
    i_perdidas['perdidas_norm'] = scaler_perdidas.fit_transform(i_perdidas[['total_perdidas']])

    # --- Normalizar métrica de tiempo de espera ---
    scaler_espera = MinMaxScaler()
    i_espera['espera_norm'] = scaler_espera.fit_transform(i_espera[['promedio_tiempo_espera']])

    # --- Unir los DataFrames de perdidas y espera ---
    df_ineficacia = pd.merge(i_perdidas[['operator_id', 'total_perdidas','perdidas_norm']],
                                i_espera[['operator_id', 'promedio_tiempo_espera','espera_norm']],
                                on='operator_id', how='inner')

    if i_saliente is not None:

        scaler_salientes = MinMaxScaler()
        i_saliente['salientes_norm'] = scaler_salientes.fit_transform(i_saliente[['total_salientes']])
        i_saliente['salientes_invertida_norm'] = 1 - i_saliente['salientes_norm']

        df_ineficacia = pd.merge(df_ineficacia,
                                    i_saliente[['operator_id', 'salientes_invertida_norm']],
                                    on='operator_id', how='left')
        df_ineficacia['salientes_invertida_norm'] = df_ineficacia['salientes_invertida_norm'].fillna(0.5)
        df_ineficacia['indice_ineficacia'] = (df_ineficacia['perdidas_norm'] + df_ineficacia['espera_norm'] + df_ineficacia['salientes_invertida_norm']) / 3
    else:
         df_ineficacia['indice_ineficacia'] = (df_ineficacia['perdidas_norm'] + df_ineficacia['espera_norm']) / 2

    # Identificar operadores que superan el umbral
    operadores_a_deshabilitar = df_ineficacia[df_ineficacia['indice_ineficacia'] >= umbral_ineficacia]['operator_id'].tolist()
    num_operadores_deshabilitar = len(operadores_a_deshabilitar)
    num_total_operadores = df_ineficacia['operator_id'].nunique()

    if num_total_operadores > 0:
        porcentaje_deshabilitar = (num_operadores_deshabilitar / num_total_operadores) * 100
        print(f"\nLa cantidad de operadores ineficaces que se recomienda eliminar es de {num_operadores_deshabilitar}, equivalentes al {porcentaje_deshabilitar:.2f}% \ny son los siguientes: {operadores_a_deshabilitar}")
    else:
        print("\nNo hay operadores para analizar.")

    # --- Generar el histograma ---
    plt.figure(figsize=(10, 6))
    sns.histplot(df_ineficacia['indice_ineficacia'], bins=15, kde=True, alpha=0.6)
    plt.axvline(umbral_ineficacia, color='red', linestyle='dashed', linewidth=2,
                label=f'Umbral de Ineficacia ({umbral_ineficacia:.2f})')

    operadores_deshabilitados_indices = df_ineficacia[df_ineficacia['indice_ineficacia'] >= umbral_ineficacia]['indice_ineficacia']
    sns.histplot(operadores_deshabilitados_indices, color='salmon', kde=False, alpha=0.7,
                label='Operadores a Deshabilitar')
    plt.title('Distribución del Índice de Ineficacia de Operadores')
    plt.xlabel('Índice de Ineficacia')
    plt.ylabel('Frecuencia')
    plt.legend()
    plt.grid(axis='y', alpha=0.5)
    plt.show()

    return operadores_a_deshabilitar, df_ineficacia """ 


- **MinMaxScaler**: Herramienta de estandarizacion
- **Umbral**: 70%

Estos resultados indican que la funcion tiene **gran capacidad para identificar operadores ineficacez y se puede graduar segun se requiera**, permitiendo estrategias de identificacion más efectivas.

---

## 🛠️ Herramientas Utilizadas

- Python 🐍
- Pandas, NumPy
- Matplotlib, Seaborn
- Scikit-learn
- Jupyter Notebook

---

## 📈 Aplicaciones Potenciales



---

## ✅ Conclusión


---

## 👨‍💻 Autor
Juan Cano  
Data Analyst | Machine Learning Enthusiast  
📧 jpcano983@gmail.com  
🔗 [GitHub](https://github.com/Juancanoanalyst)  
🔗 [LinkedIn](https://www.linkedin.com/in/juan-pablo-cano-chaparro/)  
