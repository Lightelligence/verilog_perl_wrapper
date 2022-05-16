load("@rules_python//python:defs.bzl", "py_library")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "cmn_logging",
    srcs = ["cmn_logging.py"],
)

py_library(
    name = "parse_verilog",
    srcs = ["parse_verilog.py"],
    data = [
        "verilog_perl_to_yaml.pl",
        "verilog_perl_to_yaml_discover.pl",
    ],
    deps = [":cmn_logging"],
)
