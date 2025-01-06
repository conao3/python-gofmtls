# gofmtls

## Usage

### Run server

```bash
$ pdm install
$ pdm run gofmtls -p 15329
```

### Connect from Editors (Emacs - Eglot)

1. Add advice
```elisp
(leaf eglot
  :preface
  (defun my/advice--track-changes-fetch (fn &rest args)
    (when (car args)
      (apply fn args)))
  :advice
  (:around track-changes-fetch my/advice--track-changes-fetch))
```

2. Open `sample/main.go`.

3. Run eglot via `M-x eglot`

  Then, input `localhost:15329`.

4. Run `format` command.

```elisp
(with-current-buffer "main.go"
  (let ((server (car (gethash (eglot--current-project)
                              eglot--servers-by-project))))
    (eglot-execute server `(:command "format" :arguments [,buffer-file-name]))))
```
