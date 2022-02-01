from tkinter import *
import tkinter as tk
from tkinter.messagebox import *
from database.database import WorkspaceData
from tkinter import ttk
from Models.models import *
import json
import datetime
from ScrollableFrame import ScrollableFrame
from ScrolledWindow import ScrolledWindow
from CustomClasses.CustomClasses import *
from CreateWordHelper.CreateWordHelper import *
import shutil


def raise_frame(frame):
    frame.tkraise()


def _ask_before_close():
    result = askquestion("Confirmación", "Desea cerrar la aplicación?")
    if result == "yes":
        root.destroy()  # Destroys the UI and terminates the program as no other thread is running


def create_backup():
    # get hora Formato 24hrs
    backup_hour = 18
    backup_min = 0

    now = datetime.datetime.now()

    if backup_hour == now.hour and backup_min == now.minute:
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H-%M")
        home = expanduser("~")
        print("Home")
        print(home)
        backup_app_path = home + "\\Registros Pedigree App\\Backups\\"

        if not path.exists(backup_app_path):
            os.mkdir(backup_app_path)

        # take db value and save to a file in system
        src = "database.db"
        dst = backup_app_path + "\\database " + current_time
        shutil.copyfile(src, dst)

        print("Es momento de hacer un backup")
    else:
        print("No es momento de hacer un backup")

    # Check current hour and create backup if matchs backup hour.
    root.after(60000, create_backup)  # Cada 1 min


