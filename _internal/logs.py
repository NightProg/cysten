import click


def info(msg):
    click.secho(f"[INFO] {msg}", fg="blue")

def error(msg):
    click.secho(f"[ERROR] {msg}", fg="red")

def success(msg):
    click.secho(f"[SUCCESS] {msg}", fg="green")

