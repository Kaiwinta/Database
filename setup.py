from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Outils Base to Graphe",
    version = "1.2",
    description = "Votre programme",
    executables = [Executable("essai3.py", base="Win32GUI",targetName="Graphe Titouan")],
    options={
        "build_exe": {
            "includes": ["PIL.Image","PIL.ImageTk"],
            'include_files': ['grv2.ico','gv3.png','no_image.png',"image2test.png"],
            "packages": [ "tkinter"],
            "optimize":1,
        }}
)