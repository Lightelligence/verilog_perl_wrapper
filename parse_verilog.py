import subprocess
import os
import yaml


class ParseVerilog(object):
    """Uses verilog-perl to parse the design. Implements the same callbacks as verilog-perl."""

    # FIXME, ideally this would be parsed from help?
    callbacks = {
        "class": ["token", "name", "virtual"],
        "covergroup": ["token", "name"],
        "contassign": ["token", "lhs", "rhs"],
        "defparam": ["token", "lhs", "rhs"],
        "endcell": ["token"],
        "endgroup": ["token"],
        "endinterface": ["token"],
        "endclass": ["token"],
        "endtaskfunc": ["token"],
        "endmodport": ["token"],
        "endmodule": ["token"],
        "endpackage": ["token"],
        "endprogram": ["token"],
        "function": ["keyword", "name", "data-type"],
        "import": ["package", "id"],
        "instant": ["module", "cell", "range"],
        "interface": ["keyword", "name"],
        "modport": ["keyword", "name"],
        "module": ["keyword", "name", "ignored", "in_celldefine"],
        "package": ["keyword", "name"],
        "parampin": ["name", "connection", "index"],
        "pin": ["name", "connection", "index"],
        "pinselects": ["name", "connections", "index"],
        "port": ["name", "objof", "direction", "data_type", "array", "pinnum"],
        "ppdefine": ["defvar", "definition"],
        "program": ["keyword", "name"],
        "signal_dec": ["keyword", "signame", "vector", "mem", "signed", "value"],
        "task": ["keyword", "name"],
        "var": ["kwd", "name", "objof", "nettype", "data_type", "array", "value"],
    }

    def __init__(self, do_lib_discovery, compile_options, log):
        self.log = log
        self._create_callbacks()

        # verilog_perl_to_yaml_executable = os.path.join(os.path.dirname(__file__), "verilog_perl_to_yaml.pl")
        if do_lib_discovery:
            verilog_perl_to_yaml_executable = "$PROJ_DIR/digital/dv/scripts/verilog_perl_to_yaml_discover.pl"
        else:
            verilog_perl_to_yaml_executable = "$PROJ_DIR/digital/dv/scripts/verilog_perl_to_yaml.pl"

        cmd = "{} {}".format(verilog_perl_to_yaml_executable, compile_options)

        from tempfile import TemporaryFile
        with TemporaryFile() as stdout_fp, TemporaryFile() as stderr_fp:
            kwargs = {'shell': True, 'stdout': stdout_fp, 'stderr': stderr_fp}
            p = subprocess.Popen(cmd, **kwargs)
            p.wait()

            stdout_fp.seek(0)
            stderr_fp.seek(0)

            stdout = stdout_fp.read()
            stderr = stderr_fp.read()

            if p.returncode:
                self.log.critical("verilog perl failed:\n%s\n%s", stdout.decode('ascii'), stderr.decode('ascii'))

        yd = yaml.load(stdout, Loader=yaml.Loader)

        for ycb in yd:
            cb_name = ycb[0]
            cb_args = ycb[1:]
            cb = getattr(self, cb_name)
            cb(*cb_args)

    def _create_callbacks(self):
        for cb, cb_args in self.callbacks.items():
            try:
                getattr(self, cb)
                # FIXME check argument names match
            except AttributeError:
                setattr(self, cb, lambda self, *cb_args: self)
