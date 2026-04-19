# nemo-sushi-preview

Adds GNOME Sushi file preview to the Nemo file manager via:

- **Spacebar** — preview the selected file
- **Right-click → Preview con Sushi** — context menu action

## Requirements

- `nemo`
- `nemo-python`
- `gnome-sushi`

## Install from .deb

```bash
make
sudo dpkg -i nemo-sushi-preview_1.0_all.deb
nemo -q && nemo
```

## Manual install

```bash
sudo cp src/extensions/sushi-space.py    /usr/share/nemo-python/extensions/
sudo cp src/actions/sushi.nemo_action    /usr/share/nemo/actions/
nemo -q && nemo
```

## Uninstall

```bash
make uninstall
# or
sudo dpkg -r nemo-sushi-preview
```

## How it works

The Python extension (`sushi-space.py`) registers as a `Nemo.LocationWidgetProvider`
so it connects to every Nemo window on navigation. When space is pressed it reads
the current selection via the ATK accessibility interface
(`NemoIconContainerAccessible`) and passes the file path to `/usr/bin/sushi`.
