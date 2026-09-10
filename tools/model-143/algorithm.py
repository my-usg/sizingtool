# ============================================================================
#  USG Model 143 Sizing Tool  |  sizing algorithm (SOURCE OF TRUTH)
#
#  This is "143 Script.py" with the interactive CLI input() prompts and the
#  print() output section removed. Nothing else has been changed: the
#  functions and capacity data below are byte-for-byte the original.
#
#  The module communicates through module-level globals (inlet_input,
#  outlet_input, flow_rate, maop, pipesize_input, opp_type, irv_input,
#  oversizeby, oversize_percent, gastypemult, pload, Patm, result143).
#
#  THIS FILE IS THE SOURCE OF TRUTH. Editing it and pushing is all that is
#  required: CI transpiles it to dist/usg-model-143.js, proves the JavaScript
#  matches this Python on tens of thousands of inputs, and publishes it to the
#  website. Never edit dist/ by hand.
# ============================================================================

#143 REGULATOR

data143 = {
    3.5/28: {
        0.5: {'R14334_58': 520, 'R14334_12': 500, 'R14334_38': 370, 'R14334_56': None, 'R14334_14': None, 'R14334_36': None, 'R14334_53': None, 'R14334_96': None, 'R14334_18': None, 'R14310_58': 600, 'R14310_12': 580, 'R14310_38': 370, 'R14310_56': None, 'R14310_14': None, 'R14310_36': None, 'R14310_53': None, 'R14310_96': None, 'R14310_18': None, 'R1431Q_58': 750, 'R1431Q_12': 580, 'R1431Q_38': 370, 'R1431Q_56': None, 'R1431Q_14': None, 'R1431Q_36': None, 'R1431Q_53': None, 'R1431Q_96': None, 'R1431Q_18': None},
        1: {'R14334_58': 540, 'R14334_12': 550, 'R14334_38': 600, 'R14334_56': 500, 'R14334_14': None, 'R14334_36': None, 'R14334_53': None, 'R14334_96': None, 'R14334_18': None, 'R14310_58': 650, 'R14310_12': 750, 'R14310_38': 600, 'R14310_56': 550, 'R14310_14': None, 'R14310_36': None, 'R14310_53': None, 'R14310_96': None, 'R14310_18': None, 'R1431Q_58': 850, 'R1431Q_12': 975, 'R1431Q_38': 610, 'R1431Q_56': 570, 'R1431Q_14': None, 'R1431Q_36': None, 'R1431Q_53': None, 'R1431Q_96': None, 'R1431Q_18': None},
        2: {'R14334_58': 640, 'R14334_12': 680, 'R14334_38': 780, 'R14334_56': 650, 'R14334_14': 530, 'R14334_36': None, 'R14334_53': None, 'R14334_96': None, 'R14334_18': None, 'R14310_58': 800, 'R14310_12': 1000, 'R14310_38': 975, 'R14310_56': 800, 'R14310_14': 530, 'R14310_36': None, 'R14310_53': None, 'R14310_96': None, 'R14310_18': None, 'R1431Q_58': 975, 'R1431Q_12': 1075, 'R1431Q_38': 975, 'R1431Q_56': 850, 'R1431Q_14': 530, 'R1431Q_36': None, 'R1431Q_53': None, 'R1431Q_96': None, 'R1431Q_18': None},
        3: {'R14334_58': 850, 'R14334_12': 775, 'R14334_38': 950, 'R14334_56': 925, 'R14334_14': 675, 'R14334_36': 410, 'R14334_53': None, 'R14334_96': None, 'R14334_18': None, 'R14310_58': 950, 'R14310_12': 1025, 'R14310_38': 1200, 'R14310_56': 1050, 'R14310_14': 740, 'R14310_36': 410, 'R14310_53': None, 'R14310_96': None, 'R14310_18': None, 'R1431Q_58': 1050, 'R1431Q_12': 1450, 'R1431Q_38': 1200, 'R1431Q_56': 1050, 'R1431Q_14': 780, 'R1431Q_36': 410, 'R1431Q_53': None, 'R1431Q_96': None, 'R1431Q_18': None},
        5: {'R14334_58': 1000, 'R14334_12': 950, 'R14334_38': 1250, 'R14334_56': 1000, 'R14334_14': 950, 'R14334_36': 550, 'R14334_53': 410, 'R14334_96': 270, 'R14334_18': 240, 'R14310_58': 1150, 'R14310_12': 1225, 'R14310_38': 1500, 'R14310_56': 1500, 'R14310_14': 975, 'R14310_36': 560, 'R14310_53': 420, 'R14310_96': 290, 'R14310_18': 250, 'R1431Q_58': 1300, 'R1431Q_12': 1600, 'R1431Q_38': 1700, 'R1431Q_56': 1500, 'R1431Q_14': 975, 'R1431Q_36': 560, 'R1431Q_53': 450, 'R1431Q_96': 300, 'R1431Q_18': 250},
        10: {'R14334_58': 1300, 'R14334_12': 1125, 'R14334_38': 1500, 'R14334_56': 1350, 'R14334_14': 1200, 'R14334_36': 810, 'R14334_53': 550, 'R14334_96': 420, 'R14334_18': 370, 'R14310_58': 1500, 'R14310_12': 1400, 'R14310_38': 1850, 'R14310_56': 2150, 'R14310_14': 1500, 'R14310_36': 850, 'R14310_53': 560, 'R14310_96': 440, 'R14310_18': 370, 'R1431Q_58': 1700, 'R1431Q_12': 2000, 'R1431Q_38': 2400, 'R1431Q_56': 2300, 'R1431Q_14': 1500, 'R1431Q_36': 850, 'R1431Q_53': 600, 'R1431Q_96': 450, 'R1431Q_18': 370},
        20: {'R14334_58': None, 'R14334_12': 1300, 'R14334_38': 1600, 'R14334_56': 1550, 'R14334_14': 1300, 'R14334_36': 1150, 'R14334_53': 720, 'R14334_96': 630, 'R14334_18': 530, 'R14310_58': None, 'R14310_12': 1850, 'R14310_38': 1850, 'R14310_56': 2050, 'R14310_14': 2000, 'R14310_36': 1200, 'R14310_53': 840, 'R14310_96': 630, 'R14310_18': 530, 'R1431Q_58': None, 'R1431Q_12': 2400, 'R1431Q_38': 2400, 'R1431Q_56': 2400, 'R1431Q_14': 2200, 'R1431Q_36': 1200, 'R1431Q_53': 890, 'R1431Q_96': 650, 'R1431Q_18': 630},
        40: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': 1750, 'R14334_14': 1330, 'R14334_36': 1570, 'R14334_53': 820, 'R14334_96': 900, 'R14334_18': 860, 'R14310_58': None, 'R14310_12': None, 'R14310_38': 1850, 'R14310_56': 2050, 'R14310_14': 2000, 'R14310_36': 1900, 'R14310_53': 1250, 'R14310_96': 1025, 'R14310_18': 860, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': 2400, 'R1431Q_56': 2400, 'R1431Q_14': 2400, 'R1431Q_36': 1900, 'R1431Q_53': 1400, 'R1431Q_96': 1050, 'R1431Q_18': 820},
        60: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': 1750, 'R14334_36': 1900, 'R14334_53': 1500, 'R14334_96': 1300, 'R14334_18': 1200, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': 2000, 'R14310_36': 2050, 'R14310_53': 1750, 'R14310_96': 1400, 'R14310_18': 1200, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': 2400, 'R1431Q_36': 2050, 'R1431Q_53': 1900, 'R1431Q_96': 1400, 'R1431Q_18': 1200},
        100: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': 1900, 'R14334_53': None, 'R14334_96': 1700, 'R14334_18': 1600, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': None, 'R14310_36': 2400, 'R14310_53': None, 'R14310_96': 2200, 'R14310_18': 1650, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': None, 'R1431Q_36': 2400, 'R1431Q_53': None, 'R1431Q_96': 2200, 'R1431Q_18': 1775},
        125: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': 1900, 'R14334_53': None, 'R14334_96': 1900, 'R14334_18': 1850, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': None, 'R14310_36': 2400, 'R14310_53': None, 'R14310_96': 2400, 'R14310_18': 2100, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': None, 'R1431Q_36': 2400, 'R1431Q_53': None, 'R1431Q_96': 2400, 'R1431Q_18': 2150},
    },
    0.25: {
        0.5: {'R14334_58': 520, 'R14334_12': 500, 'R14334_38': 370, 'R14334_56': None, 'R14334_14': None, 'R14334_36': None, 'R14334_53': None, 'R14334_96': None, 'R14334_18': None, 'R14310_58': 600, 'R14310_12': 580, 'R14310_38': 370, 'R14310_56': None, 'R14310_14': None, 'R14310_36': None, 'R14310_53': None, 'R14310_96': None, 'R14310_18': None, 'R1431Q_58': 750, 'R1431Q_12': 580, 'R1431Q_38': 370, 'R1431Q_56': None, 'R1431Q_14': None, 'R1431Q_36': None, 'R1431Q_53': None, 'R1431Q_96': None, 'R1431Q_18': None},
        1: {'R14334_58': 540, 'R14334_12': 550, 'R14334_38': 600, 'R14334_56': 500, 'R14334_14': None, 'R14334_36': None, 'R14334_53': None, 'R14334_96': None, 'R14334_18': None, 'R14310_58': 650, 'R14310_12': 750, 'R14310_38': 600, 'R14310_56': 550, 'R14310_14': None, 'R14310_36': None, 'R14310_53': None, 'R14310_96': None, 'R14310_18': None, 'R1431Q_58': 850, 'R1431Q_12': 975, 'R1431Q_38': 610, 'R1431Q_56': 570, 'R1431Q_14': None, 'R1431Q_36': None, 'R1431Q_53': None, 'R1431Q_96': None, 'R1431Q_18': None},
        2: {'R14334_58': 640, 'R14334_12': 680, 'R14334_38': 780, 'R14334_56': 650, 'R14334_14': 530, 'R14334_36': None, 'R14334_53': None, 'R14334_96': None, 'R14334_18': None, 'R14310_58': 800, 'R14310_12': 1000, 'R14310_38': 975, 'R14310_56': 800, 'R14310_14': 530, 'R14310_36': None, 'R14310_53': None, 'R14310_96': None, 'R14310_18': None, 'R1431Q_58': 975, 'R1431Q_12': 1075, 'R1431Q_38': 975, 'R1431Q_56': 850, 'R1431Q_14': 530, 'R1431Q_36': None, 'R1431Q_53': None, 'R1431Q_96': None, 'R1431Q_18': None},
        3: {'R14334_58': 850, 'R14334_12': 775, 'R14334_38': 950, 'R14334_56': 925, 'R14334_14': 675, 'R14334_36': 410, 'R14334_53': None, 'R14334_96': None, 'R14334_18': None, 'R14310_58': 950, 'R14310_12': 1025, 'R14310_38': 1200, 'R14310_56': 1050, 'R14310_14': 740, 'R14310_36': 410, 'R14310_53': None, 'R14310_96': None, 'R14310_18': None, 'R1431Q_58': 1050, 'R1431Q_12': 1450, 'R1431Q_38': 1200, 'R1431Q_56': 1050, 'R1431Q_14': 780, 'R1431Q_36': 410, 'R1431Q_53': None, 'R1431Q_96': None, 'R1431Q_18': None},
        5: {'R14334_58': 1000, 'R14334_12': 950, 'R14334_38': 1250, 'R14334_56': 1000, 'R14334_14': 950, 'R14334_36': 550, 'R14334_53': 410, 'R14334_96': 270, 'R14334_18': 240, 'R14310_58': 1150, 'R14310_12': 1225, 'R14310_38': 1500, 'R14310_56': 1500, 'R14310_14': 975, 'R14310_36': 560, 'R14310_53': 420, 'R14310_96': 290, 'R14310_18': 250, 'R1431Q_58': 1300, 'R1431Q_12': 1600, 'R1431Q_38': 1700, 'R1431Q_56': 1500, 'R1431Q_14': 975, 'R1431Q_36': 560, 'R1431Q_53': 450, 'R1431Q_96': 300, 'R1431Q_18': 250},
        10: {'R14334_58': 1300, 'R14334_12': 1125, 'R14334_38': 1500, 'R14334_56': 1350, 'R14334_14': 1200, 'R14334_36': 810, 'R14334_53': 550, 'R14334_96': 420, 'R14334_18': 370, 'R14310_58': 1500, 'R14310_12': 1400, 'R14310_38': 1850, 'R14310_56': 2150, 'R14310_14': 1500, 'R14310_36': 850, 'R14310_53': 560, 'R14310_96': 440, 'R14310_18': 370, 'R1431Q_58': 1700, 'R1431Q_12': 2000, 'R1431Q_38': 2400, 'R1431Q_56': 2300, 'R1431Q_14': 1500, 'R1431Q_36': 850, 'R1431Q_53': 600, 'R1431Q_96': 450, 'R1431Q_18': 370},
        20: {'R14334_58': None, 'R14334_12': 1300, 'R14334_38': 1600, 'R14334_56': 1550, 'R14334_14': 1300, 'R14334_36': 1150, 'R14334_53': 720, 'R14334_96': 630, 'R14334_18': 530, 'R14310_58': None, 'R14310_12': 1850, 'R14310_38': 1850, 'R14310_56': 2050, 'R14310_14': 2000, 'R14310_36': 1200, 'R14310_53': 840, 'R14310_96': 630, 'R14310_18': 530, 'R1431Q_58': None, 'R1431Q_12': 2400, 'R1431Q_38': 2400, 'R1431Q_56': 2400, 'R1431Q_14': 2200, 'R1431Q_36': 1200, 'R1431Q_53': 890, 'R1431Q_96': 650, 'R1431Q_18': 630},
        40: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': 1750, 'R14334_14': 1330, 'R14334_36': 1570, 'R14334_53': 820, 'R14334_96': 900, 'R14334_18': 860, 'R14310_58': None, 'R14310_12': None, 'R14310_38': 1850, 'R14310_56': 2050, 'R14310_14': 2000, 'R14310_36': 1900, 'R14310_53': 1250, 'R14310_96': 1025, 'R14310_18': 860, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': 2400, 'R1431Q_56': 2400, 'R1431Q_14': 2400, 'R1431Q_36': 1900, 'R1431Q_53': 1400, 'R1431Q_96': 1050, 'R1431Q_18': 820},
        60: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': 1750, 'R14334_36': 1900, 'R14334_53': 1500, 'R14334_96': 1300, 'R14334_18': 1200, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': 2000, 'R14310_36': 2050, 'R14310_53': 1750, 'R14310_96': 1400, 'R14310_18': 1200, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': 2400, 'R1431Q_36': 2050, 'R1431Q_53': 1900, 'R1431Q_96': 1400, 'R1431Q_18': 1200},
        100: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': 1900, 'R14334_53': None, 'R14334_96': 1700, 'R14334_18': 1600, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': None, 'R14310_36': 2400, 'R14310_53': None, 'R14310_96': 2200, 'R14310_18': 1650, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': None, 'R1431Q_36': 2400, 'R1431Q_53': None, 'R1431Q_96': 2200, 'R1431Q_18': 1775},
        125: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': 1900, 'R14334_53': None, 'R14334_96': 1900, 'R14334_18': 1850, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': None, 'R14310_36': 2400, 'R14310_53': None, 'R14310_96': 2400, 'R14310_18': 2100, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': None, 'R1431Q_36': 2400, 'R1431Q_53': None, 'R1431Q_96': 2400, 'R1431Q_18': 2150},
    },
	2.0: {	
        5: {'R14334_58': 1100, 'R14334_12': 925, 'R14334_38': 700, 'R14334_56': 600, 'R14334_14': 470, 'R14334_36': 370, 'R14334_53': 450, 'R14334_96': 300, 'R14334_18': 220, 'R14310_58': 1150, 'R14310_12': 975, 'R14310_38': 725, 'R14310_56': 600, 'R14310_14': 500, 'R14310_36': 380, 'R14310_53': 450, 'R14310_96': 300, 'R14310_18': 220, 'R1431Q_58': 1175, 'R1431Q_12': 1050, 'R1431Q_38': 750, 'R1431Q_56': 600, 'R1431Q_14': 500, 'R1431Q_36': 380, 'R1431Q_53': 450, 'R1431Q_96': 300, 'R1431Q_18': 220},
        10: {'R14334_58': 1600, 'R14334_12': 1350, 'R14334_38': 1100, 'R14334_56': 1000, 'R14334_14': 800, 'R14334_36': 600, 'R14334_53': 650, 'R14334_96': 480, 'R14334_18': 325, 'R14310_58': 1650, 'R14310_12': 1550, 'R14310_38': 1250, 'R14310_56': 1050, 'R14310_14': 850, 'R14310_36': 625, 'R14310_53': 650, 'R14310_96': 480, 'R14310_18': 325, 'R1431Q_58': 1750, 'R1431Q_12': 1700, 'R1431Q_38': 1350, 'R1431Q_56': 1050, 'R1431Q_14': 850, 'R1431Q_36': 675, 'R1431Q_53': 650, 'R1431Q_96': 480, 'R1431Q_18': 350},
        20: {'R14334_58': None, 'R14334_12': 1800, 'R14334_38': 1500, 'R14334_56': 1400, 'R14334_14': 1150, 'R14334_36': 975, 'R14334_53': 950, 'R14334_96': 700, 'R14334_18': 550, 'R14310_58': None, 'R14310_12': 2100, 'R14310_38': 2050, 'R14310_56': 1800, 'R14310_14': 1475, 'R14310_36': 1100, 'R14310_53': 950, 'R14310_96': 700, 'R14310_18': 550, 'R1431Q_58': None, 'R1431Q_12': 2400, 'R1431Q_38': 2200, 'R1431Q_56': 1950, 'R1431Q_14': 1700, 'R1431Q_36': 1100, 'R1431Q_53': 950, 'R1431Q_96': 700, 'R1431Q_18': 550},
        40: {'R14334_58': None, 'R14334_12': None, 'R14334_38': 1850, 'R14334_56': 1700, 'R14334_14': 1450, 'R14334_36': 1200, 'R14334_53': 1450, 'R14334_96': 1100, 'R14334_18': 900, 'R14310_58': None, 'R14310_12': None, 'R14310_38': 2500, 'R14310_56': 2200, 'R14310_14': 2200, 'R14310_36': 1500, 'R14310_53': 1500, 'R14310_96': 1100, 'R14310_18': 900, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': 2600, 'R1431Q_56': 2400, 'R1431Q_14': 2600, 'R1431Q_36': 1950, 'R1431Q_53': 1500, 'R1431Q_96': 1100, 'R1431Q_18': 900},
        60: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': 1825, 'R14334_36': 1650, 'R14334_53': 1675, 'R14334_96': 1525, 'R14334_18': 1100, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': 2500, 'R14310_36': 2050, 'R14310_53': 2050, 'R14310_96': 1525, 'R14310_18': 1125, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': 2600, 'R1431Q_36': 2600, 'R1431Q_53': 2050, 'R1431Q_96': 1525, 'R1431Q_18': 1125},
        100: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': 2200, 'R14334_53': None, 'R14334_96': 2200, 'R14334_18': 1550, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': None, 'R14310_36': 2600, 'R14310_53': None, 'R14310_96': 2400, 'R14310_18': 1850, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': None, 'R1431Q_36': 2600, 'R1431Q_53': None, 'R1431Q_96': 2400, 'R1431Q_18': 1850},
        125: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': 2200, 'R14334_53': None, 'R14334_96': 2200, 'R14334_18': 1850, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': None, 'R14310_36': 2600, 'R14310_53': None, 'R14310_96': 2600, 'R14310_18': 2150, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': None, 'R1431Q_36': 2600, 'R1431Q_53': None, 'R1431Q_96': 2600, 'R1431Q_18': 2150},
    },
	6.0: {	
        10: {'R14334_58': 1600, 'R14334_12': 1350, 'R14334_38': 1100, 'R14334_56': 1000, 'R14334_14': 800, 'R14334_36': 600, 'R14334_53': 650, 'R14334_96': 480, 'R14334_18': 325, 'R14310_58': 1650, 'R14310_12': 1550, 'R14310_38': 1250, 'R14310_56': 1050, 'R14310_14': 850, 'R14310_36': 625, 'R14310_53': 650, 'R14310_96': 480, 'R14310_18': 325, 'R1431Q_58': 1750, 'R1431Q_12': 1700, 'R1431Q_38': 1350, 'R1431Q_56': 1050, 'R1431Q_14': 850, 'R1431Q_36': 675, 'R1431Q_53': 650, 'R1431Q_96': 480, 'R1431Q_18': 350},
        20: {'R14334_58': None, 'R14334_12': 1800, 'R14334_38': 1500, 'R14334_56': 1400, 'R14334_14': 1150, 'R14334_36': 975, 'R14334_53': 950, 'R14334_96': 700, 'R14334_18': 550, 'R14310_58': None, 'R14310_12': 2100, 'R14310_38': 2050, 'R14310_56': 1800, 'R14310_14': 1475, 'R14310_36': 1100, 'R14310_53': 950, 'R14310_96': 700, 'R14310_18': 550, 'R1431Q_58': None, 'R1431Q_12': 2400, 'R1431Q_38': 2200, 'R1431Q_56': 1950, 'R1431Q_14': 1700, 'R1431Q_36': 1100, 'R1431Q_53': 950, 'R1431Q_96': 700, 'R1431Q_18': 550},
        40: {'R14334_58': None, 'R14334_12': None, 'R14334_38': 1850, 'R14334_56': 1700, 'R14334_14': 1450, 'R14334_36': 1200, 'R14334_53': 1450, 'R14334_96': 1100, 'R14334_18': 900, 'R14310_58': None, 'R14310_12': None, 'R14310_38': 2500, 'R14310_56': 2200, 'R14310_14': 2200, 'R14310_36': 1500, 'R14310_53': 1500, 'R14310_96': 1100, 'R14310_18': 900, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': 2600, 'R1431Q_56': 2400, 'R1431Q_14': 2600, 'R1431Q_36': 1950, 'R1431Q_53': 1500, 'R1431Q_96': 1100, 'R1431Q_18': 900},
        60: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': 1825, 'R14334_36': 1650, 'R14334_53': 1675, 'R14334_96': 1525, 'R14334_18': 1100, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': 2500, 'R14310_36': 2050, 'R14310_53': 2050, 'R14310_96': 1525, 'R14310_18': 1125, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': 2600, 'R1431Q_36': 2600, 'R1431Q_53': 2050, 'R1431Q_96': 1525, 'R1431Q_18': 1125},
        100: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': 2200, 'R14334_53': None, 'R14334_96': 2200, 'R14334_18': 1550, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': None, 'R14310_36': 2600, 'R14310_53': None, 'R14310_96': 2400, 'R14310_18': 1850, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': None, 'R1431Q_36': 2600, 'R1431Q_53': None, 'R1431Q_96': 2400, 'R1431Q_18': 1850},
        125: {'R14334_58': None, 'R14334_12': None, 'R14334_38': None, 'R14334_56': None, 'R14334_14': None, 'R14334_36': 2200, 'R14334_53': None, 'R14334_96': 2200, 'R14334_18': 1850, 'R14310_58': None, 'R14310_12': None, 'R14310_38': None, 'R14310_56': None, 'R14310_14': None, 'R14310_36': 2600, 'R14310_53': None, 'R14310_96': 2600, 'R14310_18': 2150, 'R1431Q_58': None, 'R1431Q_12': None, 'R1431Q_38': None, 'R1431Q_56': None, 'R1431Q_14': None, 'R1431Q_36': 2600, 'R1431Q_53': None, 'R1431Q_96': 2600, 'R1431Q_18': 2150},
    },
}


# Interpolation Function
# ------------------------------------------------------------------------------------------------------

def interpolate_capacity(data, inlet, outlet, monitor_used, vp):
    outlet_vals = sorted(data.keys())

    if outlet < outlet_vals[0] or outlet > outlet_vals[-1]:
        return "Error: inlet pressure is out of range for given outlet pressure"

    outlet_low = max([p for p in outlet_vals if p <= outlet])
    outlet_high = min([p for p in outlet_vals if p >= outlet])

    def inlet_interpolate(section):
        #Interpolate capacities at the target inlet pressure within one outlet section.
        inlet_vals = sorted(section.keys())
        if not inlet_vals or inlet < inlet_vals[0] or inlet > inlet_vals[-1]:
            return None
        inlet_low = max([p for p in inlet_vals if p <= inlet])
        inlet_high = min([p for p in inlet_vals if p >= inlet])
        u = (inlet - inlet_low) / (inlet_high - inlet_low) if inlet_high != inlet_low else 0
        result = {}
        for reg in section[inlet_low]:
            f0 = section[inlet_low][reg]
            f1 = section[inlet_high][reg]
            if f0 is None or f1 is None:
                result[reg] = None
            else:
                result[reg] = (1 - u) * f0 + u * f1
        return result

    cap_low = inlet_interpolate(data[outlet_low])
    cap_high = inlet_interpolate(data[outlet_high])

    if cap_low is None or cap_high is None:
        return "Error: inlet pressure is out of range for given outlet pressure"

    t = (outlet - outlet_low) / (outlet_high - outlet_low) if outlet_high != outlet_low else 0

    capacities = {}
    for reg in cap_low:
        v_low = cap_low[reg]
        v_high = cap_high.get(reg)
        if v_low is None or v_high is None:
            capacities[reg] = "N/A"
            continue
        interpolated = (1 - t) * v_low + t * v_high

        if monitor_used:
            interpolated *= 0.7

        if vp:
            interpolated *= 0.8

        interpolated *= gastypemult

        # Adjustment for altitude
        if Patm < 14.4:
            ratio = (inlet + Patm)/(outlet + Patm)
            if ratio < 1.894:
                alt_adj = (((outlet+Patm)*((inlet+Patm)-(outlet+Patm)))**0.5) / (((outlet+14.65)*((inlet+14.65)-(outlet+14.65)))**0.5)
            else:
                alt_adj = (inlet+Patm)/(inlet+14.65)
            
            if alt_adj < 1:
                interpolated *= alt_adj

        capacities[reg] = int(round(interpolated))

    return capacities


# Will Regulator Work
# ------------------------------------------------------------------------------------------------------

def will_work(cap, reg, orifice_max):
    if cap == "N/A":
        return "No"
    else:
        if cap >= (flow_rate * oversizeby) and orifice_max >= maop:
            return "Yes"
        else:
            return "No"


# Orifice Types & MAOP Function
# ------------------------------------------------------------------------------------------------------

def orifice_type143(reg):
    suf = reg[-2:]
    if suf == "18":
        return '1/8"'
    elif suf == "96":
        return '9/64"'
    elif suf == "53":
        return '5/32"'
    elif suf == "36":
        return '3/16"'
    elif suf == "14":
        return '1/4"'
    elif suf == "56":
        return '5/16"'
    elif suf == "38":
        return '3/8"'
    elif suf == "12":
        return '1/2"'
    elif suf == '58':
        return '5/8"'

def orifice_max143(reg):
    suf = reg[-2:]
    if suf == "18":
        return 125
    elif suf == "96":
        return 125
    elif suf == "53":
        return 60
    elif suf == "36":
        return 125
    elif suf == "14":
        return 60
    elif suf == "56":
        return 40
    elif suf == "38":
        return 40
    elif suf == "12":
        return 20
    elif suf == '58':
        return 10


# Spring Selections
# ------------------------------------------------------------------------------------------------------

def spring_143(op):
    if op < 6.5/28 and op >= 3.5/28:
        return {
            'color': 'Red',
            'range': '(3.5" - 6.5" wc)',
        }
    elif op < 8.5/28:
        return {
            'color': 'Blue',
            'range': '(5" - 8.5" wc)',
        }
    elif op < 14/28:
        return {
            'color': 'Green',
            'range': '(6" - 14" wc)',
        }
    elif op < 1:
        return {
            'color': 'Orange',
            'range': '(12" - 28" wc)',
        }
    elif op <= 2:
        return {
            'color': 'Black + White',
            'range': '(0.5 - 2 psi)',
        }
    elif op < 3:
        return {
            'color': 'Cadmium',
            'range': '(0.5 - 3 psi)',
        }
    elif op <= 6:
        return {
            'color': 'Black',
            'range': '(2 - 6 psi)',
        }
    

# Will IRV Work
# ------------------------------------------------------------------------------------------------------

def will_irv_work143(reg, opp):

    # Partial IRV
    if opp == "Partial":
        return "Partial"
     
    irvstddata143 = {
        0: {'18': 0, '96': 0, '53': 0, '36': 0, '14': 0, '56': 0, '38': 0, '12': 0, '58': 0},
        2: {'18': 0.24, '96': 0.27, '53': 0.28, '36': 0.29, '14': 0.31, '56': 0.19, '38': 0.32, '12': 0.43, '58': 0.56},
        3: {'18': 0.27, '96': 0.29, '53': 0.32, '36': 0.32, '14': 0.35, '56': 0.3, '38': 0.4, '12': 0.66, '58': 0.83},
        5: {'18': 0.31, '96': 0.3, '53': 0.35, '36': 0.36, '14': 0.43, '56': 0.49, '38': 0.62, '12': 1.06, '58': 1.36},
        9.3: {'18': 0.34, '96': 0.32, '53': 0.39, '36': 0.4, '14': 0.58, '56': 0.84, '38': 1.07, '12': 1.95, '58': 2.63},
        10: {'18': 0.35, '96': 0.33, '53': 0.39, '36': 0.41, '14': 0.61, '56': 0.89, '38': 1.15, '12': 2.13, '58': None},
        12.4: {'18': 0.37, '96': 0.34, '53': 0.41, '36': 0.44, '14': 0.68, '56': 1.06, '38': 1.41, '12': 2.63, '58': None},
        20: {'18': 0.41, '96': 0.39, '53': 0.47, '36': 0.58, '14': 0.91, '56': 1.62, '38': 2.34, '12': None, '58': None},
        22.5: {'18': 0.42, '96': 0.4, '53': 0.49, '36': 0.61, '14': 1, '56': 1.8, '38': 2.63, '12': None, '58': None},
        30: {'18': 0.47, '96': 0.45, '53': 0.56, '36': 0.72, '14': 1.3, '56': 2.41, '38': None, '12': None, '58': None},
        32.7: {'18': 0.48, '96': 0.47, '53': 0.58, '36': 0.77, '14': 1.42, '56': 2.63, '38': None, '12': None, '58': None},
        40: {'18': 0.53, '96': 0.51, '53': 0.63, '36': 0.88, '14': 1.72, '56': None, '38': None, '12': None, '58': None},
        50: {'18': 0.59, '96': 0.58, '53': 0.7, '36': 1.08, '14': 2.21, '56': None, '38': None, '12': None, '58': None},
        58.1: {'18': 0.63, '96': 0.65, '53': 0.79, '36': 1.23, '14': 2.63, '56': None, '38': None, '12': None, '58': None},
        60: {'18': 0.63, '96': 0.66, '53': 0.81, '36': 1.27, '14': None, '56': None, '38': None, '12': None, '58': None},
        70: {'18': 0.69, '96': 0.75, '53': 0.94, '36': 1.5, '14': None, '56': None, '38': None, '12': None, '58': None},
        80: {'18': 0.76, '96': 0.85, '53': 1.08, '36': 1.73, '14': None, '56': None, '38': None, '12': None, '58': None},
        90: {'18': 0.83, '96': 0.96, '53': 1.23, '36': 1.99, '14': None, '56': None, '38': None, '12': None, '58': None},
        100: {'18': 0.89, '96': 1.07, '53': 1.38, '36': 2.24, '14': None, '56': None, '38': None, '12': None, '58': None},
        110: {'18': 0.96, '96': 1.18, '53': 1.55, '36': 2.52, '14': None, '56': None, '38': None, '12': None, '58': None},
        114.1: {'18': 1, '96': 1.23, '53': 1.62, '36': 2.63, '14': None, '56': None, '38': None, '12': None, '58': None},
        120: {'18': 1.05, '96': 1.3, '53': 1.73, '36': None, '14': None, '56': None, '38': None, '12': None, '58': None},
        125: {'18': 1.1, '96': 1.37, '53': 1.83, '36': None, '14': None, '56': None, '38': None, '12': None, '58': None},
    }

    irvhpdata143 = {
        0: {'18': 0, '96': 0, '53': 0, '36': 0, '14': 0, '56': 0, '38': 0, '12': 0, '58': 0},
        4: {'18': 0.34, '96': 0.76, '53': 0.63, '36': 0.8, '14': 0.83, '56': 0.86, '38': 0.92, '12': 0.95, '58': 1.05},
        5: {'18': 0.68, '96': 0.82, '53': 0.79, '36': 0.82, '14': 0.85, '56': 0.9, '38': 1.05, '12': 1.14, '58': 1.31},
        7.5: {'18': 0.81, '96': 0.83, '53': 0.86, '36': 0.85, '14': 0.93, '56': 1.06, '38': 1.34, '12': 1.57, '58': 1.98},
        10: {'18': 0.83, '96': 0.87, '53': 0.9, '36': 0.89, '14': 1.02, '56': 1.24, '38': 1.58, '12': 2.08, '58': 2.79},
        12.5: {'18': 0.85, '96': 0.89, '53': 0.92, '36': 0.92, '14': 1.1, '56': 1.39, '38': 1.85, '12': 2.62, '58': 3.51},
        16.3: {'18': 0.87, '96': 0.92, '53': 0.96, '36': 0.98, '14': 1.21, '56': 1.63, '38': 2.28, '12': 3.49, '58': None},
        20: {'18': 0.89, '96': 0.95, '53': 0.99, '36': 1.02, '14': 1.33, '56': 1.9, '38': 2.72, '12': None, '58': None},
        26.6: {'18': 0.92, '96': 1, '53': 1.05, '36': 1.11, '14': 1.52, '56': 2.35, '38': 3.5, '12': None, '58': None},
        30: {'18': 0.94, '96': 1.03, '53': 1.07, '36': 1.17, '14': 1.66, '56': 2.61, '38': None, '12': None, '58': None},
        40: {'18': 0.99, '96': 1.1, '53': 1.15, '36': 1.32, '14': 2.05, '56': 3.43, '38': None, '12': None, '58': None},
        41.1: {'18': 0.99, '96': 1.1, '53': 1.16, '36': 1.33, '14': 2.09, '56': 3.52, '38': None, '12': None, '58': None},
        50: {'18': 1.04, '96': 1.17, '53': 1.23, '36': 1.43, '14': 2.49, '56': None, '38': None, '12': None, '58': None},
        60: {'18': 1.09, '96': 1.23, '53': 1.33, '36': 1.64, '14': 2.99, '56': None, '38': None, '12': None, '58': None},
        70: {'18': 1.14, '96': 1.31, '53': 1.45, '36': 1.87, '14': 3.5, '56': None, '38': None, '12': None, '58': None},
        70.3: {'18': 1.15, '96': 1.31, '53': 1.45, '36': 1.87, '14': 3.51, '56': None, '38': None, '12': None, '58': None},
        80: {'18': 1.2, '96': 1.39, '53': 1.57, '36': 2.1, '14': None, '56': None, '38': None, '12': None, '58': None},
        90: {'18': 1.27, '96': 1.48, '53': 1.72, '36': 2.32, '14': None, '56': None, '38': None, '12': None, '58': None},
        100: {'18': 1.35, '96': 1.59, '53': 1.86, '36': 2.54, '14': None, '56': None, '38': None, '12': None, '58': None},
        110: {'18': 1.43, '96': 1.7, '53': 2.02, '36': 2.78, '14': None, '56': None, '38': None, '12': None, '58': None},
        120: {'18': 1.51, '96': 1.82, '53': 2.17, '36': 3.04, '14': None, '56': None, '38': None, '12': None, '58': None},
        125: {'18': 1.56, '96': 1.89, '53': 2.26, '36': 3.19, '14': None, '56': None, '38': None, '12': None, '58': None},
    }

    # Linear Interpolaton Algorithm to determine the outlet pressure buildup for a given inlet pressure and orifice
    irv_table = irvstddata143 if outlet_input <= 0.5 else irvhpdata143
    orifice_key = reg[-2:]
    inlet_keys = sorted(irv_table.keys())
    if inlet_input <= inlet_keys[0]:
        out_pressure_build = irv_table[inlet_keys[0]][orifice_key]
    elif inlet_input >= inlet_keys[-1]:
        out_pressure_build = irv_table[inlet_keys[-1]][orifice_key]
    else:
        p_low = max(p for p in inlet_keys if p <= inlet_input)
        p_high = min(p for p in inlet_keys if p >= inlet_input)
        if p_low == p_high:
            out_pressure_build = irv_table[p_low][orifice_key]
        else:
            v_low = irv_table[p_low][orifice_key]
            v_high = irv_table[p_high][orifice_key]
            if v_low is None or v_high is None:
                out_pressure_build = None
            else:
                t = (inlet_input - p_low) / (p_high - p_low)
                out_pressure_build = (1 - t) * v_low + t * v_high

    if out_pressure_build == None or irv_input == None:
        return "No"
    elif (out_pressure_build + outlet_input) <= irv_input:
        return "Yes"
    else:
        return "No"


# Regulator Match Functions
# ------------------------------------------------------------------------------------------------------

def gen_match143(result, opp):
    match = None

    if outlet_input > 2:
        model = '143-2HP'
    elif opp == "None":
        model = '143-1'
    else:
        model = '143-2'

    body_labels143 = {
        'R14334': '3/4"',
        'R14310': '1"',
        'R1431Q': '1-1/4"',
    }

    pipe_priority = {
        '3/4"': 'R14334',
        '1"':    'R14310',
        '1-1/4"': 'R1431Q',
    }

    all_prefixes = list(body_labels143.keys())
    prioritized = pipe_priority.get(pipesize_input)
    if prioritized:
        ordered_prefixes = [prioritized] + [p for p in all_prefixes if p != prioritized]
    else:
        ordered_prefixes = all_prefixes

    # largest to smallest orifices
    orifice_order143 = ['58', '12', '38', '56', '14', '36', '53', '96', '18']

    # IRV
    if opp == "IRV" or opp == "Partial":
        for prefix in ordered_prefixes:
            for orifice in orifice_order143:
                reg = f"{prefix}_{orifice}"
                if reg in result:
                    cap = result[reg]
                    if will_work(cap, reg, orifice_max143(reg)) == "Yes" and will_irv_work143(reg, opp) != "No":
                        match = {
                            'reg' : reg,
                            'model': model,
                            'diap': None,
                            'body': body_labels143[prefix],
                            'orifice': orifice_type143(reg),
                            'seat': None,
                            'color': spring_143(outlet_input)['color'],
                            'range': spring_143(outlet_input)['range'],
                            'capacity': cap,
                            'opp': "IRV",
                            'mon_color': None,
                            'mon_range': None,
                        }
                        return match
    # No OPP
    else:
        for prefix in ordered_prefixes:
            for orifice in orifice_order143:
                reg = f"{prefix}_{orifice}"
                if reg in result:
                    cap = result[reg]
                    if will_work(cap, reg, orifice_max143(reg)) == "Yes":
                        match = {
                            'reg' : reg,
                            'model': model,
                            'diap': None,
                            'body': body_labels143[prefix],
                            'orifice': orifice_type143(reg),
                            'seat': None,
                            'color': spring_143(outlet_input)['color'],
                            'range': spring_143(outlet_input)['range'],
                            'capacity': cap,
                            'opp': "None" if model == '143-1' else "IRV",
                            'mon_color': None,
                            'mon_range': None,
                        }
                        return match


def run_regulator_selection143(inlet, outlet, opp):

    opp = "IRV" if opp == "Monitor" else opp
    
    # if opp = IRV, fail if outlet > 2 psi (for 143-2HP)
    if opp == "IRV" and outlet_input > 2:
        warning = "Cannot size IRV for outlet pressures > 2 psi"
        result = None
        match = None
        apply = False
        return result, match, apply, warning
    
    result = interpolate_capacity(data143, inlet, outlet, False, False)

    warning = None

    if isinstance(result, str):
        warning = result
        result = None
        match = None
        apply = False
        return result, match, apply, warning

    match = gen_match143(result, opp)

    if match:
        apply = True
        if opp == "IRV":
            warning = "Sized for IRV"
    else:
        apply = False

    return result, match, apply, warning


# Part Number Configurator
# ------------------------------------------------------------------------------------------------------

# Holland Part Number
def hsc_pnc143(match):
    body_map = {
        '3/4"': '3/4',
        '1"': '1',
        '1-1/4"': '1-1/4',
    }
    orifice_map = {
        '1/8"': '10',
        '9/64"': '31',
        '5/32"': '30',
        '3/16"': '11',
        '1/4"': '12',
        '5/16"': '13',
        '3/8"': '14',
        '1/2"': '15',
        '5/8"': '16',
    }
    spring_map = {
        'Red': '10',
        'Blue': '11',
        'Green': '12',
        'Orange': '13',
        'Black + White': '20',
        'Cadmium': '15',
        'Black': '14',
    }

    model = match['model']
    body = body_map.get(match['body'])
    orifice = orifice_map.get(match['orifice'])
    spring = spring_map.get(match['color'])

    output = {'worker': f"R.{model}.{body}.{orifice}.{spring}"}

    return output


# Output Functions
# ------------------------------------------------------------------------------------------------------

def print_model_table(title, prefix, opp, result):
    
    if opp == "IRV":
        rows = [
            [orifice_type143(reg), f"{cap:,.0f}" if isinstance(cap, (int, float)) else cap, will_work(cap, reg, orifice_max143(reg)), will_irv_work143(reg, opp)]
            for reg, cap in result.items()
            if reg.startswith(prefix)
        ]
        print("\n" + title)
        print(tabulate(rows, headers=["Orifice Size", "Calculated Capacity (CFH)", "Will Reg Work", "Will IRV Work?"], tablefmt="simple_grid"))
    else:
        rows = [
            [orifice_type143(reg), f"{cap:,.0f}" if isinstance(cap, (int, float)) else cap, will_work(cap, reg, orifice_max143(reg))]
            for reg, cap in result143.items()
            if reg.startswith(prefix)
        ]
        print("\n" + title)
        print(tabulate(rows, headers=["Orifice Size", "Calculated Capacity (CFH)", "Will Reg Work"], tablefmt="simple_grid"))

def print_regulator_selection(match):
    print("REGULATOR SELECTION")
    print(f"Model:", match['model'])
    if match['diap'] != None:
        print(f"Diaphragm Size:", match['diap'])
    print(f"Body Size:", match['body'])
    if match['orifice'] != None:
        print(f"Orifice Size:", match['orifice'])
    if match['seat'] != None:
        print(f"Seat:", match['seat'])
    print(f"Spring:", match['color'], match['range'])
    if match['mon_color'] != None:
        print(f"Monitor Spring:", match['mon_color'], match['mon_range'])
    capacity = match['capacity']
    cap_str = f"{capacity:,.0f}" if isinstance(capacity, (int, float)) else str(capacity)
    print(f"Calculated Capacity (CFH): {cap_str}")

    print("")
    print("Sizing Adjustments")
    print(f"Oversized by {oversize_percent:.0f}%")
    if match['opp'] == "Monitor":
        print("Monitor capacity reduction: 30%")
    if Patm < 14.4:
        print(f"Elevation capacity reduction: {elevation_reduction:.0f}%")
    if gastypemult != 1:
        print(f"Multiplier for other gas: {gastypemult}")
