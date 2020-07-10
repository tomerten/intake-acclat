intake-acclat
=============

This plugin allows to create catalogs of accelerator lattice files using an [intake-server](https://github.com/intake/intake). 

The restriction is that the urlpath in the catalog yaml file is the file base for all the extensions that can be loaded from the catalog, in other words all files belonging to the same lattice start the same and only differ in file-extension). A possible file structure would be soemthing like:


```bash
catalogdir/fodo.json
catalogdir/fodo.madx
catalogdir/fodo.lte
catalogdir/fodo.twiss
catalogdir/fodo2.json
catalogdir/fodo2.madx
catalogdir/fodo2.lte
catalogdir/fodo2.twiss
```

with a corresponding catalog yaml file:

```yaml
plugins:
  source:
    - module: intake_acclat
sources:
  fodo:
    driver: acclatsource
    args:
      urlpath: 'catalogdir/fodo'
    metadata:
      plots:
        beta:
          x: S
          y: [BETX,BETY,DX]
        phase:
          x: S
          y: [MUX, MUY]
  fodo2:
    driver: acclatsource
    args:
      urlpath: 'catalogdir/fodo2'
    metadata:
      plots:
        beta:
          x: S
          y: [BETX,BETY,DX]
        phase:
          x: S
          y: [MUX, MUY]

```


Currently implemented formats are:
- madx
- elegant (lte)
- json ([latticejson](https://github.com/nobeam/latticejson.git)
- twiss output from madx