class LoginFrame(tk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Init backups func
        root.after(2000, create_backup)
#        root.mainloop()

        # Global variables
        self.preguntas_seguridad = (
            'Seleccionar', 'Nombre de tu primera mascota?', 'Lugar de nacimiento?', 'Nombre de mejor amigo?',
            'Curso favorito?', 'Pasatiempos favorito?')

        bgloginLabel = Label(root, image=photo, width=800, height=400)
        bgloginLabel.place(x=0, y=0, relwidth=1, relheight=1)
        bgloginLabel.configure(background="black")

        frame = Frame(root, bg='white', width=560, height=320)
        frame.place(relx=.5, rely=.5, anchor="s")

        userimageLabel = Label(frame, image=userimage, bg='white')
        userimageLabel.place(x=10, y=50)
        mailLabel = Label(frame, text='Correo', font=('arial', 15, 'bold'), bg='white', fg='black')
        mailLabel.place(x=220, y=32)
        self.mailentry = Entry(frame, font=('arial', 15,), bg='white', fg='black')
        self.mailentry.place(x=220, y=70)

        passLabel = Label(frame, text='Contraseña', font=('arial', 15, 'bold'), bg='white', fg='black')
        passLabel.place(x=220, y=120)
        self.passentry = Entry(frame, show="*", font=('arial', 15,), bg='white', fg='black')
        self.passentry.place(x=220, y=160)
        regbutton = Button(frame, text='Registrar nueva cuenta?', font=('arial', 11,), bd=0, fg='gray20', bg='white',
                           cursor='hand2', command=lambda:raise_frame(RegisterFrame(root)),
                           activebackground='white', activeforeground='gray20')
        regbutton.place(x=220, y=200)

        forgetbutton = Button(frame, text='Olvidaste contraseña?', font=('arial', 11,), bd=0, fg='red', bg='white',
                              cursor='hand2', command=self.forget_password,
                              activebackground='white', activeforeground='gray20')
        forgetbutton.place(x=410, y=200)

        loginbutton2 = Button(frame, text='Login', font=('arial', 14, 'bold'), fg='white', bg='gray20', cursor='hand2',
                              activebackground='gray20', activeforeground='white', command=self.signin)
        loginbutton2.place(x=450, y=240)

    def signin(self):
        # raise_frame(PedigreeOperations(root))
        # return
        if self.mailentry.get() == '' or self.passentry.get() == '':
            showerror('Error', 'Todos los campos son obligatorios')
        else:
            try:
                # Tratar de logearse.
                db = WorkspaceData()
                data = db.check_login(self.mailentry.get(), self.passentry.get())

                if data == False:
                    showerror('error', 'Correo o contraseña invalido')
                else:
                    raise_frame(PedigreeOperations(root))
                    global user_mail
                    user_mail = self.mailentry.get()
                    # De aqui debemos abrir la otra ventana.
            except Exception as e:
                showerror('Error', f"Error debido a: {e}", parent=root)

    def register_window(self):
        return

    def reset_password(self):
        result = db.reset_pwd(self.mailentry.get(), self.securityquescombo.get(),
                              self.answerforgetEntry.get(), self.newpassEntry.get())

        if result == "exito":
            showinfo('Exito', 'La contraseña fue cambiada, porfavor ingresa de nuevo', parent=self.root2)
        elif result == "no_existe":
            showerror('Error', 'La cuenta no existe porfavor intenta de nuevo ', parent=self.root2)
        elif result == "bad_data":
            showerror('Error', 'La respuesta es erronea porfavor intenta de nuevo ', parent=self.root2)
        else:
            return

    def forget_password(self):

        if self.mailentry.get() == '':
            showerror('Error', 'Porfavor ingresa el correo de la cuenta para resetear la contraseña.', parent=root)
        else:

            self.root2 = Toplevel()
            self.root2.title('Olvidé mi contraseña')
            self.root2.geometry('470x560+400+60')
            self.root2.config(bg='white')
            self.root2.focus_force()
            self.root2.grab_set()

            forgetLabel = Label(self.root2, text='Olvidé', font=('Lucida Sans', 15, 'bold'), fg='black',
                                bg='white')
            forgetLabel.place(x=128, y=10)
            forgetpassLabel = Label(self.root2, text='Contraseña', font=('Lucida Sans', 15, 'bold'), fg='green',
                                    bg='white')
            forgetpassLabel.place(x=205, y=10)

            forgetimageLabel = Label(self.root2, image=passwordimage, bg='white')
            forgetimageLabel.place(x=170, y=70)

            securityquesLabel = Label(self.root2, text='Pregunta de seguridad', font=('Lucida Sans', 13, 'bold'),
                                      fg='black',
                                      bg='white')
            securityquesLabel.place(x=60, y=220)

            self.securityquescombo = ttk.Combobox(self.root2, font=('Lucida Sans', 13), state='readonly',
                                             justify=CENTER,
                                             width=28)
            self.securityquescombo['values'] = self.preguntas_seguridad
            self.securityquescombo.place(x=60, y=260)
            self.securityquescombo.current(0)

            answerforgetLabel = Label(self.root2, text='Respuesta', font=('Lucida Sans', 13, 'bold'), fg='black',
                                      bg='white')
            answerforgetLabel.place(x=60, y=310)
            self.answerforgetEntry = Entry(self.root2, font=('Lucida Sans', 13,), fg='black', width=30,
                                      bg='white')
            self.answerforgetEntry.place(x=60, y=350)

            newpassLabel = Label(self.root2, text='Nueva contraseña', font=('Lucida Sans', 13, 'bold'), fg='black',
                                 bg='white')
            newpassLabel.place(x=60, y=400)
            self.newpassEntry = Entry(self.root2, font=('Lucida Sans', 13,), fg='black', width=30,
                                 bg='white')
            self.newpassEntry.place(x=60, y=440)

            changepassbutton = Button(self.root2, text='Cambiar contraseña', font=('arial', 13, 'bold'), bg='green',
                                      fg='white', cursor='hand2', activebackground='green',
                                      activeforeground='white',
                                      command=lambda: self.reset_password())

            changepassbutton.place(x=130, y=500)

            self.root2.mainloop()

            # except Exception as e:
            #     showerror('Error', f"Error due to: {e}", parent=root)


class RegisterFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Global variables

        preguntas_seguridad = (
            'Seleccionar', 'Nombre de tu primera mascota?', 'Lugar de nacimiento?', 'Nombre de mejor amigo?',
            'Curso favorito?', 'Pasatiempos favorito?')

#        bg = PhotoImage(file='abci_bg.jpg')
        bgLabel = Label(root, image=photo)
        bgLabel.place(x=0, y=0, relwidth=1, relheight=1)
        bgLabel.configure(background="black")
        registerFrame = Frame(root, bg='white', width=650, height=screen_height-155)
        registerFrame.place(x=630, y=30)

        titleLabel = Label(registerFrame, text='Ingresa tus datos', font=('arial', 15, 'bold '), bg='white',
                           fg='gold', )
        titleLabel.place(x=240, y=5)

        firstnameLabel = Label(registerFrame, text='Nombre', font=('Lucida Sans', 13, 'bold'), bg='white',
                               fg='gray20', )
        firstnameLabel.place(x=20, y=80)
        self.entryfirstname = Entry(registerFrame, font=('Lucida Sans', 13), bg='lightgray')
        self.entryfirstname.place(x=20, y=115, width=250)

        emailLabel = Label(registerFrame, text='Correo', font=('Lucida Sans', 13, 'bold'), bg='white',
                              fg='gray20', )
        emailLabel.place(x=370, y=80)
        self.entryemail = Entry(registerFrame, font=('Lucida Sans', 13), bg='lightgray')
        self.entryemail.place(x=370, y=115, width=250)


        questionLabel = Label(registerFrame, text='Pregunta de seguridad', font=('Lucida Sans', 13, 'bold'), bg='white',
                              fg='gray20', )
        questionLabel.place(x=20, y=200)
        self.comboquestion = ttk.Combobox(registerFrame, font=('Lucida Sans', 13), state='readonly', justify=CENTER)
        self.comboquestion['values'] = preguntas_seguridad
        self.comboquestion.place(x=20, y=235, width=250)
        self.comboquestion.current(0)

        answerLabel = Label(registerFrame, text='Respuesta', font=('Lucida Sans', 13, 'bold'), bg='white',
                            fg='gray20', )
        answerLabel.place(x=370, y=200)
        self.entryanswer = Entry(registerFrame, font=('Lucida Sans', 13), bg='lightgray')
        self.entryanswer.place(x=370, y=235, width=250)

        passwordLabel = Label(registerFrame, text='Contraseña', font=('Lucida Sans', 13, 'bold'), bg='white',
                              fg='gray20', )
        passwordLabel.place(x=20, y=320)
        self.entrypassword = Entry(registerFrame, show="*", font=('Lucida Sans', 13), bg='lightgray')
        self.entrypassword.place(x=20, y=355, width=250)

        confirmpasswordLabel = Label(registerFrame, text='Confirma Contraseña', font=('Lucida Sans', 13, 'bold'),
                                     bg='white',
                                     fg='gray20', )
        confirmpasswordLabel.place(x=370, y=320)
        self.entryconfirmpassword = Entry(registerFrame, show="*", font=('Lucida Sans', 13), bg='lightgray')
        self.entryconfirmpassword.place(x=370, y=355, width=250)

        self.check = IntVar()
        checkButton = Checkbutton(registerFrame, text='Acepto los terminos y condiciones', variable=self.check, onvalue=1,
                                  offvalue=0, font=('Lucida Sans', 13, 'bold'), bg='white')
        checkButton.place(x=20, y=510)

        registerbutton = Button(registerFrame, text='Registrar', font=('Lucida Sans', 13, 'bold'), fg='white',
                                bg='gray20', cursor='hand2', bd=0, activeforeground='white',
                                command=self.register)
        registerbutton.place(x=100, y=570)

        loginbutton1 = Button(registerFrame, text='Tienes cuenta?, Ingresa!', font=('Lucida Sans', 13, 'bold'), fg='white',
                              bg='gray20', cursor='hand2', bd=0, activeforeground='white',
                              command=lambda:raise_frame(LoginFrame(root)))
        loginbutton1.place(x=370, y=570)

    def register(self):
        if self.entryfirstname.get() == '' or self.entryemail.get() == '' or self.entrypassword.get() == '' \
                or self.entryconfirmpassword.get() == '' or self.comboquestion.get() == 'Seleccionar' or self.entryanswer.get() == '':
            showerror('Error', "Todos los campos son obligatorios", parent=root)

        elif self.entrypassword.get() != self.entryconfirmpassword.get():
            showerror('Error', "Contraseña no coincide", parent=root)

        elif self.check.get() == 0:
            showerror('Error', "Porfavor acepte los terminos y condiciones", parent=root)
        else:
            # register user with data
            userdata_l = [(self.entryfirstname.get(),
                           self.entryemail.get(),
                           self.entrypassword.get(),
                           self.comboquestion.get(),
                           self.entryanswer.get())]
            table = "users"

            # Check if was succesfull and go to next Frame.
            response, detail = db.register(table, userdata_l)
            if response:
                # go to main
                showinfo('Registro exitoso!', 'Bienvenido')
                raise_frame(PedigreeOperations(root))
                global user_mail
                user_mail = self.entryemail.get()
            else:
                if detail == "error":
                    showerror('Error', "Error al registrarse intenta de nuevo.", parent=root)
                elif detail == "mail_in_use":
                    showerror('Error', "El correo ya está en uso, intente con uno diferente.", parent=root)


class PedigreeOperations(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.registered_pedigree_path = ""
        self.registered_cliente_path = ""

        self.registered_pedigree_path_edit = ""
        self.registered_cliente_path_edit = ""

        bgloginLabel = Label(root, image=photo, width=800, height=400)
        bgloginLabel.place(x=0, y=0, relwidth=1, relheight=1)
        bgloginLabel.configure(background="black")

        notebook = ttk.Notebook(bgloginLabel)

        tab1 = Frame(notebook)
        tab2 = Frame(notebook)
        tab3 = Frame(notebook)

        notebook.add(tab1, text="Crear Registros")
        notebook.add(tab2, text="Editar Registros")
        notebook.add(tab3, text="Buscar Clientes")

        notebook.pack(expand=True, fill="both")

        # Generar contenido para tab1 (Formulario Frame):

        # Global variables
        self.gene_fromDB_loaded = False
        self.genealogia_data = dict()
        self.gene_data_padre = dict()
        self.gene_data_madre = dict()
        self.init_form_gene_data()

        # Formulario frame (tab1)
        tab1bg = Label(tab1, image=photo, width=screen_width, height=screen_height)
        tab1bg.place(x=0, y=0, relwidth=1, relheight=1)
        tab1bg.configure(background="black")
        tab1bg.pack()

        # Formulario Frame
        formularioFrame = Frame(tab1, bg='white', width=900, height=screen_height-155)
        formularioFrame.place(x=45, y=30)
        self.populate_formulario_frame(formularioFrame, tab1)

        # Search Frame (tab2)
        tab2bg = Label(tab2, image=photo, width=screen_width, height=screen_height)
        tab2bg.place(x=0, y=0, relwidth=1, relheight=1)
        tab2bg.configure(background="black")
        tab2bg.pack()

        # Edit Frame (tab2)
        editFrame = Frame(tab2, bg='white', width=650, height=screen_height-155)
        editFrame.place(x=45, y=30)
        self.populate_edit_frame(editFrame, tab2)

        # Search Clientes Frame (tab3)
        tab3bg = Label(tab3, image=photo, width=screen_width, height=screen_height)
        tab3bg.place(x=0, y=0, relwidth=1, relheight=1)
        tab3bg.configure(background="black")
        tab3bg.pack()

        # Clientes Search Frame (tab3)
        clientesFrame = Frame(tab3, bg='white', width=650, height=screen_height-155)
        clientesFrame.place(x=45, y=30)

        self.populate_clientes_frame(clientesFrame, tab3)

        # Aca debo definir variables globales dentro de la Clase.

    # Register Formuarios

    def populate_formulario_frame(self, formularioFrame, tab1):

        bg_label = Label(formularioFrame, bg='white', image=bn_bg_abc, width=200, height=200)
        bg_label.place(x=250, y=200)

        titleLabel = Label(formularioFrame, text='Ingresa los datos del cliente y su cachorro',
                           font=('arial', 14, 'bold'), bg='white',
                           fg='gold', )
        titleLabel.place(x=110, y=10)

        old_client_Label = Label(formularioFrame, text='Afijo Cliente*', font=('Lucida Sans', 12, 'bold'), bg='white',
                              fg='gray20', )
        old_client_Label.place(x=20, y=50)

        self.entry_propietario_afijo = Entry(formularioFrame, font=('Lucida Sans', 12), bg='lightgray')
        self.entry_propietario_afijo.place(x=20, y=75, width=250)

        self.check_auto_afijo_code = IntVar()
        checkButton_auto_afijo = Checkbutton(formularioFrame, text='Auto', variable=self.check_auto_afijo_code, onvalue=1,
                                  offvalue=0, font=('Lucida Sans', 13), bg='white',
                                  command=lambda:self.set_auto_afijo_code())
        checkButton_auto_afijo.place(x=280, y=70)

        buscar_propietario_label = Label(formularioFrame, text='Cliente', font=('Lucida Sans', 12, 'bold'), bg='white',
                              fg='gray20', )
        buscar_propietario_label.place(x=370, y=40)
        self.buscar_propietario_btn = Button(formularioFrame, text='Buscar cliente', font=('arial', 12, 'bold'), fg='white',
                              bg='gray20', cursor='hand2', bd=0, activeforeground='white',
                              command=lambda:self.buscar_cliente())
        self.buscar_propietario_btn.place(x=370, y=65)

        buscar_padres_label = Label(formularioFrame, text='Padres', font=('Lucida Sans', 12, 'bold'), bg='white',
                              fg='gray20', )
        buscar_padres_label.place(x=500, y=40)
        self.buscar_afijos_padres_btn = Button(formularioFrame, text='Buscar padres', font=('arial', 12, 'bold'), fg='white',
                              bg='gray20', cursor='hand2', bd=0, activeforeground='white',
                              command=lambda:self.buscar_padres_afijos_data())
        self.buscar_afijos_padres_btn.place(x=500, y=65)


        firstnameLabel = Label(formularioFrame, text='Nombre de cachorro*', font=('Lucida Sans', 11, 'bold'), bg='white',
                               fg='gray20', )
        firstnameLabel.place(x=20, y=100)
        self.entry_nombre_cachorro = Entry(formularioFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.entry_nombre_cachorro.place(x=20, y=125, width=250)

        sexoLabel = Label(formularioFrame, text='Sexo*', font=('Lucida Sans', 11, 'bold'), bg='white',
                           fg='gray20', )
        sexoLabel.place(x=370, y=100)
        self.entry_sexo = Entry(formularioFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.entry_sexo.place(x=370, y=125, width=250)

        chipLabel = Label(formularioFrame, text='Chip*', font=('Lucida Sans', 11, 'bold'), bg='white',
                           fg='gray20', )
        chipLabel.place(x=650, y=100)
        self.entry_chip = Entry(formularioFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.entry_chip.place(x=650, y=125, width=200)


        passwordLabel = Label(formularioFrame, text='Color*', font=('Lucida Sans', 11, 'bold'), bg='white',
                              fg='gray20', )
        passwordLabel.place(x=20, y=150)
        self.entry_color = Entry(formularioFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.entry_color.place(x=20, y=175, width=250)

        answerLabel = Label(formularioFrame, text='Fecha de nacimiento*', font=('Lucida Sans', 11, 'bold'), bg='white',
                            fg='gray20', )
        answerLabel.place(x=370, y=150)
        self.entry_nacimiento = Entry(formularioFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.entry_nacimiento.place(x=370, y=175, width=250)

        razaLabel = Label(formularioFrame, text='Raza*', font=('Lucida Sans', 11, 'bold'), bg='white',
                              fg='gray20', )
        razaLabel.place(x=20, y=200)
        self.entry_raza = Entry(formularioFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.entry_raza.place(x=20, y=225, width=250)

        criadorLabel = Label(formularioFrame, text='Criador*', font=('Lucida Sans', 11, 'bold'), bg='white',
                            fg='gray20', )
        criadorLabel.place(x=370, y=200)
        self.entry_criador = Entry(formularioFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.entry_criador.place(x=370, y=225, width=250)

        afijomadreLabel = Label(formularioFrame, text='Afijo Madre*', font=('Lucida Sans', 11, 'bold'), bg='white',
                              fg='gray20', )
        afijomadreLabel.place(x=20, y=250)
        self.entry_afijo_madre = Entry(formularioFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.entry_afijo_madre.place(x=20, y=275, width=250)

        afijopadreLabel = Label(formularioFrame, text='Afijo Padre*', font=('Lucida Sans', 11, 'bold'), bg='white',
                            fg='gray20', )
        afijopadreLabel.place(x=370, y=250)
        self.entry_afijo_padre = Entry(formularioFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.entry_afijo_padre.place(x=370, y=275, width=250)


        nombremadreLabel = Label(formularioFrame, text='Nombre/Color madre*', font=('Lucida Sans', 11, 'bold'), bg='white',
                              fg='gray20', )
        nombremadreLabel.place(x=20, y=300)
        self.entry_nombre_madre = Entry(formularioFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.entry_nombre_madre.place(x=20, y=325, width=250)

        nombrepadreLabel = Label(formularioFrame, text='Nombre/Color padre*', font=('Lucida Sans', 11, 'bold'), bg='white',
                            fg='gray20', )
        nombrepadreLabel.place(x=370, y=300)
        self.entry_nombre_padre = Entry(formularioFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.entry_nombre_padre.place(x=370, y=325, width=250)

        propietarioLabel = Label(formularioFrame, text='Propietario*', font=('Lucida Sans', 11, 'bold'), bg='white',
                              fg='gray20', )
        propietarioLabel.place(x=20, y=350)
        self.entry_propietario = Entry(formularioFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.entry_propietario.place(x=20, y=375, width=250)

        direccionLabel = Label(formularioFrame, text='Direccion*', font=('Lucida Sans', 11, 'bold'), bg='white',
                            fg='gray20', )
        direccionLabel.place(x=370, y=350)
        self.entry_direccion = Entry(formularioFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.entry_direccion.place(x=370, y=375, width=250)

        distritoLabel = Label(formularioFrame, text='Distrito*', font=('Lucida Sans', 11, 'bold'), bg='white',
                              fg='gray20', )
        distritoLabel.place(x=20, y=400)
        self.entry_distrito = Entry(formularioFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.entry_distrito.place(x=20, y=425, width=250)

        telefonoLabel = Label(formularioFrame, text='Telefono*', font=('Lucida Sans', 11, 'bold'), bg='white',
                            fg='gray20', )
        telefonoLabel.place(x=370, y=400)
        self.entry_telefono = Entry(formularioFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.entry_telefono.place(x=370, y=425, width=250)

        dni_Label = Label(formularioFrame, text='DNI*', font=('Lucida Sans', 11, 'bold'), bg='white',
                              fg='gray20', )
        dni_Label.place(x=20, y=450)
        self.entry_dni = Entry(formularioFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.entry_dni.place(x=20, y=475, width=250)

        certificado_code_Label = Label(formularioFrame, text='Código de certificado*', font=('Lucida Sans', 11, 'bold'), bg='white',
                              fg='gray20', )
        certificado_code_Label.place(x=370, y=450)
        self.entry_certificado_code = Entry(formularioFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.entry_certificado_code.place(x=370, y=475, width=250)

        self.check_auto_code_perro = IntVar()
        checkButton_auto_code_perro = Checkbutton(formularioFrame, text='Auto', variable=self.check_auto_code_perro, onvalue=1,
                                  offvalue=0, font=('Lucida Sans', 11, 'bold'), bg='white',
                                  command=lambda:self.set_auto_cachorro_code())
        checkButton_auto_code_perro.place(x=620, y=470)

        self.check_homologacion = IntVar()
        checkButton = Checkbutton(formularioFrame, text='Homologación', variable=self.check_homologacion, onvalue=1,
                                  offvalue=0, font=('Lucida Sans', 11, 'bold'), bg='white')
        checkButton.place(x=20, y=510)

        agregarextrabtn = Button(formularioFrame, text='Agregar datos genealogicos', font=('arial', 13, 'bold'), fg='white',
                              bg='gray20', cursor='hand2', bd=0, activeforeground='white',
                              command=lambda:self.add_genealogia())
        agregarextrabtn.place(x=370, y=510)


        registerbutton = Button(formularioFrame, text='Crear Registro', font=('arial', 14, 'bold'), fg='white',
                                bg='gray20', cursor='hand2', bd=0, activeforeground='white',
                                command=lambda:self.register_pedigree())
        registerbutton.place(x=20, y=560)

        salir_cuenta_button = Button(tab1, text='Salir de cuenta', font=('arial', 14, 'bold'), fg='black',
                                bg='white', cursor='hand2', bd=0, activeforeground='white',
                                command=lambda:self.log_out())
        salir_cuenta_button.place(x=1150, y=600)

        open_path_button = Button(tab1, image=openfolderimage, fg='black',
                                bg='white', cursor='hand2', bd=0, activeforeground='white',
                                command=lambda:self.open_path_pedigree())
        open_path_button.place(x=410, y=590)
        open_pedigree_label = Label(formularioFrame, text='Pedigree', font=('Lucida Sans', 11, 'bold'), bg='white',
                              fg='gray20', )
        open_pedigree_label.place(x=400, y=570)

        open_path_cliente_button = Button(tab1, image=openfolderimage, fg='black',
                                bg='white', cursor='hand2', bd=0, activeforeground='white',
                                command=lambda:self.open_path_cliente())
        open_path_cliente_button.place(x=550, y=590)
        open_cliente_label = Label(formularioFrame, text='Cliente', font=('Lucida Sans', 11, 'bold'), bg='white',
                              fg='gray20', )
        open_cliente_label.place(x=540, y=570)

    def open_path_pedigree(self):
        try:
            if self.registered_pedigree_path == "":
                showerror("Error", "No hay directorio el cuál abrir.")
            else:
                print("try")
                print(self.registered_pedigree_path)
                subprocess.Popen(r'explorer /select,' + self.registered_pedigree_path)  # Abrir carpeta en escritorio
        except Exception:
            showerror("Error", "No hay directorio el cuál abrir.")

    def open_path_cliente(self):
        try:
            if self.registered_cliente_path == "":
                showerror("Error", "No hay directorio el cuál abrir.")
            else:
                print("try")
                print(self.registered_cliente_path)
                subprocess.Popen(r'explorer /select,' + self.registered_cliente_path)  # Abrir carpeta en escritorio
        except Exception:
            showerror("Error", "No hay directorio el cuál abrir.")

    def set_auto_afijo_code(self):
        # Chequear current estado del entry.
        if self.buscar_propietario_btn["text"] == "Cancelar":
            print("do nothing")
            self.check_auto_afijo_code.set(0)
        else:
            if self.check_auto_afijo_code.get() == 0:
                # No se usa o se reinicia
                self.entry_propietario_afijo.configure(state="normal")
                self.entry_propietario_afijo.delete(0, END)
                print("is 0")
            else:
                # se activa
                dynamic_afijo_code = ""
                current_time_for_new_afijo_code = datetime.datetime.today().strftime("%d%m%Y")
                current_time_for_new_afijo_code = current_time_for_new_afijo_code[:-4] + current_time_for_new_afijo_code[-2:]

                data = db.get("app_data")

                if len(data) == 0:
                    # primera vez.
                    dynamic_afijo_code = current_time_for_new_afijo_code+"/01"
                else:
                    # se obtiene data y se usa para crear nuevo codigo.
                    cant_afijos = data[0]["cant_afijos_hoy"]
                    fecha_ult_afijo = data[0]["fecha_ultimo_afijo"]

                    format = '%d/%m/%Y'
                    date_from_db = datetime.datetime.strptime(fecha_ult_afijo, format)
                    current_date_str = datetime.datetime.today().date().strftime("%d/%m/%Y")
                    current_date = datetime.datetime.strptime(current_date_str, format)

                    if date_from_db.date() < current_date.date():
                        # Esto solo sucederá al inicio del sgt día
                        dynamic_afijo_code = current_time_for_new_afijo_code + "/01"
                        print("current date is major")
                    else:
                        # Esto sucedera alrededor de to do el dia, hasta que acabe.
                        # obtengo la cant actual la convierto en string y le sumo 1
                        int_cant = int(cant_afijos) + 1
                        if int_cant < 10:
                            dynamic_afijo_code = current_time_for_new_afijo_code + "/0" + str(int_cant)
                        else:
                            dynamic_afijo_code = current_time_for_new_afijo_code + "/" + str(int_cant)

                        print("they are equal")


                self.entry_propietario_afijo.delete(0, END)
                self.entry_propietario_afijo.insert(0, dynamic_afijo_code)
                self.entry_propietario_afijo.configure(state="disabled")

    def set_auto_cachorro_code(self):
        if self.check_auto_code_perro.get() == 0:
            # No se usa o se reinicia
            self.entry_certificado_code.configure(state="normal")
            self.entry_certificado_code.delete(0, END)
            print("is 0")
        else:
            # se activa
            max_code = db.get_max_cert_code()
            new_code = max_code+1
            # print("----CODE------")
            # print(max_code)

            self.entry_certificado_code.delete(0, END)
            self.entry_certificado_code.insert(0, new_code)
            self.entry_certificado_code.configure(state="disabled")

    def log_out(self):
        # Destroy window reset current user
        global user_mail
        user_mail = ""
        result = askquestion("Confirmación", "Deseas cerrar la sesión?")
        if result == "yes":
            raise_frame(LoginFrame(root))

    def buscar_padres_afijos_data(self):
        if self.entry_afijo_padre.get() == '' or self.entry_afijo_madre.get() == '':
            showerror('Error', 'Porfavor ingrese el afijo de los padres.', parent=root)
        else:
            btn_title = self.buscar_afijos_padres_btn['text']
            if btn_title == "Buscar padres":
                madre_data = db.get_single_element_data("pedigrees", "certificado_code", self.entry_afijo_madre.get())
                padre_data = db.get_single_element_data("pedigrees", "certificado_code", self.entry_afijo_padre.get())

                if len(padre_data) == 0 and len(madre_data) == 0:
                    showerror("Error", "Afijo de Madre y Padre no existe.")
                elif len(padre_data) == 0:
                    showerror("Error", "Afijo de Padre no existe.")
                    # Madre si existe.
                    self.entry_afijo_padre.delete(0, END)
                elif len(madre_data) == 0:
                    showerror("Error", "Afijo de Madre no existe.")
                    self.entry_afijo_madre.delete(0, END)
                else:
                    # Obtenemos y seteamos data
                    nombre_padre = padre_data[0]["nombre_cachorro"]
                    color_padre = padre_data[0]["color"]

                    nombre_madre = madre_data[0]["nombre_cachorro"]
                    color_madre = madre_data[0]["color"]

                    self.gene_data_madre = json.loads(madre_data[0]['genealogia_data'])
                    self.gene_data_padre = json.loads(padre_data[0]['genealogia_data'])

                    gene_madre = self.gene_data_madre["madre"]
                    gene_padre = self.gene_data_padre["padre"]

                    print("----------------------")
                    print(str(self.gene_data_padre))
                    print(str(self.genealogia_data))

                    self.genealogia_data["madre"] = gene_madre
                    self.genealogia_data["padre"] = gene_padre

                    self.gene_fromDB_loaded = True

                    self.entry_afijo_padre.configure(state="disabled")
                    self.entry_afijo_madre.configure(state="disabled")

                    self.entry_nombre_padre.delete(0, END)
                    self.entry_nombre_padre.insert(0, nombre_padre+"/"+color_padre)
                    self.entry_nombre_padre.configure(state="disabled")

                    self.entry_nombre_madre.delete(0, END)
                    self.entry_nombre_madre.insert(0, nombre_madre+"/"+color_madre)
                    self.entry_nombre_madre.configure(state="disabled")

                    self.buscar_afijos_padres_btn['text'] = "Cancelar"

                    # Setear data obtenida

                    gene_madre_m = self.gene_data_madre["madre"]
                    gene_madre_p = self.gene_data_madre["padre"]

                    gene_padre_m = self.gene_data_padre["madre"]
                    gene_padre_p = self.gene_data_padre["padre"]

                    gene_padre = dict()
                    gene_padre["p"] = self.entry_nombre_padre.get()

                    # Madre Perro
                    gene_madre = dict()
                    gene_madre["m"] = self.entry_nombre_madre.get()
                    # Abuelo Perro
                    gene_madre["am"] = gene_madre_m["m"]
                    gene_madre["ap"] = gene_madre_p["p"]
                    # Bisabuelo Perro
                    gene_madre["bm_m"] = gene_madre_m["am"]
                    gene_madre["bm_p"] = gene_madre_m["ap"]
                    gene_madre["bp_m"] = gene_madre_p["am"]
                    gene_madre["bp_p"] = gene_madre_p["ap"]
                    # Tatarabuelo Perro
                    gene_madre["tm_bm_m"] = gene_madre_m["bm_m"]
                    gene_madre["tm_bm_p"] = gene_madre_m["bm_p"]
                    gene_madre["tm_bp_m"] = gene_madre_m["bp_m"]
                    gene_madre["tm_bp_p"] = gene_madre_m["bp_p"]

                    gene_madre["tp_bm_m"] = gene_madre_p["bm_m"]
                    gene_madre["tp_bm_p"] = gene_madre_p["bm_p"]
                    gene_madre["tp_bp_m"] = gene_madre_p["bp_m"]
                    gene_madre["tp_bp_p"] = gene_madre_p["bp_p"]

                    # Abuelo Perro
                    gene_padre["am"] = gene_padre_m["m"]
                    gene_padre["ap"] = gene_padre_p["p"]
                    # Bisabuelo Perro
                    gene_padre["bm_m"] = gene_padre_m["am"]
                    gene_padre["bm_p"] = gene_padre_m["ap"]
                    gene_padre["bp_m"] = gene_padre_p["am"]
                    gene_padre["bp_p"] = gene_padre_p["ap"]
                    # Tatarabuelo Perro
                    gene_padre["tm_bm_m"] = gene_padre_m["bm_m"]
                    gene_padre["tm_bm_p"] = gene_padre_m["bm_p"]
                    gene_padre["tm_bp_m"] = gene_padre_m["bp_m"]
                    gene_padre["tm_bp_p"] = gene_padre_m["bp_p"]

                    gene_padre["tp_bm_m"] = gene_padre_p["bm_m"]
                    gene_padre["tp_bm_p"] = gene_padre_p["bm_p"]
                    gene_padre["tp_bp_m"] = gene_padre_p["bp_m"]
                    gene_padre["tp_bp_p"] = gene_padre_p["bp_p"]
                    #
                    # self.edit_gene_data["padre"] = gene_padre
                    # self.edit_gene_data["madre"] = gene_madre

                    self.genealogia_data["padre"] = gene_padre
                    self.genealogia_data["madre"] = gene_madre

            else:
                self.buscar_afijos_padres_btn['text'] = "Buscar padres"

                self.entry_afijo_padre.configure(state="normal")
                self.entry_afijo_padre.delete(0, END)

                self.entry_afijo_madre.configure(state="normal")
                self.entry_afijo_madre.delete(0, END)

                self.entry_nombre_padre.configure(state="normal")
                self.entry_nombre_padre.delete(0, END)

                self.entry_nombre_madre.configure(state="normal")
                self.entry_nombre_madre.delete(0, END)

                self.gene_fromDB_loaded = False
                self.init_form_gene_data()

            # print("Buscaremos cliente...")
            # showinfo("Info", my_text)

    def add_genealogia(self):

        if self.entry_afijo_madre.get() == '' or self.entry_afijo_padre.get() == '' \
                or self.entry_nombre_padre.get() == '' or self.entry_nombre_madre.get() == '':
            showerror('Error', 'Porfavor ingrese los afijos y nombres de los padres.', parent=root)
        else:

            self.root_gene = Toplevel()
            self.root_gene.title('Agregar Genealogía')
            genealogia_screen_size = str(screen_width-100) + "x" + str(screen_height)
            self.root_gene.geometry(genealogia_screen_size)
            self.root_gene.config(bg='white')
#            self.root_gene.focus_force()
            self.root_gene.grab_set()

            forgetpassLabel = Label(self.root_gene, text='Agregar informacion de genealogía',
                                    font=('Lucida Sans', 16, 'bold'), fg='green',
                                    bg='white')
            forgetpassLabel.place(x=(screen_width/2)-250, y=10)

            aceptar_btn = Button(self.root_gene, text='Aceptar',
                                    font=('Lucida Sans', 14, 'bold'), fg='green',
                                    bg='white', command=lambda:self.save_gene_data())
            aceptar_btn.place(x=50, y=600)

            # PADRE Y MADRE
            gene_madre_Label = Label(self.root_gene, text='Madre', font=('Lucida Sans', 13, 'bold'),
                                   bg='white',
                                   fg='gray20', )
            gene_madre_Label.place(x=20, y=250)
            self.entry_gene_madre = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre.place(x=20, y=275, width=250)

            gene_padre_Label = Label(self.root_gene, text='Padre', font=('Lucida Sans', 13, 'bold'), bg='white',
                               fg='gray20', )
            gene_padre_Label.place(x=20, y=400)
            self.entry_gene_padre = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre.place(x=20, y=425, width=250)

            # Abuelos

            self.entry_gene_madre_m = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_m.place(x=300, y=150, width=250)

            self.entry_gene_madre_p = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_p.place(x=300, y=250, width=250)

            self.entry_gene_padre_m = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_m.place(x=300, y=450, width=250)

            self.entry_gene_padre_p = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_p.place(x=300, y=550, width=250)

            # Abuelos 2da gen (BISA)
            # madre
            self.entry_gene_madre_mm = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_mm.place(x=570, y=100, width=250)

            self.entry_gene_madre_mp = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_mp.place(x=570, y=150, width=250)

            self.entry_gene_madre_pm = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_pm.place(x=570, y=250, width=250)

            self.entry_gene_madre_pp = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_pp.place(x=570, y=300, width=250)
            # padre
            self.entry_gene_padre_mm = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_mm.place(x=570, y=400, width=250)

            self.entry_gene_padre_mp = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_mp.place(x=570, y=450, width=250)

            self.entry_gene_padre_pm = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_pm.place(x=570, y=550, width=250)

            self.entry_gene_padre_pp = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_pp.place(x=570, y=600, width=250)

            # Abuelos 3ra gen (TATA)
            # madre
            self.entry_gene_madre_mmm = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_mmm.place(x=840, y=75, width=250)

            self.entry_gene_madre_mmp = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_mmp.place(x=840, y=100, width=250)

            self.entry_gene_madre_mpm = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_mpm.place(x=840, y=150, width=250)

            self.entry_gene_madre_mpp = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_mpp.place(x=840, y=175, width=250)

            self.entry_gene_madre_pmm = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_pmm.place(x=840, y=225, width=250)

            self.entry_gene_madre_pmp = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_pmp.place(x=840, y=250, width=250)

            self.entry_gene_madre_ppm = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_ppm.place(x=840, y=300, width=250)

            self.entry_gene_madre_ppp = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_ppp.place(x=840, y=325, width=250)

            # padre
            self.entry_gene_padre_mmm = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_mmm.place(x=840, y=375, width=250)

            self.entry_gene_padre_mmp = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_mmp.place(x=840, y=400, width=250)

            self.entry_gene_padre_mpm = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_mpm.place(x=840, y=450, width=250)

            self.entry_gene_padre_mpp = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_mpp.place(x=840, y=475, width=250)

            self.entry_gene_padre_pmm = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_pmm.place(x=840, y=525, width=250)

            self.entry_gene_padre_pmp = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_pmp.place(x=840, y=550, width=250)

            self.entry_gene_padre_ppm = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_ppm.place(x=840, y=600, width=250)

            self.entry_gene_padre_ppp = Entry(self.root_gene, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_ppp.place(x=840, y=625, width=250)


            # Populate from DB
            if self.gene_fromDB_loaded:
                # Cargo nombre y color de padre/madre
                gene_madre = self.gene_data_madre["madre"]
                gene_madre_m = self.gene_data_madre["madre"]
                gene_madre_p = self.gene_data_madre["padre"]

                gene_padre = self.gene_data_padre["padre"]
                gene_padre_m = self.gene_data_padre["madre"]
                gene_padre_p = self.gene_data_padre["padre"]
                # Madre
                self.entry_gene_madre.insert(0, self.entry_nombre_madre.get())
                # Abuelos Maternos
                self.entry_gene_madre_m.insert(0, gene_madre_m["m"])
                self.entry_gene_madre_p.insert(0, gene_madre_p["p"])
                # Bisa Maternos
                self.entry_gene_madre_mm.insert(0, gene_madre_m["am"])
                self.entry_gene_madre_mp.insert(0, gene_madre_m["ap"])

                self.entry_gene_madre_pm.insert(0, gene_madre_p["am"])
                self.entry_gene_madre_pp.insert(0, gene_madre_p["ap"])
                # Tata Maternos
                self.entry_gene_madre_mmm.insert(0, gene_madre_m["bm_m"])
                self.entry_gene_madre_mmp.insert(0, gene_madre_m["bm_p"])
                self.entry_gene_madre_mpm.insert(0, gene_madre_m["bp_m"])
                self.entry_gene_madre_mpp.insert(0, gene_madre_m["bp_p"])

                self.entry_gene_madre_pmm.insert(0, gene_madre_p["bm_m"])
                self.entry_gene_madre_pmp.insert(0, gene_madre_p["bm_p"])
                self.entry_gene_madre_ppm.insert(0, gene_madre_p["bp_m"])
                self.entry_gene_madre_ppp.insert(0, gene_madre_p["bp_p"])

                # Padre
                self.entry_gene_padre.insert(0, self.entry_nombre_padre.get())
                # Abuelos Paternos
                self.entry_gene_padre_m.insert(0, gene_padre_m["m"])
                self.entry_gene_padre_p.insert(0, gene_padre_p["p"])
                # Bisa Paternos
                self.entry_gene_padre_mm.insert(0, gene_padre_m["am"])
                self.entry_gene_padre_mp.insert(0, gene_padre_m["ap"])

                self.entry_gene_padre_pm.insert(0, gene_padre_p["am"])
                self.entry_gene_padre_pp.insert(0, gene_padre_p["ap"])
                # Tata Paternos
                self.entry_gene_padre_mmm.insert(0, gene_padre_m["bm_m"])
                self.entry_gene_padre_mmp.insert(0, gene_padre_m["bm_p"])
                self.entry_gene_padre_mpm.insert(0, gene_padre_m["bp_m"])
                self.entry_gene_padre_mpp.insert(0, gene_padre_m["bp_p"])

                self.entry_gene_padre_pmm.insert(0, gene_padre_p["bm_m"])
                self.entry_gene_padre_pmp.insert(0, gene_padre_p["bm_p"])
                self.entry_gene_padre_ppm.insert(0, gene_padre_p["bp_m"])
                self.entry_gene_padre_ppp.insert(0, gene_padre_p["bp_p"])

                # Disable Madre
                self.entry_gene_madre.configure(state="disabled")
                self.entry_gene_madre_m.configure(state="disabled")
                self.entry_gene_madre_p.configure(state="disabled")
                self.entry_gene_madre_mm.configure(state="disabled")
                self.entry_gene_madre_mp.configure(state="disabled")
                self.entry_gene_madre_pm.configure(state="disabled")
                self.entry_gene_madre_pp.configure(state="disabled")
                self.entry_gene_madre_mmm.configure(state="disabled")
                self.entry_gene_madre_mmp.configure(state="disabled")
                self.entry_gene_madre_mpm.configure(state="disabled")
                self.entry_gene_madre_mpp.configure(state="disabled")
                self.entry_gene_madre_pmm.configure(state="disabled")
                self.entry_gene_madre_pmp.configure(state="disabled")
                self.entry_gene_madre_ppm.configure(state="disabled")
                self.entry_gene_madre_ppp.configure(state="disabled")
                # Disable Padre
                self.entry_gene_padre.configure(state="disabled")
                self.entry_gene_padre_m.configure(state="disabled")
                self.entry_gene_padre_p.configure(state="disabled")
                self.entry_gene_padre_mm.configure(state="disabled")
                self.entry_gene_padre_mp.configure(state="disabled")
                self.entry_gene_padre_pm.configure(state="disabled")
                self.entry_gene_padre_pp.configure(state="disabled")
                self.entry_gene_padre_mmm.configure(state="disabled")
                self.entry_gene_padre_mmp.configure(state="disabled")
                self.entry_gene_padre_mpm.configure(state="disabled")
                self.entry_gene_padre_mpp.configure(state="disabled")
                self.entry_gene_padre_pmm.configure(state="disabled")
                self.entry_gene_padre_pmp.configure(state="disabled")
                self.entry_gene_padre_ppm.configure(state="disabled")
                self.entry_gene_padre_ppp.configure(state="disabled")
            else:
                # Populate Madre y padre with Formulary data
                self.entry_gene_madre.delete(0, END)
                self.entry_gene_madre.insert(0, self.entry_nombre_madre.get())
                self.entry_gene_madre.configure(state="disabled")

                self.entry_gene_padre.delete(0, END)
                self.entry_gene_padre.insert(0, self.entry_nombre_padre.get())
                self.entry_gene_padre.configure(state="disabled")

                # populate all others Data

                gene_madre = self.genealogia_data["madre"]
                gene_padre = self.genealogia_data["padre"]
                # Madre
#                self.entry_gene_madre.insert(0, gene_madre["m"])
                # Abuelos Maternos
#                am_var if am_var != '' else "UNKNOWN"
                self.entry_gene_madre_m.insert(0, "" if gene_madre["am"] == "UNKNOWN" else gene_madre["am"])
                self.entry_gene_madre_p.insert(0, "" if gene_madre["ap"] == "UNKNOWN" else gene_madre["ap"])
                # Bisa Maternos
                self.entry_gene_madre_mm.insert(0, "" if gene_madre["bm_m"] == "UNKNOWN" else gene_madre["bm_m"])
                self.entry_gene_madre_mp.insert(0, "" if gene_madre["bm_p"] == "UNKNOWN" else gene_madre["bm_p"])

                self.entry_gene_madre_pm.insert(0, "" if gene_madre["bp_m"] == "UNKNOWN" else gene_madre["bp_m"])
                self.entry_gene_madre_pp.insert(0, "" if gene_madre["bp_p"] == "UNKNOWN" else gene_madre["bp_p"])
                # Tata Maternos
                self.entry_gene_madre_mmm.insert(0, "" if gene_madre["tm_bm_m"] == "UNKNOWN" else gene_madre["tm_bm_m"])
                self.entry_gene_madre_mmp.insert(0, "" if gene_madre["tm_bm_p"] == "UNKNOWN" else gene_madre["tm_bm_p"])
                self.entry_gene_madre_mpm.insert(0, "" if gene_madre["tm_bp_m"] == "UNKNOWN" else gene_madre["tm_bp_m"])
                self.entry_gene_madre_mpp.insert(0, "" if gene_madre["tm_bp_p"] == "UNKNOWN" else gene_madre["tm_bp_p"])

                self.entry_gene_madre_pmm.insert(0, "" if gene_madre["tp_bm_m"] == "UNKNOWN" else gene_madre["tp_bm_m"])
                self.entry_gene_madre_pmp.insert(0, "" if gene_madre["tp_bm_p"] == "UNKNOWN" else gene_madre["tp_bm_p"])
                self.entry_gene_madre_ppm.insert(0, "" if gene_madre["tp_bp_m"] == "UNKNOWN" else gene_madre["tp_bp_m"])
                self.entry_gene_madre_ppp.insert(0, "" if gene_madre["tp_bp_p"] == "UNKNOWN" else gene_madre["tp_bp_p"])

                # Padre
#                self.entry_gene_padre.insert(0, gene_padre["p"])
                # Abuelos Maternos
                self.entry_gene_padre_m.insert(0, "" if gene_padre["am"] == "UNKNOWN" else gene_padre["am"])
                self.entry_gene_padre_p.insert(0, "" if gene_padre["ap"] == "UNKNOWN" else gene_padre["ap"])
                # Bisa Maternos
                self.entry_gene_padre_mm.insert(0, "" if gene_padre["bm_m"] == "UNKNOWN" else gene_padre["bm_m"])
                self.entry_gene_padre_mp.insert(0, "" if gene_padre["bm_p"] == "UNKNOWN" else gene_padre["bm_p"])

                self.entry_gene_padre_pm.insert(0, "" if gene_padre["bp_m"] == "UNKNOWN" else gene_padre["bp_m"])
                self.entry_gene_padre_pp.insert(0, "" if gene_padre["bp_p"] == "UNKNOWN" else gene_padre["bp_p"])
                # Tata Maternos
                self.entry_gene_padre_mmm.insert(0, "" if gene_padre["tm_bm_m"] == "UNKNOWN" else gene_padre["tm_bm_m"])
                self.entry_gene_padre_mmp.insert(0, "" if gene_padre["tm_bm_p"] == "UNKNOWN" else gene_padre["tm_bm_p"])
                self.entry_gene_padre_mpm.insert(0, "" if gene_padre["tm_bp_m"] == "UNKNOWN" else gene_padre["tm_bm_p"])
                self.entry_gene_padre_mpp.insert(0, "" if gene_padre["tm_bp_p"] == "UNKNOWN" else gene_padre["tm_bp_p"])

                self.entry_gene_padre_pmm.insert(0, "" if gene_padre["tp_bm_m"] == "UNKNOWN" else gene_padre["tp_bm_m"])
                self.entry_gene_padre_pmp.insert(0, "" if gene_padre["tp_bm_p"] == "UNKNOWN" else gene_padre["tp_bm_p"])
                self.entry_gene_padre_ppm.insert(0, "" if gene_padre["tp_bp_m"] == "UNKNOWN" else gene_padre["tp_bp_m"])
                self.entry_gene_padre_ppp.insert(0, "" if gene_padre["tp_bp_p"] == "UNKNOWN" else gene_padre["tp_bp_p"])

            self.root_gene.mainloop()

    def buscar_cliente(self):

        if self.entry_propietario_afijo.get() == '':
            showerror('Error', 'Porfavor ingrese el afijo del cliente.', parent=root)
        else:
            btn_title = self.buscar_propietario_btn['text']
            if btn_title == "Buscar cliente":
                cliente_data = db.get_single_element_data("clientes", "cliente_afijo", self.entry_propietario_afijo.get())
                if len(cliente_data) == 0:
                    # cliente no existe
                    showerror("Error", "El cliente no existe.")
                else:
                    # Get data
                    propietario = cliente_data[0]["propietario"]
                    cliente_afijo = cliente_data[0]["cliente_afijo"]
                    direccion = cliente_data[0]["direccion"]
                    distrito = cliente_data[0]["distrito"]
                    telefono = cliente_data[0]["telefono"]
                    dni = cliente_data[0]["dni"]

                    # Set data
                    self.entry_propietario_afijo.configure(state="disabled")

                    self.entry_propietario.delete(0, END)
                    self.entry_propietario.insert(0, propietario)
                    self.entry_propietario.configure(state="disabled")

                    self.entry_direccion.delete(0, END)
                    self.entry_direccion.insert(0, direccion)
                    self.entry_direccion.configure(state="disabled")

                    self.entry_distrito.delete(0, END)
                    self.entry_distrito.insert(0, distrito)
                    self.entry_distrito.configure(state="disabled")

                    self.entry_telefono.delete(0, END)
                    self.entry_telefono.insert(0, telefono)
                    self.entry_telefono.configure(state="disabled")

                    self.entry_dni.delete(0, END)
                    self.entry_dni.insert(0, dni)
                    self.entry_dni.configure(state="disabled")
                    self.buscar_propietario_btn['text'] = "Cancelar"
            else:
                self.buscar_propietario_btn['text'] = "Buscar cliente"
                # limpiamos botones y habilitamos text boxs
                self.entry_propietario_afijo.configure(state="normal")
                self.entry_propietario_afijo.delete(0, END)

                self.entry_propietario.configure(state="normal")
                self.entry_propietario.delete(0, END)

                self.entry_direccion.configure(state="normal")
                self.entry_direccion.delete(0, END)

                self.entry_distrito.configure(state="normal")
                self.entry_distrito.delete(0, END)

                self.entry_telefono.configure(state="normal")
                self.entry_telefono.delete(0, END)

                self.entry_dni.configure(state="normal")
                self.entry_dni.delete(0, END)

    def save_gene_data(self):

        if not self.gene_fromDB_loaded:
            # check elements contain only one "/"
            if self.entry_gene_padre_m.get() != '' and self.entry_gene_padre_m.get().count('/') != 1 or\
                    self.entry_gene_padre_p.get() != '' and self.entry_gene_padre_p.get().count('/') != 1 or \
                    self.entry_gene_padre_mm.get() != '' and self.entry_gene_padre_mm.get().count('/') != 1 or\
                    self.entry_gene_padre_mp.get() != '' and self.entry_gene_padre_mp.get().count('/') != 1 or \
                    self.entry_gene_padre_pm.get() != '' and self.entry_gene_padre_pm.get().count('/') != 1 or \
                    self.entry_gene_padre_pp.get() != '' and self.entry_gene_padre_pp.get().count('/') != 1 or \
                    self.entry_gene_padre_mmm.get() != '' and self.entry_gene_padre_mmm.get().count('/') != 1 or \
                    self.entry_gene_padre_mmp.get() != '' and self.entry_gene_padre_mmp.get().count('/') != 1 or \
                    self.entry_gene_padre_mpm.get() != '' and self.entry_gene_padre_mpm.get().count('/') != 1 or \
                    self.entry_gene_padre_mpp.get() != '' and self.entry_gene_padre_mpp.get().count('/') != 1 or \
                    self.entry_gene_padre_pmm.get() != '' and self.entry_gene_padre_pmm.get().count('/') != 1 or \
                    self.entry_gene_padre_pmp.get() != '' and self.entry_gene_padre_pmp.get().count('/') != 1 or \
                    self.entry_gene_padre_ppm.get() != '' and self.entry_gene_padre_ppm.get().count('/') != 1 or \
                    self.entry_gene_padre_ppp.get() != '' and self.entry_gene_padre_ppp.get().count('/') != 1:
                showerror('Error', 'Campos de Nombre/color deben llenarse divididos por un solo / .', parent=root)
            elif self.entry_gene_madre_m.get() != '' and self.entry_gene_madre_m.get().count('/') != 1 or\
                    self.entry_gene_madre_p.get() != '' and self.entry_gene_madre_p.get().count('/') != 1 or \
                    self.entry_gene_madre_mm.get() != '' and self.entry_gene_madre_mm.get().count('/') != 1 or\
                    self.entry_gene_madre_mp.get() != '' and self.entry_gene_madre_mp.get().count('/') != 1 or \
                    self.entry_gene_madre_pm.get() != '' and self.entry_gene_madre_pm.get().count('/') != 1 or \
                    self.entry_gene_madre_pp.get() != '' and self.entry_gene_madre_pp.get().count('/') != 1 or \
                    self.entry_gene_madre_mmm.get() != '' and self.entry_gene_madre_mmm.get().count('/') != 1 or \
                    self.entry_gene_madre_mmp.get() != '' and self.entry_gene_madre_mmp.get().count('/') != 1 or \
                    self.entry_gene_madre_mpm.get() != '' and self.entry_gene_madre_mpm.get().count('/') != 1 or \
                    self.entry_gene_madre_mpp.get() != '' and self.entry_gene_madre_mpp.get().count('/') != 1 or \
                    self.entry_gene_madre_pmm.get() != '' and self.entry_gene_madre_pmm.get().count('/') != 1 or \
                    self.entry_gene_madre_pmp.get() != '' and self.entry_gene_madre_pmp.get().count('/') != 1 or \
                    self.entry_gene_madre_ppm.get() != '' and self.entry_gene_madre_ppm.get().count('/') != 1 or \
                    self.entry_gene_madre_ppp.get() != '' and self.entry_gene_madre_ppp.get().count('/') != 1:
                showerror('Error', 'Campos de Nombre/color deben llenarse divididos por un solo / .', parent=root)
            else:
                gene_padre = dict()
                gene_padre["p"] = self.entry_nombre_padre.get()
                # Abuelo Perro
                gene_padre["am"] = "UNKNOWN" if self.entry_gene_padre_m.get() == '' else self.entry_gene_padre_m.get()
                gene_padre["ap"] = "UNKNOWN" if self.entry_gene_padre_p.get() == '' else self.entry_gene_padre_p.get()
                # Bisabuelo Perro
                gene_padre["bm_m"] = "UNKNOWN" if self.entry_gene_padre_mm.get() == '' else self.entry_gene_padre_mm.get()
                gene_padre["bm_p"] = "UNKNOWN" if self.entry_gene_padre_mp.get() == '' else self.entry_gene_padre_mp.get()
                gene_padre["bp_m"] = "UNKNOWN" if self.entry_gene_padre_pm.get() == '' else self.entry_gene_padre_pm.get()
                gene_padre["bp_p"] = "UNKNOWN" if self.entry_gene_padre_pp.get() == '' else self.entry_gene_padre_pp.get()
                # Tatarabuelo Perro
                gene_padre["tm_bm_m"] = "UNKNOWN" if self.entry_gene_padre_mmm.get() == '' else self.entry_gene_padre_mmm.get()
                gene_padre["tm_bm_p"] = "UNKNOWN" if self.entry_gene_padre_mmp.get() == '' else self.entry_gene_padre_mmp.get()
                gene_padre["tm_bp_m"] = "UNKNOWN" if self.entry_gene_padre_mpm.get() == '' else self.entry_gene_padre_mpm.get()
                gene_padre["tm_bp_p"] = "UNKNOWN" if self.entry_gene_padre_mpp.get() == '' else self.entry_gene_padre_mpp.get()

                gene_padre["tp_bm_m"] = "UNKNOWN" if self.entry_gene_padre_pmm.get() == '' else self.entry_gene_padre_pmm.get()
                gene_padre["tp_bm_p"] = "UNKNOWN" if self.entry_gene_padre_pmp.get() == '' else self.entry_gene_padre_pmp.get()
                gene_padre["tp_bp_m"] = "UNKNOWN" if self.entry_gene_padre_ppm.get() == '' else self.entry_gene_padre_ppm.get()
                gene_padre["tp_bp_p"] = "UNKNOWN" if self.entry_gene_padre_ppp.get() == '' else self.entry_gene_padre_ppp.get()

                # Madre Perro
                gene_madre = dict()
                gene_madre["m"] = self.entry_nombre_madre.get()
                # Abuelo Perro
                gene_madre["am"] = "UNKNOWN" if self.entry_gene_madre_m.get() == '' else self.entry_gene_madre_m.get()
                gene_madre["ap"] = "UNKNOWN" if self.entry_gene_madre_p.get() == '' else self.entry_gene_madre_p.get()
                # Bisabuelo Perro
                gene_madre["bm_m"] = "UNKNOWN" if self.entry_gene_madre_mm.get() == '' else self.entry_gene_madre_mm.get()
                gene_madre["bm_p"] = "UNKNOWN" if self.entry_gene_madre_mp.get() == '' else self.entry_gene_madre_mp.get()
                gene_madre["bp_m"] = "UNKNOWN" if self.entry_gene_madre_pm.get() == '' else self.entry_gene_madre_pm.get()
                gene_madre["bp_p"] = "UNKNOWN" if self.entry_gene_madre_pp.get() == '' else self.entry_gene_madre_pp.get()
                # Tatarabuelo Perro
                gene_madre["tm_bm_m"] = "UNKNOWN" if self.entry_gene_madre_mmm.get() == '' else self.entry_gene_madre_mmm.get()
                gene_madre["tm_bm_p"] = "UNKNOWN" if self.entry_gene_madre_mmp.get() == '' else self.entry_gene_madre_mmp.get()
                gene_madre["tm_bp_m"] = "UNKNOWN" if self.entry_gene_madre_mpm.get() == '' else self.entry_gene_madre_mpm.get()
                gene_madre["tm_bp_p"] = "UNKNOWN" if self.entry_gene_madre_mpp.get() == '' else self.entry_gene_madre_mpp.get()

                gene_madre["tp_bm_m"] = "UNKNOWN" if self.entry_gene_madre_pmm.get() == '' else self.entry_gene_madre_pmm.get()
                gene_madre["tp_bm_p"] = "UNKNOWN" if self.entry_gene_madre_pmp.get() == '' else self.entry_gene_madre_pmp.get()
                gene_madre["tp_bp_m"] = "UNKNOWN" if self.entry_gene_madre_ppm.get() == '' else self.entry_gene_madre_ppm.get()
                gene_madre["tp_bp_p"] = "UNKNOWN" if self.entry_gene_madre_ppp.get() == '' else self.entry_gene_madre_ppp.get()

                self.genealogia_data["padre"] = gene_padre
                self.genealogia_data["madre"] = gene_madre

                self.root_gene.destroy()
                self.root_gene.update()
        else:
            gene_padre = dict()
            gene_padre["p"] = self.entry_nombre_padre.get()
            # Abuelo Perro
            gene_padre["am"] = "UNKNOWN" if self.entry_gene_padre_m.get() == '' else self.entry_gene_padre_m.get()
            gene_padre["ap"] = "UNKNOWN" if self.entry_gene_padre_p.get() == '' else self.entry_gene_padre_p.get()
            # Bisabuelo Perro
            gene_padre["bm_m"] = "UNKNOWN" if self.entry_gene_padre_mm.get() == '' else self.entry_gene_padre_mm.get()
            gene_padre["bm_p"] = "UNKNOWN" if self.entry_gene_padre_mp.get() == '' else self.entry_gene_padre_mp.get()
            gene_padre["bp_m"] = "UNKNOWN" if self.entry_gene_padre_pm.get() == '' else self.entry_gene_padre_pm.get()
            gene_padre["bp_p"] = "UNKNOWN" if self.entry_gene_padre_pp.get() == '' else self.entry_gene_padre_pp.get()
            # Tatarabuelo Perro
            gene_padre[
                "tm_bm_m"] = "UNKNOWN" if self.entry_gene_padre_mmm.get() == '' else self.entry_gene_padre_mmm.get()
            gene_padre[
                "tm_bm_p"] = "UNKNOWN" if self.entry_gene_padre_mmp.get() == '' else self.entry_gene_padre_mmp.get()
            gene_padre[
                "tm_bp_m"] = "UNKNOWN" if self.entry_gene_padre_mpm.get() == '' else self.entry_gene_padre_mpm.get()
            gene_padre[
                "tm_bp_p"] = "UNKNOWN" if self.entry_gene_padre_mpp.get() == '' else self.entry_gene_padre_mpp.get()

            gene_padre[
                "tp_bm_m"] = "UNKNOWN" if self.entry_gene_padre_pmm.get() == '' else self.entry_gene_padre_pmm.get()
            gene_padre[
                "tp_bm_p"] = "UNKNOWN" if self.entry_gene_padre_pmp.get() == '' else self.entry_gene_padre_pmp.get()
            gene_padre[
                "tp_bp_m"] = "UNKNOWN" if self.entry_gene_padre_ppm.get() == '' else self.entry_gene_padre_ppm.get()
            gene_padre[
                "tp_bp_p"] = "UNKNOWN" if self.entry_gene_padre_ppp.get() == '' else self.entry_gene_padre_ppp.get()

            # Madre Perro
            gene_madre = dict()
            gene_madre["m"] = self.entry_nombre_madre.get()
            # Abuelo Perro
            gene_madre["am"] = "UNKNOWN" if self.entry_gene_madre_m.get() == '' else self.entry_gene_madre_m.get()
            gene_madre["ap"] = "UNKNOWN" if self.entry_gene_madre_p.get() == '' else self.entry_gene_madre_p.get()
            # Bisabuelo Perro
            gene_madre["bm_m"] = "UNKNOWN" if self.entry_gene_madre_mm.get() == '' else self.entry_gene_madre_mm.get()
            gene_madre["bm_p"] = "UNKNOWN" if self.entry_gene_madre_mp.get() == '' else self.entry_gene_madre_mp.get()
            gene_madre["bp_m"] = "UNKNOWN" if self.entry_gene_madre_pm.get() == '' else self.entry_gene_madre_pm.get()
            gene_madre["bp_p"] = "UNKNOWN" if self.entry_gene_madre_pp.get() == '' else self.entry_gene_madre_pp.get()
            # Tatarabuelo Perro
            gene_madre[
                "tm_bm_m"] = "UNKNOWN" if self.entry_gene_madre_mmm.get() == '' else self.entry_gene_madre_mmm.get()
            gene_madre[
                "tm_bm_p"] = "UNKNOWN" if self.entry_gene_madre_mmp.get() == '' else self.entry_gene_madre_mmp.get()
            gene_madre[
                "tm_bp_m"] = "UNKNOWN" if self.entry_gene_madre_mpm.get() == '' else self.entry_gene_madre_mpm.get()
            gene_madre[
                "tm_bp_p"] = "UNKNOWN" if self.entry_gene_madre_mpp.get() == '' else self.entry_gene_madre_mpp.get()

            gene_madre[
                "tp_bm_m"] = "UNKNOWN" if self.entry_gene_madre_pmm.get() == '' else self.entry_gene_madre_pmm.get()
            gene_madre[
                "tp_bm_p"] = "UNKNOWN" if self.entry_gene_madre_pmp.get() == '' else self.entry_gene_madre_pmp.get()
            gene_madre[
                "tp_bp_m"] = "UNKNOWN" if self.entry_gene_madre_ppm.get() == '' else self.entry_gene_madre_ppm.get()
            gene_madre[
                "tp_bp_p"] = "UNKNOWN" if self.entry_gene_madre_ppp.get() == '' else self.entry_gene_madre_ppp.get()

            self.genealogia_data["padre"] = gene_padre
            self.genealogia_data["madre"] = gene_madre

            self.root_gene.destroy()
            self.root_gene.update()

    def init_form_gene_data(self):

        # Padre Perro
        gene_padre = dict()
        gene_padre["p"] = "padre/color"
        # Abuelo Perro
        gene_padre["am"] = "UNKNOWN"
        gene_padre["ap"] = "UNKNOWN"
        # Bisabuelo Perro
        gene_padre["bm_m"] = "UNKNOWN"
        gene_padre["bm_p"] = "UNKNOWN"
        gene_padre["bp_m"] = "UNKNOWN"
        gene_padre["bp_p"] = "UNKNOWN"
        # Tatarabuelo Perro
        gene_padre["tm_bm_m"] = "UNKNOWN"
        gene_padre["tm_bm_p"] = "UNKNOWN"
        gene_padre["tm_bp_m"] = "UNKNOWN"
        gene_padre["tm_bp_p"] = "UNKNOWN"

        gene_padre["tp_bm_m"] = "UNKNOWN"
        gene_padre["tp_bm_p"] = "UNKNOWN"
        gene_padre["tp_bp_m"] = "UNKNOWN"
        gene_padre["tp_bp_p"] = "UNKNOWN"

        # Madre Perro
        gene_madre = dict()
        gene_madre["m"] = "UNKNOWN"
        # Abuelo Perro
        gene_madre["am"] = "UNKNOWN"
        gene_madre["ap"] = "UNKNOWN"
        # Bisabuelo Perro
        gene_madre["bm_m"] = "UNKNOWN"
        gene_madre["bm_p"] = "UNKNOWN"
        gene_madre["bp_m"] = "UNKNOWN"
        gene_madre["bp_p"] = "UNKNOWN"
        # Tatarabuelo Perro
        gene_madre["tm_bm_m"] = "UNKNOWN"
        gene_madre["tm_bm_p"] = "UNKNOWN"
        gene_madre["tm_bp_m"] = "UNKNOWN"
        gene_madre["tm_bp_p"] = "UNKNOWN"

        gene_madre["tp_bm_m"] = "UNKNOWN"
        gene_madre["tp_bm_p"] = "UNKNOWN"
        gene_madre["tp_bp_m"] = "UNKNOWN"
        gene_madre["tp_bp_p"] = "UNKNOWN"

        self.genealogia_data["padre"] = gene_padre
        self.genealogia_data["madre"] = gene_madre

    def register_pedigree(self):

        # Al registrar Pedigree Limpiar all y notificar
        # Productir archivos para impresion.

        try:
            check_int_resul = int(self.entry_certificado_code.get())
            print(check_int_resul)
        except Exception:
            print(Exception)
            showerror('Error', 'El código del certificado solo puede ser un número, no puede contener letras.', parent=root)
            return

        if self.entry_nombre_cachorro.get() == '' or self.entry_sexo.get() == '' or \
                self.entry_color.get() == '' or self.entry_nacimiento.get() == '' or \
                self.entry_raza.get() == '' or self.entry_criador.get() == '' or \
                self.entry_afijo_madre.get() == '' or self.entry_afijo_padre.get() == '' or \
                self.entry_nombre_madre.get() == '' or self.entry_nombre_padre.get() == '' or \
                self.entry_propietario.get() == '' or self.entry_direccion.get() == '' or \
                self.entry_distrito.get() == '' or self.entry_telefono.get() == '' or \
                self.entry_dni.get() == '' or self.entry_certificado_code.get() == '' or \
                self.entry_propietario_afijo.get() == '' or self.entry_chip.get() == '':

            showerror('Error', 'Campos obligatorios vacios.', parent=root)
        elif self.entry_nombre_madre.get().count('/') != 1 or self.entry_nombre_padre.get().count('/') != 1:
            showerror('Error', 'Campos de Nombre/color deben llenarse divididos por un solo / .', parent=root)
        else:
            # si se obtuvo data desde Db.
            if not self.gene_fromDB_loaded:
                self.genealogia_data["padre"]["p"] = self.entry_nombre_padre.get()
                self.genealogia_data["madre"]["m"] = self.entry_nombre_madre.get()

            global user_mail

            time_creation = datetime.datetime.now().strftime('%H:%M:%S - %d/%m/%Y ')
            data_certificado_l = []
            data_certificado_l.append((self.entry_nombre_cachorro.get(),
                                       self.entry_sexo.get(),
                                       self.entry_color.get(),
                                       self.entry_nacimiento.get(),
                                       self.entry_raza.get(),
                                       self.entry_criador.get(),
                                       self.entry_afijo_madre.get(),
                                       self.entry_afijo_padre.get(),
                                       self.entry_nombre_madre.get(),
                                       self.entry_nombre_padre.get(),
                                       self.entry_propietario.get(),
                                       self.entry_direccion.get(),
                                       self.entry_distrito.get(),
                                       self.entry_telefono.get(),
                                       self.entry_dni.get(),
                                       int(self.entry_certificado_code.get()),
                                       json.dumps(self.genealogia_data),
                                       self.entry_propietario_afijo.get(),
                                       "no" if self.check_homologacion.get() == 0 else "si",
                                       user_mail,
                                       time_creation,
                                       self.entry_chip.get()
                                       ))

            # Crear cliente si no existe.
            cliente_afijo = self.entry_propietario_afijo.get()
            cliente_existe_response = db.get_single_element_data("clientes", "cliente_afijo", cliente_afijo)

            if len(cliente_existe_response) == 0:
                print("Cliente no existe.")
                # Cliente no existe crear
                data_cliente_l = []
                # Se genera el codigo del cliente en caso no sea uno antiguo
                # Afijo_cliente = fecha/nro_creacion_hoy

                data_cliente_l.append((self.entry_propietario.get(),
                                       self.entry_propietario_afijo.get(),
                                       self.entry_direccion.get(),
                                       self.entry_distrito.get(),
                                       self.entry_telefono.get(),
                                       self.entry_dni.get(),
                                       "si" if self.check_auto_afijo_code.get() == 1 else "no"))

                # Crear cliente en db
                db.add_new_cliente("clientes", data_cliente_l)
                # Generar Word/Carpeta Cliente

                cliente_data = db.get_single_element_data("clientes", "cliente_afijo", self.entry_propietario_afijo.get())

                if len(cliente_data) > 0:
                    wordHelper = CreateWordHelper()
                    cliente_data_model = [cliente_data[0]["propietario"],
                                          self.entry_criador.get(),
                                          cliente_data[0]["cliente_afijo"]]

                    self.registered_cliente_path = wordHelper.createClienteAfijo(cliente_data_model)

                # Cambiar estado de Afijos del dia.
                if self.check_auto_afijo_code.get() == 1:
                    data = db.get("app_data")
                    fecha = datetime.datetime.today().date().strftime("%d/%m/%Y")
                    if len(data) == 0:
                        print("vale 1 y no se ha creado")
                        # primera vez
                        db.update_app_data_afijos("1", fecha)
                    else:
                        cant_afijos = data[0]["cant_afijos_hoy"]
                        db.update_app_data_afijos(str(int(cant_afijos) + 1), fecha)

            # Check if pedigree afijo ya existe.
            cliente_afijo_perro = self.entry_certificado_code.get()
            cliente_afijo_perro = db.get_single_element_data("pedigrees", "certificado_code", cliente_afijo_perro)

            # Generar data de Pedigree
            if len(cliente_afijo_perro) == 0:
                db.add_new_certificado("pedigrees", data_certificado_l)
                # Generar Word/Carpeta Pedigree
                pedigree_data = db.get_single_pedigree_data(self.entry_certificado_code.get())

                if len(pedigree_data) > 0:
                    pedigree_data_model = PedigreeData()
                    pedigree_data_model.nombre_cachorro = pedigree_data[0]["nombre_cachorro"]
                    pedigree_data_model.sexo = pedigree_data[0]["sexo"]
                    pedigree_data_model.color = pedigree_data[0]["color"]
                    pedigree_data_model.nacimiento = pedigree_data[0]["nacimiento"]
                    pedigree_data_model.raza = pedigree_data[0]["raza"]
                    pedigree_data_model.criador = pedigree_data[0]["criador"]
                    pedigree_data_model.afijo_madre = pedigree_data[0]["afijo_madre"]
                    pedigree_data_model.afijo_padre = pedigree_data[0]["afijo_padre"]
                    pedigree_data_model.nombre_madre = pedigree_data[0]["nombre_madre"]
                    pedigree_data_model.nombre_padre = pedigree_data[0]["nombre_padre"]
                    pedigree_data_model.propietario = pedigree_data[0]["propietario"]
                    pedigree_data_model.direccion = pedigree_data[0]["direccion"]
                    pedigree_data_model.distrito = pedigree_data[0]["distrito"]
                    pedigree_data_model.telefono = pedigree_data[0]["telefono"]
                    pedigree_data_model.dni = pedigree_data[0]["dni"]
                    pedigree_data_model.certificado_code = int(pedigree_data[0]["certificado_code"])
                    pedigree_data_model.propietario_afijo = pedigree_data[0]["propietario_afijo"]
                    pedigree_data_model.homologacion = pedigree_data[0]["homologacion"]
                    pedigree_data_model.created_by = pedigree_data[0]["created_by"]
                    pedigree_data_model.time_creation = pedigree_data[0]["time_creation"]
                    pedigree_data_model.pedigree_gene_data = json.loads(pedigree_data[0]['genealogia_data'])
                    pedigree_data_model.chip_code = pedigree_data[0]['chip_code']

                    wordHelper = CreateWordHelper()
                    self.registered_pedigree_path = wordHelper.createPedigree(pedigree_data_model)
                    self.reset_clean_pedigree_frame()
                    showinfo("Info", "Registro de pedigree creado con exito.")
                else:
                    showerror("Error", "Error al crear el pedigree, intenta de nuevo..")
            else:
                showerror("Error", "El código de certificado del cachorro ya está en uso, no se puede crear.")

    def reset_clean_pedigree_frame(self):
        # Limpiar textos.
        if self.check_auto_afijo_code.get() == 1:
            self.check_auto_afijo_code.set(0)
            self.entry_propietario_afijo.configure(state="normal")
            self.entry_propietario_afijo.delete(0, END)
        else:
            self.entry_propietario_afijo.delete(0, END)

        if self.check_auto_code_perro.get() == 1:
            self.check_auto_code_perro.set(0)
            self.entry_certificado_code.configure(state="normal")
            self.entry_certificado_code.delete(0, END)
        else:
            self.entry_certificado_code.delete(0, END)

        self.check_homologacion.set(0)

        if self.entry_propietario_afijo["state"] == "disabled":
            self.entry_propietario_afijo.configure(state="normal")
            self.entry_propietario_afijo.delete(0, END)

        self.entry_nombre_cachorro.delete(0, END)
        self.entry_sexo.delete(0, END)
        self.entry_color.delete(0, END)
        self.entry_nacimiento.delete(0, END)
        self.entry_raza.delete(0, END)
        self.entry_criador.delete(0, END)
        self.entry_chip.delete(0, END)

        if self.entry_afijo_madre["state"] == "disabled":
            self.entry_afijo_madre.configure(state="normal")
            self.entry_afijo_madre.delete(0, END)
        self.entry_afijo_madre.delete(0, END)

        if self.entry_afijo_padre["state"] == "disabled":
            self.entry_afijo_padre.configure(state="normal")
            self.entry_afijo_padre.delete(0, END)
        self.entry_afijo_padre.delete(0, END)

        if self.entry_nombre_madre["state"] == "disabled":
            self.entry_nombre_madre.configure(state="normal")
            self.entry_nombre_madre.delete(0, END)
        self.entry_nombre_madre.delete(0, END)

        if self.entry_nombre_padre["state"] == "disabled":
            self.entry_nombre_padre.configure(state="normal")
            self.entry_nombre_padre.delete(0, END)
        self.entry_nombre_padre.delete(0, END)

        if self.entry_propietario["state"] == "disabled":
            self.entry_propietario.configure(state="normal")
            self.entry_nombre_padre.delete(0, END)
        self.entry_nombre_padre.delete(0, END)

        if self.entry_propietario["state"] == "disabled":
            self.entry_propietario.configure(state="normal")
            self.entry_propietario.delete(0, END)
        self.entry_propietario.delete(0, END)

        if self.entry_direccion["state"] == "disabled":
            self.entry_direccion.configure(state="normal")
            self.entry_direccion.delete(0, END)
        self.entry_direccion.delete(0, END)

        if self.entry_distrito["state"] == "disabled":
            self.entry_distrito.configure(state="normal")
            self.entry_distrito.delete(0, END)
        self.entry_distrito.delete(0, END)

        if self.entry_telefono["state"] == "disabled":
            self.entry_telefono.configure(state="normal")
            self.entry_telefono.delete(0, END)
        self.entry_telefono.delete(0, END)

        if self.entry_dni["state"] == "disabled":
            self.entry_dni.configure(state="normal")
            self.entry_dni.delete(0, END)
        self.entry_dni.delete(0, END)

        # Reset Search padres btn
        if self.buscar_afijos_padres_btn["text"] == "Cancelar":
            self.buscar_afijos_padres_btn["text"] = "Buscar padres"

        if self.buscar_propietario_btn["text"] == "Cancelar":
            self.buscar_propietario_btn["text"] = "Buscar cliente"
            self.check_auto_afijo_code.set(0)

        self.gene_fromDB_loaded = False

        self.init_form_gene_data()

    # Edit Formularios

    def populate_edit_frame(self, editFrame, tab2):

        bg_label = Label(editFrame, bg='white', image=bn_bg_abc, width=200, height=200)
        bg_label.place(x=250, y=200)

        titleLabel = Label(editFrame, text='Busca Pedigree a editar',
                           font=('arial', 14, 'bold'), bg='white',
                           fg='gold', )
        titleLabel.place(x=190, y=10)

        old_client_Label = Label(editFrame, text='Afijo Cliente', font=('Lucida Sans', 11, 'bold'), bg='white',
                                 fg='gray20', )
        old_client_Label.place(x=20, y=50)
        self.edit_entry_cliente_afijo = Entry(editFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.edit_entry_cliente_afijo.place(x=20, y=75, width=250)
        self.edit_entry_cliente_afijo.configure(state="disabled")

        firstnameLabel = Label(editFrame, text='Nombre de cachorro*', font=('Lucida Sans', 11, 'bold'), bg='white',
                               fg='gray20', )
        firstnameLabel.place(x=20, y=100)
        self.edit_entry_nombre_cachorro = Entry(editFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.edit_entry_nombre_cachorro.place(x=20, y=125, width=250)
        self.edit_entry_nombre_cachorro.configure(state="disabled")

        emailLabel = Label(editFrame, text='Sexo*', font=('Lucida Sans', 11, 'bold'), bg='white',
                           fg='gray20', )
        emailLabel.place(x=370, y=100)
        self.edit_entry_sexo = Entry(editFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.edit_entry_sexo.place(x=370, y=125, width=250)

        passwordLabel = Label(editFrame, text='Color*', font=('Lucida Sans', 11, 'bold'), bg='white',
                              fg='gray20', )
        passwordLabel.place(x=20, y=150)
        self.edit_entry_color = Entry(editFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.edit_entry_color.place(x=20, y=175, width=250)

        answerLabel = Label(editFrame, text='Fecha de nacimiento*', font=('Lucida Sans', 11, 'bold'), bg='white',
                            fg='gray20', )
        answerLabel.place(x=370, y=150)
        self.edit_entry_nacimiento = Entry(editFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.edit_entry_nacimiento.place(x=370, y=175, width=250)

        razaLabel = Label(editFrame, text='Raza*', font=('Lucida Sans', 11, 'bold'), bg='white',
                          fg='gray20', )
        razaLabel.place(x=20, y=200)
        self.edit_entry_raza = Entry(editFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.edit_entry_raza.place(x=20, y=225, width=250)

        criadorLabel = Label(editFrame, text='Criador*', font=('Lucida Sans', 11, 'bold'), bg='white',
                             fg='gray20', )
        criadorLabel.place(x=370, y=200)
        self.edit_entry_criador = Entry(editFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.edit_entry_criador.place(x=370, y=225, width=250)

        afijomadreLabel = Label(editFrame, text='Afijo Madre*', font=('Lucida Sans', 11, 'bold'), bg='white',
                                fg='gray20', )
        afijomadreLabel.place(x=20, y=250)
        self.edit_entry_afijo_madre = Entry(editFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.edit_entry_afijo_madre.place(x=20, y=275, width=250)

        afijopadreLabel = Label(editFrame, text='Afijo Padre*', font=('Lucida Sans', 11, 'bold'), bg='white',
                                fg='gray20', )
        afijopadreLabel.place(x=370, y=250)
        self.edit_entry_afijo_padre = Entry(editFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.edit_entry_afijo_padre.place(x=370, y=275, width=250)


        nombremadreLabel = Label(editFrame, text='Nombre/Color madre*', font=('Lucida Sans', 11, 'bold'), bg='white',
                                 fg='gray20', )
        nombremadreLabel.place(x=20, y=300)
        self.edit_entry_nombre_madre = Entry(editFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.edit_entry_nombre_madre.place(x=20, y=325, width=250)

        nombrepadreLabel = Label(editFrame, text='Nombre/Color padre*', font=('Lucida Sans', 11, 'bold'), bg='white',
                                 fg='gray20', )
        nombrepadreLabel.place(x=370, y=300)
        self.edit_entry_nombre_padre = Entry(editFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.edit_entry_nombre_padre.place(x=370, y=325, width=250)

        propietarioLabel = Label(editFrame, text='Propietario*', font=('Lucida Sans', 11, 'bold'), bg='white',
                                 fg='gray20', )
        propietarioLabel.place(x=20, y=350)
        self.edit_entry_propietario = Entry(editFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.edit_entry_propietario.place(x=20, y=375, width=250)

        certificado_code_Label = Label(editFrame, text='Código de certificado*', font=('Lucida Sans', 11, 'bold'), bg='white',
                                       fg='gray20', )
        certificado_code_Label.place(x=370, y=350)
        self.edit_entry_certificado_code = Entry(editFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.edit_entry_certificado_code.place(x=370, y=375, width=250)
        self.edit_entry_certificado_code.configure(state="disabled")

        distritoLabel = Label(editFrame, text='Creado por:', font=('Lucida Sans', 11, 'bold'), bg='white',
                              fg='gray20', )
        distritoLabel.place(x=20, y=400)
        self.edit_created_by = Entry(editFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.edit_created_by.place(x=20, y=425, width=250)
        self.edit_created_by.configure(state="disabled")

        dni_Label = Label(editFrame, text='Fecha creación:', font=('Lucida Sans', 11, 'bold'), bg='white',
                              fg='gray20', )
        dni_Label.place(x=20, y=450)
        self.edit_created_time = Entry(editFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.edit_created_time.place(x=20, y=475, width=250)
        self.edit_created_time.configure(state="disabled")

        chipLabel = Label(editFrame, text='Chip*', font=('Lucida Sans', 11, 'bold'), bg='white',
                           fg='gray20', )
        chipLabel.place(x=370, y=400)
        self.edit_entry_chip = Entry(editFrame, font=('Lucida Sans', 11), bg='lightgray')
        self.edit_entry_chip.place(x=370, y=425, width=250)

        agregarextrabtn = Button(editFrame, text='Editar datos genealogicos', font=('arial', 13, 'bold'), fg='white',
                                 bg='gray20', cursor='hand2', bd=0, activeforeground='white',
                                 command=lambda: self.add_genealogia_edit())
        agregarextrabtn.place(x=370, y=475)

        self.check_homologacion_edit = IntVar()
        checkButton = Checkbutton(editFrame, text='Homologación', variable=self.check_homologacion_edit, onvalue=1,
                                  offvalue=0, font=('Lucida Sans', 11, 'bold'), bg='white')
        checkButton.place(x=20, y=510)


        registerbutton = Button(editFrame, text='Editar Registro', font=('arial', 14, 'bold'), fg='white',
                                bg='gray20', cursor='hand2', bd=0, activeforeground='white',
                                command=lambda: self.edit_pedigree())
        registerbutton.place(x=20, y=560)

        open_path_button = Button(editFrame, image=openfolderimage, fg='black',
                                bg='white', cursor='hand2', bd=0, activeforeground='white',
                                command=lambda: self.open_path_pedigree_edit())
        open_path_button.place(x=365, y=560)
        open_pedigree_label = Label(editFrame, text='Pedigree', font=('Lucida Sans', 11, 'bold'), bg='white',
                              fg='gray20', )
        open_pedigree_label.place(x=400, y=570)

        open_path_cliente_button = Button(editFrame, image=openfolderimage, fg='black',
                                bg='white', cursor='hand2', bd=0, activeforeground='white',
                                command=lambda:self.open_path_cliente_edit())
        open_path_cliente_button.place(x=505, y=560)
        open_cliente_label = Label(editFrame, text='Cliente', font=('Lucida Sans', 11, 'bold'), bg='white',
                              fg='gray20', )
        open_cliente_label.place(x=540, y=570)

        # Populate SearchFrame
        searchFrame = Frame(tab2, bg='white', width=350, height=screen_height)
        searchFrame.place(x=700, y=30)

        # Name Input
        # Label(searchFrame, text='Critério de búsqueda: ').grid(row=1, column=0)
        # self.pedigree_data = Entry(searchFrame)
        # self.pedigree_data.grid(row=1, column=1)

#        ttk.Button(searchFrame, text='Buscar', command=self.get_filtered_pedigrees).grid(row=3, columnspan=2, sticky=W + E)

        #        self.tree = ttk.Treeview(searchFrame, height = 10, columns = ("#0","#1","#2"))
        self.tree = ttk.Treeview(searchFrame, height=28, columns=2)  # height(alarga el tamaño del frame)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Nombre', anchor=CENTER)
        self.tree.heading('#1', text='Codigo', anchor=CENTER)

        # Buttons
        ttk.Button(searchFrame, text='Eliminar', command=self.delete_pedigree).grid(row=5, column=0, sticky=W + E)
        ttk.Button(searchFrame, text='Seleccionar', command=self.set_selected_pedigree_data).grid(row=5, column=1, sticky=W + E)

        # Filters Frame
        filter_frame = Frame(tab2, bg='white', width=200, height=screen_height-155)
        filter_frame.place(x=1110, y=30)

        filtroLabel = Label(filter_frame, text='Filtros:', font=('Lucida Sans', 11, 'bold'), bg='white',
                              fg='gray20', )
        filtroLabel.place(x=20, y=10)

        self.name_filter = IntVar()
        check_name = Checkbutton(filter_frame, text='Nombre cachorro', variable=self.name_filter, onvalue=1,
                                  offvalue=0, font=('Lucida Sans', 10, 'bold'), bg='white')
        check_name.place(x=20, y=40)
        self.name_filter.set(1)

        self.afijo_cachorro_filter = IntVar()
        check_af_cachorro = Checkbutton(filter_frame, text='Afijo cachorro', variable=self.afijo_cachorro_filter, onvalue=1,
                                  offvalue=0, font=('Lucida Sans', 10, 'bold'), bg='white')
        check_af_cachorro.place(x=20, y=65)

        self.afijo_propiet_filter = IntVar()
        self.check_af_prop = Checkbutton(filter_frame, text='Afijo propietario', variable=self.afijo_propiet_filter, onvalue=1,
                                  offvalue=0, font=('Lucida Sans', 10, 'bold'), bg='white')
        self.check_af_prop.place(x=20, y=90)

        self.raza_filter = IntVar()
        check_raza = Checkbutton(filter_frame, text='Raza', variable=self.raza_filter, onvalue=1,
                                  offvalue=0, font=('Lucida Sans', 10, 'bold'), bg='white')
        check_raza.place(x=20, y=115)

        # Entrys
        self.entry_nombre_cachorro_filter = EntryWithPlaceholder(filter_frame, "Nombre cachorro")
        self.entry_nombre_cachorro_filter.place(x=20, y=150, width=150)

        self.entry_afijo_cachorro_filter = EntryWithPlaceholder(filter_frame, "Afijo cachorro")
        self.entry_afijo_cachorro_filter.place(x=20, y=175, width=150)

        self.entry_afijo_prop_filter = EntryWithPlaceholder(filter_frame, "Afijo propietario")
        self.entry_afijo_prop_filter.place(x=20, y=200, width=150)

        self.entry_raza_filter = EntryWithPlaceholder(filter_frame, "Raza")
        self.entry_raza_filter.place(x=20, y=225, width=150)

        ttk.Button(filter_frame, text='Buscar', command=self.get_filtered_pedigrees).place(x=0, y=555, width=200)
        ttk.Button(filter_frame, text='Limpiar filtros',
                   command=lambda: self.clean_filters(searchFrame)).place(x=0, y=585, width=200)

    def clean_filters(self, searchFrame):
        self.name_filter.set(1)
        self.afijo_cachorro_filter.set(0)
        self.afijo_propiet_filter.set(0)
        self.raza_filter.set(0)

        self.entry_nombre_cachorro_filter.delete(0, END)
        self.entry_afijo_cachorro_filter.delete(0, END)
        self.entry_afijo_prop_filter.delete(0, END)
        self.entry_raza_filter.delete(0, END)

        self.entry_nombre_cachorro_filter.focus()
        self.entry_afijo_cachorro_filter.focus()
        self.entry_afijo_prop_filter.focus()
        self.entry_raza_filter.focus()

        searchFrame.focus()
        searchFrame.focus_force()

    def add_genealogia_edit(self):

        if self.edit_entry_nombre_cachorro.get() == '':
            showerror('Error', 'Porfavor Selecciona un Pedigree a Modificar.', parent=root)
        else:

            self.root_gene_edit = Toplevel()
            self.root_gene_edit.title('Editar Genealogia')
            genealogia_screen_size = str(screen_width - 100) + "x" + str(screen_height)
            self.root_gene_edit.geometry(genealogia_screen_size)
            self.root_gene_edit.config(bg='white')
            self.root_gene_edit.focus_force()
            self.root_gene_edit.grab_set()

            forgetpassLabel = Label(self.root_gene_edit, text='Agregar informacion de genealogía',
                                    font=('Lucida Sans', 18, 'bold'), fg='green',
                                    bg='white')
            forgetpassLabel.place(x=(screen_width / 2) - 250, y=10)

            aceptar_btn = Button(self.root_gene_edit, text='Guardar cambios',
                                 font=('Lucida Sans', 14, 'bold'), fg='green',
                                 bg='white', command=lambda: self.save_edit_genealogia_data())
            aceptar_btn.place(x=50, y=600)

            # PADRE Y MADRE
            gene_madre_Label = Label(self.root_gene_edit, text='Madre', font=('Lucida Sans', 13, 'bold'),
                                     bg='white',
                                     fg='gray20', )
            gene_madre_Label.place(x=20, y=250)
            self.entry_gene_madre_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_edit.place(x=20, y=275, width=250)

            gene_padre_Label = Label(self.root_gene_edit, text='Padre', font=('Lucida Sans', 13, 'bold'), bg='white',
                                     fg='gray20', )
            gene_padre_Label.place(x=20, y=400)
            self.entry_gene_padre_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_edit.place(x=20, y=425, width=250)

            # Abuelos

            self.entry_gene_madre_m_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_m_edit.place(x=300, y=150, width=250)

            self.entry_gene_madre_p_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_p_edit.place(x=300, y=250, width=250)

            self.entry_gene_padre_m_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_m_edit.place(x=300, y=450, width=250)

            self.entry_gene_padre_p_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_p_edit.place(x=300, y=550, width=250)

            # Abuelos 2da gen (BISA)
            # madre
            self.entry_gene_madre_mm_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_mm_edit.place(x=570, y=100, width=250)

            self.entry_gene_madre_mp_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_mp_edit.place(x=570, y=150, width=250)

            self.entry_gene_madre_pm_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_pm_edit.place(x=570, y=250, width=250)

            self.entry_gene_madre_pp_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_pp_edit.place(x=570, y=300, width=250)
            # padre
            self.entry_gene_padre_mm_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_mm_edit.place(x=570, y=400, width=250)

            self.entry_gene_padre_mp_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_mp_edit.place(x=570, y=450, width=250)

            self.entry_gene_padre_pm_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_pm_edit.place(x=570, y=550, width=250)

            self.entry_gene_padre_pp_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_pp_edit.place(x=570, y=600, width=250)

            # Abuelos 3ra gen (TATA)
            # madre
            self.entry_gene_madre_mmm_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_mmm_edit.place(x=840, y=75, width=250)

            self.entry_gene_madre_mmp_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_mmp_edit.place(x=840, y=100, width=250)

            self.entry_gene_madre_mpm_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_mpm_edit.place(x=840, y=150, width=250)

            self.entry_gene_madre_mpp_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_mpp_edit.place(x=840, y=175, width=250)

            self.entry_gene_madre_pmm_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_pmm_edit.place(x=840, y=225, width=250)

            self.entry_gene_madre_pmp_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_pmp_edit.place(x=840, y=250, width=250)

            self.entry_gene_madre_ppm_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_ppm_edit.place(x=840, y=300, width=250)

            self.entry_gene_madre_ppp_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_madre_ppp_edit.place(x=840, y=325, width=250)

            # padre
            self.entry_gene_padre_mmm_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_mmm_edit.place(x=840, y=375, width=250)

            self.entry_gene_padre_mmp_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_mmp_edit.place(x=840, y=400, width=250)

            self.entry_gene_padre_mpm_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_mpm_edit.place(x=840, y=450, width=250)

            self.entry_gene_padre_mpp_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_mpp_edit.place(x=840, y=475, width=250)

            self.entry_gene_padre_pmm_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_pmm_edit.place(x=840, y=525, width=250)

            self.entry_gene_padre_pmp_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_pmp_edit.place(x=840, y=550, width=250)

            self.entry_gene_padre_ppm_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_ppm_edit.place(x=840, y=600, width=250)

            self.entry_gene_padre_ppp_edit = Entry(self.root_gene_edit, font=('Lucida Sans', 13), bg='lightgray')
            self.entry_gene_padre_ppp_edit.place(x=840, y=625, width=250)

            # Setear Datos.
            # Si está en unknown se colocará vacio.

            gene_madre = self.edit_gene_data["madre"]
            gene_padre = self.edit_gene_data["padre"]

            # gene_madre = self.gene_data_madre["madre"]
            # gene_madre_m = self.gene_data_madre["madre"]
            # gene_madre_p = self.gene_data_madre["padre"]
            #
            # gene_padre = self.gene_data_padre["padre"]
            # gene_padre_m = self.gene_data_padre["madre"]
            # gene_padre_p = self.gene_data_padre["padre"]



            self.entry_gene_madre_edit.delete(0, END)
            self.entry_gene_madre_edit.insert(0, self.edit_entry_nombre_madre.get())

            self.entry_gene_padre_edit.delete(0, END)
            self.entry_gene_padre_edit.insert(0, self.edit_entry_nombre_padre.get())

            self.entry_gene_madre_m_edit.insert(0, "" if gene_madre["am"] == "UNKNOWN" else gene_madre["am"])
            self.entry_gene_madre_p_edit.insert(0, "" if gene_madre["ap"] == "UNKNOWN" else gene_madre["ap"])
            # Bisa Maternos
            self.entry_gene_madre_mm_edit.insert(0, "" if gene_madre["bm_m"] == "UNKNOWN" else gene_madre["bm_m"])
            self.entry_gene_madre_mp_edit.insert(0, "" if gene_madre["bm_p"] == "UNKNOWN" else gene_madre["bm_p"])

            self.entry_gene_madre_pm_edit.insert(0, "" if gene_madre["bp_m"] == "UNKNOWN" else gene_madre["bp_m"])
            self.entry_gene_madre_pp_edit.insert(0, "" if gene_madre["bp_p"] == "UNKNOWN" else gene_madre["bp_p"])
            # Tata Maternos
            self.entry_gene_madre_mmm_edit.insert(0, "" if gene_madre["tm_bm_m"] == "UNKNOWN" else gene_madre["tm_bm_m"])
            self.entry_gene_madre_mmp_edit.insert(0, "" if gene_madre["tm_bm_p"] == "UNKNOWN" else gene_madre["tm_bm_p"])
            self.entry_gene_madre_mpm_edit.insert(0, "" if gene_madre["tm_bp_m"] == "UNKNOWN" else gene_madre["tm_bp_m"])
            self.entry_gene_madre_mpp_edit.insert(0, "" if gene_madre["tm_bp_p"] == "UNKNOWN" else gene_madre["tm_bp_p"])

            self.entry_gene_madre_pmm_edit.insert(0, "" if gene_madre["tp_bm_m"] == "UNKNOWN" else gene_madre["tp_bm_m"])
            self.entry_gene_madre_pmp_edit.insert(0, "" if gene_madre["tp_bm_p"] == "UNKNOWN" else gene_madre["tp_bm_p"])
            self.entry_gene_madre_ppm_edit.insert(0, "" if gene_madre["tp_bp_m"] == "UNKNOWN" else gene_madre["tp_bp_m"])
            self.entry_gene_madre_ppp_edit.insert(0, "" if gene_madre["tp_bp_p"] == "UNKNOWN" else gene_madre["tp_bp_p"])

            # Padre
            # Abuelos Maternos
            self.entry_gene_padre_m_edit.insert(0, "" if gene_padre["am"] == "UNKNOWN" else gene_padre["am"])
            self.entry_gene_padre_p_edit.insert(0, "" if gene_padre["ap"] == "UNKNOWN" else gene_padre["ap"])
            # Bisa Maternos
            self.entry_gene_padre_mm_edit.insert(0, "" if gene_padre["bm_m"] == "UNKNOWN" else gene_padre["bm_m"])
            self.entry_gene_padre_mp_edit.insert(0, "" if gene_padre["bm_p"] == "UNKNOWN" else gene_padre["bm_p"])

            self.entry_gene_padre_pm_edit.insert(0, "" if gene_padre["bp_m"] == "UNKNOWN" else gene_padre["bp_m"])
            self.entry_gene_padre_pp_edit.insert(0, "" if gene_padre["bp_p"] == "UNKNOWN" else gene_padre["bp_p"])
            # Tata Maternos
            self.entry_gene_padre_mmm_edit.insert(0, "" if gene_padre["tm_bm_m"] == "UNKNOWN" else gene_padre["tm_bm_m"])
            self.entry_gene_padre_mmp_edit.insert(0, "" if gene_padre["tm_bm_p"] == "UNKNOWN" else gene_padre["tm_bm_p"])
            self.entry_gene_padre_mpm_edit.insert(0, "" if gene_padre["tm_bp_m"] == "UNKNOWN" else gene_padre["tm_bm_p"])
            self.entry_gene_padre_mpp_edit.insert(0, "" if gene_padre["tm_bp_p"] == "UNKNOWN" else gene_padre["tm_bp_p"])

            self.entry_gene_padre_pmm_edit.insert(0, "" if gene_padre["tp_bm_m"] == "UNKNOWN" else gene_padre["tp_bm_m"])
            self.entry_gene_padre_pmp_edit.insert(0, "" if gene_padre["tp_bm_p"] == "UNKNOWN" else gene_padre["tp_bm_p"])
            self.entry_gene_padre_ppm_edit.insert(0, "" if gene_padre["tp_bp_m"] == "UNKNOWN" else gene_padre["tp_bp_m"])
            self.entry_gene_padre_ppp_edit.insert(0, "" if gene_padre["tp_bp_p"] == "UNKNOWN" else gene_padre["tp_bp_p"])

            self.root_gene_edit.mainloop()

    def get_filtered_pedigrees(self):

        if self.entry_nombre_cachorro_filter.get() == "Nombre cachorro" and\
                self.entry_afijo_cachorro_filter.get() == "Afijo cachorro" and\
                self.entry_afijo_prop_filter.get() == "Afijo propietario" and\
                self.entry_raza_filter.get() == "Raza":
            showerror("Error", "Casillas de filtro vacías.")
            return

        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # getting data

        dict_filters = {
            "nombre_cachorro": self.name_filter.get(),
            "certificado_code": self.afijo_cachorro_filter.get(),  # Afijo cachorro
            "propietario_afijo": self.afijo_propiet_filter.get(),
            "raza": self.raza_filter.get()
        }

        filters_str = [self.entry_nombre_cachorro_filter.get(), self.entry_afijo_cachorro_filter.get(),
                       self.entry_afijo_prop_filter.get(), self.entry_raza_filter.get()]

#        data = db.get("pedigrees")
        data = db.get_data_multiple_filters("pedigrees", dict_filters, filters_str)

        if len(data) == 0:
            showerror("Error", "No se encontraron coincidencias.")
        else:
            # filling data
            for row in data:
                pedigree_data_model = PedigreeData()
                pedigree_data_model.nombre_cachorro = row[0]
                pedigree_data_model.sexo = row[1]
                pedigree_data_model.color = row[2]
                pedigree_data_model.nacimiento = row[3]
                pedigree_data_model.raza = row[4]
                pedigree_data_model.criador = row[5]
                pedigree_data_model.afijo_madre = row[6]
                pedigree_data_model.afijo_padre = row[7]
                pedigree_data_model.nombre_madre = row[8]
                pedigree_data_model.nombre_padre = row[9]
                pedigree_data_model.propietario = row[10]
                pedigree_data_model.direccion = row[11]
                pedigree_data_model.distrito = row[12]
                pedigree_data_model.telefono = row[13]
                pedigree_data_model.dni = row[14]
                pedigree_data_model.certificado_code = int(row[15])

                self.tree.insert('', 0, text=pedigree_data_model.nombre_cachorro,
                                 values=pedigree_data_model.certificado_code)

    def set_selected_pedigree_data(self):
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            showerror("Error", "Selecciona el registro a editar.")
            return
        code_pedigree = self.tree.item(self.tree.selection())['values'][0]

        # Primero obtenemos y seteamos toda la data del Pedigree seleccionado

        pedigree_data = db.get_single_pedigree_data(code_pedigree)
        pedigree_data_model = PedigreeData()
        pedigree_data_model.nombre_cachorro = pedigree_data[0]["nombre_cachorro"]
        pedigree_data_model.sexo = pedigree_data[0]["sexo"]
        pedigree_data_model.color = pedigree_data[0]["color"]
        pedigree_data_model.nacimiento = pedigree_data[0]["nacimiento"]
        pedigree_data_model.raza = pedigree_data[0]["raza"]
        pedigree_data_model.criador = pedigree_data[0]["criador"]
        pedigree_data_model.afijo_madre = pedigree_data[0]["afijo_madre"]
        pedigree_data_model.afijo_padre = pedigree_data[0]["afijo_padre"]
        pedigree_data_model.nombre_madre = pedigree_data[0]["nombre_madre"]
        pedigree_data_model.nombre_padre = pedigree_data[0]["nombre_padre"]
        pedigree_data_model.propietario = pedigree_data[0]["propietario"]
        pedigree_data_model.direccion = pedigree_data[0]["direccion"]
        pedigree_data_model.distrito = pedigree_data[0]["distrito"]
        pedigree_data_model.telefono = pedigree_data[0]["telefono"]
        pedigree_data_model.dni = pedigree_data[0]["dni"]
        pedigree_data_model.certificado_code = int(pedigree_data[0]["certificado_code"])
        pedigree_data_model.propietario_afijo = pedigree_data[0]["propietario_afijo"]
        pedigree_data_model.homologacion = pedigree_data[0]["homologacion"]
        pedigree_data_model.created_by = pedigree_data[0]["created_by"]
        pedigree_data_model.time_creation = pedigree_data[0]["time_creation"]
        pedigree_data_model.chip_code = pedigree_data[0]["chip_code"]

        # Luego editamos con el boton editar registro.
        self.edit_entry_cliente_afijo.configure(state="normal")
        self.edit_entry_cliente_afijo.delete(0,END)  # Esto no necesariamente se debe borrar en las mismas condiciones
        self.edit_entry_nombre_cachorro.configure(state="normal")
        self.edit_entry_nombre_cachorro.delete(0,END)
        self.edit_entry_sexo.delete(0,END)
        self.edit_entry_color.delete(0,END)
        self.edit_entry_nacimiento.delete(0,END)
        self.edit_entry_raza.delete(0,END)
        self.edit_entry_criador.delete(0,END)
        self.edit_entry_afijo_madre.delete(0,END)
        self.edit_entry_afijo_padre.delete(0,END)
        self.edit_entry_nombre_madre.delete(0,END)
        self.edit_entry_nombre_padre.delete(0,END)
        self.edit_entry_propietario.delete(0,END)
        self.edit_entry_certificado_code.configure(state="normal")
        self.edit_entry_certificado_code.delete(0,END)
        self.edit_created_by.configure(state="normal")
        self.edit_created_time.configure(state="normal")
        self.edit_created_by.delete(0,END)
        self.edit_created_time.delete(0,END)
        self.edit_entry_chip.delete(0, END)

        self.edit_entry_cliente_afijo.insert(0, pedigree_data_model.propietario_afijo)
        self.edit_entry_nombre_cachorro.insert(0, pedigree_data_model.nombre_cachorro)
        self.edit_entry_sexo.insert(0, pedigree_data_model.sexo)
        self.edit_entry_color.insert(0, pedigree_data_model.color)
        self.edit_entry_nacimiento.insert(0, pedigree_data_model.nacimiento)
        self.edit_entry_raza.insert(0, pedigree_data_model.raza)
        self.edit_entry_criador.insert(0, pedigree_data_model.criador)
        self.edit_entry_afijo_madre.insert(0, pedigree_data_model.afijo_madre)
        self.edit_entry_afijo_padre.insert(0, pedigree_data_model.afijo_padre)
        self.edit_entry_nombre_madre.insert(0, pedigree_data_model.nombre_madre)
        self.edit_entry_nombre_padre.insert(0, pedigree_data_model.nombre_padre)
        self.edit_entry_propietario.insert(0, pedigree_data_model.propietario)
        self.edit_entry_certificado_code.insert(0, pedigree_data_model.certificado_code)
        self.edit_entry_certificado_code.configure(state="disabled")
        self.edit_entry_cliente_afijo.configure(state="disabled")
        self.edit_entry_nombre_cachorro.configure(state="disabled")

        self.edit_created_by.insert(0, pedigree_data_model.created_by)
        self.edit_created_by.configure(state="disabled")
        self.edit_created_time.insert(0, pedigree_data_model.time_creation)
        self.edit_created_time.configure(state="disabled")
        self.edit_entry_chip.insert(0, pedigree_data_model.chip_code)

        if pedigree_data_model.homologacion == "si":
            self.check_homologacion_edit.set(1)
        else:
            self.check_homologacion_edit.set(0)

        # Set paths

        home = expanduser("~")
        main_app_path = home + "\\Registros Pedigree App"
        pedigree_app_path = main_app_path + "\\Pedigrees"
        clientes_app_path = main_app_path + "\\Afijos"

        cachorro_name = pedigree_data_model.nombre_cachorro
        afijo_cachorro = str(pedigree_data_model.certificado_code)
        carpeta_name = cachorro_name.upper() + " - " + afijo_cachorro.upper()
        path_file_pedigree = pedigree_app_path + f'\\{carpeta_name}'
        pedigree_doc_path = path_file_pedigree + "\\registro_pedigree_reverso.docx"

        self.registered_pedigree_path_edit = pedigree_doc_path

        cliente_name = pedigree_data_model.propietario
        cliente_afijo = pedigree_data_model.propietario_afijo

        carpeta_name = cliente_name.upper() + " - " + cliente_afijo.replace('/', '')
        path_file = clientes_app_path + f'\\{carpeta_name}'
        afijo_cliente_doc_path = path_file + "\\afijo.docx"

        self.registered_cliente_path_edit = afijo_cliente_doc_path

        # Populate Pedigree diagram Genealogia
        self.edit_gene_data = json.loads(pedigree_data[0]['genealogia_data'])

    def save_edit_genealogia_data(self):

        gene_padre = dict()
        gene_padre["p"] = self.entry_gene_padre_edit.get()
        # Abuelo Perro
        gene_padre["am"] = "UNKNOWN" if self.entry_gene_padre_m_edit.get() == '' else self.entry_gene_padre_m_edit.get()
        gene_padre["ap"] = "UNKNOWN" if self.entry_gene_padre_p_edit.get() == '' else self.entry_gene_padre_p_edit.get()
        # Bisabuelo Perro
        gene_padre["bm_m"] = "UNKNOWN" if self.entry_gene_padre_mm_edit.get() == '' else self.entry_gene_padre_mm_edit.get()
        gene_padre["bm_p"] = "UNKNOWN" if self.entry_gene_padre_mp_edit.get() == '' else self.entry_gene_padre_mp_edit.get()
        gene_padre["bp_m"] = "UNKNOWN" if self.entry_gene_padre_pm_edit.get() == '' else self.entry_gene_padre_pm_edit.get()
        gene_padre["bp_p"] = "UNKNOWN" if self.entry_gene_padre_pp_edit.get() == '' else self.entry_gene_padre_pp_edit.get()
        # Tatarabuelo Perro
        gene_padre["tm_bm_m"] = "UNKNOWN" if self.entry_gene_padre_mmm_edit.get() == '' else self.entry_gene_padre_mmm_edit.get()
        gene_padre["tm_bm_p"] = "UNKNOWN" if self.entry_gene_padre_mmp_edit.get() == '' else self.entry_gene_padre_mmp_edit.get()
        gene_padre["tm_bp_m"] = "UNKNOWN" if self.entry_gene_padre_mpm_edit.get() == '' else self.entry_gene_padre_mpm_edit.get()
        gene_padre["tm_bp_p"] = "UNKNOWN" if self.entry_gene_padre_mpp_edit.get() == '' else self.entry_gene_padre_mpp_edit.get()

        gene_padre["tp_bm_m"] = "UNKNOWN" if self.entry_gene_padre_pmm_edit.get() == '' else self.entry_gene_padre_pmm_edit.get()
        gene_padre["tp_bm_p"] = "UNKNOWN" if self.entry_gene_padre_pmp_edit.get() == '' else self.entry_gene_padre_pmp_edit.get()
        gene_padre["tp_bp_m"] = "UNKNOWN" if self.entry_gene_padre_ppm_edit.get() == '' else self.entry_gene_padre_ppm_edit.get()
        gene_padre["tp_bp_p"] = "UNKNOWN" if self.entry_gene_padre_ppp_edit.get() == '' else self.entry_gene_padre_ppp_edit.get()

        # Madre Perro
        gene_madre = dict()
        gene_madre["m"] = self.entry_gene_madre_edit.get()
        # Abuelo Perro
        gene_madre["am"] = "UNKNOWN" if self.entry_gene_madre_m_edit.get() == '' else self.entry_gene_madre_m_edit.get()
        gene_madre["ap"] = "UNKNOWN" if self.entry_gene_madre_p_edit.get() == '' else self.entry_gene_madre_p_edit.get()
        # Bisabuelo Perro
        gene_madre["bm_m"] = "UNKNOWN" if self.entry_gene_madre_mm_edit.get() == '' else self.entry_gene_madre_mm_edit.get()
        gene_madre["bm_p"] = "UNKNOWN" if self.entry_gene_madre_mp_edit.get() == '' else self.entry_gene_madre_mp_edit.get()
        gene_madre["bp_m"] = "UNKNOWN" if self.entry_gene_madre_pm_edit.get() == '' else self.entry_gene_madre_pm_edit.get()
        gene_madre["bp_p"] = "UNKNOWN" if self.entry_gene_madre_pp_edit.get() == '' else self.entry_gene_madre_pp_edit.get()
        # Tatarabuelo Perro
        gene_madre["tm_bm_m"] = "UNKNOWN" if self.entry_gene_madre_mmm_edit.get() == '' else self.entry_gene_madre_mmm_edit.get()
        gene_madre["tm_bm_p"] = "UNKNOWN" if self.entry_gene_madre_mmp_edit.get() == '' else self.entry_gene_madre_mmp_edit.get()
        gene_madre["tm_bp_m"] = "UNKNOWN" if self.entry_gene_madre_mpm_edit.get() == '' else self.entry_gene_madre_mpm_edit.get()
        gene_madre["tm_bp_p"] = "UNKNOWN" if self.entry_gene_madre_mpp_edit.get() == '' else self.entry_gene_madre_mpp_edit.get()

        gene_madre["tp_bm_m"] = "UNKNOWN" if self.entry_gene_madre_pmm_edit.get() == '' else self.entry_gene_madre_pmm_edit.get()
        gene_madre["tp_bm_p"] = "UNKNOWN" if self.entry_gene_madre_pmp_edit.get() == '' else self.entry_gene_madre_pmp_edit.get()
        gene_madre["tp_bp_m"] = "UNKNOWN" if self.entry_gene_madre_ppm_edit.get() == '' else self.entry_gene_madre_ppm_edit.get()
        gene_madre["tp_bp_p"] = "UNKNOWN" if self.entry_gene_madre_ppp_edit.get() == '' else self.entry_gene_madre_ppp_edit.get()

        self.edit_gene_data["padre"] = gene_padre
        self.edit_gene_data["madre"] = gene_madre

        self.root_gene_edit.destroy()
        self.root_gene_edit.update()

    def edit_pedigree(self):
        # take values of current pedigree_edit_object and Ui
        if self.edit_entry_nombre_cachorro.get() == '' or self.edit_entry_sexo.get() == '' or \
                self.edit_entry_color.get() == '' or self.edit_entry_nacimiento.get() == '' or \
                self.edit_entry_raza.get() == '' or self.edit_entry_criador.get() == '' or \
                self.edit_entry_afijo_madre.get() == '' or self.edit_entry_afijo_padre.get() == '' or \
                self.edit_entry_nombre_madre.get() == '' or self.edit_entry_nombre_padre.get() == '' or \
                self.edit_entry_propietario.get() == '' or self.edit_entry_certificado_code.get() == '' or\
                self.edit_entry_chip.get() == '':

            showerror('Error', 'Campos obligatorios vacios.', parent=root)
        else:
            try:
                edited_data = PedigreeData()
                edited_data.nombre_cachorro = self.edit_entry_nombre_cachorro.get()
                edited_data.sexo = self.edit_entry_sexo.get()
                edited_data.color = self.edit_entry_color.get()
                edited_data.nacimiento = self.edit_entry_nacimiento.get()
                edited_data.raza = self.edit_entry_raza.get()
                edited_data.criador = self.edit_entry_criador.get()
                edited_data.afijo_madre = self.edit_entry_afijo_madre.get()
                edited_data.afijo_padre = self.edit_entry_afijo_padre.get()
                edited_data.nombre_madre = self.edit_entry_afijo_padre.get()
                edited_data.nombre_padre = self.edit_entry_afijo_padre.get()
                edited_data.propietario = self.edit_entry_propietario.get()
                edited_data.homologacion = "no" if self.check_homologacion_edit.get() == 0 else "si"
                edited_data.certificado_code = self.edit_entry_certificado_code.get()
                edited_data.chip_code = self.edit_entry_chip.get()
                # and set them to the db.
                db.update_pedigree_data(edited_data, json.dumps(self.edit_gene_data))
                # Update word file.
                pedigree_data_model = PedigreeData()
                pedigree_data_model.nombre_cachorro = edited_data.nombre_cachorro
                pedigree_data_model.sexo = edited_data.sexo
                pedigree_data_model.color = edited_data.color
                pedigree_data_model.nacimiento = edited_data.nacimiento
                pedigree_data_model.raza = edited_data.raza
                pedigree_data_model.criador = edited_data.criador
                pedigree_data_model.afijo_madre = edited_data.afijo_madre
                pedigree_data_model.afijo_padre = edited_data.afijo_padre
                pedigree_data_model.nombre_madre = edited_data.nombre_madre
                pedigree_data_model.nombre_padre = edited_data.nombre_padre
                pedigree_data_model.propietario = edited_data.propietario
                pedigree_data_model.certificado_code = edited_data.certificado_code
                pedigree_data_model.homologacion = edited_data.homologacion
                pedigree_data_model.pedigree_gene_data = self.edit_gene_data
                pedigree_data_model.chip_code = edited_data.chip_code

                wordHelper = CreateWordHelper()
                wordHelper.createPedigree(pedigree_data_model)
                showinfo("Info", "Se editó el registro con éxito.")
            except Exception as e:
                showinfo("Info", "El archivo que desea modificar esta abierto.")
                print("Error modificando archivo")
                print(e)

    def delete_pedigree(self):
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            showerror("Error", "Selecciona el registro a eliminar.")
            return

        result = askquestion("Confirmación", "Deseas eliminar el registro?")
        if result == "yes":
            try:
                wordHelper = CreateWordHelper()

                home = expanduser("~")
                main_app_path = home + "\\Registros Pedigree App"
                pedigree_app_path = main_app_path + "\\Pedigrees"

                pedigree_name = self.tree.item(self.tree.selection())['text']
                print("nameeeeeeeeeeeeeeeeeeeee")
                print(pedigree_name)
                pedigree_afijo = self.tree.item(self.tree.selection())['values'][0]
                print("afijoooooooooooooooo")
                print(pedigree_afijo)

                carpeta_name = pedigree_name.upper() + " - " + str(pedigree_afijo)
                path_file = pedigree_app_path + f'\\{carpeta_name}'
                print("carpeta name-------------")
                print(carpeta_name)
                wordHelper.deleteFile(path_file)

                result = db.delete_data("pedigrees", "certificado_code", pedigree_afijo)
                if result:
                    showinfo("Info", "Registro eliminado exitosamente.")
                    self.get_filtered_pedigrees()

                else:
                    showerror("Error", "Error al eliminar el registro.")
            except Exception as e:
                showerror("Error", "Error al eliminar el cliente.")
                print(e)


    def open_path_pedigree_edit(self):
        try:
            if self.registered_pedigree_path_edit == "":
                showerror("Error", "No hay directorio el cuál abrir.")
            else:
                print("try")
                print(self.registered_pedigree_path_edit)
                subprocess.Popen(r'explorer /select,' + self.registered_pedigree_path_edit)  # Abrir carpeta en escritorio
        except Exception:
            showerror("Error", "No hay directorio el cuál abrir.")

    def open_path_cliente_edit(self):
        try:
            if self.registered_cliente_path_edit == "":
                showerror("Error", "No hay directorio el cuál abrir.")
            else:
                print("try")
                print(self.registered_cliente_path_edit)
                subprocess.Popen(r'explorer /select,' + self.registered_cliente_path_edit)  # Abrir carpeta en escritorio
        except Exception:
            showerror("Error", "No hay directorio el cuál abrir.")


    # Search Clientes Formularios

    def populate_clientes_frame(self,clientesFrame, tab3):
        self.tree_clientes = ttk.Treeview(clientesFrame, selectmode="extended", show=["headings"],
                                          height=29, columns=("#1", "#2", "#3", "#4", "#5", "#6"))
        self.tree_clientes.grid(row=6, column=0, columnspan=2)

        self.tree_clientes.heading('#1', text='Nombre', anchor=CENTER)
        self.tree_clientes.column("#1", minwidth=30, width=150, stretch=NO)

        self.tree_clientes.heading('#2', text='Afijo', anchor=CENTER)
        self.tree_clientes.column("#2", minwidth=30, width=150, stretch=NO)

        self.tree_clientes.heading('#3', text='Direccion', anchor=CENTER)
        self.tree_clientes.column("#3", minwidth=30, width=150, stretch=NO)

        self.tree_clientes.heading('#4', text='Distrito', anchor=CENTER)
        self.tree_clientes.column("#4", minwidth=30, width=150, stretch=NO)

        self.tree_clientes.heading('#5', text='Telefono', anchor=CENTER)
        self.tree_clientes.column("#5", minwidth=30, width=150, stretch=NO)

        self.tree_clientes.heading('#6', text='DNI', anchor=CENTER)
        self.tree_clientes.column("#6", minwidth=30, width=150, stretch=NO)

        ttk.Button(clientesFrame, text='Eliminar',
                   command=lambda: self.delete_cliente_word(), width=150).grid(row=30, column=0, columnspan=2)

        # Filters Frame
        filter_frame = Frame(tab3, bg='white', width=200, height=screen_height-155)
        filter_frame.place(x=1110, y=30)

        filtroLabel = Label(filter_frame, text='Filtros:', font=('Lucida Sans', 11, 'bold'), bg='white',
                              fg='gray20', )
        filtroLabel.place(x=20, y=10)

        self.cliente_name_filter = IntVar()
        check_name = Checkbutton(filter_frame, text='Nombre cliente', variable=self.cliente_name_filter, onvalue=1,
                                  offvalue=0, font=('Lucida Sans', 10, 'bold'), bg='white')
        check_name.place(x=20, y=40)
        self.cliente_name_filter.set(1)

        self.cliente_afijo_filter = IntVar()
        check_af_cachorro = Checkbutton(filter_frame, text='Afijo cliente', variable=self.cliente_afijo_filter, onvalue=1,
                                  offvalue=0, font=('Lucida Sans', 10, 'bold'), bg='white')
        check_af_cachorro.place(x=20, y=65)

        self.cliente_direccion_filter = IntVar()
        self.check_af_prop = Checkbutton(filter_frame, text='Direccion', variable=self.cliente_direccion_filter, onvalue=1,
                                  offvalue=0, font=('Lucida Sans', 10, 'bold'), bg='white')
        self.check_af_prop.place(x=20, y=90)

        self.cliente_distrito_filter = IntVar()
        check_raza = Checkbutton(filter_frame, text='Distrito', variable=self.cliente_distrito_filter, onvalue=1,
                                  offvalue=0, font=('Lucida Sans', 10, 'bold'), bg='white')
        check_raza.place(x=20, y=115)

        self.cliente_telefono_filter = IntVar()
        check_raza = Checkbutton(filter_frame, text='Telefono', variable=self.cliente_telefono_filter, onvalue=1,
                                  offvalue=0, font=('Lucida Sans', 10, 'bold'), bg='white')
        check_raza.place(x=20, y=140)

        self.cliente_dni_filter = IntVar()
        check_raza = Checkbutton(filter_frame, text='DNI', variable=self.cliente_dni_filter, onvalue=1,
                                  offvalue=0, font=('Lucida Sans', 10, 'bold'), bg='white')
        check_raza.place(x=20, y=165)

        self.cliente_raza_filter = IntVar()
        check_raza = Checkbutton(filter_frame, text='Raza', variable=self.cliente_raza_filter, onvalue=1,
                                  offvalue=0, font=('Lucida Sans', 10, 'bold'), bg='white')
        check_raza.place(x=20, y=190)


        # Entrys
        self.entry_cliente_nombre_filter = EntryWithPlaceholder(filter_frame, "Nombre cliente")
        self.entry_cliente_nombre_filter.place(x=20, y=235, width=150)

        self.entry_cliente_afijo_filter = EntryWithPlaceholder(filter_frame, "Afijo cliente")
        self.entry_cliente_afijo_filter.place(x=20, y=260, width=150)

        self.entry_cliente_direccion_filter = EntryWithPlaceholder(filter_frame, "Direccion")
        self.entry_cliente_direccion_filter.place(x=20, y=285, width=150)

        self.entry_cliente_distrito_filter = EntryWithPlaceholder(filter_frame, "Distrito")
        self.entry_cliente_distrito_filter.place(x=20, y=310, width=150)

        self.entry_cliente_telefono_filter = EntryWithPlaceholder(filter_frame, "Telefono")
        self.entry_cliente_telefono_filter.place(x=20, y=335, width=150)

        self.entry_cliente_dni_filter = EntryWithPlaceholder(filter_frame, "DNI")
        self.entry_cliente_dni_filter.place(x=20, y=360, width=150)

        self.entry_cliente_raza_filter = EntryWithPlaceholder(filter_frame, "Raza")
        self.entry_cliente_raza_filter.place(x=20, y=385, width=150)

        ttk.Button(filter_frame, text='Buscar', command=self.get_filtered_clientes).place(x=0, y=555, width=200)
        ttk.Button(filter_frame, text='Limpiar filtros',
                   command=lambda: self.clean_cliente_filters(clientesFrame)).place(x=0, y=585, width=200)

    def get_filtered_clientes(self):

        if self.entry_cliente_nombre_filter.get() == "Nombre cliente" and \
                self.entry_cliente_afijo_filter.get() == "Afijo cliente" and \
                self.entry_cliente_direccion_filter.get() == "Direccion" and \
                self.entry_cliente_distrito_filter.get() == "Distrito" and \
                self.entry_cliente_telefono_filter.get() == "Telefono" and \
                self.entry_cliente_dni_filter.get() == "DNI" and \
                self.entry_cliente_raza_filter.get() == "Raza":
            showerror("Error", "Casillas de filtro vacías.")
            return

        records = self.tree_clientes.get_children()
        for element in records:
            self.tree_clientes.delete(element)

        # getting data

        dict_filters = {
            "propietario": self.cliente_name_filter.get(),
            "cliente_afijo": self.cliente_afijo_filter.get(),  # Afijo cachorro
            "direccion": self.cliente_direccion_filter.get(),
            "distrito": self.cliente_distrito_filter.get(),
            "telefono": self.cliente_telefono_filter.get(),
            "dni": self.cliente_dni_filter.get(),
            "raza": self.cliente_raza_filter.get()
        }

        filters_str = [self.entry_cliente_nombre_filter.get(), self.entry_cliente_afijo_filter.get(),
                       self.entry_cliente_direccion_filter.get(), self.entry_cliente_distrito_filter.get(),
                       self.entry_cliente_telefono_filter.get(), self.entry_cliente_dni_filter.get(),
                       self.entry_cliente_raza_filter.get()]

        #        data = db.get("pedigrees")
        data = db.get_data_clientes_filters("clientes", dict_filters, filters_str)

        if len(data) == 0:
            showerror("Error", "No se encontraron coincidencias.")
        else:
            # filling data
            for row in data:
                cliente_name = row[0]
                cliente_afijo = row[1]
                direccion = row[2]
                distrito = row[3]
                telefono = row[4]
                dni = row[5]

                self.tree_clientes.insert('', 0, text=cliente_name,
                                 values=(cliente_name, cliente_afijo, direccion, distrito, telefono, dni))

    def clean_cliente_filters(self, clientesFrame):
        self.cliente_name_filter.set(1)
        self.cliente_afijo_filter.set(0)
        self.cliente_direccion_filter.set(0)
        self.cliente_distrito_filter.set(0)
        self.cliente_telefono_filter.set(0)
        self.cliente_dni_filter.set(0)
        self.cliente_raza_filter.set(0)

        self.entry_cliente_nombre_filter.delete(0, END)
        self.entry_cliente_afijo_filter.delete(0, END)
        self.entry_cliente_direccion_filter.delete(0, END)
        self.entry_cliente_distrito_filter.delete(0, END)
        self.entry_cliente_telefono_filter.delete(0, END)
        self.entry_cliente_dni_filter.delete(0, END)
        self.entry_cliente_raza_filter.delete(0, END)

        self.entry_cliente_nombre_filter.focus()
        self.entry_cliente_afijo_filter.focus()
        self.entry_cliente_direccion_filter.focus()
        self.entry_cliente_distrito_filter.focus()
        self.entry_cliente_telefono_filter.focus()
        self.entry_cliente_dni_filter.focus()
        self.entry_cliente_raza_filter.focus()

        clientesFrame.focus()
        clientesFrame.focus_force()

    def delete_cliente_word(self):
        try:
            self.tree_clientes.item(self.tree_clientes.selection())['values'][0]
        except IndexError as e:
            showerror("Error", "Selecciona el cliente a eliminar.")
            return
        result = askquestion("Confirmación", "Deseas eliminar el cliente?")
        if result == "yes":
            try:
                wordHelper = CreateWordHelper()

                home = expanduser("~")
                main_app_path = home + "\\Registros Pedigree App"
                clientes_app_path = main_app_path + "\\Afijos"

                cliente_name = self.tree_clientes.item(self.tree_clientes.selection())['values'][0]
                cliente_afijo = self.tree_clientes.item(self.tree_clientes.selection())['values'][1]

                carpeta_name = cliente_name.upper() + " - " + cliente_afijo.replace('/', '')
                path_file = clientes_app_path + f'\\{carpeta_name}'

                wordHelper.deleteFile(path_file)

                cliente_data = db.get_single_element_data("clientes", "cliente_afijo", cliente_afijo)
                is_auto_cliente = cliente_data[0]["auto_cliente"]
                if is_auto_cliente == "si":
                    # Se disminuye de app_data var
                    data = db.get("app_data")
                    fecha = datetime.datetime.today().date().strftime("%d/%m/%Y")
                    cant_afijos = data[0]["cant_afijos_hoy"]
                    db.update_app_data_afijos(str(int(cant_afijos) - 1), fecha)

                afijo_cliente = self.tree_clientes.item(self.tree_clientes.selection())['values'][1]
                result = db.delete_data("clientes", "cliente_afijo", afijo_cliente)

                # if cliente es auto se quita uno a auto value app_data var

                if result:
                    showinfo("Info", "Registro eliminado exitosamente.")
                    self.get_filtered_clientes()
                else:
                    showerror("Error", "Error al eliminar el registro.")
            except Exception as e:
                showerror("Error", "Error al eliminar el cliente.")
                print(e)


if __name__ == '__main__':
    root = Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    full_screen = str(screen_width) + "x" + str(screen_height)
    root.geometry(full_screen)
    root.title('Inicio')
    root.protocol("WM_DELETE_WINDOW", _ask_before_close)
    root.resizable(False, True)

    login_frame = Frame(root)
    register_frame = Frame(root)
    pedigree_operation_frame = ScrolledWindow(root)
    f4 = Frame(root)

    photo = PhotoImage(file='abci_bg1.png')
    userimage = PhotoImage(file='user.png')
    loginimage = PhotoImage(file='login.png')
    openfolderimage = PhotoImage(file='openfolder.png')
    button = PhotoImage(file='button.png')
    passwordimage = PhotoImage(file='pass.png')
    bn_bg_abc = PhotoImage(file='abci_bgbn.png')

    user_name = ""
    user_mail = ""

    db = WorkspaceData()

    for frame in (LoginFrame(root), register_frame, pedigree_operation_frame, f4):
        frame.grid(row=0, column=0, sticky='news')

    # Button(login_frame, text='Go to frame 2', command=lambda:raise_frame(register_frame)).pack()
    # Label(login_frame, text='FRAME 1').pack()
    #
    # Label(register_frame, text='FRAME 2').pack()
    # Button(register_frame, text='Go to frame 3', command=lambda:raise_frame(pedigree_operation_frame)).pack()
    #
    # Label(pedigree_operation_frame, text='FRAME 3').pack(side='left')
    # Button(pedigree_operation_frame, text='Go to frame 4', command=lambda:raise_frame(f4)).pack(side='left')
    #
    # Label(f4, text='FRAME 4').pack()
    # Button(f4, text='Goto to frame 1', command=lambda:raise_frame(login_frame)).pack()

    raise_frame(login_frame)
    root.mainloop()