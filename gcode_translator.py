#!/usr/bin/env python

import sys, datetime
import re

def main():
    final_gcode = "parsed_final_out.gcode"
    input_gcode = "gui_test.ngc"#"final_out.gcode"
    write_flag = 1
    illegal_chars = set('ZMIJF')

    with open(final_gcode, "w+") as f:
        f.write("; generated on {}\n".format(datetime.datetime.now()))
        '''f.write()
        f.write()
        f.write()'''
        with open(input_gcode, "r") as g:
            line_count = 0
            '''for line in g:
                line_count = line_count + 1
                if line_count > 12:
                    write_flag = 1'''
            for line in g:
                line_count = line_count + 1
                if line_count > 2:
                    if line[0] in ";ME":
                        f.write("{}\n".format(line))
                        pass

                    elif any((c in illegal_chars)for c in line):
                        pass
                        '''print("Before: {}".format(line))
                        try:
                            valid = re.split(r"[IJ]", line)[0]
                        except:
                            pass
                        print("After: {}".format(valid))
                        f.write("{}\n".format(valid))
                    elif ("G1 " or "G0 ") not in line: 
                        pass'''

                    elif "G0" in line and write_flag:
                        f.write(line)
                        f.write("G1 E10\n")
                        write_flag = 0

                    elif line == "":
                        pass
                    else:
                        f.write(line)
        g.close()
    f.close()

if __name__ == '__main__':
    main()
    # All the E, F, Z, M have to go.