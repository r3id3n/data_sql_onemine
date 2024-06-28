import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, ttk
from tkcalendar import Calendar
from sql_queries_server import QUERIES_SERVER
from sql_queries_mtbox import QUERIES_MTBOX
from datetime import datetime

class SQLQueryApp:
    # Constructor de la clase
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Consultas SQL Onemine")
        self.root.geometry("800x700")

        self.fechaInicio = datetime.now().strftime("%Y-%m-%d")
        self.fechaFin = datetime.now().strftime("%Y-%m-%d")
        self.horaInicio = ""
        self.horaFin = ""
        self.pala = ""

        self.queries = None

        self.create_widgets()

    def create_widgets(self):
        # Título de la aplicación
        title = tk.Label(self.root, text="Generador de Consultas SQL", font=("Helvetica", 18, "bold"))
        title.pack(pady=10)

        # Frame principal para los botones de selección de consultas
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10, fill="x")

        # Botones para seleccionar el tipo de consulta
        server_button = tk.Button(main_frame, text="Consultas Servidor", command=self.select_server_queries, width=20)
        server_button.pack(side=tk.LEFT, padx=20)

        # Botón para seleccionar consultas de MTBox
        mtbox_button = tk.Button(main_frame, text="Consultas MTBox", command=self.select_mtbox_queries, width=20)
        mtbox_button.pack(side=tk.LEFT, padx=20)

        # Frame para la selección de consultas
        self.query_frame = tk.LabelFrame(self.root, text="Selecciona una consulta", padx=10, pady=10)
        self.query_frame.pack(pady=10, fill="x")

        # Combobox para seleccionar la consulta
        self.query_var = tk.StringVar()
        self.query_combobox = ttk.Combobox(self.query_frame, textvariable=self.query_var, state="disabled", width=70)
        self.query_combobox.pack(fill="x")

        # Frame para la selección de fecha y hora
        datetime_frame = tk.LabelFrame(self.root, text="Selecciona Fecha y Hora", padx=10, pady=10)
        datetime_frame.pack(pady=10, fill="x")

        # Frame para fechas
        date_frame = tk.Frame(datetime_frame)
        date_frame.pack(side=tk.LEFT, padx=20, pady=10)

        # Botones para seleccionar fechas
        date_button_inicio = tk.Button(date_frame, text="Fecha de Inicio", command=lambda: self.ask_date("inicio"), width=20)
        date_button_inicio.grid(row=0, column=0, padx=10, pady=5)

        # Labels para mostrar las fechas seleccionadas
        self.label_fecha_inicio = tk.Label(date_frame, text=self.fechaInicio)
        self.label_fecha_inicio.grid(row=0, column=1, padx=10, pady=5)

        # Botón para seleccionar fecha de fin
        date_button_fin = tk.Button(date_frame, text="Fecha de Fin", command=lambda: self.ask_date("fin"), width=20)
        date_button_fin.grid(row=1, column=0, padx=10, pady=5)

        # Labels para mostrar las fechas seleccionadas
        self.label_fecha_fin = tk.Label(date_frame, text=self.fechaFin)
        self.label_fecha_fin.grid(row=1, column=1, padx=10, pady=5)

        # Frame para horas
        time_frame = tk.Frame(datetime_frame)
        time_frame.pack(side=tk.RIGHT, padx=20, pady=10)

        # Labels y entradas para las horas
        time_label_inicio = tk.Label(time_frame, text="Hora de Inicio (HH:MM)", width=20)
        time_label_inicio.grid(row=0, column=0, padx=10, pady=5)

        # Entrada para la hora de inicio
        self.entry_hora_inicio = tk.Entry(time_frame)
        self.entry_hora_inicio.grid(row=0, column=1, padx=10, pady=5)

        # Label y entrada para la hora de fin
        time_label_fin = tk.Label(time_frame, text="Hora de Fin (HH:MM)", width=20)
        time_label_fin.grid(row=1, column=0, padx=10, pady=5)

        # Entrada para la hora de fin
        self.entry_hora_fin = tk.Entry(time_frame)
        self.entry_hora_fin.grid(row=1, column=1, padx=10, pady=5)

        # Frame para la selección de pala
        pala_frame = tk.LabelFrame(self.root, text="Selecciona Pala", padx=10, pady=10)
        pala_frame.pack(pady=10, fill="x")

        # Lista de valores para la pala
        pala_values = [f"LE{str(i).zfill(3)}" for i in range(1, 38)]

        # Combobox para seleccionar pala
        self.pala_var = tk.StringVar()
        self.pala_combobox = ttk.Combobox(pala_frame, textvariable=self.pala_var, values=pala_values, state="readonly", width=70)
        self.pala_combobox.pack(fill="x", padx=10, pady=10)

        # Frame para los botones de acción
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=10)

        # Botón para generar la consulta
        generate_button = tk.Button(action_frame, text="Generar Consulta", command=self.generate_query, width=30, font=("Helvetica", 12, "bold"))
        generate_button.pack(side=tk.LEFT, padx=10)

        # Botón para copiar la consulta
        copy_button = tk.Button(action_frame, text="Copiar Consulta", command=self.copy_query, width=30, font=("Helvetica", 12, "bold"))
        copy_button.pack(side=tk.LEFT, padx=10)

        # Cuadro de texto para mostrar la consulta
        self.query_text = scrolledtext.ScrolledText(self.root, width=80, height=15)
        self.query_text.pack(pady=10)

    # Métodos de la clase
    # Método para seleccionar consultas del servidor
    def select_server_queries(self):
        self.queries = QUERIES_SERVER
        self.update_query_combobox()
    # Método para seleccionar consultas de MTBox
    def select_mtbox_queries(self):
        self.queries = QUERIES_MTBOX
        self.update_query_combobox()
    # Método para actualizar el combobox de consultas
    def update_query_combobox(self):
        self.query_combobox.config(values=list(self.queries.keys()), state="readonly")
    
    # Método para seleccionar la fecha
    def ask_date(self, which):
        date_window = tk.Toplevel(self.root)
        date_window.title("Seleccionar Fecha")
        # Calendario para seleccionar la fecha
        cal = Calendar(date_window, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(pady=20)
        # Método para establecer la fecha seleccionada
        def set_date():
            date = cal.get_date()
            if which == "inicio":
                self.fechaInicio = date
                self.label_fecha_inicio.config(text=self.fechaInicio)
            else:
                self.fechaFin = date
                self.label_fecha_fin.config(text=self.fechaFin)
            date_window.destroy()
        # Botón para seleccionar la fecha
        select_button = tk.Button(date_window, text="Seleccionar", command=set_date)
        select_button.pack(pady=20)

    # Método para generar la consulta
    def generate_query(self):
        # Formatear las fechas y horas
        self.horaInicio = self.entry_hora_inicio.get() + ":00"  # Añadir segundos por defecto
        self.horaFin = self.entry_hora_fin.get() + ":00"  # Añadir segundos por defecto
        # Formatear las fechas y horas
        fechaInicio = f"{self.fechaInicio} {self.horaInicio}.0000000 -04:00"
        fechaFin = f"{self.fechaFin} {self.horaFin}.0000000 -04:00"
        self.pala = self.pala_var.get()

        # Obtener la consulta seleccionada
        selected_query = self.query_var.get()
        query = self.queries.get(selected_query, "")

        # Reemplazar las fechas y pala en la consulta
        if self.fechaInicio and self.horaInicio and self.fechaFin and self.horaFin and self.pala:
            query = query.format(fechaInicio=fechaInicio, fechaFin=fechaFin, pala=self.pala)

        # Mostrar la consulta en el cuadro de texto
        self.query_text.delete(1.0, tk.END)
        self.query_text.insert(tk.END, query)
    # Método para copiar la consulta
    def copy_query(self):
        # Copiar el contenido del cuadro de texto al portapapeles
        self.root.clipboard_clear()
        self.root.clipboard_append(self.query_text.get(1.0, tk.END).strip())
        messagebox.showinfo("Copiado", "La consulta SQL ha sido copiada al portapapeles.")

# Crear la ventana principal de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = SQLQueryApp(root)
    root.mainloop()
