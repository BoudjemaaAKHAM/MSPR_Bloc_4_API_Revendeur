def get_version_from_init():
    with open("revendeurapi/__init__.py") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.strip().split("=")[-1].strip(" '\"")


version = get_version_from_init()
print(f'"version"={version}')
