import streamlit as st
import pandas as pd
import math as math
import plotly.express as px
import numpy as np


class DataAnalysisApp:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.options = ['Selecciona una opción', 'Estadísticas descriptivas', "Convertir a CLP/EUR", "Histogramas y Boxplots", "Dispersión y Correlación", "Solucionar errores en datos", "Corregir Fechas"
                        ]

   # obtiene el df
    def get_df(self):
        return self.df

    # actualiza el df
    def set_df(self, new_df):
        self.df = new_df

    def sidebar(self):
        selected = st.sidebar.selectbox(
            '¿Qué acción desea realizar?', self.options)
        return selected

    def mostrar_estadistica(self):
        df = self.get_df()
        col1, col2 = st.columns(2)
        col1.header("Resumen de Salarios")
        summary_stats = df.Salary.describe(include='all')
        mode_sal = df.Salary.mode()
        mode_age = df.Age.mode()
        age_stats = df.Age.describe(include='all')
        col1.write(summary_stats)
        col1.write("## Moda ")
        col1.write(mode_sal)
        col2.header("Resumen de Edades")
        col2.write(age_stats)
        col2.write("## Moda ")
        col2.write(mode_age)
        st.write("# Rango InterCuartil")
        col3, col4 = st.columns(2)
        col3.header("De Salario")
        S_Q1 = df.Salary.quantile(0.25)
        S_Q3 = df.Salary.quantile(0.75)
        IQR_S = S_Q3-S_Q1
        col3.write(str(IQR_S))
        A_Q1 = df.Age.quantile(0.25)
        A_Q3 = df.Age.quantile(0.75)
        IQR_A = A_Q3-A_Q1
        col4.header("De Edades")
        col4.write(str(IQR_A))

    def cleanup_everything_minus_date(self):
        # Elimina filas con valores faltantes en Salary
        clean = self.limpiar_datos(self.df.copy())
        return clean

    def show_manejar_valores_faltantes(self):
        st.write("### Manejo de valores faltantes")
        st.write("Valores faltantes o edad mayor a 80 años:")

        missing_salary = self.df[self.df['Salary'].isna()]
        old_age = self.df[self.df['Age'] > 80]
        problematic_data = pd.concat([missing_salary, old_age])
        st.dataframe(problematic_data, hide_index=True)

        st.write("Valores faltantes eliminados:")
        clean = self.cleanup_everything_minus_date()
        st.dataframe(clean, hide_index=True)
        clean.to_csv('data/clean.csv', index=False)

        return clean

    def grafico_barra(self):
        df = self.get_df()
        sturges_salary = 1 + round(math.log2(df.Salary.count()))
        sturges_age = 1 + round(math.log2(df.Age.count()))
        fig = px.histogram(df, x='Salary',
                           title='Histograma de Salario', nbins=sturges_salary)
        st.plotly_chart(fig)
        fig4 = px.histogram(df, x='Age',
                            title='Histograma de Edad', nbins=sturges_age)
        st.plotly_chart(fig4)
        fig2 = px.box(df, x='Age',
                      title='Boxplot de Edad')
        fig3 = px.box(df, x='Salary',
                      title='Boxplot de Salario')
        st.plotly_chart(fig2)
        st.plotly_chart(fig3)

    def correlacion(self):
        st.write("# Diagrama de Dispersión")
        df = self.get_df()
        fig = px.scatter(x=df.Age, y=df.Salary)
        st.plotly_chart(fig)
        st.write("# Correlación de Edad y Salario")
        st.write("## Test de Pearson")
        pearson = df['Age'].corr(df.Salary, method='pearson')
        pearson
        st.write("## Test de Kendall")
        kendall = df['Age'].corr(df.Salary, method='kendall')
        kendall
        st.write("## Test de Spearman")
        spearman = df['Age'].corr(df.Salary, method='spearman')
        spearman

    def convertir_unidad_medida(self):
        df = self.get_df()

        st.write("## Locaciones y Salarios")
        mostrar_locaciones = df['Location'].value_counts()
        st.write(mostrar_locaciones)
        st.write("## Salarios con Unidad de Medida")
        columna_seleccionada = 'Salary'

        col = df[columna_seleccionada]

        st.write("Seleccione la unidad de medida a la que desea convertir:")
        unidad_medida = st.selectbox(
            "Unidad de medida:", ["CLP", "EUR"])

        if unidad_medida == "CLP":
            df[columna_seleccionada] = col * 923  # 1 USD = 923 CLP
            df['Unidad'] = 'CLP'

        elif unidad_medida == "EUR":
            df[columna_seleccionada] = col * 0.90  # 1 USD = 0.90 EUR
            df['Unidad'] = 'EUR'

        else:
            df[columna_seleccionada] = col
            df['Unidad'] = 'USD'

        st.write(df[['Name', 'Location', 'Salary', 'Unidad']])

    def limpiar_datos(self, df):
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col == 'Age':
                df[col] = df[col].apply(
                    lambda x: round(self.df.Age.mean()) if x < 0 or x > 80 else x)
        return df

    def tipos_datos(self, df):
        col1, col2 = st.columns(2)
        df_copy = df.copy()

        col1.write("### Tipos de datos")
        col1.write(df.dtypes)
        df_copy['Join_Date'] = pd.to_datetime(
            df_copy['Join_Date'], errors='coerce')
        col2.write("### Conversion a datetime")
        col2.write(df_copy.dtypes)
        st.write("### Dataframe")

        df['Join_Date'] = pd.to_datetime(
            df['Join_Date'], format='mixed', yearfirst=True)
        st.dataframe(df, hide_index=True)

        # guarda al csv limpio
        df.to_csv('data/clean.csv', index=False)

    def run(self):
        selected_option = self.sidebar()

        if selected_option == self.options[0]:
            st.write("# Elige una opción")
            st.dataframe(self.df, hide_index=True)

        elif selected_option == self.options[1]:
            self.mostrar_estadistica()

        elif selected_option == self.options[2]:
            self.convertir_unidad_medida()

        elif selected_option == self.options[3]:
            self.grafico_barra()

        elif selected_option == self.options[4]:
            self.correlacion()

        elif selected_option == self.options[5]:
            self.show_manejar_valores_faltantes()

        elif selected_option == self.options[6]:
            self.tipos_datos(self.cleanup_everything_minus_date())


def run():

    app = DataAnalysisApp('data/synthetic_data_usd.csv')
    app.run()


if __name__ == "__main__":
    run()
