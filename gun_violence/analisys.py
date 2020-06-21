import itertools
import random
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

COLOR = itertools.cycle(random.sample(['#e53935', '#8e24aa', '#3949ab', '#0288d1',
                                       '#009688', '#cddc39', '#ffb300', '#f4511e'], 6))
matplotlib.use('Qt5Agg')


def load_data_frame(iterable):
    df = pd.DataFrame(iterable)
    df['date'] = pd.to_datetime(df['date'])
    return df


def plot_states_incident_number(df):
    states = df['state'].unique()
    incident_number = [df[df['state'] == state].size for state in states]
    indexes = np.argsort(incident_number)
    plt.barh(np.array(states)[indexes], np.array(incident_number)[indexes], color=next(COLOR), zorder=2)
    plt.xlabel('Количество инцидентов за все время')
    plt.grid(color='grey', zorder=0)
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()


def plot_states_chronological_incidents_stats(df, states):
    for state in states:
        state_df = df[df['state'] == state]
        years = list(set([d.year for d in state_df['date']]))
        incident_number_by_year = [state_df[(state_df['date'] >= datetime(y, 1, 1)) &
                                            (state_df['date'] <= datetime(y, 12, 31))].size
                                   for y in years]
        indexes = np.argsort(years)
        plt.plot(np.array(years)[indexes], np.array(incident_number_by_year)[indexes],
                 color=next(COLOR), zorder=2, label=state, linewidth=4)
        plt.ylabel('Количество инцидентов за год')
    plt.legend(loc='best')
    plt.grid(color='grey', zorder=0)
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()


def plot_states_chronological_victims_stats(df, state):
    state_df = df[df['state'] == state]
    years = np.array(list(set([d.year for d in state_df['date']])))
    bar_width = 0.4
    killed_number_by_year = [state_df[(state_df['date'] >= datetime(y, 1, 1)) &
                                      (state_df['date'] <= datetime(y, 12, 31))]['n_killed'].sum()
                             for y in years]
    injured_number_by_year = [state_df[(state_df['date'] >= datetime(y, 1, 1)) &
                                       (state_df['date'] <= datetime(y, 12, 31))]['n_injured'].sum()
                              for y, killed in zip(years, killed_number_by_year)]
    plt.bar(years - 0.5 * bar_width, killed_number_by_year, zorder=2,
            width=bar_width, color=next(COLOR), label='Убитых за год')
    plt.bar(years + 0.5 * bar_width, injured_number_by_year, zorder=2,
            width=bar_width, color=next(COLOR), label='Раненых за год')

    plt.legend(loc='best')
    plt.grid(color='grey', zorder=0)
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()


def plot_victims_and_suspects_gender_stats(df):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.tight_layout()

    victim_male_count = df[df['victim_gender'].str.contains('Male')].size
    victim_female_count = df[df['victim_gender'].str.contains('Female')].size
    ax1.pie([victim_male_count, victim_female_count], labels=['Мужчины', 'Женщины'],
            autopct='%1.1f%%', explode=(0, 0.1))
    ax1.set_title('Соотношение мужчин/женщин среди жертв')

    suspect_male_count = df[df['suspect_gender'].str.contains('Male')].size
    suspect_female_count = df[df['suspect_gender'].str.contains('Female')].size
    ax2.pie([suspect_male_count, suspect_female_count], labels=['Мужчины', 'Женщины'],
            autopct='%1.1f%%', explode=(0, 0.1))
    ax2.set_title('Соотношение мужчин/женщин среди подозреваемых')

    plt.get_current_fig_manager().window.showMaximized()
    plt.show()


def plot_victims_and_suspects_age_stats(df):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.tight_layout()

    victim_child_count = df[df['victim_age'].str.contains('Child')].size
    victim_teen_count = df[df['victim_age'].str.contains('Teen')].size
    victim_adult_count = df[df['victim_age'].str.contains('Adult')].size
    ax1.pie([victim_child_count, victim_teen_count, victim_adult_count],
            labels=['Дети 0-11', 'Подростки 12-17', 'Взрослые 18+'],
            autopct='%1.1f%%', explode=(0.05, 0.05, 0.05))
    ax1.set_title('Соотношение возрастных категорий среди жертв')

    suspect_child_count = df[df['suspect_age'].str.contains('Child')].size
    suspect_teen_count = df[df['suspect_age'].str.contains('Teen')].size
    suspect_adult_count = df[df['suspect_age'].str.contains('Adult')].size
    ax2.pie([suspect_child_count, suspect_teen_count, suspect_adult_count],
            labels=['Дети 0-11', 'Подростки 12-17', 'Взрослые 18+'],
            autopct='%1.1f%%', explode=(0.05, 0.05, 0.05))
    ax2.set_title('Соотношение возрастных категорий среди подозреваемых')

    plt.get_current_fig_manager().window.showMaximized()
    plt.show()
