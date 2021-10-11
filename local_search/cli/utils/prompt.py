import click
from local_search.cli.utils.console import console


def get_or_prompt_if_not_exists_or_invalid(options, option_key: str, option_config=None) -> str:
    """
    Prompts for :param option_key: if it doesn't exists in options or if it is invalid.
    """
    option_config = option_config or {}
    if options.setdefault(option_key, None) is None:
        get_or_prompt(options, option_key, option_config)
    if option_config.setdefault('type', False):
        if isinstance(option_config['type'], click.Choice) and options[option_key] not in option_config['type'].choices:
            console.print(
                f"Value {options[option_key]} is invalid for for option {option_key} in this context.")
            get_or_prompt(options, option_key, option_config)
    return options[option_key]


def get_or_prompt(options, option_key: str, option_config=None):
    prompt = f'Select {option_key.replace("_", " ")}'
    option_config = option_config or {}
    options[option_key] = click.prompt(prompt,
                                       type=option_config.setdefault(
                                           'type', None),
                                       default=option_config.setdefault(
                                           'default', None)
                                       )
    return options[option_key]
