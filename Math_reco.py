class MathReco:
    def __init__(self):
        self.digit_list=[]
        self.result_list=[]
    def translate_list_to_math(self,math_list:list):
        self.digit_list=[]
        self.result_list=[]
        for x in math_list:
            if x.isdigit() or x == 'million' or x == 'billion' :
                self.digit_list.append(x)

        if len(self.digit_list) == 2:
                return self.digit_list

        if len(self.digit_list) == 3:
                if self.digit_list[1].isalpha():
                    match self.digit_list[1]:
                        case 'million':
                            self.result_list.append(int(self.digit_list[0])*10**6)
                        case 'billion':
                            self.result_list.append(int(self.digit_list[0])*10**9)
                else:
                    self.result_list.append(int(self.digit_list[0]))

                if self.digit_list[2].isalpha():
                        match self.digit_list[2]:
                            case 'million':
                                self.result_list.append(int(self.digit_list[1])*10**6)
                            case 'billion':
                                self.result_list.append(int(self.digit_list[1])*10**9)
                else:
                    self.result_list.append(int(self.digit_list[2]))

        if len(self.digit_list) == 4:
                match self.digit_list[1]:
                    case 'million':
                        self.result_list.append(int(self.digit_list[0])*10**6)
                    case 'billion':
                        self.result_list.append(int(self.digit_list[0])*10**6)

                match self.digit_list[3]:
                    case 'million':
                        self.result_list.append(int(self.digit_list[2])*10**6)
                    case 'billion':
                        self.result_list.append(int(self.digit_list[2])*10**9)


        return self.result_list

    def main_math(self,string):
        try:

            input_math=string.split()
            math_list=self.translate_list_to_math(input_math)
            if '/' in string:
                return int(math_list[0]) / int(math_list[1])
            elif  any( patterns in ["x","*"] for patterns in string):
                return int(math_list[0]) * int(math_list[1])
            elif '+' in string:
                return int(math_list[0]) + int(math_list[1])
            elif '-' in string:
                return int(math_list[0]) - int(math_list[1])
            else:
                return 'Nothing'
        except :
            pass

