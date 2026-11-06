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
│   ├── fases_suelo.py
│   ├── shear_strength.py
│   ├── atterberg.py
│   ├── slope_core.py
│   ├── alerta_umbral.py
│   ├── nivelacion.py
│   └── curva_circular.py
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
| Resistencia al corte (c, φ desde corte directo o triaxial) | `python/shear_strength.py` | [/es/foundations/shear-strength](https://insarwatch.com/es/foundations/shear-strength) |
| Límites de Atterberg (LL, IP, IL desde la curva de fluencia) | `python/atterberg.py` | [/es/foundations/atterberg-limits](https://insarwatch.com/es/foundations/atterberg-limits) |
| Estabilidad de taludes (Fellenius / Bishop / Spencer) | `python/slope_core.py` | [/es/taludes/slip-surface](https://insarwatch.com/es/taludes/slip-surface) |
| Alerta InSAR por umbrales (verde / amarillo / rojo) | `python/alerta_umbral.py` | [/es/insar/alerta-umbral](https://insarwatch.com/es/insar/alerta-umbral) |
| Cierre y compensación de nivelación | `python/nivelacion.py` | [/es/medicion/cierre-nivelacion](https://insarwatch.com/es/medicion/cierre-nivelacion) |
| Curva circular simple y replanteo por deflexiones | `python/curva_circular.py` | [/es/medicion/curva-circular](https://insarwatch.com/es/medicion/curva-circular) |

## Licencia

MIT. Úselo libremente; cite la fuente si lo publica.
