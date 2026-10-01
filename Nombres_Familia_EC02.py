import clr

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FamilyInstance

# Elementos recibidos desde All Elements of Category.
elementos = UnwrapElement(IN[0])

# Registrar cada familia una sola vez.
familias = {}

for elemento in elementos:
    if isinstance(elemento, FamilyInstance):
        familia = elemento.Symbol.Family
        id_familia = str(familia.Id.Value)

        if id_familia not in familias:
            familias[id_familia] = familia

# Encabezados del reporte.
reporte = [[
    "Id familia",
    "Categoria",
    "Nombre actual",
    "Nombre propuesto",
    "Estado"
]]

# Revisar las familias ordenadas por nombre.
for familia in sorted(
    familias.values(),
    key=lambda f: f.Name.lower()
):
    nombre = familia.Name
    tiene_espacios = " " in nombre

    nombre_propuesto = nombre.replace(" ", "_")
    estado = "NO CUMPLE" if tiene_espacios else "CUMPLE"

    categoria = familia.FamilyCategory
    nombre_categoria = (
        categoria.Name if categoria is not None
        else "Sin categoria"
    )

    reporte.append([
        str(familia.Id.Value),
        nombre_categoria,
        nombre,
        nombre_propuesto,
        estado
    ])

OUT = reporte