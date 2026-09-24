# JUDAS · Miranda de Ebro

Web estática, sin dependencias ni compilación obligatoria. Abre `index.html` para verla.

## Estructura

```
index.html  historia.html  musicos.html  fotos.html  videos.html
conciertos.html  prensa.html  archivo.html  50-aniversario.html
css/style.css        estilos, con las variables de color al principio
js/site.js           menú en móvil y marca de la página actual
build.py             generador de las páginas (cabecera, menú y pie)
logo.png             logo limpio, usado en la web
logo-original.png    logo tal como se entregó, con la marca de agua
```

## Cómo cambiar cosas

- **Colores, tipos y espacios**: bloque `:root` de `css/style.css`.
- **Menú, pie o etiquetas de todas las páginas**: `build.py`, y después `python3 build.py`.
- **Texto de una sola página**: puedes editar el HTML directamente, pero si luego
  ejecutas `build.py` se sobrescribirá. Lo seguro es cambiar el texto en `build.py`.
- **Dominio**: pon la dirección en `BASE_URL` dentro de `build.py` para que las
  etiquetas Open Graph y `canonical` apunten a la web publicada.

## Paleta

| Uso | Color |
|---|---|
| Fondo | `#0a0a0a` |
| Paneles | `#141414` |
| Texto | `#f4f4f4` |
| Texto secundario | `#9d9d9d` |
| Líneas | `#2e2e2e` |
| Acento | `#ffffff` |

El tema es blanco y negro: el único color de la web es el verde menta del propio logo.

## Fuentes documentales

- Ayuntamiento de Miranda de Ebro: León de Oro a JUDAS (29/01/2025)
- La de Miranda TV: crónica del León de Oro (25/02/2025)
- El Correo: reseña del concierto del Teatro Apolo (10/06/2017)

Las tipografías (Anton y Archivo) se cargan desde Google Fonts. Si prefieres una web
sin peticiones externas, descarga los `.woff2`, colócalos en `fonts/` y sustituye el
`<link>` de la plantilla por una regla `@font-face`.
