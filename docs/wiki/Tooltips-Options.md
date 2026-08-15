# Tooltips Options

> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/Tooltips_Options>
> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.

This page lists the tooltips for every option in the options menu, taken directly from the game's current string files. See also <a href="Tooltips_Buttons" class="wikilink" title="Tooltips Buttons">Tooltips Buttons</a>.

## Graphics

### `Graphics`

Affects various render pipeline settings like shadows, ambient occlusion and bloom.

### `VFX Limit`

Limits the number of visual effects that can be played per second.

### `Frames`

Limit the game's fps. Vsync syncs the fps to your monitor's refresh rate.

### `Resolution`

Change the screen resolution.

### `Code Highlights`

Turn off the flashing highlights when the code is running.

### `Increment Number Effect`

Disable the effects in the inventory that play when the numbers change.

### `Color Theme`

Change the color theme of the UI. Custom themes can be added in the "Themes" folder in the save directory.

### `UI Size`

Change the size of UI elements.

### `Viewport Sliding`

Disables the sliding of the viewport when you drag and release.

## Audio

### `Volume`

Adjust the volume of all audio.

### `Music Volume`

Adjust the volume of the music.

### `Drone Volume`

Adjust the volume of the drone buzzing sounds.

### `SFX Volume`

Adjust the volume of sound effects from the farm.

### `UI Volume`

Adjust the volume of UI sounds like button clicks.

### `Ambience Volume`

Adjust the volume of ambient sounds like wind and birds.

### `Volume Damping`

The volume is multiplied by this factor for every sound effect playing concurrently so your ears don't explode at high drone speeds.

### `SFX Limit`

Limits the number of sounds that can be played per second.

## General

### `Autosave`

Automatically saves the code every 30s when enabled. Can't be enabled while file watcher is enabled.

### `Autosave Progress`

Automatically saves the game progress every 30s when enabled.

### `File Watcher`

Automatically applies changes made to the code files in the save folder allowing the use of an external code editor. Can't be enabled while autosaves are enabled.

### `Tabs to Spaces`

Turns all tabs into 4 spaces.

### `Language`

Change the language of the game.

### `Print Warnings`

Activates warnings and the warning icon that sometimes appears.

## Safeguards

### `Error: Forgot Call`

When enabled, the game will throw a safeguard error if you try to evaluate the truthiness of a function object, because this usually means that you forgot the `()`.

### `Error: Shadow`

When enabled, the game will throw a safeguard error if there is a local variable that has the same name as a global variable.

### `Allow Locked Features`

When enabled, locked features can be used even if they haven't been unlocked yet. This is not the intended way of playing.

## Footnotes
