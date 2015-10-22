# coding: utf-8
# (c) 2015-10-21 Teruhisa Okada


def run_time(real_sec, model_sec, max_day=366):
    print real_sec / model_sec * max_day * 24, 'hours'

if __name__ == '__main__':
    run_time(9.5, 3600, 366)