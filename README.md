# Ranking Evolution Bot

¡Bienvenido a Ranking Evolution Bot! Este es un bot de Discord que te ayuda a mantener un registro de los rankings de los jugadores en tu servidor. Puedes obtener información actualizada sobre la clasificación, recibir notificaciones sobre cambios en el ranking y más.

## Características

- Muestra información detallada sobre el ranking de jugadores en un formato fácil de leer.
- Detecta automáticamente cambios en el ranking y envía notificaciones a un canal específico.
- Permite personalizar el intervalo de tiempo para actualizaciones automáticas.
- **¡Más características increíbles que ofrece tu bot!**

## Instalación

1. Clona este repositorio en tu máquina local: `git clone https://github.com/termitaklk/Ranking-bot.git`
2. Navega al directorio del repositorio: `cd turepositorio`
3. Instala las dependencias requeridas: `pip install -r requirements.txt`
4. Crea un archivo `.env` basado en `.env.example` y configura las variables según tus necesidades.

## Uso

1. Asegúrate de que el bot tenga acceso al servidor de Discord donde deseas utilizarlo.
2. Ejecuta el bot utilizando `python Bot.py`.
3. Invoca los comandos del bot en Discord siguiendo el prefijo definido (por defecto es `!`).

## Configuración

- Abre el archivo `.env` y configura las siguientes variables:
  - `TOKEN`: Tu token de bot de Discord.
  - `URL`: La URL para obtener los datos del ranking.
  - `CANAL_ID`: El ID del canal donde se enviarán las actualizaciones del ranking.
  - `CANAL_ID_NOT`: El ID del canal para notificaciones de cambios importantes.
  - `TIME_EJECUCION`: El intervalo de tiempo en minutos para ejecutar actualizaciones automáticas.

## Contribución

¡Tu contribución es bienvenida! Si deseas contribuir a este proyecto, sigue estos pasos:
1. Realiza un fork de este repositorio.
2. Crea una rama para tu función/fix: `git checkout -b mi-funcion-genial`
3. Haz tus cambios y realiza commits: `git commit -am 'Añade una función genial'`
4. Envía tus cambios: `git push origin mi-funcion-genial`
5. Abre una solicitud de extracción en GitHub.

## Créditos

Este bot ha sido desarrollado por [Juan M.](https://github.com/termitaklk).

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para obtener más detalles.

