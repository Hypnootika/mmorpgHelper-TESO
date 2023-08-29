from logging import info, error
from random import uniform
from time import sleep

from helper import input_helper, image_helper, timer_helper, config_helper
from helper.timer_helper import TIMER_STOPPED


SKILLPATH = ".\\assets\\skills\\"


cfg = config_helper.read_config()
class_var = cfg['class']
swap = cfg['swap']
skill1 = cfg['skill01']
skill2 = cfg['skill02']
skill3 = cfg['skill03']
skill4 = cfg['skill04']
skill5 = cfg['skill05']
skill6 = cfg['skill06']
skill7 = cfg['skill07']
skill8 = cfg['skill08']
skill9 = cfg['skill09']
skill10 = cfg['skill10']
skillUlt = cfg['skillUlt']

timer1 = timer_helper.TimerHelper('timer1')
timer2 = timer_helper.TimerHelper('timer2')
timer3 = timer_helper.TimerHelper('timer3')
timer4 = timer_helper.TimerHelper('timer4')
timer5 = timer_helper.TimerHelper('timer5')
timer6 = timer_helper.TimerHelper('timer6')
timer7 = timer_helper.TimerHelper('timer7')
timer8 = timer_helper.TimerHelper('timer8')
timer9 = timer_helper.TimerHelper('timer9')
timer10 = timer_helper.TimerHelper('timer10')
timer11 = timer_helper.TimerHelper('timer11')
timer12 = timer_helper.TimerHelper('timer12')


def press_combo(key1, key2):
    input_helper.keyDown(key1)
    input_helper.press(key2)
    input_helper.keyUp(key1)


def rotation():
    """set up the skill rotation for a specific class, by the config value"""
    if class_var == 'Dragonknight':
        combat_rotation('dk')
    elif class_var == 'Nightblade Bow':
        combat_rotation('nb_bow')
    elif class_var == 'Nightblade Enrage':
        combat_rotation('nb_enrage')
    elif class_var == 'Arcanist':
        combat_rotation('arc')
    elif class_var == 'Necromancer':
        combat_rotation('nec')
    elif class_var == 'Warden':
        combat_rotation('war')
    elif class_var == 'Sorcerer':
        combat_rotation('sor')
    elif class_var == 'Templar':
        combat_rotation('tem')
    else:
        error('No vaible class')


def combat_rotation(value):
    # target check
    if image_helper.pixel_matches_color(960,105, 114,35,35): # or image_helper.line_detection('mob') != False:
        # class skill check
        if value == 'nb_bow':
            # https://alcasthq.com/eso-stamina-nightblade-bow-build-for-pve/
            if image_helper.locate_needle(SKILLPATH+value+'\\ult.png', conf=0.9) and timer12.GetTimerState() == TIMER_STOPPED:
                timer12.StartTimer(4)
                input_helper.press(skillUlt)
                info('Execute ability ultimate')
                sleep(uniform(0.11, 0.14))
            elif timer11.GetTimerState() == TIMER_STOPPED:
                timer11.StartTimer(9)
                input_helper.press(swap)
                info('Execute ability weapon swap')
                sleep(uniform(0.11, 0.14))
            elif image_helper.locate_needle(SKILLPATH+value+'\\10.png', conf=0.6) and timer1.GetTimerState() == TIMER_STOPPED:
                timer1.StartTimer(11)
                input_helper.press(skill10)
                info('Execute ability 10')
                sleep(uniform(0.11, 0.14))
            elif image_helper.locate_needle(SKILLPATH+value+'\\09.png', conf=0.6) and not image_helper.pixel_matches_color(940,105, 129,37,37):
                input_helper.press(skill9)
                info('Execute ability 9')
                sleep(uniform(0.11, 0.14))
            elif image_helper.locate_needle(SKILLPATH+value+'\\08.png', conf=0.6) and timer3.GetTimerState() == TIMER_STOPPED:
                timer3.StartTimer(19)
                input_helper.press(skill8)
                info('Execute ability 8')
                sleep(uniform(0.11, 0.14))
            elif image_helper.locate_needle(SKILLPATH+value+'\\07.png', conf=0.6) and timer4.GetTimerState() == TIMER_STOPPED:
                timer4.StartTimer(3)
                input_helper.press(skill7)
                info('Execute ability 7')
                sleep(uniform(0.11, 0.14))
            elif image_helper.locate_needle(SKILLPATH+value+'\\06.png', conf=0.6) and timer5.GetTimerState() == TIMER_STOPPED:
                timer5.StartTimer(3)
                input_helper.press(skill6)
                info('Execute ability 6')
                sleep(uniform(0.11, 0.14))
            elif image_helper.locate_needle(SKILLPATH+value+'\\05.png', conf=0.6) and timer6.GetTimerState() == TIMER_STOPPED:
                timer6.StartTimer(4)
                input_helper.press(skill5)
                info('Execute ability 5')
                sleep(uniform(0.11, 0.14))
            elif image_helper.locate_needle(SKILLPATH+value+'\\04.png', conf=0.6) and timer7.GetTimerState() == TIMER_STOPPED:
                timer7.StartTimer(16)
                input_helper.press(skill4)
                info('Execute ability 4')
                sleep(uniform(0.11, 0.14))
            elif image_helper.locate_needle(SKILLPATH+value+'\\03.png', conf=0.6) and timer8.GetTimerState() == TIMER_STOPPED:
                timer8.StartTimer(21)
                input_helper.press(skill3)
                info('Execute ability 3')
                sleep(uniform(0.11, 0.14))
            elif image_helper.locate_needle(SKILLPATH+value+'\\02.png', conf=0.6) and timer9.GetTimerState() == TIMER_STOPPED:
                timer9.StartTimer(19)
                input_helper.press(skill2)
                info('Execute ability 2')
                sleep(uniform(0.11, 0.14))
            elif image_helper.locate_needle(SKILLPATH+value+'\\01.png', conf=0.6) and timer10.GetTimerState() == TIMER_STOPPED:
                timer10.StartTimer(14)
                input_helper.press(skill1)
                info('Execute ability 1')
                sleep(uniform(0.11, 0.14))
        elif value == 'nb_enrage':
            # https://alcasthq.com/eso-stamina-nightblade-build-for-pve/
            pass

        input_helper.leftClick()
        info('Execute ability left mouse')
        sleep(uniform(0.11, 0.14))

