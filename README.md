# own_game
Кликер-кнопка для «Своей игры»

### Как собрать
- Из консоли запускается `auto-py-to-exe`
- Выставляются режимы «One File» и «Window based»
- **ВНИМАНИЕ, ВАЖНО:** файл звука `beep.mp3` должен быть добавлен через Additional files (просто выбираем файл, более ничего не указываем)

```shell
pyinstaller --noconfirm --onefile --windowed --add-data "Z:\Python\Projects\own_game\media\beep.mp3;."  "Z:\Python\Projects\own_game\server.py"
```
