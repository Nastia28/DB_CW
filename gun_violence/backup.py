import consolemenu

import database


if __name__ == '__main__':
    menu = consolemenu.SelectionMenu(['Сделать резервную копию', 'Восстановить данные из резервной копии'])
    menu.show()
    if menu.is_selected_item_exit():
        exit()

    if menu.selected_option == 0:
        url = input('Введите URL базы данных, для которой нужно сделать бекап: ')
        database.backup(url)
        print('Резервная копия сохранена в backup.csv')
    else:
        url = input('Введите URL базы данных, в которую нужно восстановить данные: ')
        database.restore(url)
        print('Резервная копия из backup.csv восстановлена')
