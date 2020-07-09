from copy import copy
import turtle
import math

class Vector:
    def __init__(self, *args):
        if len(args) == 0:
            args = (0,)
        self._vector = list(args)
        self._length = round(sum([i ** 2 for i in self._vector]) ** 0.5, 3)

    def __add__(self, other):
        if len(self._vector) > len(other._vector):
            other_vrm = other._vector + [0] * (len(self._vector) - len(other._vector))
            return Vector(*[other_vrm[i] + self._vector[i] for i in range(len(self._vector))])
        if len(other._vector) > len(self._vector):
            self_vrm = self._vector + [0] * (len(other._vector) - len(self._vector))
            return Vector(*[self_vrm[i] + other._vector[i] for i in range(len(other._vector))])
        return Vector(*[self._vector[i] + other._vector[i] for i in range(len(self._vector))])

    def __sub__(self, other):
        if len(self._vector) > len(other._vector):
            other_vrm = other._vector + [0] * (len(self._vector) - len(other._vector))
            return Vector(*[self._vector[i] - other_vrm[i] for i in range(len(self._vector))])
        if len(other._vector) > len(self._vector):
            self_vrm = self._vector + [0] * (len(other._vector) - len(self._vector))
            return Vector(*[self_vrm[i] - other._vector[i] for i in range(len(other._vector))])
        return Vector(*[self._vector[i] - other._vector[i] for i in range(len(self._vector))])

    def __mul__(self, other):
        if type(other) == Vector:
            if len(self._vector) > len(other._vector):
                other_vrm = other._vector + [0] * (len(self._vector) - len(other._vector))
                return sum([self._vector[i] * other_vrm[i] for i in range(len(self._vector))])
            if len(other._vector) > len(self._vector):
                self_vrm = self._vector + [0] * (len(other._vector) - len(self._vector))
                return sum([self_vrm[i] * other._vector[i] for i in range(len(other._vector))])
            return sum([self._vector[i] * other._vector[i] for i in range(len(self._vector))])
        return Vector(*[other * i for i in self._vector])

    def __eq__(self, other):
        if len(self._vector) > len(other._vector):
            self_vrm = self._vector
            other_vrm = other._vector + [0] * (len(self._vector) - len(other._vector))
        elif len(other._vector) > len(self._vector):
            self_vrm = self._vector + [0] * (len(other._vector) - len(self._vector))
            other_vrm = other._vector
        else:
            self_vrm = self._vector
            other_vrm = other._vector
        equal = True
        for i in range(len(self_vrm)):
            if self_vrm[i] != other_vrm[i]:
                equal = False
                break
        return equal

    def __ne__(self, other):
        return not self == other

    def __len__(self):  
        return len(self._vector)

    def length(self):
        return self._length

    def __getitem__(self, index):
        return self._vector[index - 1]

    def __str__(self):
        return '{' + ''.join([str(i) + ', ' for i in self._vector])[:-2] + '}'

    def draw_vector2d(self):
        if sum(self._vector) == 0:
            print ('Нулевой вектор невозможно нарисовать.')
        elif len(self._vector) > 2:
            print('Функция рисования доступна только для двумерных векторов')
        else:
            self_vrm = self._vector
            if len(self_vrm) < 2:
                self_vrm = self_vrm + [0] 
            turtle.shape('classic')
            turtle.width(2)
            if self_vrm[1] > 0:
                turtle.left(math.degrees(math.acos(self._vector[0] / self._length)))
            else:
                turtle.right(math.degrees(math.acos(self._vector[0] / self._length)))
            turtle.forward(self._length * 10)

    def angle(self, other):
        return round(math.degrees(math.acos((self * other)/(self._length * other.length))), 2)

    def mul_vector3d(self, other):
        if len(self._vector) <= 3 and len(other._vector) <= 3:
            self_vrm = self._vector
            other_vrm = other._vector
            if len(self_vrm) < 3:
                self_vrm = self_vrm + [0] * (3 - len(self_vrm))
            if len(other_vrm) < 3:
                other_vrm = other_vrm + [0] * (3 - len(other_vrm))
            i = (self_vrm[1] * other_vrm[2]) - (self_vrm[2] * other_vrm[1])
            j = -((self_vrm[0] * other_vrm[2]) - (self_vrm[2] * other_vrm[0]))
            k = (self_vrm[0] * other_vrm[1]) - (self_vrm[1] * other_vrm[0])
            return Vector(i, j, k)
        else:
            print('Функция векторного умножения доступна только для трёхмерных векторов')
