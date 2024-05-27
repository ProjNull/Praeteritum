# Conventions

## SQLAlchemy

Model classes should be named in PascalCase, tables and columns in snake_case.
Functions and other variables will use snake_case.

## Modules

All files and folders are named in lowercase using snake_case.  
If you end up with a file like `script.py` inside a module with the same name: `script`, you should rename `script.py` to `__init__.py`. If this is not viable, instead rename the file.

This is because something like _this_ feels wrong:

```py
import my_func from script.script
```

## Frontend

All components are to be named in PascalCase: `MyComponent.tsx`

Static resources should use lower case, except for when they're scoped to components, ie.: `App.module.css`
