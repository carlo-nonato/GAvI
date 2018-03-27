Running from terminal usage example:

$ python -m core.parse txt/test.txt -o out/test
$ python -m core.translate out/test -o out/test_translated
$ python -m core.tag out/test_translated -o out/test_tagged
$ python -m core.tagging_pie_chart out/test_tagged
$ python -m core.sentiment out/test_tagged 2


Real input results are placed at 'results/'
