import numpy as np
import struct
import re

class OpCodes():
    def __init__(self):
        self._op_stack = []  # operand stack for the opcodes
        self._lva = []  # local variable array initialized
        self._table = {0x00: self._not_implemented, 0x02: self._iconst_m1, 0x03: self._iconst_0, 0x04: self._iconst_1,
                      0x05: self._iconst_2, 0x06: self._iconst_3, 0x07: self._iconst_4, 0x08: self._iconst_5,
                      0x60: self._iadd, 0x7e: self._iand, 0x6c: self._idiv, 0x68: self._imul, 0x74: self._ineg,
                      0x80: self._ior, 0x70: self._irem, 0x78: self._ishl, 0x7a: self._ishr, 0x64: self._isub,
                      0x7c: self._iushr, 0x82: self._ixor, 0x15: self._iload, 0x1a: self._iload_0, 0x1b: self._iload_1,
                      0x1c: self._iload_2, 0x1d: self._iload_3, 0x36: self._istore, 0x3b: self._istore_0,
                      0x38: self._fstore, 0x43: self._fstore_0, 0x44: self._fstore_1, 0x45: self._fstore_2,
                      0x46: self._fstore_3, 0x62: self._fadd, 0x66: self._fsub, 0x6a: self._fmul,
                      0x6e: self._fdiv, 0x72: self._frem, 0x76: self._fneg,
                      0x3c: self._istore_1, 0x3d: self._istore_2, 0x3e: self._istore_3, 0x91: self._i2b, 0x92: self._i2c,
                      0x87: self._i2d, 0x86: self._i2f,
                      0x85: self._i2l, 0x93: self._i2s, 0xb6: self._invokevirtual, 0xb2: self._getstatic, 0x12: self._ldc,
                      0x8b: self._f2i, 0x8c: self._f2l, 0x8d: self._f2d, 0xb1: self._ret, 0xb: self._fconst_0,
                      0xc: self._fconst_1, 0xd: self._fconst_2, 0x17: self._fload, 0x22: self._fload_0, 0x23: self._fload_1,
                      0x24: self._fload_2, 0x25: self._fload_3,
                      0x1e: self._lload_0, 0x1f: self._lload_1, 0x20:self._lload_2, 0x21:self._lload_3, 0x16:self._lload,
                      0x9: self._lconst_0, 0xa: self._lconst_1, 0x3f: self._lstore_0, 0x40: self._lstore_1,
                      0x41: self._lstore_2, 0x42: self._lstore_3, 0x37: self._lstore, 0x61: self._ladd, 0x65: self._lsub,
                      0x69: self._lmul, 0x6d: self._ldiv, 0x71: self._lrem, 0x75: self._lneg, 0x7d: self._lushr,
                      0x7f: self._land, 0x81: self._lor, 0x83: self._lxor, 0x88: self._l2i, 0x89: self._l2f, 0x8a: self._l2d, 
                      0x79: self._lshl, 0x7b: self._lshr}

    def _not_implemented(self):
        return 'not implemented'

    def interpret(self, value, operands=None, constants=None):
        """
        Takes an input of a hex value that represents a byte long Opcode label for the Java Virtual machine and then
        executes the corresponding method in this file using the other input fields.

        The operands variable takes an optional array of operands to be used with the executed Opcode.

        The constants variable takes an optional array of constants to be used with the executed Opcode.
        """
        try:
            if operands is not None and constants is not None:
                return self._table[value](operands, constants)
            elif operands is not None and constants is None:
                return self._table[value](operands)
            else:
                return self._table[value]()
        except:
            print("Opcode ", value, " not implemented, skipping it.")

    def _iconst_m1(self):
        self._op_stack.append(-1)

    def _iconst_0(self):
        self._op_stack.append(0)

    def _iconst_1(self):
        self._op_stack.append(1)

    def _iconst_2(self):
        self._op_stack.append(2)

    def _iconst_3(self):
        self._op_stack.append(3)

    def _iconst_4(self):
        self._op_stack.append(4)

    def _iconst_5(self):
        self._op_stack.append(5)

    def _iadd(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        self._op_stack.append(value1 + value2)

    def _iand(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        self._op_stack.append(value1 & value2)

    def _idiv(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        try:
            self._op_stack.append(value1//value2)
        except ZeroDivisionError:
            return 'Error: Divides by Zero'

    def _imul(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        self._op_stack.append(value1 * value2)

    def _ineg(self):
        self._op_stack.append(self._op_stack.pop() * -1)

    def _ior(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        self._op_stack.append(value1 | value2)

    def _irem(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        try:
            self._op_stack.append(value1 % value2)
        except ZeroDivisionError:
            return 'Error: Divides by Zero'

    def _ishl(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        self._op_stack.append(value1 << value2)

    def _ishr(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        self._op_stack.append(value1 >> value2)

    def _isub(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        self._op_stack.append(value1 - value2)

    def _iushr(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        s = value2 & 0x1f
        if value1 >= 0:
            self._op_stack.append(value1 >> s)
        else:
            self._op_stack.append((value1 + 0x100000000) >> s)

    def _ixor(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        self._op_stack.append(value1 ^ value2)

    def _iload(self, operands):
        index = operands.pop()
        self._op_stack.append(self._lva[index])

    def _iload_0(self):
        self._op_stack.append(self._lva[0])

    def _iload_1(self):
        self._op_stack.append(self._lva[1])

    def _iload_2(self):
        self._op_stack.append(self._lva[2])

    def _iload_3(self):
        self._op_stack.append(self._lva[3])

    def _istore(self, operands):
        index = operands.pop()
        if len(self._lva) <= index:
            self._lva.append(self._op_stack.pop())
        else:
            self._lva[index] = self._op_stack.pop()

    def _istore_0(self):
        if len(self._lva) == 0:
            self._lva.append(self._op_stack.pop())
        else:
            self._lva[0] = self._op_stack.pop()

    def _istore_1(self):
        if len(self._lva) == 1:
            self._lva.append(self._op_stack.pop())
        else:
            self._lva[1] = self._op_stack.pop()

    def _istore_2(self):
        if len(self._lva) == 2:
            self._lva.append(self._op_stack.pop())
        else:
            self._lva[2] = self._op_stack.pop()

    def _istore_3(self):
        if len(self._lva) == 3:
            self._lva.append(self._op_stack.pop())
        else:
            self._lva[3] = self._op_stack.pop()

    def _i2b(self):  # Josh
        value1 = self._op_stack.pop()
        self._op_stack.append(int(value1))

    def _i2c(self):
        value1 = self._op_stack.pop()
        self._op_stack.append(chr(value1))

    def _i2d(self):
        value1 = self._op_stack.pop()
        self._op_stack.append(float(value1))

    def _i2f(self):
        value1 = self._op_stack.pop()
        self._op_stack.append(float(value1))

    def _i2l(self):
        value1 = self._op_stack.pop()
        self._op_stack.append(int(value1))

    def _i2s(self):
        value1 = self._op_stack.pop()
        self._op_stack.append(int(value1))

    def _lload_0(self):
        frag1 = self._lva[0]
        frag2 = self._lva[1]
        self._op_stack.append(frag1)
        self._op_stack.append(frag2)

    def _lload_1(self):
        frag1 = self._lva[1]
        frag2 = self._lva[2]
        self._op_stack.append(frag1)
        self._op_stack.append(frag2)

    def _lload_2(self):
        frag1 = self._lva[2]
        frag2 = self._lva[3]
        self._op_stack.append(frag1)
        self._op_stack.append(frag2)

    def _lload_3(self):
        frag1 = self._lva[3]
        frag2 = self._lva[4]
        self._op_stack.append(frag1)
        self._op_stack.append(frag2)

    def _lload(self, operands):
        index = operands.pop()
        frag1 = self._lva[index]
        frag2 = self._lva[index+1]
        self._op_stack.append(frag1)
        self._op_stack.append(frag2)

    def _lconst_0(self):
        self._op_stack.append(0)
        self._op_stack.append(0)

    def _lconst_1(self):
        self._op_stack.append(0)
        self._op_stack.append(1)

    def _lstore_0(self):
        frag2 = self._op_stack.pop()
        frag1 = self._op_stack.pop()
        if len(self._lva) == 0:
            self._lva.append(frag1)
            self._lva.append(frag2)
        else:
            self._lva[0] = frag1
            if len(self._lva) == 1:
                self._lva.append(frag2)
            else:
                self._lva[1] = frag2

    def _lstore_1(self):
        frag2 = self._op_stack.pop()
        frag1 = self._op_stack.pop()
        if len(self._lva) == 1:
            self._lva.append(frag1)
            self._lva.append(frag2)
        else:
            self._lva[1] = frag1
            if len(self._lva) == 2:
                self._lva.append(frag2)
            else:
                self._lva[2] = frag2

    def _lstore_2(self):
        frag2 = self._op_stack.pop()
        frag1 = self._op_stack.pop()
        if len(self._lva) == 2:
            self._lva.append(frag1)
            self._lva.append(frag2)
        else:
            self._lva[2] = frag1
            if len(self._lva) == 3:
                self._lva.append(frag2)
            else:
                self._lva[3] = frag2

    def _lstore_3(self):
        frag2 = self._op_stack.pop()
        frag1 = self._op_stack.pop()
        if len(self._lva) == 3:
            self._lva.append(frag1)
            self._lva.append(frag2)
        else:
            self._lva[3] = frag1
            if len(self._lva) == 4:
                self._lva.append(frag2)
            else:
                self._lva[4] = frag2

    def _lstore(self, operands):
        index = operands.pop()
        frag2 = self._op_stack.pop()
        frag1 = self._op_stack.pop()
        if len(self._lva) == index:
            self._lva.append(frag1)
            self._lva.append(frag2)
        else:
            self._lva[index] = frag1
            if len(self._lva) == index + 1:
                self._lva.append(frag2)
            else:
                self._lva[index + 1] = frag2

    def _ladd(self):
        second_op2 = self._op_stack.pop()
        second_op1 = self._op_stack.pop()
        first_op2 = self._op_stack.pop()
        first_op1 = self._op_stack.pop()
        first_op = self._longcomb(first_op1, first_op2)
        second_op = self._longcomb(second_op1, second_op2)
        answer = first_op + second_op
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _lsub(self):
        second_op2 = self._op_stack.pop()
        second_op1 = self._op_stack.pop()
        first_op2 = self._op_stack.pop()
        first_op1 = self._op_stack.pop()
        first_op = self._longcomb(first_op1, first_op2)
        second_op = self._longcomb(second_op1, second_op2)
        answer = first_op - second_op
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _lmul(self):
        second_op2 = self._op_stack.pop()
        second_op1 = self._op_stack.pop()
        first_op2 = self._op_stack.pop()
        first_op1 = self._op_stack.pop()
        first_op = self._longcomb(first_op1, first_op2)
        second_op = self._longcomb(second_op1, second_op2)
        answer = first_op * second_op
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _ldiv(self):
        second_op2 = self._op_stack.pop()
        second_op1 = self._op_stack.pop()
        first_op2 = self._op_stack.pop()
        first_op1 = self._op_stack.pop()
        first_op = self._longcomb(first_op1, first_op2)
        second_op = self._longcomb(second_op1, second_op2)
        answer = first_op / second_op
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _lrem(self):
        second_op2 = self._op_stack.pop()
        second_op1 = self._op_stack.pop()
        first_op2 = self._op_stack.pop()
        first_op1 = self._op_stack.pop()
        first_op = self._longcomb(first_op1, first_op2)
        second_op = self._longcomb(second_op1, second_op2)
        answer = first_op % second_op
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _lneg(self):
        val2 = self._op_stack.pop()
        val1 = self._op_stack.pop()
        val = self._longcomb(val1, val2)
        answer = val * -1
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _lushr(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        s = value2 & 0x3f
        if value1 >= 0:
            self._op_stack.append(value1 >> s)
        else:
            self._op_stack.append((value1 + 0x10000000000000000) >> s)

    def _land(self):
        second_op2 = self._op_stack.pop()
        second_op1 = self._op_stack.pop()
        first_op2 = self._op_stack.pop()
        first_op1 = self._op_stack.pop()
        first_op = self._longcomb(first_op1, first_op2)
        second_op = self._longcomb(second_op1, second_op2)
        answer = first_op & second_op
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _lor(self):
        second_op2 = self._op_stack.pop()
        second_op1 = self._op_stack.pop()
        first_op2 = self._op_stack.pop()
        first_op1 = self._op_stack.pop()
        first_op = self._longcomb(first_op1, first_op2)
        second_op = self._longcomb(second_op1, second_op2)
        answer = first_op | second_op
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _lxor(self):
        second_op2 = self._op_stack.pop()
        second_op1 = self._op_stack.pop()
        first_op2 = self._op_stack.pop()
        first_op1 = self._op_stack.pop()
        first_op = self._longcomb(first_op1, first_op2)
        second_op = self._longcomb(second_op1, second_op2)
        answer = first_op ^ second_op
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _l2i(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        valuea = self._longcomb(value1, value2)
        self._op_stack.append(int(valuea))

    def _l2f(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        valuea = self._longcomb(value1, value2)
        self._op_stack.append(float(valuea))

    def _l2d(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        valuea = self._longcomb(value1, value2)
        self._op_stack.append(float(valuea))

    def _fstore(self, operands):
        index = operands.pop()
        if len(self._lva) <= index:
            self._lva.append(np.float32(self._op_stack.pop()))
        else:
            self._lva[index] = np.float32(self._op_stack.pop())

    def _fstore_0(self):
        if len(self._lva) == 0.0:
            self._lva.append(np.float32(self._op_stack.pop()))
        else:
            self._lva[0] = np.float32(self._op_stack.pop())

    def _fstore_1(self):
        if len(self._lva) == 1.0:
            self._lva.append(np.float32(self._op_stack.pop()))
        else:
            self._lva[1] = np.float32(self._op_stack.pop())

    def _fstore_2(self):
        if len(self._lva) == 2.0:
            self._lva.append(np.float32(self._op_stack.pop()))
        else:
            self._lva[2] = np.float32(self._op_stack.pop())

    def _fstore_3(self):
        if len(self._lva) == 3.0:
            self._lva.append(np.float32(self._op_stack.pop()))
        else:
            self._lva[3] = np.float32(self._op_stack.pop())

    def _fadd(self):
        value2 = np.float32(self._op_stack.pop())
        value1 = np.float32(self._op_stack.pop())
        self._op_stack.append(np.float32(value1 + value2))

    def _fsub(self):
        value2 = np.float32(self._op_stack.pop())
        value1 = np.float32(self._op_stack.pop())
        self._op_stack.append(np.float32(value1 - value2))

    def _fmul(self):
        value2 = np.float32(self._op_stack.pop())
        value1 = np.float32(self._op_stack.pop())
        self._op_stack.append(np.float32(value1 * value2))

    def _fdiv(self):
        value2 = np.float32(self._op_stack.pop())
        value1 = np.float32(self._op_stack.pop())
        if value2 == 0.0:
            return 'Error: Divides by Zero'
        self._op_stack.append(np.float32(value1 / value2))

    def _frem(self):
        value2 = np.float32(self._op_stack.pop())
        value1 = np.float32(self._op_stack.pop())
        if value2 == 0.0:
            return 'Error: Divides by Zero'
        self._op_stack.append(np.float32(value1 % value2))

    def _lshl(self):
        operand1 = self._op_stack.pop()
        val1, val2 = self._longsplit(self._op_stack.pop())
        answer = self._longcomb(val1, val2) << operand1
        self._op_stack.append(answer)

    def _lshr(self):
        operand1 = self._op_stack.pop()
        val1, val2 = self._longsplit(self._op_stack.pop())
        answer = self._longcomb(val1, val2) >> operand1
        self._op_stack.append(answer)

    def _fneg(self):
        value = np.float32(self._op_stack.pop())
        self._op_stack.append(np.float32(- value))

    def _get_str_from_cpool(self, index, c_pool):
        const_ref = c_pool[index]

        if const_ref.tag != 1:
            class_index = const_ref.info[0] + const_ref.info[1] - 1
            val = self._get_str_from_cpool(class_index, c_pool)

            if const_ref.tag == 10:
                val += '.'
            elif const_ref.tag == 12:
                val += ':'

            if const_ref.info.__len__() > 2:
                name_type_index = const_ref.info[2] + const_ref.info[3] - 1
                val += self._get_str_from_cpool(name_type_index, c_pool)

            return val

        else:
            return bytes(const_ref.info).decode("utf-8")

    def _invokevirtual(self, operands, c_pool):
        num1 = operands.pop()
        num2 = operands.pop()
        method = self._get_str_from_cpool(num1 + num2 - 1, c_pool)
        if method == 'java/io/PrintStream.println:(I)V':
            print(self._op_stack.pop())
        elif method == 'java/io/PrintStream.println:(Ljava/lang/String;)V':
            print(self._op_stack.pop())
        elif method == 'java/util/Scanner.nextInt:()I':
            data = input("Enter a number: ")
            while re.match(r"[-+]?\d+$", data) is None:
                print("Invalid input")
                data = input("Enter a number: ")
            int1 = int(data)
            self._op_stack.append(int1)

    def _getstatic(self, operands, c_pool):
        value1 = operands.pop()
        value2 = operands.pop()
        return self._get_str_from_cpool(value1 + value2 - 1, c_pool)

    def _ldc(self, operands, c_pool):
        value = operands.pop()
        self._op_stack.append(self._get_str_from_cpool(value - 1, c_pool))

    def _longsplit(self, val):    # Splits long in half and returns first and second frag as int32
        val = np.int64(val)
        frag2 = np.int32(val & 0x00000000ffffffff)
        frag1 = np.int32((val >> 32) & 0x00000000ffffffff)
        return frag1, frag2

    def _longcomb(self, frag1, frag2):   # Takes two fragments and combines them, returning a 64 bit int
        frag1 = np.int64((0x00000000ffffffff & frag1) << 32)
        frag2 = np.int64(0x00000000ffffffff & frag2)
        return frag1 + frag2
      
    def _fconst_0(self):
        self._op_stack.append(np.float32(0.0))

    def _fconst_1(self):
        self._op_stack.append(np.float32(1.0))

    def _fconst_2(self):
        self._op_stack.append(np.float32(2.0))

    def _fload(self, operands):
        index = operands.pop()
        self._op_stack.append(self._lva[index])

    def _fload_0(self):
        self._op_stack.append(self._lva[0])

    def _fload_1(self):
        self._op_stack.append(self._lva[1])

    def _fload_2(self):
        self._op_stack.append(self._lva[2])

    def _fload_3(self):
        self._op_stack.append(self._lva[3])

    def _f2i(self):
        value1 = struct.unpack('!f', bytes.fromhex(self._op_stack.pop()))[0]
        self._op_stack.append(np.int32(value1))

    def _f2l(self):
        value1 = np.int64(struct.unpack('!f', bytes.fromhex(self._op_stack.pop()))[0])
        value2 = np.right_shift(value1, 32)
        value3 = np.bitwise_and(value1, 0x00000000FFFFFFFF)
        self._op_stack.append(np.int32(value2))
        self._op_stack.append(np.int32(value3))

    def _f2d(self):
        value1 = np.float64(struct.unpack('!f', bytes.fromhex(self._op_stack.pop()))[0])
        hexval = hex(struct.unpack('<Q', struct.pack('<d', value1))[0])
        value2 = hexval[2:10]
        value3 = hexval[10:18]
        self._op_stack.append(int(value2, 16))
        self._op_stack.append(int(value3, 16))

    def _ret(self):
        return ''
