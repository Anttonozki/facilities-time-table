"""
Convierte un DXF (exportado desde el DWG con ODA File Converter) en un SVG
simplificado: fondo blanco, trazos negros, pensado para un visor web interactivo.

Uso:
    python dxf_to_svg.py Plano.dxf Plano.svg
    python dxf_to_svg.py Plano.dxf Plano.svg --list-layers   (para ver qué capas existen)
    python dxf_to_svg.py Plano.dxf Plano.svg --layers MUROS,A-WALL,PAREDES

Si no se pasa --layers, exporta TODAS las entidades geométricas visibles
(líneas, polilíneas, círculos, arcos) ignorando texto/cotas/punteados de
referencia, para dar un primer vistazo del plano completo.
"""

import argparse
import sys

import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.svg import SVGBackend
from ezdxf.addons.drawing.config import Configuration, ColorPolicy, BackgroundPolicy, HatchPolicy
from ezdxf.addons.drawing.layout import Page, Units


def list_layers(doc):
    print("Capas encontradas en el DXF:")
    for layer in doc.layers:
        print(f"  - {layer.dxf.name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dxf")
    parser.add_argument("output_svg")
    parser.add_argument("--layers", help="Lista de capas a incluir, separadas por coma")
    parser.add_argument("--list-layers", action="store_true")
    args = parser.parse_args()

    try:
        doc = ezdxf.readfile(args.input_dxf)
    except IOError:
        print(f"No se pudo abrir {args.input_dxf}", file=sys.stderr)
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print("Archivo DXF invalido o corrupto.", file=sys.stderr)
        sys.exit(1)

    if args.list_layers:
        list_layers(doc)
        return

    msp = doc.modelspace()

    if args.layers:
        wanted = {name.strip().upper() for name in args.layers.split(",")}
        for e in list(msp):
            if e.dxf.layer.upper() not in wanted:
                msp.delete_entity(e)

    config = Configuration(
        color_policy=ColorPolicy.BLACK,
        background_policy=BackgroundPolicy.WHITE,
        hatch_policy=HatchPolicy.IGNORE,
    )

    doc.layers.get("0").off = False
    context = RenderContext(doc)
    backend = SVGBackend()
    frontend = Frontend(context, backend, config=config)
    frontend.draw_layout(msp, finalize=True)

    page = Page(0, 0, units=Units.mm)  # 0,0 = auto-ajustar al contenido
    svg_string = backend.get_string(page=page)
    with open(args.output_svg, "w", encoding="utf-8") as f:
        f.write(svg_string)

    print(f"SVG generado: {args.output_svg}")


if __name__ == "__main__":
    main()
