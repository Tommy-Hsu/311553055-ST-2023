import angr
import sys

main_addr = 0x4011a9
find_addr = 0x401371
avoid_addr = 0x40134d

class my_scanf(angr.SimProcedure):
    def run(self, fmt, ptr): 
        simfd = self.state.posix.get_fd(sys.stdin.fileno())
        data, ret_size = simfd.read_data(0x4)
        self.state.memory.store(ptr, data)
        return 1

proj = angr.Project('./src/prog', load_options={'auto_load_libs': False})
proj.hook_symbol('__isoc99_scanf', my_scanf(), replace=True)
state = proj.factory.blank_state(addr=main_addr)
simgr = proj.factory.simulation_manager(state)
simgr.explore(find=find_addr, avoid=avoid_addr)

file = open("solve_input", "w")
# TODO
if simgr.found:
    # print("success")
    input_string = simgr.found[0].posix.dumps(sys.stdin.fileno())
    print(input_string)
    num_bytes_to_read = 4
    for i in range(0, len(input_string), num_bytes_to_read):
        temp = input_string[i:i+num_bytes_to_read]
        print('Input x{}: {} {}'.format(i//num_bytes_to_read, temp, int.from_bytes(temp, byteorder="little", signed=True)))
        file.write(str(int.from_bytes(temp,  byteorder="little", signed=True)) + '\n')

else:
    print('Failed')

file.close()