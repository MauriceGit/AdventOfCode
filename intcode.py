from collections import defaultdict

class IntCode:

    def __init__(self, data):
        self.inputs = []
        self.outputs = []
        self.all_outputs = []
        self.data = defaultdict(int, enumerate(data[:]))
        self.finished = False
        self.current_index = 0
        self.errors = []
        self.relative_base = 0

        self._run()

    def _parse_instruction(self, i):
        return i%10**2, (i // 10**2)%10, (i // 10**3)%10, (i // 10**4)%10

    def _get_parameter(self, p, i):
        if p == 0:
            return self.data[self.current_index+i]
        elif p == 1:
            return self.current_index+i
        elif p == 2:
            return self.relative_base + self.data[self.current_index+i]

    def _run(self):

        while True:
            op, p1, p2, p3 = self._parse_instruction(self.data[self.current_index])

            # explicit exit so at1/2/3 doesn't crash
            if op == 99:
                self.finished = True
                return

            # position mode
            at1 = self._get_parameter(p1, 1)
            at2 = self._get_parameter(p2, 2)
            at3 = self._get_parameter(p3, 3)

            if op == 1:
                self.data[at3] = self.data[at1] + self.data[at2]
                self.current_index += 4
            elif op == 2:
                self.data[at3] = self.data[at1] * self.data[at2]
                self.current_index += 4
            elif op == 3:
                # Halt the machine and restart as soon, as we have some more input!
                if len(self.inputs) == 0:
                    return
                input_value = self.inputs.pop(0)
                self.data[at1] = input_value
                self.current_index += 2
            elif op == 4:
                value = self.data[at1]
                self.current_index += 2
                self.outputs.append(value)
                self.all_outputs.append(value)
            elif op == 5:
                if self.data[at1] != 0:
                    self.current_index = self.data[at2]
                else:
                    self.current_index += 3
            elif op == 6:
                if self.data[at1] == 0:
                    self.current_index = self.data[at2]
                else:
                    self.current_index += 3
            elif op == 7:
                self.data[at3] = int(self.data[at1] < self.data[at2])
                self.current_index += 4
            elif op == 8:
                self.data[at3] = int(self.data[at1] == self.data[at2])
                self.current_index += 4
            elif op == 9:
                self.relative_base += self.data[at1]
                self.current_index += 2
            else:
                self.errors.append("ERROR - unknown op code")
                return

    def set_input(self, input_value):
        self.inputs.append(input_value)
        self._run()

    def set_inputs(self, input_list):
        self.inputs.extend(input_list)
        self._run()

    def get_outputs(self):
        out = self.outputs[:]
        self.outputs = []
        return out

    def get_outputs_str(self):
        return "".join(map(chr, self.get_outputs()))

    def get_all_outputs(self):
        return self.all_outputs

    def is_finished(self):
        return self.finished

    def get_errors(self):
        return self.errors
