import importlib
from config.config import Config


def get_parser(file_type):

    parsers = Config.PARSERS

    if file_type not in parsers:
        raise Exception(f"No parser configured for type: {file_type}")

    parser_path = parsers[file_type]

    module_path, function_name = parser_path.rsplit(".", 1)

    module = importlib.import_module(module_path)

    parser_function = getattr(module, function_name)

    return parser_function