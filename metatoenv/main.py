import yaml
import argparse

parser = argparse.ArgumentParser(
    description=
    'Generate a conda environment file from a conda recipe meta.yaml file')
parser.add_argument('--meta-file', default='meta.yaml')
parser.add_argument('--config-file', default='conda_build_config.yaml')
parser.add_argument('--env-file', default='environment.yml')
parser.add_argument('--env-name', '--name', default='myenv')
parser.add_argument('--channels', default='conda-forge')
parser.add_argument('--platform', '--os', default='linux64')


def main(metafile, configfile, envfile, envname, channels, platform):
    with open(configfile, "r") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    with open(metafile, "r") as f:
        asstring = f.read()

    for key, value in config.items():
        asstring = asstring.replace("{{{{ {} }}}}".format(key),
                                    "= {}".format(value[0]))
    asstring = asstring.replace("{{", "")
    asstring = asstring.replace("}}", "")
    content = yaml.safe_load(asstring)

    # Create dependencies
    all_dependencies = []
    for r in content["requirements"].values():
        all_dependencies += r
    all_dependencies += content["test"]["requires"]

    # Filter out deps for selected OS
    dependencies = []
    for dep in all_dependencies:
        ok = True
        if dep.endswith(']'):
            left = dep.rfind('[')
            if left == -1:
                raise RuntimeError(
                    "Unmatched square bracket in preprocessing selector")
            selector = dep[left:]
            if selector.startswith('[not'):
                if (platform in selector) or (selector.replace(
                        '[not', '')[:-1].strip() in platform):
                    ok = False
            else:
                if (platform not in selector) and (selector[1:-1]
                                                   not in platform):
                    ok = False
            if ok:
                dep = dep.replace(selector, '').strip()
        if ok and (dep not in dependencies):
            dependencies.append(dep)

    output = {
        "name": envname,
        "channels": channels,
        "dependencies": dependencies
    }

    with open(envfile, "w") as out:
        yaml.dump(output, out, default_flow_style=False)


if __name__ == '__main__':
    args = parser.parse_args()

    channels = [args.channels]
    for delimiter in ":,":
        if delimiter in args.channels:
            channels = args.channels.split(delimiter)

    main(metafile=args.meta_file,
         configfile=args.config_file,
         envfile=args.env_file,
         envname=args.env_name,
         channels=channels,
         platform=args.platform)
