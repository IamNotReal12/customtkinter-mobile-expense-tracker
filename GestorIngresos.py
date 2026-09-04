import customtkinter as kc
from time import strftime
import logging
import json
import os

carpeta = "dt"
ArchivoJson = "Dtb.json"
RutaCarpeta = os.path.join(carpeta, ArchivoJson)

if not os.path.exists(carpeta):
    os.mkdir(carpeta)

Mis_Ejercicios = {}

if os.path.exists(carpeta):
    try:
        if os.path.exists(RutaCarpeta):
            with open(RutaCarpeta, "r", encoding="utf-8") as archivo:
                Mis_Ejercicios = json.load(archivo)
    except json.JSONDecodeError:
        Mis_Ejercicios = {}
        with open(RutaCarpeta, "w", encoding="utf-8") as archivo:
            json.dump(Mis_Ejercicios, archivo)

logging.basicConfig(
    filename="console.log",
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
)


class VentanaSecundaria(kc.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.GestorKC = parent

        self.geometry("400x400")
        self.configure(fg_color="#1E293B")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.title("Ingresar Monto")

        self.transient(parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame_interno = kc.CTkFrame(self, fg_color="transparent")
        self.frame_interno.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.frame_interno.grid_propagate(False)

        self.frame_interno.grid_rowconfigure((0, 1, 2), weight=1)
        self.frame_interno.grid_columnconfigure(0, weight=1)

        texto_dinamico = "¿Cuánto deseas ingresar?"
        ref = self.GestorKC.Referencia

        if ref == 1:
            texto_dinamico = "¿Cuánto destinarás a Configuración?"
            logging.info("Seccion de configuracion,abierta correctamente.")
        elif ref == 2:
            texto_dinamico = "¿Cuánto destinarás a Chats/Mensajes?"
            logging.info("Seccion de Chats/Mensajes,abierta correctamente.")
        elif ref == 3:
            texto_dinamico = "¿Cuánto destinarás a Llamadas?"
            logging.info("Seccion de Llamadas,abierta correctamente.")
        elif ref == 4:
            texto_dinamico = "¿Cuánto destinarás a Navegación Web?"
            logging.info("Seccion de Navegacion Web,abierta correctamente.")
        elif ref == 5:
            texto_dinamico = "¿Cuánto destinarás a Música?"
        elif ref == 6:
            texto_dinamico = "¿Cuánto deseas ingresar a otros?"

        self.label_titulo = kc.CTkLabel(
            self.frame_interno,
            text=texto_dinamico,
            font=("Helvetica", 15, "bold"),
            text_color="#F8FAFC",
        )
        self.label_titulo.grid(row=0, column=0, sticky="s", pady=(0, 10))

        self.entry_monto = kc.CTkEntry(
            self.frame_interno,
            placeholder_text="$ 0.00",
            width=200,
            height=40,
            border_width=2,
            border_color="#334155",
            fg_color="#0F172A",
            text_color="#4ADE80",
            font=("Helvetica", 16, "bold"),
            justify="center",
            corner_radius=10,
        )
        self.entry_monto.grid(row=1, column=0)
        self.entry_monto.focus()

        self.BotonE = kc.CTkButton(
            self.frame_interno,
            text="Enviar",
            command=self.Ingresos,
            fg_color="#042B87",
            hover_color="#16264C",
        )
        self.BotonE.grid(row=2, column=0)

    def Ingresos(self):
        
        
        
        try:
            DineroSuma = int(self.entry_monto.get())
            
            if DineroSuma <=0:
                return
            self.GestorKC.DineroInicial += DineroSuma
            self.GestorKC.LabelDinero.configure(text=f"${self.GestorKC.DineroInicial}")
            
            Mis_Ejercicios["DineroInicial"] = self.GestorKC.DineroInicial
            with open(RutaCarpeta, "w", encoding="utf-8") as archivo:
                json.dump(Mis_Ejercicios, archivo)
                
            logging.info("Dinero depositado correctamente.")
            self.destroy()
        except ValueError:
            self.entry_monto.configure(border_color="red")
            logging.error("Error:Tipo de dato incorrecto/Campo vacio")


class GestorI(kc.CTk):
    def __init__(self):
        super().__init__()
        self.ventana_abierta = None
        self.DineroInicial = Mis_Ejercicios.get("DineroInicial", 0)
        self.Referencia = 0
        self.title("GestorI - Mobile UI")
        self.configure(fg_color="#0F172A")

        self.after(0, lambda: self.state("zoomed"))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.FrameCelular = kc.CTkFrame(
            self,
            width=375,
            height=680,
            border_width=4,
            border_color="#334155",
            fg_color="#1E293B",
            corner_radius=32,
        )
        self.FrameCelular.grid(row=0, column=0)
        self.FrameCelular.grid_propagate(False)
        self.FrameCelular.grid_rowconfigure((0, 1, 2), weight=1)
        self.FrameCelular.grid_columnconfigure(0, weight=1)

        self.frameSuperior = kc.CTkFrame(
            self.FrameCelular,
            width=340,
            height=45,
            fg_color="#334155",
            corner_radius=12,
        )
        self.frameSuperior.grid(row=0, column=0, sticky="N", pady=15)
        self.frameSuperior.grid_propagate(False)
        self.frameSuperior.grid_columnconfigure(0, weight=1)
        self.frameSuperior.grid_rowconfigure(0, weight=1)

        self.LabelTiempo = kc.CTkLabel(
            self.frameSuperior,
            text="",
            text_color="#F8FAFC",
            font=("Helvetica", 16, "bold"),
        )
        self.LabelTiempo.grid(row=0, column=0, sticky="W", padx=(2, 0))

        self.TiempoUpdate()

        self.FrameCamera = kc.CTkFrame(
            self.frameSuperior,
            width=50,
            height=20,
            fg_color="#1E293B",
            corner_radius=10,
        )
        self.FrameCamera.place(relx=0.5, rely=0.5, anchor="center")

        self.FrameOpciones = kc.CTkFrame(
            self.FrameCelular,
            width=340,
            height=540,
            fg_color="#1E293B",
            border_width=2,
            border_color="#334155",
            corner_radius=24,
        )
        self.FrameOpciones.grid(row=1, column=0, sticky="N", pady=(0, 10))
        self.FrameOpciones.grid_propagate(False)

        self.FrameOpciones.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.FrameOpciones.grid_columnconfigure((0, 1, 2), weight=1)

        self.SubFrame1 = kc.CTkFrame(
            self.FrameOpciones, width=80, height=80, fg_color="transparent"
        )
        self.SubFrame1.grid(row=0, column=0)
        self.SubFrame1.pack_propagate(False)
        self.Icono1 = kc.CTkButton(
            self.SubFrame1,
            text="⚙️",
            font=("Helvetica", 22),
            width=60,
            height=60,
            corner_radius=16,
            fg_color="#334155",
            hover_color="#475569",
            command=self.VSecuIcon1,
        )
        self.Icono1.place(relx=0.5, rely=0.5, anchor="center")

        self.SubFrame2 = kc.CTkFrame(
            self.FrameOpciones, width=80, height=80, fg_color="transparent"
        )
        self.SubFrame2.grid(row=0, column=1)
        self.SubFrame2.pack_propagate(False)
        self.Icono2 = kc.CTkButton(
            self.SubFrame2,
            text="💬",
            font=("Helvetica", 22),
            width=60,
            height=60,
            corner_radius=16,
            fg_color="#334155",
            hover_color="#475569",
            command=self.VSecuIcon2,
        )
        self.Icono2.place(relx=0.5, rely=0.5, anchor="center")

        self.SubFrame3 = kc.CTkFrame(
            self.FrameOpciones, width=80, height=80, fg_color="transparent"
        )
        self.SubFrame3.grid(row=0, column=2)
        self.SubFrame3.pack_propagate(False)
        self.Icono3 = kc.CTkButton(
            self.SubFrame3,
            text="📞",
            font=("Helvetica", 22),
            width=60,
            height=60,
            corner_radius=16,
            fg_color="#334155",
            hover_color="#475569",
            command=self.VSecuIcon3,
        )
        self.Icono3.place(relx=0.5, rely=0.5, anchor="center")

        self.SubFrame4 = kc.CTkFrame(
            self.FrameOpciones, width=80, height=80, fg_color="transparent"
        )
        self.SubFrame4.grid(row=1, column=0)
        self.SubFrame4.pack_propagate(False)
        self.Icono4 = kc.CTkButton(
            self.SubFrame4,
            text="🌐",
            font=("Helvetica", 22),
            width=60,
            height=60,
            corner_radius=16,
            fg_color="#334155",
            hover_color="#475569",
            command=self.VSecuIcon4,
        )
        self.Icono4.place(relx=0.5, rely=0.5, anchor="center")

        self.SubFrame5 = kc.CTkFrame(
            self.FrameOpciones, width=80, height=80, fg_color="transparent"
        )
        self.SubFrame5.grid(row=1, column=1)
        self.SubFrame5.pack_propagate(False)
        self.Icono5 = kc.CTkButton(
            self.SubFrame5,
            text="🎵",
            font=("Helvetica", 22),
            width=60,
            height=60,
            corner_radius=16,
            fg_color="#334155",
            hover_color="#475569",
            command=self.VSecuIcon5,
        )
        self.Icono5.place(relx=0.5, rely=0.5, anchor="center")

        self.SubFrame6 = kc.CTkFrame(
            self.FrameOpciones, width=80, height=80, fg_color="transparent"
        )
        self.SubFrame6.grid(row=1, column=2)
        self.SubFrame6.pack_propagate(False)
        self.Icono6 = kc.CTkButton(
            self.SubFrame6,
            text="📷",
            font=("Helvetica", 22),
            width=60,
            height=60,
            corner_radius=16,
            fg_color="#334155",
            hover_color="#475569",
            command=self.VSecuIcon6,
        )
        self.Icono6.place(relx=0.5, rely=0.5, anchor="center")

        self.Icono1.bind(
            "<Enter>", lambda e: self.Icono1.configure(width=66, height=66)
        )
        self.Icono1.bind(
            "<Leave>", lambda e: self.Icono1.configure(width=60, height=60)
        )

        self.Icono2.bind(
            "<Enter>", lambda e: self.Icono2.configure(width=66, height=66)
        )
        self.Icono2.bind(
            "<Leave>", lambda e: self.Icono2.configure(width=60, height=60)
        )

        self.Icono3.bind(
            "<Enter>", lambda e: self.Icono3.configure(width=66, height=66)
        )
        self.Icono3.bind(
            "<Leave>", lambda e: self.Icono3.configure(width=60, height=60)
        )

        self.Icono4.bind(
            "<Enter>", lambda e: self.Icono4.configure(width=66, height=66)
        )
        self.Icono4.bind(
            "<Leave>", lambda e: self.Icono4.configure(width=60, height=60)
        )

        self.Icono5.bind(
            "<Enter>", lambda e: self.Icono5.configure(width=66, height=66)
        )
        self.Icono5.bind(
            "<Leave>", lambda e: self.Icono5.configure(width=60, height=60)
        )

        self.Icono6.bind(
            "<Enter>", lambda e: self.Icono6.configure(width=66, height=66)
        )
        self.Icono6.bind(
            "<Leave>", lambda e: self.Icono6.configure(width=60, height=60)
        )

        self.ButtonExit = kc.CTkButton(
            self.FrameCelular,
            text="",
            fg_color="#334155",
            hover_color="#475569",
            border_width=2,
            border_color="#475569",
            width=120,
            height=6,
            corner_radius=50,
            command=self.Exit,
        )
        self.ButtonExit.grid(row=2, column=0, sticky="S", pady=(0, 15))

        self.FrameDinero = kc.CTkFrame(
            self.FrameOpciones,
            width=300,
            height=200,
            fg_color="#334155",
            border_width=2,
            border_color="#475569",
        )
        self.FrameDinero.grid(row=2, column=0, columnspan=3, rowspan=2, pady=(10, 20))
        self.FrameDinero.grid_propagate(False)

        self.LabelDinero = kc.CTkLabel(
            self.FrameDinero,
            text=f"${self.DineroInicial}",
            font=("comic sans", 30, "bold"),
            text_color="#08f137",
        )
        self.LabelDinero.place(rely=0.5, relx=0.5, anchor="center")

    def TiempoUpdate(self):
        Tiempo = strftime("%H:%M:%S")
        self.LabelTiempo.configure(text=Tiempo)
        self.LabelTiempo.after(1000, self.TiempoUpdate)

    def Exit(self):
        self.destroy()

    def abrir_ventana_secundaria(self):
        if self.ventana_abierta is None or not self.ventana_abierta.winfo_exists():
            self.ventana_abierta = VentanaSecundaria(self)
        else:
            self.ventana_abierta.destroy()
            self.ventana_abierta = VentanaSecundaria(self)

    def VSecuIcon1(self):
        self.Referencia = 1
        self.abrir_ventana_secundaria()

    def VSecuIcon2(self):
        self.Referencia = 2
        self.abrir_ventana_secundaria()

    def VSecuIcon3(self):
        self.Referencia = 3
        self.abrir_ventana_secundaria()

    def VSecuIcon4(self):
        self.Referencia = 4
        self.abrir_ventana_secundaria()

    def VSecuIcon5(self):
        self.Referencia = 5
        self.abrir_ventana_secundaria()

    def VSecuIcon6(self):
        self.Referencia = 6
        self.abrir_ventana_secundaria()


if __name__ == "__main__":
    App = GestorI()
    App.mainloop()