import angr
from angr.sim_type import SimTypeString, SimTypeInt

import logging
l = logging.getLogger("angr.procedures.libc.strcmp")

class strcmp(angr.SimProcedure):
    #pylint:disable=arguments-differ

    def run(self, a_addr, b_addr, wchar=False, ignore_case=False):
        self.argument_types = {0: self.ty_ptr(SimTypeString()),
                       1: self.ty_ptr(SimTypeString())}
        self.return_type = SimTypeInt(32, True)

        strlen = angr.SIM_PROCEDURES['libc']['strlen']

        a_strlen = self.inline_call(strlen, a_addr, wchar=wchar)
        b_strlen = self.inline_call(strlen, b_addr, wchar=wchar)
        maxlen = self.state.se.BVV(max(a_strlen.max_null_index, b_strlen.max_null_index), self.state.arch.bits)

        strncmp = self.inline_call(angr.SIM_PROCEDURES['libc']['strncmp'], a_addr, b_addr, maxlen, a_len=a_strlen, b_len=b_strlen, wchar=wchar, ignore_case=ignore_case)
        return strncmp.ret_expr
