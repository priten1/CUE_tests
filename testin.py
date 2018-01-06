from cue_sdk import *
import time
import inflect
import datetime


def getTime():
    now = datetime.datetime.now()
    return now.hour, now.minute


def hourWrite():
    p = inflect.engine()
    hrs, mins = getTime()
    for letter in p.number_to_words(int(hrs)):
        print(letter)
        led_id = Corsair.GetLedIdForKeyName(str(letter))
        print(led_id)
        highlight_key_bland(led_id, 'w')
        time.sleep(.5)
        highlight_key_bland(led_id, 'r')


def minWrite():
    p = inflect.engine()
    hrs, mins = getTime()
    for letter in p.number_to_words(int(mins)).replace('-', ''):
        print(letter)
        try:
            led_id = Corsair.GetLedIdForKeyName(str(letter))
            print(led_id)
            highlight_key_bland(led_id, 'b')
            time.sleep(.5)
            highlight_key_bland(led_id, 'r')
        except:
            print('    FAILED')


def range_float(start, stop, step):
    while start < stop:
        yield start
        start += step


def highlight_key(led_id):
    for x in range_float(0, 2, 0.1):
        val = int((1 - abs(x - 1)) * 255)
        led_color = CorsairLedColor(led_id, val, val, val)
        Corsair.SetLedsColors(led_color)
        time.sleep(0.03)


def highlight_key_bland(led_id, RGB='w'):
    val = int(255)
    if RGB == 'w':
        led_color = CorsairLedColor(led_id, val, val, val)
        Corsair.SetLedsColors(led_color)
    elif RGB == 'R' or RGB == 'r':
        led_color = CorsairLedColor(led_id, val, 0, 0)
        Corsair.SetLedsColors(led_color)

    elif RGB == 'G' or RGB == 'g':
        led_color = CorsairLedColor(led_id, 0, val, 0)
        Corsair.SetLedsColors(led_color)

    elif RGB == 'B' or RGB == 'b':
        led_color = CorsairLedColor(led_id, 0, 0, val)
        Corsair.SetLedsColors(led_color)


def main():
    word = input("Please, input a word...\n")

    for letter in word:
        print(letter)
        led_id = Corsair.GetLedIdForKeyName(str(letter))
        print(led_id)
        highlight_key_bland(led_id, 'g')


def diff_times_in_seconds(t1, t2):
    # caveat emptor - assumes t1 & t2 are python times, on the same day and t2 is after t1
    h1, m1, s1 = t1.hour, t1.minute, t1.second
    h2, m2, s2 = t2.hour, t2.minute, t2.second
    t1_secs = s1 + 60 * (m1 + 60 * h1)
    t2_secs = s2 + 60 * (m2 + 60 * h2)
    return t2_secs - t1_secs


def diff_times(t1, t2):
    # caveat emptor - assumes t1 & t2 are python times, on the same day and t2 is after t1
    h1, m1, s1 = t1.hour, t1.minute, t1.second
    h2, m2, s2 = t2.hour, t2.minute, t2.second
    t1_secs = s1 + 60 * (m1 + 60 * h1)
    t2_secs = s2 + 60 * (m2 + 60 * h2)
    return (t2_secs - t1_secs) / 3600


def percentBar(perc=5):
    p = int(perc)
    bar = 'qwertyuiop'
    if perc < 10:
        for i in range(p):
            led_id = Corsair.GetLedIdForKeyName(str(bar[i]))
            highlight_key_bland(led_id, 'w')


def hoursLeft(now, end):
    hrs = diff_times(now, end)
    perc = int(int(hrs) * 10 / 9)
    percentBar(perc)


def getDate():
    now = datetime.datetime.now()
    return now.year, now.month, now.day


if __name__ == "__main__":
    Corsair = CUE("CUESDK.x64_2013.dll")
    while True:
        hourWrite()
        minWrite()
        y, m, d = getDate()
        now = datetime.datetime.now()
        end = datetime.datetime(y, m, d, 17, 00)
        hoursLeft(now, end)
        time.sleep(60)
