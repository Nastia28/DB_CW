from functools import partial

import consolemenu

import analisys
import database

df = analisys.load_data_frame(database.collection().find({}))


def plot_states_chronological_incidents_stats():
    analisys.plot_states_chronological_incidents_stats(df, input('Введите штаты через пробел: ').split())


def plot_states_chronological_victims_stats():
    analisys.plot_states_chronological_victims_stats(df, input('Введите название штата: '))


def main_menu():
    menu = consolemenu.SelectionMenu(['Статистика по количеству инцидентов во всех штатах',
                                      'Статистика по количеству инцидентов по годам',
                                      'Статистика по количеству раненных/убитых по годам',
                                      'Распределение гендеров среди жертв и подозреваемых',
                                      'Распределение возрастных групп среди жертв и подозреваемых'])
    menu.show()
    if menu.is_selected_item_exit():
        exit()

    opts = [partial(analisys.plot_states_incident_number, df),
            plot_states_chronological_incidents_stats,
            plot_states_chronological_victims_stats,
            partial(analisys.plot_victims_and_suspects_gender_stats, df),
            partial(analisys.plot_victims_and_suspects_age_stats, df)]
    opts[menu.selected_option]()
    main_menu()


if __name__ == '__main__':
    main_menu()
