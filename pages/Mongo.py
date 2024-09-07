import streamlit as st
import pandas as pd
import math as math
import pymongo


class DataAnalysisApp:
    def __init__(self):
        self.options = ['Ver todos los datos', 'Agregar estudiante', 'Agregar curso','Filtro código curso o carrera','Filtro año ingreso o nota final','Actualizar dato existente','Eliminar dato existente'
                        ]
        self.uri = "mongodb+srv://cluster0.h8mex.mongodb.net/"
        self.client = pymongo.MongoClient(self.uri,username="matyplop",password="Eminemlomejor1@")

    def sidebar(self):
        selected = st.sidebar.selectbox(
            '¿Qué acción desea realizar?', self.options)
        return selected

    def see(self):
        database = self.client.get_database("Proyecto_1_parte_2")
        collections = database.list_collection_names()

        students_collection = database.get_collection("Estudiantes")
        courses_collection = database.get_collection("Cursos")

        students_data = list(students_collection.find())
        courses_data = list(courses_collection.find())

        joined_data = self.join_students_courses(students_data, courses_data)

        st.write("### Todos los Estudiantes")
        st.json(students_data, expanded=False)
        student_df=self.to_table(students_data)
        student_df[['Nombre','Edad','Rut','Carrera','Año_Ingreso']]
        st.write("### Todos los Cursos")
        st.json(courses_data, expanded=False)
        courses_df=self.to_table(courses_data)
        courses_df[['Curso','Codigo_curso']]
        st.write("### Intersección de Estudiantes y Cursos")
        st.write(pd.DataFrame(joined_data))

        self.client.close()

    def join_students_courses(self, students_data, courses_data):
        joined_data = []
        for student in students_data:
            if "Rut" in student:
                student_rut = student["Rut"]
                for course in courses_data:
                    if "Rut_estudiante" in course and course["Rut_estudiante"] == student_rut:
                        joined_data.append({
                            "Nombre": student["Nombre"],
                            "Edad": student["Edad"],
                            "Rut": student["Rut"],
                            "Carrera": student["Carrera"],
                            "Año_Ingreso": student["Año_Ingreso"],
                            "Curso": course["Curso"],
                            "Codigo_curso": course["Codigo_curso"],
                            "Nota_final": course["Nota_final"]
                        })
        return joined_data

    def create_collections(self):
        db=self.client["Proyecto_1_parte_2"]
        courses=db["Cursos"]
        students=db["Estudiantes"]
        collections= [courses,students]
        return collections

    def add_data_student(self):
        collections=self.create_collections()
        nombre = st.text_input("Ingrese el nombre")
        edad =  st.text_input("Ingrese la edad")
        rut= st.text_input("Ingrese el rut")
        carrera= st.text_input("Ingrese la carrera")
        año= st.text_input("Ingrese el año de ingreso")
        agregar =st.button("Agregar")

        


        estudiantes = {
            "Nombre": nombre,
            "Edad": edad,
            "Rut": rut,
            "Carrera": carrera,
            "Año_Ingreso": año
        }

        if agregar == True:

            collections[1].insert_one(estudiantes)
            self.see()



    def add_data_course(self): 
        collections=self.create_collections()
        curso = st.text_input("Ingrese el curso")
        codigo_curso = st.text_input("Ingrese el código del curso")
        rut_estudiante = st.text_input("Ingrese el rut del estudiante")
        nota_final = st.text_input("Ingrese la nota final")
        agregar = st.button("Agregar")

        ramo = {
            "Curso": curso,
            "Codigo_curso": codigo_curso,
            "Rut_estudiante": rut_estudiante,
            "Nota_final": nota_final
        }

        if agregar:
            # Verificar si el rut del estudiante ya existe
            students_collection = collections[1]
            student_exists = students_collection.find_one({"Rut": rut_estudiante})
            if not student_exists:
                st.error("El rut del estudiante no existe. Por favor, agregue el estudiante antes de agregar el curso.")
            else:
                # Verificar si el código del curso ya existe
                existing_course = collections[0].find_one({"Codigo_curso": codigo_curso})
                if existing_course:
                    st.error("El código de curso ya existe. Por favor, ingrese un código único.")
                else:
                    # Agregar curso a la lista de cursos del estudiante
                    student_data = student_exists
                    if "Cursos" not in student_data:
                        student_data["Cursos"] = []
                    student_data["Cursos"].append(ramo)
                    students_collection.update_one({"Rut": rut_estudiante}, {"$set": student_data})
                    collections[0].insert_one(ramo)
                    st.json(ramo)

        #Lo mismo que la función anterior pero para cursos


    def filter_data(self):
        collections = self.create_collections()

        tipo_de_coleccion = st.selectbox("Selecciona la colección a filtrar", ["Estudiantes", "Cursos"])
    
        if tipo_de_coleccion == "Estudiantes":
            coleccion = collections[1]  
            carrera = st.text_input("Ingrese la carrera")
           
        else:
            coleccion = collections[0]  
            codigo_curso = st.text_input("Ingrese el código del curso")
            


        filtrar = st.button("Filtrar")

        if tipo_de_coleccion == "Estudiantes":
            filtro = {
                "Carrera": carrera,
                
            }
        else:
            filtro = {
                "Codigo_curso": codigo_curso,
               
            }
        
        resultados = list(coleccion.find(filtro))
        st.json(resultados)

    def filter_data_2(self):
        collections = self.create_collections()
        tipo_de_coleccion = st.selectbox("Selecciona la colección para filtrar", ["Estudiantes", "Cursos"])

        if tipo_de_coleccion == "Estudiantes":
            coleccion = collections[1]
            Año_Ingreso = st.text_input("Ingrese el año de ingreso del estudiante")
            filtro = {"Año_Ingreso": Año_Ingreso}
        else:
            coleccion = collections[0]
            Nota_final = st.text_input("Ingrese Nota final del curso")
            filtro = {"Nota_final": Nota_final}

        filtrar = st.button("Filtrar")

        resultados = list(coleccion.find(filtro))
        st.json(resultados)
        

       
        

    def update_data(self):
        collections = self.create_collections()
        tipo_de_coleccion = st.selectbox("Selecciona la colección a actualizar", ["Estudiantes", "Cursos"])

        if tipo_de_coleccion == "Estudiantes":
            coleccion = collections[1]
            rut_estudiante = st.text_input("Ingrese el rut del estudiante a actualizar")
            campo_a_actualizar = st.selectbox("Seleccione el campo a actualizar", ["Nombre", "Edad", "Carrera", "Año_Ingreso"])
            nuevo_valor = st.text_input("Ingrese el nuevo valor")
        else:
            coleccion = collections[0]
            codigo_curso = st.text_input("Ingrese el código del curso a actualizar")
            campo_a_actualizar = st.selectbox("Seleccione el campo a actualizar", ["Curso", "Codigo_curso", "Nota_final"])
            nuevo_valor = st.text_input("Ingrese el nuevo valor")

        actualizar = st.button("Actualizar")

        if tipo_de_coleccion == "Estudiantes":
            filtro = {"Rut": rut_estudiante}
        else:
            filtro = {"Codigo_curso": codigo_curso}

        if actualizar:
            resultado = coleccion.update_one(filtro, {"$set": {campo_a_actualizar: nuevo_valor}})
            if resultado.modified_count > 0:
                st.success("Registro actualizado con éxito")
                self.see()
            else:
                st.error("No se encontró el registro a actualizar")

    def delete_data(self):
        collections = self.create_collections()
        tipo_de_coleccion = st.selectbox("Selecciona la colección a eliminar", ["Estudiantes", "Cursos"])

        if tipo_de_coleccion == "Estudiantes":
            coleccion = collections[1]
            rut_estudiante = st.text_input("Ingrese el rut del estudiante a eliminar")
        else:
            coleccion = collections[0]
            codigo_curso = st.text_input("Ingrese el código del curso a eliminar")

        eliminar = st.button("Eliminar")

        if tipo_de_coleccion == "Estudiantes":
            filtro = {"Rut": rut_estudiante}
        else:
            filtro = {"Codigo_curso": codigo_curso}

        if eliminar:
            resultado = coleccion.delete_one(filtro)
            if resultado.deleted_count > 0:
                st.success("Registro eliminado con éxito")
                self.see()
            else:
                st.error("No se encontró el registro a eliminar")     

    def run(self):
        selected_option = self.sidebar()

        if selected_option == self.options[0]:
            self.see()
        elif selected_option == self.options[1]:
            self.add_data_student()
        elif selected_option == self.options[2]:
            self.add_data_course()
        elif selected_option == self.options[3]:
            self.filter_data()
        elif selected_option == self.options[4]:
            self.filter_data_2()
        elif selected_option == self.options[5]:
            self.update_data()
        elif selected_option == self.options[6]:
            self.delete_data()    

    def to_table(self,json):
        reff = pd.json_normalize(json)
        
        return pd.DataFrame(data=reff)

def start():

    app = DataAnalysisApp()
    app.run()


if __name__ == "__main__":
    start()
