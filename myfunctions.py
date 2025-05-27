"Funciones para el analisis de datos"




def cambiar_tipo(df):

    import pandas as pd
    import numpy as np

    """
    Cambia el tipo de datos de las columnas de un DataFrame.
    Cambia el tipo de las columnas de un dataframe"""

    for column in df.columns:
        if "fecha" in column.lower() or "date" in column.lower():
            try:
                df[column] = pd.to_datetime(df[column])
                print(f"columna '{column}' convertida a datetime.")
            except Exception as e:
                print(f"No se pudo convertir la columna '{column} a datetime : {e}")
        
        elif "id" in column.lower():
            df[column] = df[column].where(df[column].isnull(), df[column].astype(str))
            print(f"Columna '{column}' convertida a object (string).")

    return df.info()


def nulos_analisis(df):
    import pandas as pd
    """
    Analiza los valores nulos en un DataFrame.
    Muestra la cantidad de valores nulos por columna y muestra porcentualmente el nivel de nulos.
    """

    for column in df.columns:
        
        null_count = df[column].isnull().sum()
        null_percentage = (null_count / len(df)) * 100


        if null_count > 0:
            print(
                f"La cantidad de nulos para la columna {column} es "
                f"de {null_count},\n puedes usar la funcion eliminar_nulos!!!"
                f"si lo consideras correcto,\n"
                f"lo que representa un {null_percentage:.2f}% del total de filas"
            )
        else:
            print(f"La columna {column} no tiene valores nulos.")

    return df.info()



def eliminar_nulos(df, columnas=None):
    """
    Elimina las filas con valores nulos en el DataFrame.
    
    Parámetros:
    - df: DataFrame original
    - columnas: lista de columnas a revisar (si es None, revisa todas)
    
    Retorna:
    - DataFrame sin las filas que tienen nulos en las columnas indicadas
    """
    if columnas:
        df = df.dropna(subset=columnas , inplace=True)
        print(f"Se eliminaron las filas con nulos en las columnas: {columnas}")
    else:
        df = df.dropna()
    return df



def analisis_duplicados(df):
    """
    Analiza los duplicados en un DataFrame.
    Muestra la cantidad de filas duplicadas y las columnas que las componen.
    """
    duplicated_rows = df[df.duplicated()]
    if not duplicated_rows.empty:
        print(f"Hay {len(duplicated_rows)} filas duplicadas.")
        print(f"El porcentaje de filas duplicadas es: {len(duplicated_rows)/ len(df) * 100:.2f}%\n\n")
    else:
        print("No hay filas duplicadas en el DataFrame.")
    
    return df.info()


def histrogramas(df, columns=None , bins =5):
    import seaborn as sns 
    import matplotlib.pyplot as plt
    """
    Genera histogramas según la columna seleccionada en el dataframe
    - df: DataFrame original
    - columnas: lista de columnas a graficar

    Retorna:
    - Grafica histrograma estandarizado
    
    """
    for column in columns:
        if column in df.columns:
            plt.figure(figsize=(8, 5))
            sns.histplot(data=df[column], kde=True, bins=bins)
            plt.ylim(0,1000)
            plt.title(f'Histograma de {column}')
            plt.xlabel(column)
            plt.ylabel('Frecuencia')
            plt.grid(True, alpha=0.5)
            plt.show()
    
    return 



def agrup_condicion(df ,filtro, condition ,columna , value , agrupado):
    """
    Agrupa bajo dos condiciones y realiza una operación de agregación en un DataFrame.
    - df: DataFrame original
    - columnas: columna a operar
    - filtro :Valor a filtrar
    - condition: Valor a filtrar
    - Value:operacion a usar
    - Agrupado: columna a agrupar

    Retorna:
    - Df agrupado según se requierea
    """

    for column in columna:
        df_n = df[df[filtro] == condition]
        df_n = df_n.groupby(agrupado).agg({columna:value}).reset_index()
        df_n = df_n.sort_values(by=columna, ascending=False)
    return df_n




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

    return operadores_a_deshabilitar, df_ineficacia


def eliminar_operadores(df, operadores_a_eliminar):
    """
    Elimina los operadores especificados del DataFrame.

    Args:
        df: DataFrame original con una columna 'operator_id'.
        operadores_a_eliminar: Lista de IDs de operadores a eliminar.

    Returns:
        DataFrame sin los operadores especificados.
    """
    if not operadores_a_eliminar:
        print("No hay operadores para eliminar.")
        return df
    
    operadores_id = operadores_a_eliminar[0]
    df_filtrado = df[~df['operator_id'].isin(operadores_id)]
    print("Operadores originales:", df['operator_id'].nunique())
    print("Operadores actualizados:", df_filtrado['operator_id'].nunique())
    
    return df_filtrado.head(10)

def convertir_a_excel(df, nombre_archivo):
    """
    Convierte un DataFrame a un archivo Excel.

    Args:
        df: DataFrame a convertir.
        nombre_archivo: Nombre del archivo Excel a crear (sin extensión).

    Returns:
        None
    """
    import pandas as pd

    for col in df.select_dtypes(include=['datetimetz']).columns:
        df[col] = df[col].dt.tz_localize(None)

    nombre_archivo = f"{nombre_archivo}"
    df.to_excel(nombre_archivo, index=False ,engine='openpyxl')
    print(f"Archivo {nombre_archivo} creado exitosamente.")
    
    return nombre_archivo