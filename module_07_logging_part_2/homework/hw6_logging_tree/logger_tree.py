import logging_tree

# После того как настроены логгеры (dictConfig и созданы логгеры)
with open('logging_tree.txt', 'w', encoding='utf-8') as f:
    logging_tree.printout(file=f)