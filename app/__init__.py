import coloredlogs

coloredlogs.install(
    level='INFO',
    fmt='%(asctime)s [%(levelname)s] %(message)s',
    # fmt='%(host)s - - [%(asctime)s] %(message)s',
    field_styles={
        'asctime': {
            'color': 'black',
            'faint': True,
            'background': 'white'
        },
        'levelname': {
            'bold': True,
            'color': 'white',
            'bright': True
        },
        'message': {
            'color': 'white',
            'bright': True
        }
    }
)