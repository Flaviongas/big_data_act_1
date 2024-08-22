import streamlit as st
import pandas as pd
from functions import agregar_campeon, buscar_campeon



class ChampionApp:
    def __init__(self):
        self.encabezado = ["Nombre", "Rol", "Vida base", "Mana base",
                           "Armadura base", "Daño ataque base", "Eficiencia de Oro"]
        self.roles_disponibles = ['Support', 'Mid', 'ADC', 'Jungle', 'Top']
        self.df = pd.read_csv('data/champions.csv',
                              names=self.encabezado, skiprows=1)
        self.logo = st.sidebar.image("./assets/logito.png", width=200)


    def mostrar_menu(self):
        st.write("### Bienvenido a la base de datos de campeones de LoL")

        opciones = ['Selecciona una opción', 'Ingresar nuevo campeón',
                    'Filtrar por datos', 'Modificar campeón existente']
        seleccionar = st.sidebar.selectbox(
            '¿Qué acción desea realizar?', opciones)
        return seleccionar

    def mostrar_dataframe(self):
        st.dataframe(self.df)

    

    def añadir_campeon(self):
        df_show = st.dataframe(self.df)
        valor_predeterminado_vida = 100  # un valor cualquiera
        with st.sidebar.form(key='my_form'):
            nombre = st.text_input("Ingresa nombre")
            rol = st.selectbox("Rol", self.roles_disponibles)
            vida_base = st.number_input(
                "Vida base", value=float(valor_predeterminado_vida))
            mana_base = st.number_input(
                "Mana base", value=float(valor_predeterminado_vida))
            armadura_base = st.number_input(
                "Armadura base", value=float(valor_predeterminado_vida))
            daño_ataque_base = st.number_input(
                "Daño de ataque base", value=float(valor_predeterminado_vida))
            eficiencia_oro = st.number_input(
                "Eficiencia de oro", value=float(valor_predeterminado_vida))
            submit_button = st.form_submit_button(label='Agregar')

        if submit_button:
            df2 = agregar_campeon(nombre, rol, vida_base, mana_base,
                                  armadura_base, daño_ataque_base, eficiencia_oro)
            df2.to_csv('data/champions.csv', mode='w', index=False)
            df_show.empty()
            st.dataframe(df2)

    def filtar_campeon(self):
        selected_type = st.sidebar.selectbox(
            'Seleccione tipo de dato', self.encabezado)
        with st.sidebar.form(key='my_form'):
            if selected_type in ['Nombre', 'Rol']:
                data = st.text_input("Ingrese parámetro de búsqueda")
            else:
                data = st.number_input("Ingrese parámetro de búsqueda")
            submit_button = st.form_submit_button(label='Aceptar')

        if submit_button:
            if selected_type == "Eficiencia de Oro":
                data = float(data)
            elif selected_type not in ['Nombre', 'Rol']:
                data = int(data)
            df3 = buscar_campeon(selected_type, data)
            st.dataframe(df3)

    def modificar_campeon(self):
        seleccionar_campeon = st.sidebar.selectbox(
            "Selecciona Campeón a modificar", self.df["Nombre"])
        with st.sidebar.form(key='my_form'):
            if seleccionar_campeon:
                champion_data = self.df[self.df['Nombre']
                                        == seleccionar_campeon].iloc[0]
                rol = st.selectbox("Rol", self.roles_disponibles,
                                   index=self.roles_disponibles.index(champion_data["Rol"]))
                vida_base = st.number_input(
                    "Vida base", value=float(champion_data["Vida base"]))
                mana_base = st.number_input(
                    "Mana base", value=float(champion_data["Mana base"]))
                armadura_base = st.number_input(
                    "Armadura base", value=float(champion_data["Armadura base"]))
                daño_ataque_base = st.number_input(
                    "Daño ataque base", value=float(champion_data["Daño ataque base"]))
                eficiencia_oro = st.number_input(
                    "Eficiencia de Oro", value=float(champion_data["Eficiencia de Oro"]))
                submit_button = st.form_submit_button(label='Guardar cambios')

            if submit_button:
                with st.spinner("Generando cambios.."):
                    st.balloons()
                self.df.loc[self.df['Nombre'] ==
                            seleccionar_campeon, 'Vida base'] = vida_base
                self.df.loc[self.df['Nombre'] ==
                            seleccionar_campeon, 'Rol'] = rol
                self.df.loc[self.df['Nombre'] ==
                            seleccionar_campeon, 'Mana base'] = mana_base
                self.df.loc[self.df['Nombre'] == seleccionar_campeon,
                            'Armadura base'] = armadura_base
                self.df.loc[self.df['Nombre'] == seleccionar_campeon,
                            'Daño ataque base'] = daño_ataque_base
                self.df.loc[self.df['Nombre'] == seleccionar_campeon,
                            'Eficiencia de Oro'] = eficiencia_oro
                self.df.to_csv("data/champions.csv", mode='w', index=False)
        st.dataframe(self.df)

    def run(self):


        
        selected_option = self.mostrar_menu()

        if selected_option == 'Selecciona una opción':
            self.mostrar_dataframe()
        elif selected_option == 'Ingresar nuevo campeón':
            self.añadir_campeon()
        elif selected_option == 'Filtrar por datos':
            self.filtar_campeon()
        elif selected_option == 'Modificar campeón existente':
            self.modificar_campeon()


def main():
    app = ChampionApp()
    app.run()

if __name__ == "__main__":
    main()