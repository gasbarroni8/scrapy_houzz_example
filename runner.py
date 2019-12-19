# https://stackoverflow.com/questions/49201915/debugging-scrapy-project-in-visual-studio-code

import os
from scrapy.cmdline import execute

os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    execute(
        [
            'scrapy',
            'crawl',
            'houzz',
            '-o',
            'houzz.json',
        ]
    )
except SystemExit:
    pass