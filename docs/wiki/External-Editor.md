# External Editor

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/External_Editor>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.
> Also known as: External editor.

The in-game text editor is usually sufficient to play this game, but of course it cannot compete with more sophisticated text editors like Visual Studio Code.

The game saves all code files as .py files, so you can edit them with Python editors. Note that this is for convenience only. The in-game language isn't actually Python, but it's close enough that Python IntelliSense works decently on it. You can access the save folder using the "Open Folder" button in the "Load" menu.

Each save also contains a `__builtins__.py` file, which contains built-in Python definitions that match the in-game builtins to enable IntelliSense. The game will ignore pythons import statements, so you can add them to help your external editor pick up on function definitions from other files.

To see external changes in-game without having to reload the save, you must enable the File Watcher option. If you create or delete files externally, you will still need to reload the save to see them.
