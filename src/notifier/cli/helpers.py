import argparse


class ConfigKV(argparse.Action):

    @staticmethod
    def auto_cast(v: str):
        if v.lower() in ("true", "false"): return v.lower() == "true"

        try: return int(v)
        except ValueError: pass

        try: return float(v)
        except ValueError: pass

        return v

    def __call__(self, parser, namespace, value, option_string=None):
        if "=" not in value: parser.error(f"{option_string}: expected KEY=VALUE")
        k, v = value.split("=", 1)
        d = getattr(namespace, self.dest, {}) or {}
        d[k] = self.auto_cast(v)
        setattr(namespace, self.dest, d)

