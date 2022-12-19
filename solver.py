import collections
import random
import rubiks


class Solver:
    @classmethod
    def scramble(cls, cube):
        actions = []
        for n in range(30):
            sign = random.choice("+-")
            axis = random.choice("xyz")
            direction = random.choice("lr")

            print(f"{sign}{axis}", direction)
            actions.append((f"{sign}{axis}", direction))
            cube.rotate(f"{sign}{axis}", direction)
        return actions

    @classmethod
    def is_solved(cls, cube):
        return cube.sides == cube.solved_map()

    @classmethod
    def misplaced_pebbles(cls, cube):
        solved = rubiks.Rubiks()
        results = []
        for face in cube.enum_faces():
            for i in range(3):
                for j in range(3):
                    if solved.label(face, i, j) != cube.label(face, i, j):
                        peb3d = cube.embed_pebble(face, (i, j))
                        results.append((face, peb3d))
        return results

    @classmethod
    def next_steps(cls, cube):
        if cls.is_solved(cube):
            return ["__done__"]

        misplaced = cls.misplaced_pebbles(cube)
        facecounts = collections.Counter(m[0] for m in misplaced)
