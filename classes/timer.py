

class Timer:
    def __init__(self, font: object, init_value: dict = None) -> None:
        self.font = font
        self.active = False

        if init_value:
            self.value = init_value
        else:
            self.value = {'h': '00', 'm': '00', 's': '00', 'ms': '000'}

    def reset(self) -> None:
        self.value = {'h': '00', 'm': '00', 's': '00', 'ms': '000'}

    def increment_ms(self, incr_value: float) -> None:
        self.value['ms'] = int(self.value['ms']) + incr_value

        # increment other stuff if... y'know
        if self.value['ms'] > 999:
            self.value['s'] = int(self.value['s']) + 1
            self.value['ms'] = '000'
            if self.value['s'] == 60:
                self.value['m'] = int(self.value['m']) + 1
                self.value['s'] = '00'
                if self.value['m'] == 60:
                    self.value['h'] = int(self.value['h']) + 1
                    self.value['m'] = '00'

        # correct formatting
        for key in self.value:
            if key != 'ms':
                if len(str(self.value[key])) != 2:
                    self.value[key] = f'0{self.value[key]}'
                else:
                    self.value[key] = str(self.value[key])
            else:
                if len(str(self.value[key])) == 1:
                    self.value[key] = f'00{self.value[key]}'
                elif len(str(self.value[key])) == 2:
                    self.value[key] = f'0{self.value[key]}'
                else:
                    self.value[key] = str(self.value[key])


    def render(self, display: object, pos: tuple, color: tuple = (237, 224, 212)) -> None:
        text = f"{self.value['h']}:{self.value['m']}:{self.value['s']}:{self.value['ms']}"
        display.blit(self.font.render(text, 0, color), pos)
