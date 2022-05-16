load("@rules_python//python:defs.bzl", "py_library")
load("@com_github_bazelbuild_buildtools//buildifier:def.bzl", "buildifier")

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

buildifier(
    name = "buildifier_format_diff",
    diff_command = "diff",
    mode = "diff",
)

buildifier(
    name = "buildifier_lint",
    lint_mode = "warn",
    lint_warnings = [
        "-function-docstring-args",
        "-function-docstring",
    ],
    mode = "fix",
)

buildifier(
    name = "buildifier_fix",
    lint_mode = "fix",
    mode = "fix",
)
