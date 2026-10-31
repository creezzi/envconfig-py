# envconfig

Load typed, validated configuration from environment variables and report every problem at once.

## Usage

```python
from envconfig import load, Var

cfg = load({
    "PORT": Var(int, default=8080),
    "DEBUG": Var(bool, default=False),
    "HOSTS": Var(list, default=[]),
    "DATABASE_URL": Var(str),  # required
})
```

## Test

```bash
pip install pytest && pytest
```

## License

MIT
