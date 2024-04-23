'''
Copyright (c) 2023 Gouvernement du Québec

SPDX-License-Identifier: LiLiQ-R-1.1
License-Filename: LICENSES/EN/LiLiQ-R11unicode.txt
'''
from mosek_tuner.argument_parser import TunerParser

def main()->int:
    parser = TunerParser()
    new_tuner = parser.get_tuner()
    return int(not new_tuner.run())

if __name__ == "__main__":
    main()