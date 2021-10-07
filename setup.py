from setuptools import setup

setup(
    name='Local search',
    version='1.0.0',
    install_requires=[
        'numpy',
        'rich',
        'click',
        'pygame',
        'pillow'
    ],
    entry_points='''
        [console_scripts]
        local_search_solver=local_search.cli.entry_point:entry_point
    '''
)
