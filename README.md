# Planos Colegio — Sistema de Reservas de Espacios

Aplicación web (Python) para que los usuarios reserven horarios de uso de
espacios del colegio (canchas de fútbol, salones, salas de reuniones),
mostrando un plano interactivo simplificado (blanco y negro, solo paredes)
en lugar del DWG original.

## Estado actual

- `Plano.dwg`: plano original en AutoCAD, contiene toda la distribución de
  espacios del colegio.
- `dxf_to_svg.py`: script en Python que convierte un DXF a un SVG limpio
  (fondo blanco, trazos negros), con opción de filtrar por capas
  (ej. solo muros/paredes) para quedarse solo con los contornos.

## Por qué no se usa el DWG directamente en la web

DWG es un formato propietario y pesado de renderizar en navegador (requiere
librerías tipo Autodesk Forge/APS). En su lugar:

1. Se convierte el DWG a **DXF** (formato abierto) o directo a SVG con una
   herramienta externa.
2. Se limpia el dibujo dejando solo paredes/contornos (sin cotas, texto
   técnico, instalaciones, etc.).
3. El resultado es un **SVG interactivo**: cada espacio reservable es un
   `<path>`/`<g>` con un `id` (ej. `id="cancha-futbol-1"`), que desde
   JavaScript se puede resaltar al pasar el mouse, mostrar su nombre, y
   al hacer clic abrir el formulario de reserva.

## Pasos pendientes (conversión DWG → DXF)

Opciones evaluadas para convertir `Plano.dwg` a DXF:

- **ODA File Converter** (gratis, oficial de Open Design Alliance) —
  https://www.opendesign.com/guestfiles/oda_file_converter
- **DWG TrueView** (gratis, de Autodesk) — más simple de usar, convierte
  DWG a DXF.
- **LibreCAD** / **QCAD** (gratis, open source) — abren DWG y exportan
  directo a SVG o DXF desde su interfaz.
- **online-convert.com** — conversor online. Funciona, pero implica subir
  el archivo a un servidor de terceros; usar solo si el plano no tiene
  información sensible. Conviene exportar a **DXF** (no SVG directo) para
  poder filtrar capas después con `dxf_to_svg.py`.

**Recomendación:** convertir a DXF (no SVG directo desde el conversor
online), así se mantiene control por capas usando el script de este repo.

## Cómo usar `dxf_to_svg.py`

Una vez que tengas `Plano.dxf` en esta carpeta:

```bash
# 1. Ver qué capas tiene el dibujo
python dxf_to_svg.py Plano.dxf Plano.svg --list-layers

# 2. Generar el SVG filtrando solo la(s) capa(s) de muros
python dxf_to_svg.py Plano.dxf Plano.svg --layers MUROS,A-WALL,PAREDES

# 3. (opcional) generar el SVG completo sin filtrar, para un primer vistazo
python dxf_to_svg.py Plano.dxf Plano.svg
```

Requiere `ezdxf`, `svgwrite` y `pillow` (ya instalados en este entorno):

```bash
pip install ezdxf svgwrite pillow
```

## Próximos pasos sugeridos

1. Convertir `Plano.dwg` → `Plano.dxf` (usuario, con alguna de las
   herramientas de arriba).
2. Correr `dxf_to_svg.py --list-layers` para identificar la capa de muros.
3. Generar el SVG filtrado y revisarlo (agrupar/etiquetar cada espacio con
   un `id` legible: `cancha-futbol-1`, `salon-201`, `sala-reuniones-a`).
4. Armar el backend (Flask o FastAPI) con modelos `espacios`, `reservas`,
   `horarios`, y la lógica de disponibilidad (evitar solapamientos).
5. Embeber el SVG en el frontend y conectar cada espacio clickeable con el
   formulario/calendario de reserva, consultando el backend.

## Stack sugerido

- **Backend:** Flask o FastAPI + SQLite (o Postgres si escala).
- **Frontend:** SVG embebido + JavaScript vanilla para la interactividad
  (hover, click, tooltip) — no se necesita un framework pesado para el
  plano en sí.
