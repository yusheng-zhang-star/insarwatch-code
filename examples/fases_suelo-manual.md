# Verificación manual — Relaciones volumétricas del suelo

Datos de un certificado de laboratorio (arcilla de la Ciudad de México):

| Magnitud | Valor |
|---|---|
| Gravedad específica Gs | 2,70 |
| Peso específico natural γ | 18 kN/m³ |
| Humedad w | 15 % |

## Paso 1 — Índice de vacíos e

A partir de la relación de pesos γ = Gs·γw·(1+w)/(1+e), despejando e:

```
e = Gs·γw·(1+w)/γ − 1
  = 2,70 × 9,81 × 1,15 / 18 − 1
  = 30,46 / 18 − 1
  = 0,692
```

## Paso 2 — Porosidad n

```
n = e/(1+e) = 0,692 / 1,692 = 0,409  →  40,9 %
```

## Paso 3 — Saturación S

```
S = w·Gs/e = 0,15 × 2,70 / 0,692 = 0,585  →  58,5 %
```

## Paso 4 — Pesos específicos derivados

```
γd   = γ/(1+w) = 18/1,15 = 15,65 kN/m³
γsat = (Gs+e)·γw/(1+e) = 3,392 × 9,81 / 1,692 = 19,67 kN/m³
γ′   = γsat − γw = 19,67 − 9,81 = 9,86 kN/m³
```

## Resultado

| Magnitud | Valor |
|---|---|
| e | 0,692 |
| n | 40,9 % |
| S | 58,5 % |
| γd | 15,65 kN/m³ |
| γsat | 19,67 kN/m³ |
| γ′ | 9,86 kN/m³ |

Estos valores deben coincidir con los que entrega el calculador en línea
[insarwatch.com/es/foundations/fases-suelo](https://insarwatch.com/es/foundations/fases-suelo)
y con la salida de `python/fases_suelo.py`.
