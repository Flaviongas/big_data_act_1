import streamlit as st
import scipy
import seaborn as sns
from matplotlib import pyplot
import pandas as pd
import math as math
import plotly.express as px
import numpy as np


class DataAnalysis:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.options = ['Selecciona una opción', 'Gráficos diversos',
                        'Primeras y últimas 5 columnas', 'Grafico de línea y Matriz de Correlación', 'Analizar Fechas', "Medidas de Tendencia Central", "Pairplots", "Análisis por Localidad"]

    def pair_plots(self):
        df = self.get_df()
        st.write("# Pairplots ")
        pairplot = sns.pairplot(df, hue="Age", palette='rocket')
        st.pyplot(pairplot)

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

    # con esto es mas facil controlar el df
    # accede al df

    def get_df(self):
        return self.df

    # actualiza el df
    def set_df(self, new_df):
        self.df = new_df

    def sidebar(self):
        selected = st.sidebar.selectbox(
            '¿Qué acción desea realizar?', self.options)
        return selected

    def mostrar_dataframe(self):
        st.dataframe(self.get_df(), hide_index=True)

    def line_graph(self):
        df = self.get_df()
        fig = px.line(df, x='Age', y='Salary',
                      title='Salario')
        st.plotly_chart(fig)

    def grafico(self):
        df = self.get_df()

        st.title('Gráfico de todos los salarios')
        st.line_chart(df.Salary, color='#000000')

        st.title('Gráfico de todos las edades')
        st.line_chart(df.Age, color='#000000')

        st.title('Histograma de Salario')
        sturges_salary = 1 + round(math.log2(df.Salary.count()))
        fig = px.histogram(df, x='Salary', nbins=sturges_salary)

        sturges_age = 1 + round(math.log2(df.Age.count()))
        fig5 = px.histogram(df, x='Age', nbins=sturges_age)
        st.plotly_chart(fig)
        st.title('Histograma de Edad')
        st.plotly_chart(fig5)

        st.title('Boxplot de Salario')
        fig2 = px.box(df, x='Age',
                      title='Boxplot de Edad')
        fig3 = px.box(df, x='Salary',
                      title='Boxplot de Salario')
        st.plotly_chart(fig3)

        st.title('Boxplot de Edad')
        st.plotly_chart(fig2)

        st.title("Diagrama de Dispersión")

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

    def mostrar_5(self):
        st.write(
            "### Primeras 5 columnas")
        st.write(self.get_df().head())

    def mostrar_ultimos_5(self):
        st.write(
            "### Últimas 5 columnas")
        st.write(self.get_df().tail())

    def tipos_datos(self):
        st.write("## Datos de fecha limpias")
        df = self.get_df()

        st.write(df)

    def correlation_matrix(self):
        corrM = self.get_df()[['Age', 'Salary']].corr()
        corrM

    def analyze_dates(self):
        df = self.get_df()

        st.write("# Fecha vs Salario")
        fig = px.line(df, x='Join_Date', y="Salary")
        st.plotly_chart(fig)
        st.write("### No parece haber estacionalidad")

        st.write("# Fecha vs Edad")
        fig2 = px.line(df, x='Join_Date', y="Age")
        st.plotly_chart(fig2)
        st.write("### No parece haber estacionalidad")

    def correlations(self):
        df = self.get_df()

        st.write("# Gente de Chicago")
        df_chicago = df[df["Location"] == "Chicago"]

        sturges_salary = 1 + round(math.log2(df_chicago.Salary.count()))
        sturges_age = 1 + round(math.log2(df_chicago.Age.count()))

        fig = px.histogram(df_chicago, x='Salary', nbins=sturges_salary)
        fig2 = px.histogram(df_chicago, x='Age', nbins=sturges_age)

        st.plotly_chart(fig)
        st.plotly_chart(fig2)
        st.write(df_chicago.describe())

        st.write("# Gente de Los Angeles")
        df_angeles = df[df["Location"] == "Los Angeles"]

        sturges_salary = 1 + round(math.log2(df_angeles.Salary.count()))
        sturges_age = 1 + round(math.log2(df_angeles.Age.count()))

        fig = px.histogram(df_angeles, x='Salary', nbins=sturges_salary)
        fig2 = px.histogram(df_angeles, x='Age', nbins=sturges_age)

        st.plotly_chart(fig)
        st.plotly_chart(fig2)
        st.write(df_angeles.describe())

        st.write("# Gente de New York")
        df_new_york = df[df["Location"] == "New York"]

        sturges_salary = 1 + round(math.log2(df_new_york.Salary.count()))
        sturges_age = 1 + round(math.log2(df_new_york.Age.count()))

        fig = px.histogram(df_new_york, x='Salary', nbins=sturges_salary)
        fig2 = px.histogram(df_new_york, x='Age', nbins=sturges_age)

        st.plotly_chart(fig)
        st.plotly_chart(fig2)
        st.write(df_new_york.describe())

        st.write("# Gente de San Francisco")
        df_san_francisco = df[df["Location"] == "San Francisco"]

        sturges_salary = 1 + round(math.log2(df_san_francisco.Salary.count()))
        sturges_age = 1 + round(math.log2(df_san_francisco.Age.count()))

        fig = px.histogram(df_san_francisco, x='Salary', nbins=sturges_salary)
        fig2 = px.histogram(df_san_francisco, x='Age', nbins=sturges_age)

        st.plotly_chart(fig)
        st.plotly_chart(fig2)
        st.write(df_san_francisco.describe())

    def run(self):
        selected_option = self.sidebar()

        if selected_option == self.options[0]:
            self.mostrar_dataframe()

        elif selected_option == self.options[1]:
            self.grafico()

        elif selected_option == self.options[2]:
            self.mostrar_5()
            self.mostrar_ultimos_5()

        elif selected_option == self.options[3]:

            st.write("# Análisis de Tendencias")
            self.line_graph()
            st.write("# Matriz de correlación")
            self.correlation_matrix()

        elif selected_option == self.options[4]:
            self.analyze_dates()

        elif selected_option == self.options[5]:
            self.mostrar_estadistica()

        elif selected_option == self.options[6]:
            self.pair_plots()

        else:
            self.correlations()


app = DataAnalysis('data/clean.csv')
app.run()
