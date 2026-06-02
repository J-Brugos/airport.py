from tkinter import *
from tkinter import filedialog, messagebox

# Matplotlib se incrusta en Tkinter para que las graficas queden dentro del panel.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

# Funciones del proyecto. La interfaz las llama para no repetir la logica principal.
from airport import (
    AddAirport,
    Airport,
    IsSchengenAirport,
    LoadAirports,
    MapAirports,
    RemoveAirport,
    SaveSchengenAirports,
    SetSchengen
)
from aircraft import (
    CountTerminalOccupancy,
    LoadArrivals,
    LoadDepartures,
    MergeMovements,
    NightAircraft,
    SaveFlights,
    MapFlights,
    AssignGatesAtTime,
    TimeToMinutes
)
from LEBL import (
    LoadAirportStructure,
    AssignGate,
    AssignNightGates,
    ResetGates
)


# Ventana principal de Tkinter que coordina datos, botones, graficas y registros.
class AirportDashboardUI:
    def __init__(self):
        # Paleta de colores usada por todos los paneles y graficas.
        self.colors = {
            "background": "#0B1020",
            "panel": "#111A2E",
            "panel2": "#17233B",
            "accent": "#00D4FF",
            "accent2": "#2F80ED",
            "success": "#2ECC71",
            "warning": "#F2C94C",
            "error": "#EB5757",
            "text": "#EAF2FF",
            "muted": "#8FA3BF"
        }

        # Datos cargados desde los archivos del proyecto y reutilizados por los botones.
        self.airports = []
        self.aircrafts = []
        self.departures = []
        self.movements = []
        self.night_aircrafts = []
        self.bcn_airport = None
        self.logs = []
        self.buttons = []
        self.view_buttons = []
        self.selected_view = ""
        self.selected_gate_hour = "00:00"
        self.selected_gate_area = ""

        # La ventana principal debe existir antes de crear cualquier widget de Tkinter.
        self.window = Tk()
        self.window.title("Airport Management System")
        self.window.geometry("1480x880")
        self.window.configure(bg=self.colors["background"])
        self.window.minsize(1280, 760)

        self.setup_theme()
        self.build_layout()
        self.render_chart("Select Display")
        self.update_output("Dashboard ready.", "success")
        self.update_log("SYSTEM ONLINE - Airport operations dashboard initialized.", "success")

    def setup_theme(self):
        # Fuentes compartidas para mantener la interfaz visualmente coherente.
        self.font_title = ("Arial", 22, "bold")
        self.font_subtitle = ("Arial", 10)
        self.font_section = ("Arial", 10, "bold")
        self.font_button = ("Arial", 9, "bold")
        self.font_text = ("Arial", 10)
        self.font_small = ("Arial", 9)

    def build_layout(self):
        # Distribucion general: controles a la izquierda, grafica al centro y salidas a la derecha.
        self.build_title_bar()

        self.body = Frame(self.window, bg=self.colors["background"])
        self.body.pack(fill="both", expand=True, padx=14, pady=(8, 10))

        self.left_panel = Frame(self.body, bg=self.colors["panel"], width=280, highlightthickness=1,
                                highlightbackground=self.colors["accent2"])
        self.left_panel.pack(side="left", fill="y", padx=(0, 10))
        self.left_panel.pack_propagate(False)

        self.right_panel = Frame(self.body, bg=self.colors["panel"], width=330, highlightthickness=1,
                                 highlightbackground=self.colors["accent2"])
        self.right_panel.pack(side="right", fill="y")
        self.right_panel.pack_propagate(False)

        self.center_panel = Frame(self.body, bg=self.colors["background"])
        self.center_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.build_control_panel()
        self.build_chart_panel()
        self.build_text_panels()
        self.build_airport_table()
        self.build_display_selector()

    def build_title_bar(self):
        # Cabecera superior del proyecto.
        title_bar = Frame(self.window, bg=self.colors["panel"], height=72, highlightthickness=1,
                          highlightbackground=self.colors["accent2"])
        title_bar.pack(fill="x", padx=14, pady=(14, 0))
        title_bar.pack_propagate(False)

        title_block = Frame(title_bar, bg=self.colors["panel"])
        title_block.pack(side="left", fill="both", expand=True, padx=18, pady=10)

        Label(
            title_block,
            text="AIRPORT MANAGEMENT SYSTEM",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=self.font_title
        ).pack(anchor="w")

        Label(
            title_block,
            text="Operations Dashboard · Version 4",
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=self.font_subtitle
        ).pack(anchor="w")

        status = Frame(title_bar, bg=self.colors["panel"])
        status.pack(side="right", padx=18)

        Label(
            status,
            text="PROJECT GROUP 2",
            bg=self.colors["panel2"],
            fg=self.colors["accent"],
            font=("Arial", 10, "bold"),
            padx=14,
            pady=8
        ).pack()

    def build_control_panel(self):
        # Botones del panel izquierdo organizados por version del proyecto.
        Label(
            self.left_panel,
            text="CONTROL PANEL",
            bg=self.colors["panel"],
            fg=self.colors["accent"],
            font=("Arial", 13, "bold")
        ).pack(anchor="w", padx=14, pady=(14, 8))

        Label(
            self.left_panel,
            text="Input",
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=self.font_section
        ).pack(anchor="w", padx=14, pady=(0, 4))

        self.command_entry = Entry(
            self.left_panel,
            bg=self.colors["panel2"],
            fg=self.colors["text"],
            insertbackground=self.colors["accent"],
            relief="flat",
            font=self.font_text
        )
        self.command_entry.pack(fill="x", padx=14, pady=(0, 8), ipady=7)

        self.control_inner = Frame(self.left_panel, bg=self.colors["panel"])
        self.control_inner.pack(fill="both", expand=True, padx=8, pady=(0, 10))

        self.add_section("Version 1 · Core", [
            ("Load Airports", self.load_airports_file),
            ("Add Airport", self.add_airport),
            ("Remove Airport", self.remove_airport),
            ("Set Schengen", self.set_schengen_all),
            ("Save Schengen", self.save_schengen),
            ("Map Airports", self.map_airports)
        ])

        self.add_section("Version 2 · Flights", [
            ("Load Arrivals", self.load_arrivals_file),
            ("Save Flights", self.save_flights),
            ("Map Flights", self.map_flights)
        ])

        self.add_section("Version 3 · Gates", [
            ("Load LEBL Structure", self.load_lebl_structure),
            ("Assign Gates", self.assign_gates)
        ])

        self.add_section("Version 4 · Movements / Analytics", [
            ("Load Departures", self.load_departures_file),
            ("Merge Movements", self.merge_movements),
            ("Assign Night Gates", self.assign_night_gates)
        ])

    def add_section(self, title, actions):
        # Crea un grupo etiquetado de botones de accion.
        frame = LabelFrame(
            self.control_inner,
            text=title,
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=self.font_section,
            labelanchor="nw",
            bd=1,
            relief="solid"
        )
        frame.pack(fill="x", padx=10, pady=7)

        i = 0
        while i < len(actions):
            label, command = actions[i]
            button = self.create_action_button(frame, label, command)
            button.pack(fill="x", padx=8, pady=3)
            self.buttons.append(button)
            i += 1

    def create_action_button(self, parent, label, command):
        # Los Label se usan como botones oscuros personalizados.
        button = Label(
            parent,
            text=label,
            bg=self.colors["panel2"],
            fg=self.colors["text"],
            font=self.font_button,
            anchor="w",
            padx=12,
            pady=8,
            cursor="hand2",
            highlightthickness=1,
            highlightbackground=self.colors["accent2"],
            highlightcolor=self.colors["accent"]
        )
        button.bind("<Button-1>", lambda event: command())
        button.bind("<Enter>", lambda event: button.configure(bg=self.colors["accent2"], fg=self.colors["text"]))
        button.bind("<Leave>", lambda event: button.configure(bg=self.colors["panel2"], fg=self.colors["text"]))
        return button

    def build_chart_panel(self):
        # Panel central de graficas. Los controles de hora y area solo aparecen en ocupacion de puertas.
        chart_header = Frame(self.center_panel, bg=self.colors["panel"], height=42, highlightthickness=1,
                             highlightbackground=self.colors["accent2"])
        chart_header.pack(fill="x", pady=(0, 8))
        chart_header.pack_propagate(False)

        self.chart_title = Label(
            chart_header,
            text="Select Display",
            bg=self.colors["panel"],
            fg=self.colors["accent"],
            font=("Arial", 13, "bold")
        )
        self.chart_title.pack(side="left", padx=14)

        self.gate_hour_frame = Frame(chart_header, bg=self.colors["panel"])
        self.gate_hour_var = StringVar(value=self.selected_gate_hour)

        Label(
            self.gate_hour_frame,
            text="Hour",
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=self.font_small
        ).pack(side="left", padx=(0, 6))

        hour_options = []
        i = 0
        while i < 24:
            hour_options.append(f"{i:02d}:00")
            i += 1

        self.gate_hour_menu = OptionMenu(self.gate_hour_frame, self.gate_hour_var, *hour_options,
                                         command=self.change_gate_hour)
        self.gate_hour_menu.configure(
            bg=self.colors["panel2"],
            fg=self.colors["text"],
            activebackground=self.colors["accent2"],
            activeforeground=self.colors["text"],
            highlightthickness=1,
            highlightbackground=self.colors["accent2"],
            relief="flat",
            font=self.font_small,
            width=6
        )
        self.gate_hour_menu["menu"].configure(
            bg=self.colors["panel2"],
            fg=self.colors["text"],
            activebackground=self.colors["accent2"],
            activeforeground=self.colors["text"]
        )
        self.gate_hour_menu.pack(side="left")

        Label(
            self.gate_hour_frame,
            text="Area",
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=self.font_small
        ).pack(side="left", padx=(12, 6))

        self.gate_area_var = StringVar(master=self.window, value="Select area")
        self.gate_area_menu = OptionMenu(self.gate_hour_frame, self.gate_area_var, "Select area",
                                         command=self.change_gate_area)
        self.gate_area_menu.configure(
            bg=self.colors["panel2"],
            fg=self.colors["text"],
            activebackground=self.colors["accent2"],
            activeforeground=self.colors["text"],
            highlightthickness=1,
            highlightbackground=self.colors["accent2"],
            relief="flat",
            font=self.font_small,
            width=8
        )
        self.gate_area_menu["menu"].configure(
            bg=self.colors["panel2"],
            fg=self.colors["text"],
            activebackground=self.colors["accent2"],
            activeforeground=self.colors["text"]
        )
        self.gate_area_menu.pack(side="left")

        self.info_label = Label(
            chart_header,
            text="Airports: 0 | Schengen: 0 | Arrivals: 0 | Departures: 0 | LEBL: No",
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=self.font_small
        )
        self.info_label.pack(side="right", padx=14)

        self.figure = Figure(figsize=(8.6, 5.8), dpi=100, facecolor=self.colors["panel"])
        self.chart_ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.center_panel)
        self.canvas.get_tk_widget().configure(bg=self.colors["panel"], highlightthickness=1,
                                              highlightbackground=self.colors["accent2"])
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def build_text_panels(self):
        # Tarjetas de estado del lado derecho.
        self.output_box = self.create_text_card(self.right_panel, "Operation Output", 10)
        self.log_box = self.create_text_card(self.right_panel, "System Log / Details", 19)

    def create_text_card(self, parent, title, height):
        frame = Frame(parent, bg=self.colors["panel"], highlightthickness=1, highlightbackground=self.colors["accent2"])
        frame.pack(fill="x", padx=12, pady=(12, 0))

        Label(
            frame,
            text=title,
            bg=self.colors["panel"],
            fg=self.colors["accent"],
            font=self.font_section
        ).pack(anchor="w", padx=10, pady=(8, 4))

        text = Text(
            frame,
            height=height,
            bg=self.colors["panel2"],
            fg=self.colors["text"],
            insertbackground=self.colors["accent"],
            relief="flat",
            wrap="word",
            font=self.font_small,
            padx=8,
            pady=8
        )
        text.pack(fill="x", padx=10, pady=(0, 10))
        text.configure(state="disabled")
        return text

    def build_airport_table(self):
        # Tabla inferior para mantener visibles los aeropuertos cargados mientras cambia la grafica.
        bottom = Frame(self.center_panel, bg=self.colors["panel"], height=150, highlightthickness=1,
                       highlightbackground=self.colors["accent2"])
        bottom.pack(fill="x", pady=(8, 0))
        bottom.pack_propagate(False)

        header = Frame(bottom, bg=self.colors["panel"])
        header.pack(fill="x", padx=12, pady=(8, 4))

        Label(
            header,
            text="Loaded Airports",
            bg=self.colors["panel"],
            fg=self.colors["accent"],
            font=self.font_section
        ).pack(side="left")

        self.airport_count_label = Label(
            header,
            text="0 shown",
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=self.font_small
        )
        self.airport_count_label.pack(side="right")

        table_frame = Frame(bottom, bg=self.colors["panel"])
        table_frame.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        self.airport_table = Text(
            table_frame,
            height=5,
            bg=self.colors["panel2"],
            fg=self.colors["text"],
            insertbackground=self.colors["accent"],
            relief="flat",
            wrap="none",
            font=("Menlo", 10),
            padx=8,
            pady=6
        )
        self.airport_table.pack(side="left", fill="both", expand=True)
        self.airport_table.configure(state="disabled")

        airport_scroll = Scrollbar(table_frame, orient="vertical", command=self.airport_table.yview)
        airport_scroll.pack(side="right", fill="y")
        self.airport_table.configure(yscrollcommand=airport_scroll.set)

        self.update_airport_table()

    def build_display_selector(self):
        # Solo estos selectores redibujan la grafica central.
        selector = Frame(self.right_panel, bg=self.colors["panel"], highlightthickness=1,
                         highlightbackground=self.colors["accent2"])
        selector.pack(fill="x", padx=12, pady=12)

        Label(
            selector,
            text="Display Selector",
            bg=self.colors["panel"],
            fg=self.colors["accent"],
            font=self.font_section
        ).pack(anchor="w", padx=10, pady=(8, 4))

        views = [
            "Plot Airports",
            "Plot Arrivals",
            "Plot Airlines",
            "Plot Arrivals Schengen",
            "Plot Gate Occupancy",
            "Plot Day Occupancy"
        ]

        i = 0
        while i < len(views):
            view = views[i]
            button = Label(
                selector,
                text=view,
                bg=self.colors["panel2"],
                fg=self.colors["text"],
                font=self.font_button,
                anchor="w",
                padx=10,
                pady=7,
                cursor="hand2",
                highlightthickness=1,
                highlightbackground=self.colors["accent2"]
            )
            button.bind("<Button-1>", lambda event, v=view: self.render_chart(v))
            button.bind("<Enter>", lambda event, b=button: b.configure(bg=self.colors["accent2"]))
            button.bind("<Leave>", lambda event, b=button, v=view: self.restore_view_button_color(b, v))
            button.pack(fill="x", padx=10, pady=2)
            self.view_buttons.append(button)
            i += 1

    def restore_view_button_color(self, button, view):
        # Restaura el color tras pasar el raton manteniendo resaltada la vista seleccionada.
        if view == self.selected_view:
            button.configure(bg=self.colors["accent2"])
        else:
            button.configure(bg=self.colors["panel2"])

    def clear_axis(self):
        # Reinicia el eje de Matplotlib antes de dibujar la vista seleccionada.
        self.chart_ax.clear()
        self.chart_ax.set_facecolor(self.colors["panel"])
        self.chart_ax.tick_params(colors=self.colors["muted"])

        spines = list(self.chart_ax.spines.values())
        i = 0
        while i < len(spines):
            spines[i].set_color(self.colors["panel2"])
            i += 1

        self.chart_ax.grid(True, color="#263752", alpha=0.35)

    def render_chart(self, view_name="Select Display"):
        # Distribuidor central de las vistas del selector derecho.
        self.selected_view = view_name
        self.chart_title.config(text=view_name)
        self.update_hour_selector()
        self.update_view_buttons()
        self.clear_axis()

        if view_name == "Plot Airports":
            self.render_plot_airports()
        elif view_name == "Plot Arrivals":
            self.render_plot_arrivals()
        elif view_name == "Plot Airlines":
            self.render_plot_airlines()
        elif view_name == "Plot Arrivals Schengen":
            self.render_plot_arrivals_schengen()
        elif view_name == "Plot Gate Occupancy":
            self.render_plot_gate_occupancy()
        elif view_name == "Plot Day Occupancy":
            self.render_plot_day_occupancy()
        else:
            self.render_placeholder("Select a plot from the Display Selector.")

        if view_name == "Plot Airlines":
            self.figure.subplots_adjust(left=0.08, right=0.99, top=0.88, bottom=0.22)
        else:
            self.figure.tight_layout()
        self.canvas.draw_idle()
        self.update_info()

    def update_hour_selector(self):
        # La ocupacion de puertas necesita selectores extra; las demas vistas usan cabecera simple.
        if self.selected_view == "Plot Gate Occupancy":
            self.update_gate_area_options()
            self.gate_hour_frame.pack(side="right", padx=(0, 8))
        else:
            self.gate_hour_frame.pack_forget()

    def change_gate_hour(self, value):
        # Redibuja la ocupacion de puertas cuando cambia la hora seleccionada.
        self.selected_gate_hour = value
        if self.selected_view == "Plot Gate Occupancy":
            self.render_chart("Plot Gate Occupancy")

    def change_gate_area(self, value):
        # Redibuja la ocupacion de puertas cuando cambia el area seleccionada.
        self.selected_gate_area = value
        if self.selected_view == "Plot Gate Occupancy":
            self.render_chart("Plot Gate Occupancy")

    def update_gate_area_options(self):
        # Reconstruye el menu de areas a partir de la estructura LEBL cargada.
        options = []

        if self.bcn_airport is not None:
            t = 0
            while t < len(self.bcn_airport.terminals):
                terminal = self.bcn_airport.terminals[t]
                a = 0
                while a < len(terminal.boarding_areas):
                    options.append(terminal.name + "-" + terminal.boarding_areas[a].name)
                    a += 1
                t += 1

        if len(options) == 0:
            options.append("Select area")

        if self.selected_gate_area == "" or self.selected_gate_area not in options:
            self.selected_gate_area = options[0]
            self.gate_area_var.set(self.selected_gate_area)

        menu = self.gate_area_menu["menu"]
        menu.delete(0, "end")

        i = 0
        while i < len(options):
            option = options[i]
            menu.add_command(label=option, command=lambda value=option: self.gate_area_var.set(value) or self.change_gate_area(value))
            i += 1

    def refresh_current_display(self):
        # Los botones que cambian datos refrescan solo la grafica seleccionada.
        plot_views = [
            "Plot Airports",
            "Plot Arrivals",
            "Plot Airlines",
            "Plot Arrivals Schengen",
            "Plot Gate Occupancy",
            "Plot Day Occupancy"
        ]

        if self.selected_view in plot_views:
            self.render_chart(self.selected_view)
        else:
            self.update_info()

    def update_view_buttons(self):
        # Resalta el boton de la vista seleccionada.
        i = 0
        while i < len(self.view_buttons):
            button = self.view_buttons[i]

            if button.cget("text") == self.selected_view:
                button.configure(bg=self.colors["accent2"])
            else:
                button.configure(bg=self.colors["panel2"])

            i += 1

    def render_plot_airports(self):
        # Versión integrada en la interfaz de PlotAirports.
        if not self.airports:
            self.render_placeholder("No airports loaded.")
            return

        schengen_count = 0
        non_schengen_count = 0

        i = 0
        while i < len(self.airports):
            if self.airports[i].SCHENGEN:
                schengen_count += 1
            else:
                non_schengen_count += 1
            i += 1

        self.chart_ax.bar(["Airports"], [schengen_count], color=self.colors["success"], label="Schengen")
        self.chart_ax.bar(["Airports"], [non_schengen_count], bottom=[schengen_count], color=self.colors["warning"],
                          label="Non-Schengen")
        self.chart_ax.set_title("Schengen airports", color=self.colors["text"], fontsize=14, weight="bold")
        self.chart_ax.set_ylabel("Count", color=self.colors["muted"])
        self.chart_ax.legend(facecolor=self.colors["panel"], edgecolor=self.colors["panel2"], labelcolor=self.colors["text"])

    def render_flights(self):
        # Versión integrada en la interfaz de PlotArrivals.
        if not self.aircrafts:
            self.render_placeholder("No arrivals loaded.")
            return

        frequencies = [0] * 24

        i = 0
        while i < len(self.aircrafts):
            minutes = TimeToMinutes(self.aircrafts[i].arrival)

            if minutes != -1:
                hour = minutes // 60
                frequencies[hour] += 1

            i += 1

        hours = list(range(24))
        self.chart_ax.bar(hours, frequencies, color=self.colors["accent"])
        self.chart_ax.set_title("Arrivals by Hour", color=self.colors["text"], fontsize=14, weight="bold")
        self.chart_ax.set_xlabel("Hour", color=self.colors["muted"])
        self.chart_ax.set_ylabel("Arrivals", color=self.colors["muted"])
        self.chart_ax.set_xticks(hours)

    def render_plot_arrivals(self):
        # Funcion auxiliar pequena para conservar nombres claros en el selector.
        self.render_flights()

    def render_plot_airlines(self):
        # Grafica vertical de todas las aerolineas con etiquetas inclinadas.
        if not self.aircrafts:
            self.render_placeholder("No arrivals loaded.")
            return

        airlines = []
        frequencies = []

        i = 0
        while i < len(self.aircrafts):
            airline = self.aircrafts[i].airline
            found = False
            position = 0

            j = 0
            while j < len(airlines):
                if airlines[j] == airline:
                    found = True
                    position = j
                j += 1

            if found:
                frequencies[position] += 1
            else:
                airlines.append(airline)
                frequencies.append(1)

            i += 1

        x_positions = list(range(len(airlines)))
        label_size = 8

        if len(airlines) > 80:
            label_size = 5
        elif len(airlines) > 50:
            label_size = 6
        elif len(airlines) > 30:
            label_size = 7

        self.chart_ax.bar(x_positions, frequencies, color=self.colors["warning"], width=0.72)
        self.chart_ax.set_xticks(x_positions)
        self.chart_ax.set_xticklabels(airlines, rotation=45, ha="right", fontsize=label_size)

        labels = self.chart_ax.get_xticklabels()
        i = 0
        while i < len(labels):
            if i % 2 == 0:
                labels[i].set_y(-0.015)
            else:
                labels[i].set_y(-0.055)
            i += 1

        self.chart_ax.set_title("Number of flights by airline", color=self.colors["text"], fontsize=14, weight="bold")
        self.chart_ax.set_xlabel("Airline", color=self.colors["muted"], labelpad=24)
        self.chart_ax.set_ylabel("Number of flights", color=self.colors["muted"])
        self.chart_ax.tick_params(axis="x", pad=2)
        self.chart_ax.margins(x=0.01)

    def render_plot_arrivals_schengen(self):
        # Grafica horaria apilada para llegadas Schengen y no Schengen.
        if not self.aircrafts:
            self.render_placeholder("No arrivals loaded.")
            return

        schengen_hours = [0] * 24
        non_schengen_hours = [0] * 24

        i = 0
        while i < len(self.aircrafts):
            aircraft = self.aircrafts[i]
            minutes = TimeToMinutes(aircraft.arrival)

            if aircraft.origin != "" and minutes != -1:
                hour = minutes // 60

                if IsSchengenAirport(aircraft.origin[:2]):
                    schengen_hours[hour] += 1
                else:
                    non_schengen_hours[hour] += 1

            i += 1

        hours = list(range(24))
        self.chart_ax.bar(hours, schengen_hours, color=self.colors["success"], label="Schengen")
        self.chart_ax.bar(hours, non_schengen_hours, bottom=schengen_hours, color=self.colors["warning"],
                          label="Non-Schengen")
        self.chart_ax.set_title("Arrivals by hour: Schengen / Non-Schengen", color=self.colors["text"], fontsize=14,
                                weight="bold")
        self.chart_ax.set_xlabel("Hour of day", color=self.colors["muted"])
        self.chart_ax.set_ylabel("Number of arrivals", color=self.colors["muted"])
        self.chart_ax.set_xticks(hours)
        self.chart_ax.legend(facecolor=self.colors["panel"], edgecolor=self.colors["panel2"], labelcolor=self.colors["text"])

    def draw_box(self, x, y, width, height, color, text, text_color, font_size):
        # Utilidad para dibujar rectangulos etiquetados en la vista de puertas.
        rect = Rectangle((x, y), width, height, facecolor=color, edgecolor=self.colors["accent"],
                         linewidth=1.0, alpha=0.95)
        self.chart_ax.add_patch(rect)
        self.chart_ax.text(
            x + width / 2,
            y + height / 2,
            text,
            color=text_color,
            ha="center",
            va="center",
            fontsize=font_size,
            weight="bold"
        )

    def find_selected_gate_area(self):
        # Busca la terminal y el area seleccionadas en el menu superior.
        if self.bcn_airport is None:
            return None, None

        t = 0
        while t < len(self.bcn_airport.terminals):
            terminal = self.bcn_airport.terminals[t]

            a = 0
            while a < len(terminal.boarding_areas):
                area = terminal.boarding_areas[a]
                label = terminal.name + "-" + area.name

                if label == self.selected_gate_area:
                    return terminal, area

                a += 1

            t += 1

        return None, None

    def render_gate_area_detail(self, title_suffix):
        # Vista detallada de puertas: nombre de puerta y avion asignado o libre.
        terminal, area = self.find_selected_gate_area()

        if terminal is None or area is None:
            self.render_placeholder("Select a boarding area.")
            return

        self.chart_ax.axis("off")
        self.chart_ax.set_xlim(0, 100)
        self.chart_ax.set_ylim(0, 100)

        area_type = "Schengen" if area.area_type else "Non-Schengen"
        occupied = 0

        i = 0
        while i < len(area.gates):
            if area.gates[i].occupied:
                occupied += 1
            i += 1

        self.chart_ax.set_title(
            terminal.name + " area " + area.name + " · " + area_type + " · " + title_suffix,
            color=self.colors["text"],
            fontsize=14,
            weight="bold"
        )

        self.draw_box(
            35,
            88,
            30,
            7,
            self.colors["accent2"],
            f"{occupied}/{len(area.gates)} occupied",
            self.colors["text"],
            10
        )

        cols = 8

        if len(area.gates) > 32:
            cols = 10
        elif len(area.gates) <= 16:
            cols = 6

        rows = (len(area.gates) - 1) // cols + 1
        cell_width = 90 / cols
        cell_height = min(8.5, 68 / rows)
        start_x = 5
        start_y = 78

        font_size = 6.5

        if rows > 5:
            font_size = 5.2

        i = 0
        while i < len(area.gates):
            gate = area.gates[i]
            col = i % cols
            row = i // cols
            x = start_x + col * cell_width
            y = start_y - row * cell_height

            if gate.occupied:
                color = self.colors["error"]
                text_color = self.colors["text"]
                aircraft_text = str(gate.aircraft_id)
            else:
                color = self.colors["success"]
                text_color = self.colors["background"]
                aircraft_text = "FREE"

            rect = Rectangle(
                (x, y),
                cell_width * 0.9,
                cell_height * 0.78,
                facecolor=color,
                edgecolor=self.colors["accent2"],
                linewidth=0.7
            )
            self.chart_ax.add_patch(rect)

            self.chart_ax.text(
                x + cell_width * 0.45,
                y + cell_height * 0.39,
                gate.name + "\n" + aircraft_text,
                color=text_color,
                ha="center",
                va="center",
                fontsize=font_size,
                weight="bold",
                clip_on=True
            )

            i += 1

    def render_plot_gate_occupancy(self):
        # Reconstruye el estado de puertas desde el inicio del dia hasta la hora seleccionada.
        if self.bcn_airport is None:
            self.render_placeholder("No LEBL structure loaded.")
            return

        title_suffix = "current state"

        if self.movements and self.night_aircrafts != -1:
            ResetGates(self.bcn_airport)

            if self.night_aircrafts:
                AssignNightGates(self.bcn_airport, self.night_aircrafts)

            selected_hour = int(self.selected_gate_hour.split(":")[0])
            hour = 0
            current_unassigned = 0

            while hour <= selected_hour:
                time = f"{hour:02d}:00"
                current_unassigned = AssignGatesAtTime(self.bcn_airport, self.movements, time)
                hour += 1

            title_suffix = self.selected_gate_hour + " end state"
            self.update_output(
                f"Gate occupancy shown for {self.selected_gate_hour}. Unassigned in that hour: {current_unassigned}.",
                "success" if current_unassigned == 0 else "warning"
            )

        self.render_gate_area_detail(title_suffix)

    def render_plot_day_occupancy(self):
        # Ejecuta el flujo completo de 24 horas de la V4 y grafica la ocupacion por terminal.
        if self.bcn_airport is None:
            self.render_placeholder("No LEBL structure loaded.")
            return

        if not self.movements:
            self.render_placeholder("No merged movements available. Load arrivals/departures and use Merge Movements.")
            return

        from LEBL import ResetGates
        from LEBL import AssignNightGates

        ResetGates(self.bcn_airport)

        if self.night_aircrafts != -1 and self.night_aircrafts:
            AssignNightGates(self.bcn_airport, self.night_aircrafts)

        hours = []
        unassigned = []
        terminal_counts = []

        t = 0
        while t < len(self.bcn_airport.terminals):
            terminal_counts.append([])
            t += 1

        hour = 0
        while hour < 24:
            time = f"{hour:02d}:00"
            not_assigned = AssignGatesAtTime(self.bcn_airport, self.movements, time)
            counts = CountTerminalOccupancy(self.bcn_airport)

            hours.append(hour)
            unassigned.append(not_assigned)

            t = 0
            while t < len(counts):
                terminal_counts[t].append(counts[t])
                t += 1

            hour += 1

        t = 0
        while t < len(self.bcn_airport.terminals):
            self.chart_ax.plot(hours, terminal_counts[t], marker="o",
                               label=self.bcn_airport.terminals[t].name + " occupied gates")
            t += 1

        self.chart_ax.bar(hours, unassigned, alpha=0.35, color=self.colors["error"], label="Unassigned arrivals")
        self.chart_ax.set_title("Gate occupancy during the day", color=self.colors["text"], fontsize=14, weight="bold")
        self.chart_ax.set_xlabel("Hour of day", color=self.colors["muted"])
        self.chart_ax.set_ylabel("Aircraft / gates", color=self.colors["muted"])
        self.chart_ax.set_xticks(hours)
        self.chart_ax.legend(facecolor=self.colors["panel"], edgecolor=self.colors["panel2"], labelcolor=self.colors["text"])

    def render_placeholder(self, message):
        # Muestra un mensaje centrado cuando todavia no se puede dibujar una grafica.
        self.chart_ax.axis("off")
        self.chart_ax.text(
            0.5,
            0.55,
            message,
            ha="center",
            va="center",
            color=self.colors["muted"],
            fontsize=14,
            transform=self.chart_ax.transAxes
        )

    def status_prefix(self, status):
        # Etiquetas de texto para no depender solo del color.
        if status == "success":
            return "OK"
        if status == "warning":
            return "WARNING"
        if status == "error":
            return "ERROR"
        return "INFO"

    def status_color(self, status):
        # Relaciona cada estado con su color de la interfaz.
        if status == "success":
            return self.colors["success"]
        if status == "warning":
            return self.colors["warning"]
        if status == "error":
            return self.colors["error"]
        return self.colors["accent"]

    def update_output(self, message, status="info"):
        # Resultado breve de la ultima operacion.
        prefix = self.status_prefix(status)
        self.write_text_box(self.output_box, prefix + " · " + message, status)

    def update_log(self, message, status="info"):
        # Mantiene el historial reciente de operaciones en el panel de detalles.
        prefix = self.status_prefix(status)
        line = prefix + " · " + message
        self.logs.append(line)

        if len(self.logs) > 50:
            self.logs = self.logs[-50:]

        text = "\n".join(self.logs[-10:])
        self.write_text_box(self.log_box, text, status)

    def write_text_box(self, text_box, message, status):
        # Los cuadros de texto quedan bloqueados salvo durante la actualizacion.
        text_box.configure(state="normal")
        text_box.delete("1.0", END)
        text_box.insert(END, message)
        text_box.tag_configure("status", foreground=self.status_color(status))
        text_box.tag_add("status", "1.0", "1.end")
        text_box.configure(state="disabled")

    def update_airport_table(self):
        # Reescribe la tabla inferior cuando cambian los datos de aeropuertos.
        if not hasattr(self, "airport_table"):
            return

        self.airport_table.configure(state="normal")
        self.airport_table.delete("1.0", END)

        if not self.airports:
            self.airport_table.insert(END, "No airports loaded. Use Load Airports to import Airports.txt.\n")
        else:
            self.airport_table.insert(END, "ICAO      LATITUDE     LONGITUDE    STATUS\n")
            self.airport_table.insert(END, "-----------------------------------------------\n")

            i = 0
            while i < len(self.airports):
                airport = self.airports[i]

                if airport.SCHENGEN:
                    status = "Schengen"
                else:
                    status = "Non-Schengen"

                line = f"{airport.ICAO:<8} {airport.latitude:>10.4f} {airport.longitude:>11.4f}   {status}\n"
                self.airport_table.insert(END, line)
                i += 1

        self.airport_table.configure(state="disabled")
        self.airport_table.yview_moveto(0)

        if hasattr(self, "airport_count_label"):
            self.airport_count_label.config(text=f"{len(self.airports)} shown")

    def update_info(self):
        # Actualiza los contadores compactos de la cabecera de la grafica.
        schengen = 0
        i = 0
        while i < len(self.airports):
            if self.airports[i].SCHENGEN:
                schengen += 1
            i += 1

        if self.bcn_airport is None:
            lebl_text = "No"
        else:
            lebl_text = "Yes"

        self.info_label.config(
            text=(
                f"Airports: {len(self.airports)} | Schengen: {schengen} | "
                f"Arrivals: {len(self.aircrafts)} | Departures: {len(self.departures)} | LEBL: {lebl_text}"
            )
        )
        self.update_airport_table()

    def update_schengen_values(self, loaded_airports):
        # Aplica la funcion SetSchengen del proyecto a todos los aeropuertos cargados.
        i = 0
        while i < len(loaded_airports):
            SetSchengen(loaded_airports[i])
            i += 1

    def load_airports_file(self):
        # Abre un archivo de aeropuertos y lo carga mediante la funcion del proyecto.
        filename = filedialog.askopenfilename(
            title="Select airports file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )

        if not filename:
            self.update_log("Airport load cancelled.", "warning")
            return

        try:
            self.airports = LoadAirports(filename)
        except ValueError as exc:
            self.update_output(str(exc), "error")
            self.update_log(str(exc), "error")
            messagebox.showerror("Error", str(exc))
            return

        self.update_schengen_values(self.airports)
        self.update_output(f"Loaded {len(self.airports)} airports.", "success")
        self.update_log(f"Airports loaded from {filename}", "success")
        self.refresh_current_display()

    def save_schengen(self):
        # Guarda solo los aeropuertos Schengen en el archivo elegido.
        if not self.airports:
            self.warn("No airports loaded")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".txt")

        if not filename:
            self.update_log("Save Schengen cancelled.", "warning")
            return

        result = SaveSchengenAirports(self.airports, filename)

        if result == -1:
            self.error("No Schengen airports")
        else:
            self.update_output("Schengen airports saved.", "success")
            self.update_log(f"Schengen airport file saved to {filename}", "success")

    def add_airport(self):
        # Anade un aeropuerto desde el campo Input: CODE LAT LON.
        data = self.command_entry.get().strip().split()

        if len(data) != 3:
            self.warn("Format: CODE LAT LON")
            return

        try:
            code = data[0].upper()

            if len(code) != 4 or not code.isalpha():
                self.warn("ICAO code must have exactly 4 letters")
                return

            lat = float(data[1])
            lon = float(data[2])

            airport = Airport(code, lat, lon, False)
            SetSchengen(airport)
            result = AddAirport(self.airports, airport)

            if result == -1:
                self.update_output("Airport already exists or ICAO code is invalid.", "warning")
                self.update_log(f"Add airport skipped: {code} is duplicated or invalid.", "warning")
                return

            self.command_entry.delete(0, END)
            self.update_output(f"Airport {code} added.", "success")
            self.update_log(f"Airport {code} added manually.", "success")
            self.refresh_current_display()

        except ValueError:
            self.error("Latitude and longitude must be numbers")

    def remove_airport(self):
        # Elimina un aeropuerto por codigo ICAO desde el campo Input.
        code = self.command_entry.get().strip().upper()

        if not code:
            self.warn("Enter the ICAO code to remove")
            return

        result = RemoveAirport(self.airports, code)

        if result == -1:
            self.error("Airport not found")
            return

        self.command_entry.delete(0, END)
        self.update_output(f"Airport {code} removed.", "success")
        self.update_log(f"Airport {code} removed from loaded list.", "success")
        self.refresh_current_display()

    def set_schengen_all(self):
        # Recalcula el estado Schengen de todos los aeropuertos cargados.
        if not self.airports:
            self.warn("No airports loaded")
            return

        self.update_schengen_values(self.airports)
        self.update_output("Schengen values updated.", "success")
        self.update_log("Schengen values recalculated for all loaded airports.", "success")
        self.refresh_current_display()

    def map_airports(self):
        # Escribe el KML de aeropuertos usando la funcion MapAirports del proyecto.
        if not self.airports:
            self.warn("No airports loaded")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".kml")

        if not filename:
            self.update_log("Map airports cancelled.", "warning")
            return

        MapAirports(self.airports, filename)
        self.update_output("Airport KML saved.", "success")
        self.update_log(f"Airport KML saved to {filename}", "success")

    def load_arrivals_file(self):
        # Carga los vuelos de llegada para la Versión 2 y graficas posteriores.
        filename = filedialog.askopenfilename(
            title="Select arrivals file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )

        if not filename:
            self.update_log("Arrival load cancelled.", "warning")
            return

        self.aircrafts = LoadArrivals(filename)
        self.update_output(f"Loaded {len(self.aircrafts)} arrivals.", "success")
        self.update_log(f"Arrivals loaded from {filename}", "success")
        self.refresh_current_display()

    def load_departures_file(self):
        # Carga las salidas usadas para combinar movimientos en la Versión 4.
        filename = filedialog.askopenfilename(
            title="Select departures file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )

        if not filename:
            self.update_log("Departure load cancelled.", "warning")
            return

        self.departures = LoadDepartures(filename)
        self.update_output(f"Loaded {len(self.departures)} departures.", "success")
        self.update_log(f"Departures loaded from {filename}", "success")
        self.refresh_current_display()

    def save_flights(self):
        # Guarda las llegadas cargadas usando la funcion SaveFlights del proyecto.
        if not self.aircrafts:
            self.warn("No arrivals loaded")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".txt")

        if not filename:
            self.update_log("Save flights cancelled.", "warning")
            return

        SaveFlights(self.aircrafts, filename)
        self.update_output("Flights saved.", "success")
        self.update_log(f"Flights saved to {filename}", "success")

    def map_flights(self):
        # Escribe el archivo KML con las trayectorias de los vuelos.
        if not self.aircrafts:
            self.warn("No arrivals loaded")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".kml")

        if not filename:
            self.update_log("Map flights cancelled.", "warning")
            return

        MapFlights(self.aircrafts, filename)
        self.update_output("Flights KML saved.", "success")
        self.update_log(f"Flights KML saved to {filename}", "success")

    def load_lebl_structure(self):
        # Carga terminales, areas, puertas y asignacion de aerolineas por terminal.
        filename = filedialog.askopenfilename(
            title="Select terminal structure file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )

        if not filename:
            self.update_log("LEBL structure load cancelled.", "warning")
            return

        self.bcn_airport = LoadAirportStructure(filename)

        if self.bcn_airport == -1:
            self.bcn_airport = None
            self.error("Could not load LEBL structure")
            return

        self.update_output("LEBL structure loaded.", "success")
        self.update_log(f"LEBL structure loaded from {filename}", "success")
        self.refresh_current_display()

    def assign_gates(self):
        # Asignacion de Versión 3: las llegadas ocupan puertas durante el resto del dia.
        if self.bcn_airport is None:
            self.warn("No LEBL structure loaded")
            return

        if not self.aircrafts:
            self.warn("No arrivals loaded")
            return

        ResetGates(self.bcn_airport)

        assigned = 0
        failed = 0

        i = 0
        while i < len(self.aircrafts):
            result = AssignGate(self.bcn_airport, self.aircrafts[i])

            if result == 0:
                assigned += 1
            else:
                failed += 1

            i += 1

        self.update_output(f"Assigned: {assigned} | Failed: {failed}", "success" if failed == 0 else "warning")
        self.update_log(f"Gate assignment completed. Assigned={assigned}, Failed={failed}", "info")
        self.refresh_current_display()

    def merge_movements(self):
        # Paso de Versión 4: une llegadas y salidas por identificador de avion.
        if not self.aircrafts:
            self.warn("No arrivals loaded")
            return

        if not self.departures:
            self.warn("No departures loaded")
            return

        result = MergeMovements(self.aircrafts, self.departures)

        if result == -1:
            self.error("Could not merge movements")
            return

        self.movements = result
        self.night_aircrafts = NightAircraft(self.movements)

        night_count = 0
        if self.night_aircrafts != -1:
            night_count = len(self.night_aircrafts)

        self.update_output(f"Merged movements: {len(self.movements)} | Night aircraft: {night_count}", "success")
        self.update_log("Arrivals and departures merged for Version 4 gate flow.", "success")
        self.refresh_current_display()

    def assign_night_gates(self):
        # Inicia el dia ocupando puertas para aviones que solo tienen salida.
        if self.bcn_airport is None:
            self.warn("No LEBL structure loaded")
            return

        if not self.movements:
            self.merge_movements()

        if not self.night_aircrafts or self.night_aircrafts == -1:
            self.warn("No night aircraft available")
            return

        ResetGates(self.bcn_airport)
        result = AssignNightGates(self.bcn_airport, self.night_aircrafts)

        if result == -1:
            self.error("Night gate assignment failed")
            return

        self.update_output("Night aircraft gates assigned.", "success")
        self.update_log("AssignNightGates executed for start-of-day state.", "success")
        self.refresh_current_display()

    def warn(self, message):
        # Gestion comun de avisos en salida, registro y ventana emergente.
        self.update_output(message, "warning")
        self.update_log(message, "warning")
        messagebox.showwarning("Warning", message)

    def error(self, message):
        # Gestion comun de errores en salida, registro y ventana emergente.
        self.update_output(message, "error")
        self.update_log(message, "error")
        messagebox.showerror("Error", message)

    def run(self):
        # Inicia el bucle principal de Tkinter.
        self.window.mainloop()


if __name__ == "__main__":
    dashboard = AirportDashboardUI()
    dashboard.run()
