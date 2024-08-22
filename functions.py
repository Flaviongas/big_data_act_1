import pandas as pd


def agregar_campeon(nombre, rol, vida_base, mana_base, armadura_base, daño_ataque_base, eficiencia_oro):
    nuevo_campeon = {
        "Nombre": [nombre],
        "Rol": [rol],
        "Vida base": [vida_base],
        "Mana base": [mana_base],
        "Armadura base": [armadura_base],
        "Daño ataque base": [daño_ataque_base],
        "Eficiencia de Oro": [eficiencia_oro]
    }

    nuevo_campeon_df = pd.DataFrame(nuevo_campeon)

    df = pd.read_csv('data/champions.csv')

    df = pd.concat([df, nuevo_campeon_df], ignore_index=True)

    return df


def buscar_campeon(column, value):
    df = pd.read_csv('data/champions.csv')
    resultado = df[df[column] == value]
    return resultado
