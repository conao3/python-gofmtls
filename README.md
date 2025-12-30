# gofmtls

A lightweight Language Server that provides Go formatting via `go fmt`.

## Overview

gofmtls is a simple LSP server written in Python that exposes Go's `go fmt` command through the Language Server Protocol. It enables editor integration for formatting Go source files without requiring a full-featured Go language server.

## Features

- Minimal LSP implementation focused on formatting
- TCP server mode for network-based editor connections
- Execute command support for `format` operation

## Requirements

- Python 3.13 or later
- Go toolchain (for `go fmt`)
- PDM package manager

## Installation

```bash
pdm install
```

## Usage

Start the server on a specified port:

```bash
pdm run gofmtls -p 15329
```

## Editor Integration

### Emacs with Eglot

1. Add the following advice to handle edge cases:

```elisp
(leaf eglot
  :preface
  (defun my/advice--track-changes-fetch (fn &rest args)
    (when (car args)
      (apply fn args)))
  :advice
  (:around track-changes-fetch my/advice--track-changes-fetch))
```

2. Open a Go file (e.g., `sample/main.go`)

3. Start Eglot with `M-x eglot` and connect to `localhost:15329`

4. Execute the format command:

```elisp
(with-current-buffer "main.go"
  (let ((server (car (gethash (eglot--current-project)
                              eglot--servers-by-project))))
    (eglot-execute server `(:command "format" :arguments [,buffer-file-name]))))
```

## License

Apache-2.0
