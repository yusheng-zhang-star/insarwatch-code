# insarwatch-code

Código fuente (Python + JavaScript) de los calculadores de ingeniería
geotécnica, topográfica y de monitoreo InSAR de
[insarwatch.com](https://insarwatch.com).

Cada calculador en línea ejecuta un módulo JavaScript; este repositorio
ofrece la **versión Python equivalente**, para que estudiantes y
profesionales puedan copiar el cálculo a sus propios scripts o verificar
los resultados a mano.

## Estructura

```
insarwatch-code/
├── python/          # Versión Python (biblioteca estándar, sin dependencias)
│   └── fases_suelo.py
├── javascript/      # Módulos JS (espejo de los que corren en el sitio)
├── examples/        # Verificación manual paso a paso
│   └── fases_suelo-manual.md
└── README.md
```

## Uso

```bash
python python/fases_suelo.py
```

Cada archivo imprime un ejemplo con su verificación manual; el resultado
debe coincidir con el calculador en línea con un error < 0,1 %.

## Calculadores disponibles

| Función | Python | Calculador en línea |
|---|---|---|
| Relaciones volumétricas (γ, w, Gs, e, n, S) | `python/fases_suelo.py` | [/es/foundations/fases-suelo](https://insarwatch.com/es/foundations/fases-suelo) |

*(Se irán agregando los demás módulos: resistencia al corte, límites de
Atterberg, cierre de nivelación, curva circular, alerta InSAR…)*

## Licencia

MIT. Úselo libremente; cite la fuente si lo publica.
