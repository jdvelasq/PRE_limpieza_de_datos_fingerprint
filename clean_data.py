"""Taller evaluable presencial"""

import nltk
import pandas as pd


def load_data(input_file):
    """Lea el archivo usando pandas y devuelva un DataFrame"""

# Lee el archivo de texto utilizando Pandas
    datos = pd.read_csv(input_file, sep='\t')  # Cambia el separador según sea necesario

# Muestra los primeros registros para verificar si se han leído correctamente
    return(datos)



def create_fingerprint(df):
    """Cree una nueva columna en el DataFrame que contenga el fingerprint de la columna 'text'"""

    # 1. Copie la columna 'text' a la columna 'fingerprint'
    # 2. Remueva los espacios en blanco al principio y al final de la cadena
    # 3. Convierta el texto a minúsculas
    # 4. Transforme palabras que pueden (o no) contener guiones por su version sin guion.
    # 5. Remueva puntuación y caracteres de control
    # 6. Convierta el texto a una lista de tokens
    # 7. Transforme cada palabra con un stemmer de Porter
    # 8. Ordene la lista de tokens y remueve duplicados
    # 9. Convierta la lista de tokens a una cadena de texto separada por espacios

    df["fingerprint"]=df["text"]

    df["fingerprint"]=(
        df["fingerprint"]
        .str.strip()
        .str.lower()
        .str.replace("-","")
        .str.replace(",","")
        .str.split()
        .apply(lambda x:[nltk.PorterStemmer().stem(w) for w in x])
        .apply(lambda x: sorted(set(x)))
        .str.join(" ")
    )

    return df




def generate_cleaned_column(df):
    """Crea la columna 'cleaned' en el DataFrame"""

    df = df.copy()

    fingerprints = df.sort_values(by=["fingerprint","text"]).copy()
    fingerprints = fingerprints.groupby("fingerprint").first().reset_index()
    fingerprints= fingerprints.set_index("fingerprint")["text"].to_dict()
    df["cleaned"]=df["fingerprint"].map(fingerprints)

    return df



    # 1. Ordene el dataframe por 'fingerprint' y 'text'
    # 2. Seleccione la primera fila de cada grupo de 'fingerprint'
    # 3.  Cree un diccionario con 'fingerprint' como clave y 'text' como valor
    # 4. Cree la columna 'cleaned' usando el diccionario


def save_data(df, output_file):
    """Guarda el DataFrame en un archivo"""
    # Solo contiene una columna llamada 'texto' al igual
    # que en el archivo original pero con los datos limpios
    df=df.copy()
    df=df[("cleaned")]
    df = pd.DataFrame(df)
    df=df.rename(columns={"cleaned": "text"})
    df.to_csv(output_file, sep="\t", index=False)


def main(input_file, output_file):
    """Ejecuta la limpieza de datos"""

    df = load_data(input_file)
    df = create_fingerprint(df)
    df = generate_cleaned_column(df)
    df.to_csv("test.csv", index=False)
    save_data(df, output_file)


if __name__ == "__main__":
    main(
        input_file="input.txt",
        output_file="output.txt",
    )
